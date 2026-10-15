[Semana 10](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · **Taller de laboratorio**

# Taller de laboratorio 10 · Almacenamiento seguro, cifrado y verificación MASVS

**SI-988 · Soluciones Móviles II** - Semana 10 - Sesión 2 en laboratorio - calificación **procedimental**

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

---

## Qué entregas

| | |
|---|---|
| **Archivo** | `SI988-S10-TALLER-Grupo<N>.pdf` |
| **Plantilla obligatoria** | [SI988-PLANTILLA-TALLER.docx](../PLANTILLAS/SI988-PLANTILLA-TALLER.docx) |
| **Formato** | PDF exportado desde la plantilla en Word, con la carátula de la UPT, el índice actualizado y las capturas numeradas |
| **Qué va dentro** | Las secciones de la plantilla. La **5. Resultados y evidencias** se califica contra la tabla de resultados esperados de esta guía, y **cada resultado necesita la evidencia que lo demuestre**. No se copian de aquí los objetivos, la duración ni los resultados de aprendizaje |
| **Dónde se sube** | Aula virtual, tarea «Taller · Semana 10» |
| **Cuándo vence** | Según lo programado en el aula virtual |

> No se califica un informe entregado en `.docx`, sin carátula, sin los códigos de los integrantes o con resultados declarados sin evidencia.

---

El avance de Sprint 3 lo ejecuta el equipo fuera de la sesión.

## 1. Información sobre el evento práctico

### 1.1. Título del evento práctico

Auditoría del almacenamiento de la propia aplicación, migración de los datos sensibles al almacén seguro del sistema, implementación del cifrado de la base de datos local y verificación contra las categorías del OWASP (*Open Worldwide Application Security Project*) MASVS.

### 1.2. Objetivos

- **Auditar qué guarda hoy la app** y en qué estado, extrayendo su almacenamiento del dispositivo.
- **Migrar los tokens** al almacén seguro del sistema.
- Implementar el **cifrado de la base de datos local** con clave custodiada por el sistema.
- Corregir los **errores criptográficos** encontrados.
- Eliminar los **secretos embebidos** del artefacto.
- Verificar la app contra **seis categorías del MASVS**, con evidencia por control.
- **Demostrar la corrección**. Volver a extraer el almacenamiento y comprobar que ya no revela nada.

### 1.3. Resultados de Aprendizaje (RA)

- **RA1** Desarrolla la geolocalización en una app móvil.
- **RA2** Implementa y gestiona los permisos de geolocalización en una app móvil.

### 1.4. Recursos

| Recurso | Detalle |
|---|---|
| **OWASP MASVS** | https://mas.owasp.org/MASVS/ |
| **OWASP MASTG** | https://mas.owasp.org/MASTG/ |
| **Android Keystore** | https://developer.android.com/privacy-and-security/keystore |
| **Apple Keychain Services** | https://developer.apple.com/documentation/security/keychain-services |
| **MobSF** | Análisis estático del artefacto |
| **SQLCipher** o el cifrado nativo del stack | Cifrado de la base local |
| `adb` / herramientas de dispositivo | Extracción del almacenamiento |
| Bibliotecas de almacenamiento seguro | EncryptedSharedPreferences · flutter_secure_storage · react-native-keychain |

### 1.5. Seguridad

> **Dónde se trabaja.** El taller se hace en el **laboratorio de la universidad, sobre el emulador**. Cuando un escenario no se reproduce fielmente en el emulador, la verificación en un teléfono real la hace el equipo **fuera de la sesión** y adjunta el video como anexo. Ningún resultado del taller depende de tener un teléfono en clase.

1. **La extracción del almacenamiento se realiza solo en dispositivos propios del equipo**, con datos de prueba. Extraer datos de un dispositivo ajeno sin autorización constituye acceso no autorizado, tipificado en la Ley 30096.
2. Los hallazgos de la auditoría —tokens, rutas, claves— **no se publican** ni se suben al repositorio.
3. Si durante la auditoría se encuentra un token real de un servicio, **se revoca inmediatamente** antes de continuar.
4. **Ningún artefacto de release se distribuye** durante este laboratorio. Se trabaja con compilaciones de depuración firmadas para pruebas.

---

## 2. Procedimiento o Metodología

### Paso A — Auditar el almacenamiento actual

**A.1 — Extraer y revisar** (dispositivo propio, datos de prueba):

```bash
# --- Android · respaldo del almacenamiento de la app (compilación de depuración) ---
adb shell "run-as <paquete> ls -R /data/data/<paquete>"

# Preferencias — el lugar donde suelen aparecer los tokens en texto claro
adb shell "run-as <paquete> cat /data/data/<paquete>/shared_prefs/*.xml"

# Base de datos local
adb shell "run-as <paquete> ls /data/data/<paquete>/databases/"
adb exec-out run-as <paquete> cat databases/app.db > /tmp/app.db
sqlite3 /tmp/app.db ".tables"
sqlite3 /tmp/app.db "SELECT * FROM usuarios LIMIT 5;"     # ¿se lee en claro?

# Archivos y caché
adb shell "run-as <paquete> ls -R /data/data/<paquete>/files /data/data/<paquete>/cache"

# --- Secretos embebidos en el artefacto ---
unzip -o app-debug.apk -d /tmp/apk
strings /tmp/apk/classes*.dex | grep -Ei "api[_-]?key|secret|password|token|bearer" | head -20
grep -rEi "api[_-]?key|secret" /tmp/apk/res/values/strings.xml 2>/dev/null
```

**A.2 — Registro de hallazgos** (`docs/seguridad/AUDITORIA_ALMACENAMIENTO.csv`):

| # | Qué se encontró | Dónde | ¿En texto claro? | Categoría MASVS | Severidad | Qué permite a un atacante |
|---|---|---|---|---|---|---|
| 1 | Token de acceso | `shared_prefs/auth.xml` | **Sí** | MASVS-STORAGE | **Crítica** | Suplantar al usuario en la API |
| 2 | Correo y teléfono del usuario | `databases/app.db` | **Sí** | MASVS-STORAGE | Alta | Acceso a datos personales |
| 3 | Clave de API del proveedor de mapas | `strings.xml` | **Sí** | MASVS-STORAGE | Alta | Consumir la cuota del equipo |
| 4 | Fotos con metadatos de ubicación | `files/fotos/` | Sí | MASVS-PRIVACY | Media | Inferir ubicaciones del usuario |

> **Resultado esperado.** La mayoría de los equipos encuentra su token en texto claro. **No es un fracaso. Es el punto de partida del laboratorio.**

### Paso B — Migrar al almacén seguro del sistema

```
// --- DOMINIO: interfaz, como siempre ---
interface AlmacenSeguro {
  suspend fun guardar(clave: String, valor: String)
  suspend fun leer(clave: String): String?
  suspend fun eliminar(clave: String)
  suspend fun limpiar()
}

// --- IMPLEMENTACIÓN: usa el almacén del SISTEMA ---
// Android: EncryptedSharedPreferences con clave maestra en Keystore
// iOS:     Keychain con nivel de accesibilidad restringido
// Flutter: flutter_secure_storage, que envuelve ambos

class AlmacenSeguroImpl(contexto) : AlmacenSeguro {
  private val claveMaestra = ClaveMaestra.Builder(contexto)
      .setKeyScheme(AES256_GCM)                 // modo AUTENTICADO
      .setUserAuthenticationRequired(false)     // true si se exige biometría — Semana 11
      .build()                                   // ← la clave vive en el hardware seguro

  private val prefs = AlmacenCifrado.create(
      contexto, "auth_seguro", claveMaestra,
      esquemaClave = AES256_SIV, esquemaValor = AES256_GCM)

  override suspend fun guardar(clave, valor) = prefs.edit { putString(clave, valor) }
  override suspend fun leer(clave) = prefs.getString(clave, null)
  // ...
}

// iOS — nivel de accesibilidad del Keychain: la elección importa
//   kSecAttrAccessibleWhenUnlockedThisDeviceOnly
//     · solo con el dispositivo desbloqueado
//     · NO se incluye en respaldos ni se migra a otro dispositivo   ← el correcto para tokens
```

**Migración de los datos existentes** —los usuarios ya tienen el token en el lugar inseguro:

```
suspend fun migrarAlmacenamiento() {
  val prefsAntiguas = contexto.preferenciasNormales("auth")
  prefsAntiguas.getString("access_token", null)?.let { token ->
    almacenSeguro.guardar("access_token", token)
    prefsAntiguas.edit { remove("access_token") }        // ← SE ELIMINA del lugar inseguro
  }
  // Se registra que la migración ya ocurrió para no repetirla
  prefsAntiguas.edit { putBoolean("migrado_v2", true) }
}
```

> **La migración es obligatoria y se olvida siempre.** Guardar en el lugar correcto sin eliminar del incorrecto deja el dato expuesto exactamente igual.

### Paso C — Cifrar la base de datos local

```
// La clave de la base NUNCA está en el código: la genera y custodia el sistema
suspend fun obtenerClaveBaseDatos(): ByteArray {
  almacenSeguro.leer("db_key")?.let { return Base64.decode(it) }

  // Primera vez: se genera con el generador CRIPTOGRÁFICAMENTE SEGURO del sistema
  val clave = ByteArray(32).also { SecureRandom().nextBytes(it) }
  almacenSeguro.guardar("db_key", Base64.encode(clave))
  return clave
}

// Apertura de la base cifrada
val baseDatos = ConstructorBaseDatos(contexto, AppDatabase::class, "app.db")
    .abrirConClave(obtenerClaveBaseDatos())       // SQLCipher o el cifrado nativo
    .build()
```

**Cifrado de campos concretos** cuando no se cifra toda la base:

```
// Cifrado autenticado con IV ALEATORIO por operación
fun cifrar(textoPlano: String, alias: String): String {
  val cifrador = Cipher.getInstance("AES/GCM/NoPadding")     // modo AUTENTICADO
  cifrador.init(Cipher.ENCRYPT_MODE, obtenerClaveDelKeystore(alias))
  val iv = cifrador.iv                                        // ← ALEATORIO, generado por el sistema
  val cifrado = cifrador.doFinal(textoPlano.toByteArray(UTF_8))
  // El IV se almacena JUNTO al dato: no es secreto, pero debe ser único
  return Base64.encode(iv + cifrado)
}

fun descifrar(almacenado: String, alias: String): String {
  val bytes = Base64.decode(almacenado)
  val iv = bytes.copyOfRange(0, 12)                           // GCM usa IV de 12 bytes
  val cifrado = bytes.copyOfRange(12, bytes.size)
  val cifrador = Cipher.getInstance("AES/GCM/NoPadding")
  cifrador.init(Cipher.DECRYPT_MODE, obtenerClaveDelKeystore(alias), GCMParameterSpec(128, iv))
  return String(cifrador.doFinal(cifrado), UTF_8)             // lanza si el dato fue alterado
}
```

**Eliminación de secretos embebidos.**

| Secreto | Corrección |
|---|---|
| Clave de API del proveedor de mapas | **Al servidor**: la app pide al backend y este consulta al proveedor. Si el proveedor exige clave en cliente, se restringe por firma del artefacto y por dominio |
| URL del backend | No es secreto, pero se inyecta por configuración de compilación |
| Credenciales de servicios | **Nunca en el cliente.** Van al backend |
| Claves de firma | Fuera del repositorio, en el almacén de secretos de la CI |

### Paso D — Verificación MASVS con evidencia

`docs/seguridad/VERIFICACION_MASVS.csv` — se verifica **cada control con evidencia**:

| Categoría | Control verificado | ¿Cumple? | **Cómo se verificó** | Evidencia |
|---|---|---|---|---|
| **STORAGE** | Los datos sensibles se guardan en el almacén seguro del sistema | | Extracción del almacenamiento tras la corrección | Captura |
| **STORAGE** | No hay datos sensibles en el registro de la app | | `adb logcat` durante 10 min de uso | Registro |
| **STORAGE** | No hay datos sensibles en la caché ni en archivos temporales | | Inspección del directorio | Listado |
| **STORAGE** | La base local está cifrada | | Intento de abrir con `sqlite3` sin clave | Captura del fallo |
| **CRYPTO** | Se usan algoritmos y modos vigentes y autenticados | | Revisión de código y análisis de MobSF | Reporte |
| **CRYPTO** | Las claves las gestiona el almacén del sistema | | Revisión de código | Código |
| **CRYPTO** | Se usa un generador aleatorio criptográficamente seguro | | Revisión de código | Código |
| **CRYPTO** | El IV es aleatorio y único por operación | | Cifrar dos veces el mismo texto y comparar la salida | Prueba en verde |
| **AUTH** | La autorización se verifica en el servidor | | Llamar a la API con un token de otro usuario | Respuesta 403 |
| **AUTH** | Los tokens tienen expiración y se renuevan | | Inspección del token y prueba de expiración | Prueba |
| **NETWORK** | Todo el tráfico usa TLS | | mitmproxy: cero peticiones en claro | Captura |
| **NETWORK** | La app no acepta certificados inválidos | | Prueba con certificado autofirmado | Semana 12 |
| **PLATFORM** | Se declaran solo los permisos usados | | MobSF: permisos declarados vs. usados | Reporte |
| **PLATFORM** | Las capturas de pantalla de fondo no exponen datos | | Multitarea con una pantalla sensible abierta | Captura |
| **CODE** | Sin dependencias con vulnerabilidades conocidas | | Análisis de dependencias en la CI | Reporte |
| **CODE** | Sin secretos en el artefacto | | `strings` sobre el artefacto | Salida |

**Automatización en la CI.**

```yaml
      - name: MASVS-CODE · Vulnerabilidades en dependencias
        run: docker run --rm -v "$PWD":/src aquasec/trivy fs --scanners vuln --severity HIGH,CRITICAL --exit-code 1 /src

      - name: MASVS-STORAGE · Sin secretos en el código
        run: docker run --rm -v "$PWD":/src aquasec/trivy fs --scanners secret --exit-code 1 /src
```

### Paso E — Demostrar la corrección

Se **repite la extracción del Paso A** y se compara:

| Hallazgo original | Antes | Después | ¿Corregido? |
|---|---|---|---|
| Token en `shared_prefs` | Legible en texto claro | **Cifrado; ilegible sin el Keystore** | Sí |
| Datos personales en la base | Legibles con `sqlite3` | **`sqlite3` falla: base cifrada** | Sí |
| Clave de API en `strings.xml` | Presente | **Eliminada; ahora en el servidor** | Sí |
| Metadatos de ubicación en fotos | Presentes | **Eliminados antes de guardar** | Sí |

**Video de la demostración**, con la extracción antes y después.

### Trabajo del equipo fuera de la sesión — Sprint 3

> Lo que no alcance a completarse en la sesión lo ejecuta el equipo durante la semana, y llega al siguiente taller con el incremento listo. El docente lo revisa en el repositorio y en el tablero, no en clase.

Desarrollo de las historias del Sprint 3, incorporando las correcciones de seguridad como parte del incremento.

---

### Paso F — Validar y corregir

El resultado no vale por estar hecho, sino por resistir una comprobación. Se ejecutan estas tres y **se corrige lo que falle antes de cerrar la sesión**.

1. Repetir la extracción del almacenamiento sobre el artefacto corregido y comprobar que ya no aparece ningún dato sensible.
2. Ejecutar `strings` sobre el artefacto y verificar que no queda ninguna clave fija ni secreto de terceros.
3. Comprobar que la migración **elimina** el dato del lugar inseguro, no solo lo copia al seguro.

> Lo que no se pueda corregir hoy se anota en la sección **Problemas y mejoras** de la evidencia, con lo que faltó y por qué. Un resultado parcial documentado con honestidad vale más que uno declarado sin prueba.

### Paso G — Registrar la evidencia y cerrar

Se versiona lo producido, se anota la URL de cada resultado y se responde en dos frases la pregunta de transferencia — **qué riesgo correría una organización real si esto se hiciera mal**.

---

## 3. Resultados

> **Evidencia obligatoria en GitHub.** Todo resultado de este taller se versiona en el repositorio del equipo. El informe **no consigna capturas sueltas**. Consigna la **URL** del artefacto en GitHub. Una captura no permite verificar autoría, fecha ni contenido; un enlace sí.
>
> | Qué se entrega | Dónde vive | Qué se escribe en el informe |
> |---|---|---|
> | Código y archivos de configuración | Rama del taller, fusionada a `develop` vía Pull Request | URL del Pull Request |
> | Documentos y matrices | `docs/`, en formato de texto versionable | URL del archivo en la rama |
> | Capturas y videos que el taller exija | `docs/evidencias/S10/` | URL del archivo |
> | Salida de comandos | `docs/evidencias/S10/salidas/*.txt` | URL del archivo |
>
> **Etiqueta del taller.** Al cerrar el taller se crea la etiqueta `taller-10` sobre el commit entregado:
>
> ```bash
> git tag -a taller-10 -m "Taller 10 · SI988"
> git push origin taller-10
> ```
>
> La URL que se consigna en el informe apunta a esa etiqueta:
> `https://github.com/<organizacion>/<repositorio>/tree/taller-10`
>
> **El informe es lo que se califica; el repositorio es lo que lo prueba.** Cada resultado de la sección 3 del informe lleva la URL con la que se verifica, y **un resultado sin su URL se califica como no logrado**, por bien redactado que esté. Lo que no se puede abrir no se puede dar por hecho.

### 3.1. Los tres resultados que se califican

Son los que la rúbrica evalúa. El resto de la lista tiene que existir, pero no se califica fila por fila.

| Resultado | Qué demuestra | Dónde está |
|---|---|---|
| **La migración al almacén seguro** | El token movido y **eliminado** del lugar inseguro | Código y extracción |
| **El cifrado autenticado** | Vector de inicialización aleatorio por operación y detección de alteración, con sus pruebas | Pruebas en verde |
| **La extracción repetida** | El antes y el después en video, con el almacenamiento ya sin datos sensibles | Evidencia |

### 3.2. Lista de comprobación del taller

Todo esto debe existir al cerrar la sesión.

| # | Resultado esperado | Verificación |
|---|---|---|
| 1 | Auditoría del almacenamiento con **≥ 4 hallazgos** documentados | `AUDITORIA_ALMACENAMIENTO.csv` |
| 2 | Tokens **migrados al almacén seguro** del sistema | Código y extracción |
| 3 | **Migración implementada**: el dato se elimina del lugar inseguro | Código |
| 4 | Base de datos local **cifrada**, con clave custodiada por el sistema | Intento fallido de `sqlite3` |
| 5 | **Ninguna clave fija en el código** | Revisión y `strings` |
| 6 | **IV aleatorio y único por operación**, verificado por prueba | Prueba en verde |
| 7 | Modo de cifrado **autenticado**, que detecta la alteración | Prueba con dato alterado |
| 8 | Generador aleatorio **criptográficamente seguro** | Código |
| 9 | **Secretos eliminados del artefacto**; las claves de terceros al servidor | Salida de `strings` |
| 10 | **Los 16 controles MASVS verificados con evidencia** | `VERIFICACION_MASVS.csv` |
| 11 | CI ampliada con análisis de vulnerabilidades de dependencias | Ejecución en verde |
| 12 | **Extracción repetida**: el almacenamiento ya no revela datos sensibles | Video antes/después |
| 13 | Registro de la app sin datos sensibles durante 10 min de uso | `logcat` |
| 14 | Historias del Sprint 3 avanzando | Tablero |

## Rúbrica procedimental (20 puntos)

Se aplica sobre el informe entregado y la evidencia enlazada en el repositorio. **Cada criterio se califica de forma independiente.**

| Criterio | 4 — Logrado | 2 — En proceso | 0 — Insuficiente |
|---|---|---|---|
| **Auditar el almacenamiento actual** | Completo y correcto, con la evidencia que lo respalda | Completo con errores menores, o correcto pero sin toda la evidencia | Incompleto, o entregado sin ejecutar |
| **Migrar al almacén seguro del sistema** | Completo y correcto, con la evidencia que lo respalda | Completo con errores menores, o correcto pero sin toda la evidencia | Incompleto, o entregado sin ejecutar |
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

1. En una aplicación móvil el atacante controla el dispositivo. Cualquier secreto embebido en el artefacto es público, y por eso la seguridad no puede depender del cliente sino del servidor.
2. La diferencia entre el almacén seguro del sistema y un archivo cifrado por la app no es el algoritmo sino la custodia de la clave. En el primero la clave nunca sale del hardware seguro y la app jamás la ve.
3. Migrar un dato al almacén seguro sin eliminarlo del lugar inseguro deja la exposición intacta; la migración es la parte de la corrección que más se olvida y la que la vuelve efectiva.

## 5. Referencias Bibliográficas

- OWASP Foundation. *Mobile Application Security Verification Standard (MASVS)*. https://mas.owasp.org/MASVS/
- OWASP Foundation. *Mobile Application Security Testing Guide (MASTG)*. https://mas.owasp.org/MASTG/
- OWASP Foundation. *Mobile Application Security Weakness Enumeration (MASWE)*. https://mas.owasp.org/news/2024/07/30/new-maswe/
- Google. *Android Keystore system*. https://developer.android.com/privacy-and-security/keystore
- Google. *Security best practices*. https://developer.android.com/privacy-and-security/security-tips
- Apple. *Keychain services*. https://developer.apple.com/documentation/security/keychain-services
- Apple. *Restricting keychain item accessibility*. https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility
- NIST. *SP 800-175B · Guideline for Using Cryptographic Standards*. https://csrc.nist.gov/pubs/sp/800/175/b/r1/final
- OWASP Foundation. *Cryptographic Storage Cheat Sheet*. https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
- MobSF. *Documentation*. https://mobsf.github.io/docs/
- Ley 30096, Ley de Delitos Informáticos — límites de la auditoría sobre dispositivos ajenos.

## 6. Anexos

- `anexo_A_auditoria_almacenamiento.pdf` — **sin exponer los valores hallados**
- `anexo_B_verificacion_masvs.xlsx` — los 16 controles con su evidencia
- `anexo_C_antes_despues.mp4` — extracción antes y después de la corrección
- `anexo_D_mobsf.pdf`
- `anexo_E_ci_seguridad.png`

---

---

[Semana 10](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · **Taller de laboratorio**

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
