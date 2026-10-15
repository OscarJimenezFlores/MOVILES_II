[Semana 12](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · **Taller de laboratorio**

# Taller de laboratorio 12 · TLS, fijación de certificados y prueba con proxy interceptor

**SI-988 · Soluciones Móviles II** · Semana 12 · Sesión 2 en laboratorio · calificación **procedimental**

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

---

## Qué entregas

| | |
|---|---|
| **Archivo** | `SI988-S12-TALLER-Grupo<N>.pdf` |
| **Plantilla obligatoria** | [SI988-PLANTILLA-TALLER.docx](../PLANTILLAS/SI988-PLANTILLA-TALLER.docx) |
| **Formato** | PDF exportado desde la plantilla en Word, con la carátula de la UPT, el índice actualizado y las capturas numeradas |
| **Qué va dentro** | Las secciones de la plantilla. La **5. Resultados y evidencias** se califica contra la tabla de resultados esperados de esta guía, y **cada resultado necesita la evidencia que lo demuestre**. No se copian de aquí los objetivos, la duración ni los resultados de aprendizaje |
| **Dónde se sube** | Aula virtual, tarea «Taller · Semana 12» |
| **Cuándo vence** | Según lo programado en el aula virtual. El plazo se cuenta desde la sesión de laboratorio de la semana, se desarrolle el taller dentro de ella o fuera de ella |

> No se califica un informe entregado en `.docx`, sin carátula, sin los códigos de los integrantes o con resultados declarados sin evidencia.

---

El avance de Sprint 4 Review y Retrospective lo ejecuta el equipo fuera de la sesión.

## 1. Información sobre el evento práctico

### 1.1. Título del evento práctico

Aseguramiento de las conexiones de la aplicación mediante configuración de seguridad de red, implementación de fijación de clave pública con respaldo y plan de rotación, y verificación con un proxy interceptor de que la app rechaza la interceptación.

### 1.2. Objetivos

- Configurar la **seguridad de red** en ambas plataformas, prohibiendo el tráfico en claro.
- **Demostrar la vulnerabilidad**. Interceptar el tráfico con mitmproxy antes de la fijación.
- Implementar la **fijación de clave pública** con al menos un valor de respaldo.
- **Verificar que la app rechaza** la interceptación tras la fijación.
- Documentar el **plan de rotación** de las claves fijadas.
- Verificar los **controles del backend**. Límite de paginación, limitación de tasa y errores sin detalle.
- Completar la verificación **MASVS-NETWORK**.

### 1.3. Resultados de Aprendizaje (RA)

- **RA1** Desarrolla la geolocalización en una app móvil.
- **RA2** Implementa y gestiona los permisos de geolocalización en una app móvil.

### 1.4. Recursos

| Recurso | Detalle |
|---|---|
| **Android — Network security configuration** | https://developer.android.com/privacy-and-security/security-config |
| **Apple — Preventing insecure network connections** | https://developer.apple.com/documentation/security/preventing-insecure-network-connections |
| **OWASP MASVS-NETWORK** | https://mas.owasp.org/MASVS/ |
| **mitmproxy** | https://docs.mitmproxy.org/ |
| **openssl** | Extracción del resumen de la clave pública |
| **SSL Labs** o equivalente | Evaluación de la configuración TLS del backend |
| Emulador con el certificado de mitmproxy instalado | Se instala en el AVD, no en un teléfono |

### 1.5. Seguridad

> **Dónde se trabaja.** El taller se hace en el **laboratorio de la universidad, sobre el emulador**. Cuando un escenario no se reproduce fielmente en el emulador, la verificación en un teléfono real la hace el equipo **fuera de la sesión** y adjunta el video como anexo. Ningún resultado del taller depende de tener un teléfono en clase.

1. **La interceptación se realiza únicamente sobre el propio backend del equipo**, con datos de prueba. Interceptar el tráfico de servicios ajenos sin autorización es acceso no autorizado, tipificado en la Ley 30096.
2. El certificado de mitmproxy se instala **solo en el dispositivo de pruebas** y **se desinstala al terminar**. Mientras esté instalado, todo el tráfico del dispositivo es interceptable.
3. **La fijación no se activa en producción sin plan de rotación documentado y valor de respaldo.** Una fijación mal gestionada deja la app inutilizable.
4. Las excepciones de desarrollo **no deben llegar al artefacto de release**. Se verifica explícitamente.

---

## 2. Procedimiento o Metodología

### Paso A — Configuración de seguridad de red

**Android** — `res/xml/network_security_config.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>

  <!-- Base: NADA en claro, y en producción NO se confía en certificados
       instalados por el usuario. Esto es lo que bloquea un proxy interceptor. -->
  <base-config cleartextTrafficPermitted="false">
    <trust-anchors>
      <certificates src="system" />
    </trust-anchors>
  </base-config>

  <!-- Dominio propio: fijación de CLAVE PÚBLICA con RESPALDO -->
  <domain-config cleartextTrafficPermitted="false">
    <domain includeSubdomains="true">api.miapp.pe</domain>
    <pin-set expiration="aaaa-mm-dd">        <!-- ← FECHA DE EXPIRACIÓN OBLIGATORIA -->
      <!-- Clave actual -->
      <pin digest="SHA-256">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</pin>
      <!-- Clave de RESPALDO: ya generada, aún no en uso -->
      <pin digest="SHA-256">BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=</pin>
    </pin-set>
    <trust-anchors><certificates src="system" /></trust-anchors>
  </domain-config>

  <!-- Desarrollo: SOLO en la variante de depuración, NUNCA en release -->
  <debug-overrides>
    <trust-anchors>
      <certificates src="system" />
      <certificates src="user" />          <!-- permite mitmproxy en depuración -->
    </trust-anchors>
  </debug-overrides>

</network-security-config>
```

> **La `expiration` del conjunto de claves fijadas es la salvaguarda.** Pasada esa fecha, el sistema **ignora la fijación** en lugar de romper la app. Es la red de seguridad ante una rotación no prevista. **Fijar sin fecha de expiración es imprudente.**

**iOS** — App Transport Security en la configuración de la app:

```
· Se mantienen las restricciones por defecto: TLS 1.2 mínimo, algoritmos vigentes
· NO se declara ninguna excepción global de carga arbitraria
· Si se requiere una excepción para desarrollo, se limita al dominio local
  y se verifica que NO esté en la configuración de release
· La fijación se implementa en el delegado de sesión, validando la cadena
  y comparando el resumen de la clave pública
```

### Paso B — Demostrar la vulnerabilidad antes de fijar

```bash
# 1. mitmproxy en el equipo
mitmproxy --listen-port 8080 --set block_global=false

# 2. En el dispositivo · proxy manual apuntando al equipo, puerto 8080
# 3. En el dispositivo · abrir http://mitm.it e instalar el certificado
#    (Ajustes → Seguridad → Credenciales → Instalar certificado de CA)

# 4. Usar la app normalmente y observar en mitmproxy
```

`docs/seguridad/INTERCEPCION_ANTES.md` —lo que se observa **sin fijación**:

| Qué se observa | Registro |
|---|---|
| ¿Se ve el tráfico en claro dentro del túnel? | **Sí** — todo el contenido es legible |
| ¿Se ve la cabecera `Authorization` con el token? | **Sí** |
| ¿Se puede modificar una respuesta y la app la acepta? | **Sí** — se prueba alterando un campo |
| ¿Se puede reenviar una petición? | **Sí** |
| Datos personales visibles | Listar cuáles |

> **Este es el momento pedagógico del laboratorio.** El equipo ve **sus propios tokens** en la pantalla de mitmproxy. TLS estaba activo y funcionando. El problema es que el certificado del proxy era de confianza para el dispositivo.

### Paso C — Implementar la fijación

**Extraer el resumen de la clave pública.**

```bash
# Clave ACTUAL del servidor
openssl s_client -servername api.miapp.pe -connect api.miapp.pe:443 </dev/null 2>/dev/null \
 | openssl x509 -pubkey -noout \
 | openssl pkey -pubin -outform der \
 | openssl dgst -sha256 -binary \
 | openssl enc -base64
# → AAAAAAAA...=   ← clave actual

# Clave de RESPALDO · se genera AHORA, se guarda, y se usará en la próxima rotación
openssl genrsa -out respaldo.key 2048
openssl rsa -in respaldo.key -pubout -outform der \
 | openssl dgst -sha256 -binary | openssl enc -base64
# → BBBBBBBB...=   ← respaldo. La clave privada se guarda en el almacén de secretos.

# Verificación de la cadena completa
openssl s_client -servername api.miapp.pe -connect api.miapp.pe:443 -showcerts </dev/null
```

**Implementación programática** cuando el stack no usa la configuración declarativa:

```
val fijador = FijadorCertificados.Builder()
  .add("api.miapp.pe", "sha256/AAAAAAAA...=")        // actual
  .add("api.miapp.pe", "sha256/BBBBBBBB...=")        // respaldo — INDISPENSABLE
  .build()

val cliente = ClienteHttp.Builder()
  .fijadorCertificados(fijador)
  .build()

// Manejo del fallo de fijación: NO se reintenta ni se desactiva
onError { e ->
  if (e is FallaDeFijacion) {
    registrarEventoSeguridad("fijacion_fallida", dominio = e.dominio)   // sin datos personales
    mostrarPantalla(
      titulo = "No podemos conectarnos de forma segura",
      cuerpo = "La conexión no pudo verificarse. Esto puede ocurrir si estás en una red "
             + "no confiable. Intenta desde otra red o actualiza la aplicación.",
      accion = "Reintentar",
    )
    // NUNCA: continuar sin verificar, ni ofrecer "conectar de todas formas"
  }
}
```

**Plan de rotación** (`docs/seguridad/PLAN_ROTACION_FIJACION.md`) —obligatorio antes de activar:

| Paso | Actividad | Responsable | Cuándo |
|---|---|---|---|
| 1 | Generar la clave de respaldo y custodiar su privada | Responsable de infraestructura | Antes de activar la fijación |
| 2 | Publicar una versión de la app con **ambas** claves fijadas | Equipo | Antes de rotar |
| 3 | Esperar a que la mayoría de usuarios haya actualizado | — | Mínimo 30 días |
| 4 | Rotar el certificado del servidor a la clave de respaldo | Infraestructura | Ventana planificada |
| 5 | Generar una nueva clave de respaldo | Infraestructura | Inmediatamente después |
| 6 | Publicar una versión con la nueva pareja de claves | Equipo | Siguiente versión |
| **Salvaguarda** | La `expiration` del conjunto fijado desactiva la fijación si algo falla | — | Fecha declarada |
| **Contingencia** | Si la app queda inutilizable. Publicar corrección de emergencia y comunicar a los usuarios | Equipo | Inmediato |

### Paso D — Verificar el rechazo y los controles del backend

**D.1 — Verificar que la fijación funciona.**

```bash
# Con mitmproxy activo y el certificado aún instalado, se usa el artefacto de RELEASE
# → La app DEBE fallar la conexión y mostrar la pantalla de error de seguridad.
# → En mitmproxy se observa el handshake rechazado por el cliente.
```

`docs/seguridad/INTERCEPCION_DESPUES.md`:

| Verificación | Antes de fijar | Después de fijar |
|---|---|---|
| ¿mitmproxy ve el tráfico? | **Sí** | **No — conexión rechazada** |
| ¿La app muestra un error claro? | No aplica | **Sí, con explicación y sin opción de continuar** |
| ¿La app ofrece «conectar de todas formas»? | — | **No — nunca debe ofrecerlo** |
| ¿Funciona normalmente sin proxy? | Sí | **Sí** |

**D.2 — Controles del backend.**

```bash
# Límite máximo de paginación
curl -H "Authorization: Bearer $TOKEN" "$API/v1/recursos?limit=1000000"
#   → DEBE devolver como máximo el límite del servidor (p. ej. 100), no un millón

# Limitación de tasa
for i in $(seq 1 200); do
  curl -s -o /dev/null -w "%{http_code} " -H "Authorization: Bearer $TOKEN" "$API/v1/recursos"
done
#   → DEBE aparecer 429 en algún punto, con la cabecera Retry-After

# Errores sin detalle técnico
curl -H "Authorization: Bearer $TOKEN" "$API/v1/recursos/'; DROP TABLE--"
#   → DEBE devolver un error genérico, SIN traza, SIN nombre de motor de base de datos

# Versión mínima de app admitida
curl -H "Authorization: Bearer $TOKEN" -H "X-App-Version: 0.0.1" "$API/v1/recursos"
#   → Idealmente 426 o una respuesta que indique actualización requerida
```

**D.3 — Verificación MASVS-NETWORK completa.**

| Control | ¿Cumple? | Cómo se verificó | Evidencia |
|---|---|---|---|
| Todo el tráfico usa TLS 1.2 o superior | | mitmproxy y evaluación del servidor | |
| No hay tráfico en claro en ningún dominio | | Configuración y tráfico observado | |
| La app **rechaza certificados no confiables** | | Prueba con proxy interceptor | |
| **La app rechaza la interceptación** (fijación) | | Prueba con mitmproxy sobre el artefacto de release | |
| La app **no ofrece continuar** ante un fallo de verificación | | Revisión del código y de la interfaz | |
| Las excepciones de desarrollo **no están en release** | | Inspección del artefacto de release | |
| El backend limita la tasa | | Prueba de 200 peticiones | |
| El backend limita la paginación | | Prueba con límite excesivo | |
| Los errores no filtran detalle técnico | | Pruebas de error | |

### Trabajo del equipo fuera de la sesión — Sprint 4 Review y Retrospective

> Lo que no alcance a completarse en la sesión lo ejecuta el equipo durante la semana, y llega al siguiente taller con el incremento listo. El docente lo revisa en el repositorio y en el tablero, no en clase.

**Review** con interesados externos, demostrando el incremento en el emulador del laboratorio. Se demuestran también las **medidas de seguridad**. El desbloqueo biométrico y el rechazo de la interceptación, que son entregables visibles.

**Retrospective** con el formato de la Semana 06 y **una sola acción comprometida**, que entra al Sprint Backlog 5.

**Cálculo de velocidad.** Con cuatro sprints completados, se promedian los **tres últimos** para proyectar el Sprint 5, que es el último y debe cerrarse completo.

```bash
git add . && git commit -m "S12: seguridad de conexiones, fijacion verificada y cierre del Sprint 4"
git tag -a sprint-4 -m "Sprint 4 completado - Unidad II cerrada"
```

---

### Paso E — Validar y corregir

El resultado no vale por estar hecho, sino por resistir una comprobación. Se ejecutan estas tres y **se corrige lo que falle antes de cerrar la sesión**.

1. Repetir la interceptación **sobre el artefacto de release**, no sobre el de depuración, y comprobar que se rechaza.
2. Inspeccionar el artefacto de release y verificar que las excepciones de desarrollo no viajan en él.
3. Comprobar que la app **no ofrece continuar** ante un fallo de verificación del certificado.

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
> | Capturas y videos que el taller exija | `docs/evidencias/S12/` | URL del archivo |
> | Salida de comandos | `docs/evidencias/S12/salidas/*.txt` | URL del archivo |
>
> **Etiqueta del taller.** Al cerrar el taller se crea la etiqueta `taller-12` sobre el commit entregado:
>
> ```bash
> git tag -a taller-12 -m "Taller 12 · SI988"
> git push origin taller-12
> ```
>
> La URL que se consigna en el informe apunta a esa etiqueta:
> `https://github.com/<organizacion>/<repositorio>/tree/taller-12`
>
> **El informe es lo que se califica; el repositorio es lo que lo prueba.** Cada resultado de la sección 3 del informe lleva la URL con la que se verifica, y **un resultado sin su URL se califica como no logrado**, por bien redactado que esté. Lo que no se puede abrir no se puede dar por hecho.

### 3.1. Los tres resultados que se califican

Son los que la rúbrica evalúa. El resto de la lista tiene que existir, pero no se califica fila por fila.

| Resultado | Qué demuestra | Dónde está |
|---|---|---|
| **El antes y el después** | El token visible antes de fijar y la conexión rechazada después, sobre release | `INTERCEPCION_ANTES.md`, `INTERCEPCION_DESPUES.md` y video |
| **La clave de respaldo** | Generada y fijada junto a la actual, con fecha de expiración declarada | Configuración |
| **El plan de rotación** | Los seis pasos y la contingencia si la clave fijada caduca en producción | `PLAN_ROTACION_FIJACION.md` |

### 3.2. Lista de comprobación del taller

Todo esto debe existir al cerrar la sesión.

| # | Resultado esperado | Verificación |
|---|---|---|
| 1 | Configuración de seguridad de red en ambas plataformas, **sin tráfico en claro** | Archivos de configuración |
| 2 | **Certificados de usuario no confiados** en la configuración de producción | Configuración |
| 3 | Excepciones de desarrollo **solo en la variante de depuración** | Inspección del artefacto de release |
| 4 | **Interceptación demostrada antes de fijar**, con el token visible | `INTERCEPCION_ANTES.md` y captura |
| 5 | Resumen de la clave pública extraído correctamente | Salida de `openssl` |
| 6 | **Clave de respaldo generada y fijada** junto a la actual | Configuración |
| 7 | **Fecha de expiración declarada** en el conjunto de claves fijadas | Configuración |
| 8 | **Interceptación rechazada tras fijar**, verificada sobre el artefacto de release | `INTERCEPCION_DESPUES.md` y video |
| 9 | La app **no ofrece continuar** ante un fallo de verificación | Revisión y demostración |
| 10 | **Plan de rotación documentado**, con los seis pasos y la contingencia | `PLAN_ROTACION_FIJACION.md` |
| 11 | Límite máximo de paginación verificado en el backend | Salida de la prueba |
| 12 | Limitación de tasa verificada, con `429` y `Retry-After` | Salida de la prueba |
| 13 | Errores del backend **sin detalle técnico** | Salida de la prueba |
| 14 | **Los nueve controles MASVS-NETWORK verificados con evidencia** | Tabla completa |
| 15 | Sprint 4 Review con interesados y Retrospective con una acción | Documentos y etiqueta `sprint-4` |

## Rúbrica procedimental (20 puntos)

Se aplica sobre el informe entregado y la evidencia enlazada en el repositorio. **Cada criterio se califica de forma independiente.**

| Criterio | 4 — Logrado | 2 — En proceso | 0 — Insuficiente |
|---|---|---|---|
| **Demostrar la vulnerabilidad antes de fijar** | Completo y correcto, con la evidencia que lo respalda | Completo con errores menores, o correcto pero sin toda la evidencia | Incompleto, o entregado sin ejecutar |
| **Implementar la fijación** | Completo y correcto, con la evidencia que lo respalda | Completo con errores menores, o correcto pero sin toda la evidencia | Incompleto, o entregado sin ejecutar |
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

1. TLS puede estar funcionando perfectamente y aun así el tráfico ser legible para un atacante que instaló su certificado en el dispositivo; ver los propios tokens en la pantalla de un proxy es lo que hace comprensible por qué existe la fijación.
2. La fijación de certificados es la medida que más fácilmente inutiliza una app publicada — sin clave de respaldo, sin fecha de expiración y sin plan de rotación, su riesgo supera al beneficio.
3. Asegurar el canal no protege el backend — cualquiera puede llamar a la API con las credenciales extraídas del artefacto, y por eso los límites de paginación, de tasa y de autorización deben imponerse en el servidor.

## 5. Referencias Bibliográficas

- Google. *Network security configuration*. https://developer.android.com/privacy-and-security/security-config
- Google. *Security with HTTPS and SSL*. https://developer.android.com/privacy-and-security/security-ssl
- Apple. *Preventing insecure network connections*. https://developer.apple.com/documentation/security/preventing-insecure-network-connections
- Apple. *Identity pinning: How to configura server certificates for your app*. https://developer.apple.com/news/?id=g9ejcf8y
- OWASP (*Open Worldwide Application Security Project*) Foundation. *MASVS-NETWORK*. https://mas.owasp.org/MASVS/
- OWASP Foundation. *Certificate and Public Key Pinning*. https://owasp.org/www-community/controls/Certificate_and_Public_Key_Pinning
- OWASP Foundation. *Transport Layer Security Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
- IETF. *RFC 8446 · The Transport Layer Security (TLS) Protocol Version 1.3*. https://www.rfc-editor.org/rfc/rfc8446.html
- mitmproxy. *Documentation*. https://docs.mitmproxy.org/
- Ley 30096, Ley de Delitos Informáticos — límites de la interceptación de tráfico.

## 6. Anexos

- `anexo_A_intercepcion_antes.pdf` — **con los tokens enmascarados**
- `anexo_B_intercepcion_despues.mp4` — rechazo verificado
- `anexo_C_plan_rotacion.pdf`
- `anexo_D_masvs_network.xlsx` — los nueve controles
- `anexo_E_controles_backend.pdf`
- `anexo_F_sprint4_review_retro.pdf`

---

---

[Semana 12](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · **Taller de laboratorio**

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
