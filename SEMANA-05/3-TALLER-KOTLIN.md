[Semana 05](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · [Flutter](3-TALLER-FLUTTER.md) · **Kotlin Multiplatform**

# Taller 05 · Implementación en **Kotlin Multiplatform**

**SI-988 · Soluciones Móviles II** · Semana 05 · Laboratorio · 100 min

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

> Código del **Paso C** del [Taller 05](3-TALLER.md). Los pasos A, B, D y E no dependen del stack elegido.
>
> **Requisito previo.** El servicio SOAP corriendo (`python3 servicio-soap/servidor.py`) y las llamadas del Paso B ya ejecutadas con `curl`.

---

## C.1 — Dependencias

En `gradle/libs.versions.toml`:

```toml
[versions]
xmlutil = "0.90.3"

[libraries]
xmlutil-core = { module = "io.github.pdvrieze.xmlutil:core", version.ref = "xmlutil" }
xmlutil-serialization = { module = "io.github.pdvrieze.xmlutil:serialization", version.ref = "xmlutil" }
```

En `composeApp/build.gradle.kts`, dentro de `commonMain.dependencies`:

```kotlin
implementation(libs.xmlutil.core)
implementation(libs.xmlutil.serialization)
```

`xmlutil` funciona en `commonMain`. Las alternativas de la JVM —`javax.xml`, JAXB— solo compilan en `androidMain` y obligarían a duplicar el cliente por plataforma.

## C.2 — La URL según el entorno

`commonMain/.../core/Config.kt`:

```kotlin
package pe.edu.upt.si988.app.core

// En el emulador de Android, 10.0.2.2 apunta a la máquina anfitriona.
// localhost apuntaría al propio emulador y la conexión sería rechazada.
expect val soapBaseUrl: String
```

`androidMain/.../core/Config.android.kt`:

```kotlin
actual val soapBaseUrl: String = "http://10.0.2.2:8080"
```

Android bloquea tráfico HTTP en claro desde API 28. Solo en el build de depuración, `androidApp/src/debug/AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:usesCleartextTraffic="true" />
</manifest>
```

El directorio es `src/debug/`. En `src/main/` habilitaría cleartext también en release.

## C.3 — Serializar el request

En REST, el body del request es JSON y la librería HTTP lo serializa sola. En SOAP no el protocolo exige que **cada request viaje envuelto en una estructura XML fija**, llamada *envelope*. No hay librería en Flutter ni en Kotlin que la genere automáticamente, así que la construye el cliente.

La estructura es siempre la misma:

```
<soap:Envelope>            ← el sobre; obligatorio, siempre igual
  <soap:Body>              ← el contenido; obligatorio
    <OperacionRequest>     ← el nombre lo define el WSDL
      <parametro>valor</parametro>
    </OperacionRequest>
  </soap:Body>
</soap:Envelope>
```

Comparado con lo que ya hizo en la Semana 04:

| | REST (Semana 04) | SOAP (esta semana) |
|---|---|---|
| Body del request | `{"codigo":"P-002"}` | Los 6 elementos XML de arriba |
| Quién lo genera | La librería, con `json_serializable` | **Usted, a mano** |
| Cómo se elige la operación | La URL: `GET /productos/P-002` | El nombre del elemento y la cabecera `SOAPAction` |
| Tamaño típico | ~30 bytes | ~250 bytes |

Lo único que cambia entre una llamada y otra son el nombre de la operación y los parámetros. Todo lo demás es fijo. Por eso se escribe **una función que arma el XML** y se reutiliza, en lugar de repetir el bloque en cada llamada.

`commonMain/.../data/soap/Envelope.kt`:

```kotlin
package pe.edu.upt.si988.app.data.soap

const val NS_SERVICIO = "http://si988.upt.pe/servicio"

/** Escapa los cinco caracteres reservados de XML. */
private fun escaparXml(v: String): String = v
    .replace("&", "&amp;")
    .replace("<", "&lt;")
    .replace(">", "&gt;")
    .replace("\"", "&quot;")
    .replace("'", "&apos;")

/**
 * Genera el XML del request SOAP para una operación del WSDL.
 *
 * Ejemplo: construirEnvelope("ObtenerProducto", mapOf("codigo" to "P-002"))
 * produce el envelope completo, listo para enviar como body del POST.
 */
fun construirEnvelope(operacion: String, parametros: Map<String, String>): String {
    val cuerpo = parametros.entries.joinToString("") { (clave, valor) ->
        "<$clave>${escaparXml(valor)}</$clave>"
    }
    return """<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <${operacion}Request xmlns="$NS_SERVICIO">$cuerpo</${operacion}Request>
  </soap:Body>
</soap:Envelope>"""
}
```

**Por qué los valores pasan por `escaparXml`.** Si el código de producto llega con `<` o `&`, el XML sale inválido y el servicio responde error. Si llega con `</codigo><otro>`, el atacante inserta elementos en el request. Es **inyección de XML**, el equivalente a un `SQL injection`.

Compruébelo:

```kotlin
println(construirEnvelope("ObtenerProducto", mapOf("codigo" to "P-002")))
println(construirEnvelope("ObtenerProducto", mapOf("codigo" to "A & B <script>")))
// el segundo produce &amp; y &lt;script&gt;, no XML roto
```

## C.4 — Análisis de la respuesta

`xmlutil` no resuelve entidades externas, por lo que no expone a XXE. Se añade un límite de tamaño para acotar la expansión de entidades:

```kotlin
package pe.edu.upt.si988.app.data.soap

import nl.adaptivity.xmlutil.XmlStreaming
import nl.adaptivity.xmlutil.EventType

private const val MAX_BYTES_RESPONSE = 2 * 1024 * 1024

/** Devuelve el texto del primer elemento con ese nombre local, ignorando el namespace. */
fun leerTexto(xml: String, nombreLocal: String): String? {
    require(xml.length <= MAX_BYTES_RESPONSE) { "Response demasiado grande" }
    val reader = XmlStreaming.newReader(xml)
    while (reader.hasNext()) {
        if (reader.next() == EventType.START_ELEMENT && reader.localName == nombreLocal) {
            return reader.readSimpleElement()
        }
    }
    return null
}

/** Devuelve los bloques de texto de todos los elementos con ese nombre local. */
fun leerBloques(xml: String, nombreLocal: String): List<Map<String, String>> {
    val salida = mutableListOf<Map<String, String>>()
    val reader = XmlStreaming.newReader(xml)
    var actual: MutableMap<String, String>? = null
    while (reader.hasNext()) {
        when (reader.next()) {
            EventType.START_ELEMENT ->
                if (reader.localName == nombreLocal) actual = mutableMapOf()
                else actual?.put(reader.localName, reader.readSimpleElement())
            EventType.END_ELEMENT ->
                if (reader.localName == nombreLocal) { actual?.let(salida::add); actual = null }
            else -> Unit
        }
    }
    return salida
}
```

## C.5 — Detección del Fault

`commonMain/.../data/soap/SoapFault.kt`:

```kotlin
package pe.edu.upt.si988.app.data.soap

class SoapFault(
    val codigo: String,
    val razon: String,
) : Exception("SoapFault($codigo): $razon")

/**
 * Devuelve el Fault si el cuerpo lo contiene.
 * Se invoca siempre, sin consultar el status HTTP: el servicio puede
 * devolver un Fault con HTTP 200.
 */
fun detectarFault(xml: String): SoapFault? {
    if (!xml.contains("Fault")) return null
    return SoapFault(
        codigo = leerTexto(xml, "CodigoNegocio") ?: "DESCONOCIDO",
        razon = leerTexto(xml, "faultstring") ?: "Error del servicio",
    )
}
```

## C.6 — El cliente con medición

`commonMain/.../data/soap/CatalogoSoap.kt`:

```kotlin
package pe.edu.upt.si988.app.data.soap

import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import kotlin.time.TimeSource
import pe.edu.upt.si988.app.core.soapBaseUrl

data class MedicionSoap(
    val bytesRequest: Int,
    val bytesResponse: Int,
    val milisegundos: Long,
    val statusHttp: Int,
)

data class ProductoDto(
    val codigo: String,
    val nombre: String,
    val precio: Double,
    val stock: Int,
)

class CatalogoSoap(private val client: HttpClient) {

    var ultimaMedicion: MedicionSoap? = null
        private set

    suspend fun listarProductos(): List<ProductoDto> {
        val xml = invocar("ListarProductos", emptyMap())
        return leerBloques(xml, "producto").map {
            ProductoDto(
                codigo = it["codigo"].orEmpty(),
                nombre = it["nombre"].orEmpty(),
                precio = it["precio"]?.toDoubleOrNull() ?: 0.0,
                stock = it["stock"]?.toIntOrNull() ?: 0,
            )
        }
    }

    suspend fun obtenerProducto(codigo: String): ProductoDto {
        val xml = invocar("ObtenerProducto", mapOf("codigo" to codigo))
        return ProductoDto(
            codigo = leerTexto(xml, "codigo").orEmpty(),
            nombre = leerTexto(xml, "nombre").orEmpty(),
            precio = leerTexto(xml, "precio")?.toDoubleOrNull() ?: 0.0,
            stock = leerTexto(xml, "stock")?.toIntOrNull() ?: 0,
        )
    }

    private suspend fun invocar(operacion: String, params: Map<String, String>): String {
        val envelope = construirEnvelope(operacion, params)
        val inicio = TimeSource.Monotonic.markNow()

        val response = client.post("$soapBaseUrl/servicio") {
            contentType(ContentType.Text.Xml.withCharset(Charsets.UTF_8))
            header("SOAPAction", "\"$NS_SERVICIO/$operacion\"")
            setBody(envelope)
        }
        val cuerpo = response.bodyAsText()
        val transcurrido = inicio.elapsedNow().inWholeMilliseconds

        ultimaMedicion = MedicionSoap(
            bytesRequest = envelope.length,
            bytesResponse = cuerpo.length,
            milisegundos = transcurrido,
            statusHttp = response.status.value,
        )

        detectarFault(cuerpo)?.let { throw it }
        return cuerpo
    }
}
```

El cliente se construye con `expectSuccess = false`, configurado en la Semana 04. Con `expectSuccess = true` Ktor lanzaría en el 500 antes de que el código llegue a `detectarFault`, y el `CodigoNegocio` del detalle se perdería.

## C.7 — Pruebas

`commonTest/.../CatalogoSoapTest.kt`, con `MockEngine`:

```kotlin
import io.ktor.client.engine.mock.*
import io.ktor.http.*
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

private val FAULT_CON_200 = """<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body>
<soap:Fault><faultcode>soap:Server</faultcode>
<faultstring>Error de negocio devuelto con HTTP 200</faultstring>
<detail><CodigoNegocio>FAULT_CON_200</CodigoNegocio></detail>
</soap:Fault></soap:Body></soap:Envelope>"""

class CatalogoSoapTest {

    @Test
    fun `detecta el Fault aunque el status sea 200`() = runTest {
        val engine = MockEngine { respond(FAULT_CON_200, HttpStatusCode.OK) }
        val catalogo = CatalogoSoap(crearHttpClient(engine, "http://t", esDebug = false))

        val e = assertFailsWith<SoapFault> { catalogo.obtenerProducto("ERR-200") }
        assertEquals("FAULT_CON_200", e.codigo)
    }

    @Test
    fun `detecta el Fault con status 500`() = runTest {
        val engine = MockEngine { respond(FAULT_CON_200, HttpStatusCode.InternalServerError) }
        val catalogo = CatalogoSoap(crearHttpClient(engine, "http://t", esDebug = false))
        assertFailsWith<SoapFault> { catalogo.obtenerProducto("ERR-404") }
    }
}
```

```bash
./gradlew :composeApp:testDebugUnitTest
./gradlew :composeApp:installDebug
```

## C.8 — Registro de mediciones

```kotlin
val catalogo = CatalogoSoap(client)
repeat(3) {
    catalogo.listarProductos()
    val m = catalogo.ultimaMedicion!!
    println("req=${m.bytesRequest}B res=${m.bytesResponse}B ${m.milisegundos}ms")
}
```

Se registra la mediana de las tres ejecuciones en `docs/api/MEDICIONES.md`.

---

## Verificación de cierre

| | Comprobación |
|---|---|
| ☐ | El servicio responde desde la app en el emulador |
| ☐ | `ERR-404` lanza `SoapFault` con código `PROD_NO_ENCONTRADO` |
| ☐ | `ERR-200` lanza `SoapFault` pese a llegar con HTTP 200 |
| ☐ | Los parámetros del envelope pasan por `escaparXml` |
| ☐ | Las dos pruebas del Fault pasan |
| ☐ | El código está en `commonMain`, salvo `soapBaseUrl` |
| ☐ | Las mediciones se tomaron tres veces |

---

## Errores frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `Connection refused` | `localhost` en el emulador | Use `10.0.2.2` |
| `CLEARTEXT communication not permitted` | Android bloquea HTTP | `usesCleartextTraffic` en `src/debug/` |
| `ClientRequestException` antes de leer el Fault | `expectSuccess = true` | Configúrelo en `false` |
| `leerTexto` devuelve `null` | Se buscó con prefijo de namespace | Use el nombre local, sin prefijo |
| `Unresolved reference: XmlStreaming` | Falta `xmlutil` en `commonMain` | Añada la dependencia en el source set correcto |
| El Fault con 200 no se detecta | Se consultó el status antes que el cuerpo | Invoque `detectarFault` siempre |

---

## Con Antigravity

> «Implementa `CatalogoSoap` en `commonMain` para el servicio de `docs/api/catalogo.wsdl`, usando Ktor y `xmlutil`. Los parámetros del envelope deben escaparse. El cliente usa `expectSuccess = false` y debe invocar `detectarFault` sobre el cuerpo antes de leer datos, sin consultar el status HTTP. Registra bytes de request, bytes de response y milisegundos. Muéstrame el plan antes de escribir código.»

Verifique que el Fault se detecta con HTTP 200 y que nada quedó en `androidMain` salvo `soapBaseUrl`.

---

---

[Semana 05](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · [Flutter](3-TALLER-FLUTTER.md) · **Kotlin Multiplatform**

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
