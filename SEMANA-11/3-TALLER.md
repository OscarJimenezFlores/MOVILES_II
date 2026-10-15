[Semana 11](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · **Taller de laboratorio**

# Taller de laboratorio 11 · Autenticación con OAuth 2.0 + PKCE y desbloqueo biométrico

**SI-988 · Soluciones Móviles II** · Semana 11 · Sesión 2 en laboratorio · calificación **procedimental**

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

---

## Qué entregas

| | |
|---|---|
| **Archivo** | `SI988-S11-TALLER-Grupo<N>.pdf` |
| **Plantilla obligatoria** | [SI988-PLANTILLA-TALLER.docx](../PLANTILLAS/SI988-PLANTILLA-TALLER.docx) |
| **Formato** | PDF exportado desde la plantilla en Word, con la carátula de la UPT, el índice actualizado y las capturas numeradas |
| **Qué va dentro** | Las secciones de la plantilla. La **5. Resultados y evidencias** se califica contra la tabla de resultados esperados de esta guía, y **cada resultado necesita la evidencia que lo demuestre**. No se copian de aquí los objetivos, la duración ni los resultados de aprendizaje |
| **Dónde se sube** | Aula virtual, tarea «Taller · Semana 11» |
| **Cuándo vence** | Según lo programado en el aula virtual |

> No se califica un informe entregado en `.docx`, sin carátula, sin los códigos de los integrantes o con resultados declarados sin evidencia.

---

El avance de Sprint 4 lo ejecuta el equipo fuera de la sesión.

## 1. Información sobre el evento práctico

### 1.1. Título del evento práctico

Implementación de la autenticación de la aplicación con el flujo de código de autorización y PKCE en el navegador del sistema, gestión segura de tokens con rotación, y desbloqueo biométrico vinculado al almacén seguro.

### 1.2. Objetivos

- Implementar **OAuth 2.0 con PKCE** usando el navegador del sistema.
- Verificar el parámetro **`state`** y configurar la redirección de forma segura.
- Almacenar los tokens en el **almacén seguro**, con la exigencia adecuada.
- Implementar la **renovación automática** con rotación del token de renovación.
- Implementar el **desbloqueo biométrico** vinculado a la clave del almacén.
- Manejar **los seis casos de fallo** de la biometría.
- Implementar el **cierre de sesión con revocación en el servidor**.
- **Verificar la autorización en el servidor**, no solo en la interfaz.

### 1.3. Resultados de Aprendizaje (RA)

- **RA1** Desarrolla la geolocalización en una app móvil.
- **RA2** Implementa y gestiona los permisos de geolocalización en una app móvil.

### 1.4. Recursos

| Recurso | Detalle |
|---|---|
| **RFC 6749 · OAuth 2.0** | https://www.rfc-editor.org/rfc/rfc6749.html |
| **RFC 7636 · PKCE** | https://www.rfc-editor.org/rfc/rfc7636.html |
| **RFC 8252 · OAuth 2.0 for Native Apps** | https://www.rfc-editor.org/rfc/rfc8252.html |
| **OpenID Connect Core** | https://openid.net/specs/openid-connect-core-1_0.html |
| **Android — Biometric authentication** | https://developer.android.com/identity/sign-in/biometric-auth |
| **Apple — Local Authentication** | https://developer.apple.com/documentation/localauthentication |
| Proveedor de identidad | **Keycloak** (Docker), Auth0, Supabase Auth o el backend propio |
| Bibliotecas de OAuth del stack | AppAuth · flutter_appauth · react-native-app-auth |

### 1.5. Seguridad

> **Dónde se trabaja.** El taller se hace en el **laboratorio de la universidad, sobre el emulador**. Cuando un escenario no se reproduce fielmente en el emulador, la verificación en un teléfono real la hace el equipo **fuera de la sesión** y adjunta el video como anexo. Ningún resultado del taller depende de tener un teléfono en clase.

1. **Nunca se usa una vista web embebida** para la autenticación. Permite a la app observar lo que el usuario escribe y no comparte la sesión del navegador. RFC 8252 lo establece explícitamente.
2. **Ningún secreto de cliente en la app.** Es un cliente público.
3. El token de renovación va al almacén seguro **con exigencia de autenticación del usuario** cuando se activa la biometría.
4. **La autorización se verifica siempre en el servidor.** Se prueba explícitamente llamando a la API con el token de otro usuario.
5. Los tokens **no se registran en el log** ni se muestran en pantallas de depuración.

---

## 2. Procedimiento o Metodología

### Paso A — Proveedor de identidad y configuración

```bash
# Keycloak como proveedor de identidad para el laboratorio
docker run -d --name sm2_keycloak -p 127.0.0.1:8080:8080 \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest start-dev
```

Configuración del cliente en el proveedor:

| Ajuste | Valor | Por qué |
|---|---|---|
| Tipo de cliente | **Público** | La app no puede guardar un secreto |
| Flujo estándar | Habilitado | Código de autorización |
| Flujo implícito | **Deshabilitado** | Obsoleto |
| Concesión directa de credenciales | **Deshabilitada** | La app no debe ver la contraseña |
| Método del reto PKCE | **S256** | Obligatorio |
| URI de redirección | `<esquema>://oauth/callback` **y** enlace verificado | Enumerada, no comodín |
| Vida del token de acceso | 15 minutos | Corta |
| Vida del token de renovación | 30 días | Con rotación |
| **Rotación del token de renovación** | Habilitada, con detección de reutilización | Detecta el robo |

### Paso B — Flujo PKCE

```
class AutenticacionOAuth(
  private val almacen: AlmacenSeguro,          // Semana 10
  private val navegador: NavegadorSistema,
) {

  suspend fun iniciarSesion(): Result<Sesion> {
    // ① Verificador aleatorio con el generador SEGURO
    val verificador = base64UrlSinRelleno(SecureRandom().generarBytes(32))
    // ② Reto
    val reto = base64UrlSinRelleno(sha256(verificador.toByteArray(ASCII)))
    // Estado aleatorio contra falsificación de petición
    val estado = base64UrlSinRelleno(SecureRandom().generarBytes(16))

    // Se guardan temporalmente: se necesitan al volver
    almacen.guardar("pkce_verificador", verificador)
    almacen.guardar("oauth_estado", estado)

    // ③ NAVEGADOR DEL SISTEMA — nunca una vista web embebida
    val url = "$AUTORIZACION?client_id=$CLIENT_ID" +
              "&redirect_uri=$REDIRECT_URI&response_type=code&scope=openid+profile+offline_access" +
              "&code_challenge=$reto&code_challenge_method=S256&state=$estado"
    val respuesta = navegador.abrirYEsperarRedireccion(url)   // pestaña personalizada / sesión web

    // ⑤ Verificación del estado ANTES de continuar
    if (respuesta.estado != almacen.leer("oauth_estado")) {
      return Result.failure(ErrorAuth.EstadoInvalido)         // ← posible ataque
    }

    // ⑥ Canje del código con el VERIFICADOR
    val tokens = api.canjearCodigo(
      code = respuesta.codigo,
      codeVerifier = almacen.leer("pkce_verificador")!!,
      redirectUri = REDIRECT_URI,
      clientId = CLIENT_ID,                                    // SIN secreto de cliente
    )

    almacen.eliminar("pkce_verificador"); almacen.eliminar("oauth_estado")
    guardarTokens(tokens)
    return Result.success(Sesion(validarTokenIdentidad(tokens.idToken)))
  }

  // Validación del token de identidad — NO se confía en su contenido sin verificar
  private fun validarTokenIdentidad(idToken: String): Usuario {
    val jwt = JWT.decode(idToken)
    require(jwt.emisor == EMISOR_ESPERADO)               { "Emisor inválido" }
    require(jwt.audiencia.contains(CLIENT_ID))          { "Audiencia inválida" }
    require(jwt.expiracion.isAfter(Instant.now()))      { "Token expirado" }
    verificarFirmaConJWKS(jwt)                           // ← indispensable
    return Usuario(id = jwt.subject, correo = jwt.claim("email"))
  }
}
```

**Almacenamiento de tokens y renovación con rotación.**

```
private suspend fun guardarTokens(t: Tokens) {
  almacen.guardar("access_token", t.accessToken)
  // El token de RENOVACIÓN, con exigencia de autenticación si la biometría está activa
  if (biometriaActivada) almacenConBiometria.guardar("refresh_token", t.refreshToken)
  else                   almacen.guardar("refresh_token", t.refreshToken)
  almacen.guardar("access_expira", (Instant.now() + t.expiresIn.seconds).toString())
}

suspend fun tokenValido(): String? {
  val expira = Instant.parse(almacen.leer("access_expira") ?: return null)
  // Se renueva ANTES de expirar, con margen
  if (expira.isAfter(Instant.now() + 60.seconds)) return almacen.leer("access_token")

  val refresh = leerRefreshToken() ?: return null      // puede pedir biometría
  return try {
    val nuevos = api.renovar(refresh, CLIENT_ID)
    guardarTokens(nuevos)                               // ← ROTACIÓN: el refresh también es nuevo
    nuevos.accessToken
  } catch (e: Exception) {
    cerrarSesionLocal(); null                           // el refresh expiró o fue revocado
  }
}

suspend fun cerrarSesion() {
  // REVOCACIÓN EN EL SERVIDOR: borrar localmente no basta
  runCatching { api.revocar(almacen.leer("refresh_token"), CLIENT_ID) }
  almacen.limpiar()
  navegador.abrir("$FIN_SESION?client_id=$CLIENT_ID")   // cierra también la sesión del navegador
}
```

### Paso C — Desbloqueo biométrico

```
class DesbloqueoBiometrico(private val contexto: Contexto) {

  fun disponibilidad(): DisponibilidadBiometria = when (gestorBiometrico.puedeAutenticar(FUERTE)) {
    EXITO                      -> Disponible
    SIN_HARDWARE               -> SinSensor
    HARDWARE_NO_DISPONIBLE     -> TemporalmenteNoDisponible
    NINGUNA_REGISTRADA         -> SinBiometriaRegistrada
    ACTUALIZACION_REQUERIDA    -> RequiereActualizacion
    else                       -> NoDisponible
  }

  suspend fun activar(): Result<Unit> {
    if (disponibilidad() != Disponible) return Result.failure(...)
    // Clave vinculada a la biometría: se invalida si se registra una nueva
    generarClaveEnKeystore(
      alias = "clave_sesion",
      requiereAutenticacionUsuario = true,
      invalidarSiSeAgregaBiometria = true,       // ← protección clave
      permitirRespaldoDelDispositivo = true,     // PIN o patrón como alternativa
    )
    // Se regraba el token de renovación con esta clave
    val refresh = almacen.leer("refresh_token")!!
    almacenConBiometria.guardar("refresh_token", refresh)
    almacen.eliminar("refresh_token")            // ← se elimina del almacén sin biometría
    return Result.success(Unit)
  }

  suspend fun desbloquear(): Result<String> {
    val prompt = PromptBiometrico.Builder()
      .setTitulo("Ingresa a <app>")
      .setSubtitulo("Usa tu huella o rostro para continuar")
      .setTextoNegativo(null)                    // null: se ofrece el respaldo del dispositivo
      .setAutenticadoresPermitidos(BIOMETRICO_FUERTE or CREDENCIAL_DISPOSITIVO)
      .build()

    return try {
      val resultado = prompt.autenticar()        // el sistema muestra el diálogo
      if (!resultado.exito) return Result.failure(ErrorBiometria.Cancelado)
      // La clave del Keystore ya está desbloqueada: se lee el token
      Result.success(almacenConBiometria.leer("refresh_token")!!)

    } catch (e: ClaveInvalidadaException) {
      // ← BIOMETRÍA NUEVA REGISTRADA: la clave se invalidó. Es una PROTECCIÓN.
      limpiarSesionLocal()
      Result.failure(ErrorBiometria.RequiereAutenticacionCompleta)
    }
  }
}
```

**Los seis casos, manejados explícitamente.**

| Caso | Comportamiento implementado |
|---|---|
| Sin sensor | No se ofrece la opción; se usa autenticación completa |
| Sin biometría registrada | Se ofrece registrarla, con acceso al ajuste; no se bloquea |
| Falla varias veces | El sistema ofrece el respaldo del dispositivo automáticamente |
| **Biometría nueva registrada** | **Se detecta la invalidación de la clave, se limpia la sesión y se pide autenticación completa con explicación** |
| Usuario desactiva la biometría | Se vuelve al almacén sin biometría; se pide autenticación completa |
| Usuario cancela el diálogo | Se ofrece autenticación completa, sin insistir |

### Paso D — Verificar la autorización en el servidor

**La prueba que casi nadie hace.**

```bash
# 1. Se obtiene el token del usuario A
TOKEN_A=$(curl -s -X POST "$KEYCLOAK/token" -d "grant_type=password" \
  -d "client_id=$CLIENT_ID" -d "username=usuarioA" -d "password=..." | jq -r .access_token)

# 2. Se identifica un recurso del usuario B
RECURSO_B="<id de un recurso que pertenece a B>"

# 3. Se intenta acceder al recurso de B con el token de A
curl -i -H "Authorization: Bearer $TOKEN_A" "$API/v1/recursos/$RECURSO_B"
#    → DEBE responder 403 o 404. Si responde 200, la autorización NO se verifica
#      en el servidor y la app tiene una vulnerabilidad crítica.

# 4. Se intenta una operación de administrador con un token de usuario común
curl -i -X DELETE -H "Authorization: Bearer $TOKEN_A" "$API/v1/admin/recursos/$RECURSO_B"
#    → DEBE responder 403.

# 5. Se intenta con un token manipulado
TOKEN_FALSO=$(echo "$TOKEN_A" | sed 's/.$/X/')
curl -i -H "Authorization: Bearer $TOKEN_FALSO" "$API/v1/recursos"
#    → DEBE responder 401 · la firma no valida.
```

`docs/seguridad/PRUEBAS_AUTORIZACION.md`:

| # | Prueba | Respuesta esperada | Respuesta obtenida | Veredicto |
|---|---|---|---|---|
| 1 | Recurso ajeno con token válido | 403 o 404 | | |
| 2 | Operación de administrador con token de usuario | 403 | | |
| 3 | Token con firma manipulada | 401 | | |
| 4 | Token expirado | 401 | | |
| 5 | Sin cabecera de autorización | 401 | | |
| 6 | Token de otro cliente (audiencia distinta) | 401 | | |

### Trabajo del equipo fuera de la sesión — Sprint 4

> Lo que no alcance a completarse en la sesión lo ejecuta el equipo durante la semana, y llega al siguiente taller con el incremento listo. El docente lo revisa en el repositorio y en el tablero, no en clase.

**Sprint 4 Planning** al inicio, con Sprint Goal orientado a autenticación y seguridad de las conexiones. Luego, desarrollo.

---

### Paso E — Validar y corregir

El resultado no vale por estar hecho, sino por resistir una comprobación. Se ejecutan estas tres y **se corrige lo que falle antes de cerrar la sesión**.

1. Ejecutar `strings` sobre el artefacto de release y comprobar que **no** aparece ningún secreto de cliente.
2. Verificar en el tráfico que PKCE usa el método S256 y que el parámetro `state` se comprueba antes de canjear el código.
3. Revisar el registro de la app durante una sesión completa y comprobar que ningún token aparece en él.

> Lo que no se pueda corregir hoy se anota en la sección **Problemas y mejoras** de la evidencia, con lo que faltó y por qué. Un resultado parcial documentado con honestidad vale más que uno declarado sin prueba.

### Paso F — Registrar la evidencia y cerrar

Se versiona lo producido, se anota la URL de cada resultado y se responde en dos frases la pregunta de transferencia — **qué riesgo correría una organización real si esto se hiciera mal**.

---

## 3. Resultados

> **Evidencia obligatoria en GitHub.** Todo resultado de este taller se versiona en el repositorio del equipo. El informe **no consigna capturas sueltas**. Consigna la **URL** del artefacto en GitHub. Una captura no permite verificar autoría, fecha ni contenido; un enlace sí.
>
> | Qué se entrega | Dónde vive | Qué se escribe en el informe |
> |---|---|---|
> | Código y archivos de configuración | Rama del taller, fusionada a `develop` vía Pull Request | URL del Pull Request |
> | Documentos y matrices | `docs/`, en formato de texto versionable | URL del archivo en la rama |
> | Capturas y videos que el taller exija | `docs/evidencias/S11/` | URL del archivo |
> | Salida de comandos | `docs/evidencias/S11/salidas/*.txt` | URL del archivo |
>
> **Etiqueta del taller.** Al cerrar el taller se crea la etiqueta `taller-11` sobre el commit entregado:
>
> ```bash
> git tag -a taller-11 -m "Taller 11 · SI988"
> git push origin taller-11
> ```
>
> La URL que se consigna en el informe apunta a esa etiqueta:
> `https://github.com/<organizacion>/<repositorio>/tree/taller-11`
>
> **El informe es lo que se califica; el repositorio es lo que lo prueba.** Cada resultado de la sección 3 del informe lleva la URL con la que se verifica, y **un resultado sin su URL se califica como no logrado**, por bien redactado que esté. Lo que no se puede abrir no se puede dar por hecho.

### 3.1. Los tres resultados que se califican

Son los que la rúbrica evalúa. El resto de la lista tiene que existir, pero no se califica fila por fila.

| Resultado | Qué demuestra | Dónde está |
|---|---|---|
| **El flujo PKCE** | Método S256, navegador del sistema y `state` verificado antes del canje | Código y tráfico |
| **La validación del token de identidad** | Emisor, audiencia, expiración y firma comprobados | Código |
| **Las seis pruebas de autorización** | Ejecutadas contra el servidor, todas con su veredicto esperado | `PRUEBAS_AUTORIZACION.md` |

### 3.2. Lista de comprobación del taller

Todo esto debe existir al cerrar la sesión.

| # | Resultado esperado | Verificación |
|---|---|---|
| 1 | Proveedor de identidad configurado como **cliente público**, sin flujos obsoletos | Captura de la configuración |
| 2 | **PKCE con método S256** implementado | Código y tráfico |
| 3 | Autenticación en el **navegador del sistema**, no en vista web embebida | Demostración |
| 4 | **Parámetro `state` verificado** antes de canjear el código | Código y prueba |
| 5 | **Sin secreto de cliente** en la app | `strings` sobre el artefacto |
| 6 | Token de identidad **validado** — emisor, audiencia, expiración y firma | Código |
| 7 | Tokens en el **almacén seguro**, con la exigencia adecuada | Extracción del almacenamiento |
| 8 | **Renovación automática con rotación** del token de renovación | Prueba |
| 9 | Desbloqueo biométrico vinculado a la clave del almacén | Demostración en dispositivo |
| 10 | **Los seis casos de biometría manejados**, incluida la invalidación | Video |
| 11 | **Cierre de sesión con revocación en el servidor** | Tráfico y prueba |
| 12 | **Las seis pruebas de autorización ejecutadas**, todas con el veredicto esperado | `PRUEBAS_AUTORIZACION.md` |
| 13 | Ningún token en el registro de la app | `logcat` |
| 14 | Sprint 4 planificado | Tablero |

## Rúbrica procedimental (20 puntos)

Se aplica sobre el informe entregado y la evidencia enlazada en el repositorio. **Cada criterio se califica de forma independiente.**

| Criterio | 4 — Logrado | 2 — En proceso | 0 — Insuficiente |
|---|---|---|---|
| **Flujo PKCE** | Completo y correcto, con la evidencia que lo respalda | Completo con errores menores, o correcto pero sin toda la evidencia | Incompleto, o entregado sin ejecutar |
| **Desbloqueo biométrico** | Completo y correcto, con la evidencia que lo respalda | Completo con errores menores, o correcto pero sin toda la evidencia | Incompleto, o entregado sin ejecutar |
| **Evidencia verificable en el repositorio** | Cada resultado tiene su URL sobre la etiqueta `taller-NN`, y el enlace abre lo que dice | La mayoría tiene URL; alguna evidencia es una captura suelta | Se declaran resultados sin enlace, o el enlace no corresponde |
| **Rigor técnico de la implementación** | El código compila, las pruebas pasan y el análisis estático sale limpio | Compila y funciona, con avisos del análisis sin resolver | No compila, o se entregó sin ejecutar |
| **La evidencia entregada** | Las secciones de la plantilla completas; los resultados se sustentan con la evidencia enlazada | Secciones completas con sustento parcial | Faltan secciones o los resultados se afirman sin evidencia |

| Puntaje | Equivalencia |
|---|---|
| 18 – 20 | Destacado |
| 14 – 17 | Logrado |
| 6 – 13 | En proceso |
| 0 – 5 | Insuficiente |

> **Un resultado declarado sin evidencia enlazada no se califica**, aunque el trabajo se haya hecho. La tabla de la sección 3.1 es la lista de cotejo; esta rúbrica es lo que determina la nota.

## 4. Conclusiones

Mínimo tres. Líneas argumentales esperadas:

1. La biometría no autentica ante el servidor. Desbloquea una clave local que permite leer un token, y es el token lo que el servidor verifica. Diseñarla como sustituto de la autenticación produce una app que cree estar protegida y no lo está.
2. Ocultar una opción en la interfaz es usabilidad, no seguridad. La prueba de acceder al recurso de otro usuario con un token válido es la que revela si la autorización se verifica realmente en el servidor.
3. La invalidación de la clave al registrar una biometría nueva es una protección deliberada del sistema; una app que no la detecta y falla en silencio deja al usuario sin explicación y sin acceso.

## 5. Referencias Bibliográficas

- IETF. *RFC 6749 · The OAuth 2.0 Authorization Framework*. https://www.rfc-editor.org/rfc/rfc6749.html
- IETF. *RFC 7636 · Proof Key for Code Exchange by OAuth Public Clients*. https://www.rfc-editor.org/rfc/rfc7636.html
- IETF. *RFC 8252 · OAuth 2.0 for Native Apps*. https://www.rfc-editor.org/rfc/rfc8252.html
- IETF. *RFC 9700 · Best Current Practice for OAuth 2.0 Security*. https://www.rfc-editor.org/rfc/rfc9700.html
- OpenID Foundation. *OpenID Connect Core 1.0*. https://openid.net/specs/openid-connect-core-1_0.html
- Google. *Show a biometric authentication dialog*. https://developer.android.com/identity/sign-in/biometric-auth
- Google. *Biometric security levels*. https://source.android.com/docs/security/features/biometric
- Apple. *Local Authentication*. https://developer.apple.com/documentation/localauthentication
- OWASP (*Open Worldwide Application Security Project*) Foundation. *MASVS-AUTH*. https://mas.owasp.org/MASVS/
- OWASP Foundation. *Authentication Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- Keycloak. *Server Administration Guide*. https://www.keycloak.org/documentation

## 6. Anexos

- `anexo_A_flujo_autenticacion.png` — diagrama de secuencia
- `anexo_B_pkce_trafico.pdf` — evidencia del reto y del canje
- `anexo_C_biometria.mp4` — los seis casos
- `anexo_D_pruebas_autorizacion.pdf` — las seis pruebas con su veredicto
- `anexo_E_almacenamiento_tokens.png` — extracción tras la corrección

---

---

[Semana 11](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · **Taller de laboratorio**

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
