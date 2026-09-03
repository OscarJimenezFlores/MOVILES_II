[Semana 04](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · [Flutter](3-TALLER-FLUTTER.md) · **Kotlin Multiplatform**

# Taller 04 · Implementación en **Kotlin Multiplatform**

**SI-988 · Soluciones Móviles II** · Semana 04 · Laboratorio · 100 min

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

> Implementación del [Taller 04](3-TALLER.md) en la Kotlin Multiplatform. El contrato OpenAPI, los objetivos y la evaluación están en el taller; aquí está el código.

---

## Dependencias

En `gradle/libs.versions.toml`:

```toml
[versions]
ktor = "3.0.3"
serialization = "1.7.3"

[libraries]
ktor-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
ktor-content-negotiation = { module = "io.ktor:ktor-client-content-negotiation", version.ref = "ktor" }
ktor-json = { module = "io.ktor:ktor-serialization-kotlinx-json", version.ref = "ktor" }
ktor-logging = { module = "io.ktor:ktor-client-logging", version.ref = "ktor" }
ktor-okhttp = { module = "io.ktor:ktor-client-okhttp", version.ref = "ktor" }
ktor-darwin = { module = "io.ktor:ktor-client-darwin", version.ref = "ktor" }
ktor-mock = { module = "io.ktor:ktor-client-mock", version.ref = "ktor" }
kotlinx-serialization-json = { module = "org.jetbrains.kotlinx:kotlinx-serialization-json", version.ref = "serialization" }
```

`commonMain` toma `ktor-core`, negociación de contenido, JSON y registro. `androidMain` toma `ktor-okhttp`; `iosMain`, `ktor-darwin`.

---

## Paso A — Contrato en OpenAPI (15 min)

> **El contrato es el de su app.** `/items` es un marcador de posición: el equipo define los recursos de su propio dominio en `docs/api/openapi.yaml`. El mock server sirve **ese** contrato, no uno genérico.


Sin código específico del stack: el contrato está en el [taller](3-TALLER.md). Levante el mock server:

```bash
docker run --rm -p 4010:4010 -v "$PWD/docs/api:/api" \
  stoplight/prism:4 mock -h 0.0.0.0 /api/openapi.yaml
curl -i http://localhost:4010/items
```

> En el emulador, `localhost` es el propio emulador. La máquina anfitriona es **`10.0.2.2`**. Es la causa más frecuente de `Connection refused` en este taller.

---

## Paso B — Cliente HTTP e interceptores (25 min)

`commonMain/.../core/network/HttpClientFactory.kt`:

```kotlin
package pe.edu.upt.si988.app.core.network

import io.ktor.client.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.logging.*
import io.ktor.client.request.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json

private const val SENSIBLES_ENMASCARADAS = "***"

fun crearHttpClient(engine: HttpClientEngine, baseUrl: String, esDebug: Boolean) =
    HttpClient(engine) {
        expectSuccess = false                       // el mapeo de errores es nuestro

        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true; isLenient = false })
        }

        install(HttpTimeout) {
            connectTimeoutMillis = 10_000
            requestTimeoutMillis = 10_000
            socketTimeoutMillis = 10_000
        }

        // --- Registro: solo en depuración, nunca el cuerpo ---
        if (esDebug) {
            install(Logging) {
                level = LogLevel.HEADERS             // NO LogLevel.ALL
                sanitizeHeader { nombre ->
                    nombre.equals(HttpHeaders.Authorization, ignoreCase = true) ||
                    nombre.equals(HttpHeaders.Cookie, ignoreCase = true)
                }
            }
        }

        // --- Reintento: solo donde corresponde ---
        install(HttpRequestRetry) {
            maxRetries = 3
            retryIf { _, respuesta ->
                respuesta.status.value == 429 || respuesta.status.value >= 500
            }
            retryOnExceptionIf { _, causa -> causa is java.io.IOException }
            delayMillis { intento -> 400L shl (intento - 1) }   // backoff exponencial
        }

        defaultRequest {
            url(baseUrl)
            accept(ContentType.Application.Json)
        }
    }
```

> **Tres decisiones que se evalúan.** `LogLevel.HEADERS`, nunca `ALL`: `ALL` imprime el cuerpo, y ahí van los datos personales. `sanitizeHeader` enmascara el token. Y `retryIf` **solo** cubre `429` y `5xx`: reintentar un `400` es repetir el mismo error, y reintentar un `401` puede bloquear la cuenta.

### B.1 El token, fuera del código

`commonMain/.../core/network/AuthPlugin.kt`:

```kotlin
import io.ktor.client.plugins.api.*
import io.ktor.client.request.*

val Autenticacion = createClientPlugin("Autenticacion", ::AuthConfig) {
    val proveedor = pluginConfig.proveedorDeToken
    onRequest { request, _ ->
        proveedor()?.let { request.header("Authorization", "Bearer $it") }
    }
}

class AuthConfig { var proveedorDeToken: () -> String? = { null } }
```

> **El token nunca se escribe en el código.** Hoy llega por configuración; en la Semana 11 saldrá del almacén seguro del sistema. Un token en el fuente viaja al repositorio y al artefacto, que es descompilable.

---

## Paso C — Mapeo de errores y repositorio (30 min)

### C.1 Fallos de dominio

`commonMain/.../domain/Fallo.kt`:

```kotlin
package pe.edu.upt.si988.app.domain

sealed class Fallo(val mensaje: String) {
    data object Red             : Fallo("Sin conexión. Revise su red.")
    data object Tiempo          : Fallo("El servidor tardó demasiado.")
    data object Autenticacion   : Fallo("Su sesión expiró.")
    data object Permiso         : Fallo("No tiene permiso para esta acción.")
    data object NoEncontrado    : Fallo("No se encontró lo solicitado.")
    data class  Validacion(val detalle: String) : Fallo(detalle)
    data object Conflicto       : Fallo("El recurso cambió. Actualice e intente de nuevo.")
    data object Limite          : Fallo("Demasiadas solicitudes. Espere un momento.")
    data object Servidor        : Fallo("Error del servidor. Intente más tarde.")
}

class FalloException(val fallo: Fallo) : Exception(fallo.mensaje)
```

> **El usuario no ve códigos HTTP.** La capa de datos traduce el código de estado a un fallo de dominio con un mensaje accionable.

### C.2 El mapeador

`commonMain/.../data/ErrorMapper.kt`:

```kotlin
import io.ktor.client.statement.*
import io.ktor.http.*
import kotlinx.coroutines.TimeoutCancellationException
import kotlinx.serialization.Serializable

@Serializable
data class ErrorApi(val codigo: String, val mensaje: String)

suspend fun mapearRespuesta(r: HttpResponse): Fallo = when (r.status.value) {
    400  -> Fallo.Validacion(runCatching { r.body<ErrorApi>().mensaje }
                .getOrDefault("Datos inválidos"))
    401  -> Fallo.Autenticacion
    403  -> Fallo.Permiso
    404  -> Fallo.NoEncontrado
    409  -> Fallo.Conflicto
    429  -> Fallo.Limite
    else -> Fallo.Servidor
}

fun mapearExcepcion(e: Throwable): Fallo = when (e) {
    is TimeoutCancellationException -> Fallo.Tiempo
    is java.io.IOException          -> Fallo.Red
    else                            -> Fallo.Servidor
}
```

### C.3 El repositorio con caché

`commonMain/.../data/repository/ItemRepositoryImpl.kt`:

```kotlin
class ItemRepositoryImpl(
    private val client: HttpClient,
    private val dao: ItemDao,
    private val scope: CoroutineScope,
) : ItemRepository {

    override suspend fun obtenerItems(forzarRed: Boolean): List<Item> {
        val enCache = dao.leerTodos()
        if (enCache.isNotEmpty() && !forzarRed) {
            scope.launch { refrescarEnSegundoPlano() }   // devuelve rápido, actualiza después
            return enCache
        }
        return try {
            val r = client.get("/items")
            if (!r.status.isSuccess()) throw FalloException(mapearRespuesta(r))
            r.body<List<ItemDto>>().map { it.aDominio() }.also { dao.guardarTodos(it) }
        } catch (e: FalloException) {
            if (enCache.isNotEmpty()) enCache else throw e
        } catch (e: Throwable) {
            if (enCache.isNotEmpty()) enCache else throw FalloException(mapearExcepcion(e))
        }
    }

    private suspend fun refrescarEnSegundoPlano() {
        runCatching {
            val r = client.get("/items")
            if (r.status.isSuccess()) dao.guardarTodos(r.body<List<ItemDto>>().map { it.aDominio() })
        }   // silencioso: ya se devolvió la caché
    }
}
```

> **Estrategia *cache-first*.** La app abre con datos aunque no haya red. Esperar siempre a la red produce pantallas vacías en el arranque.

---

## Paso D — Pruebas con mock server (20 min)

`commonTest/.../ItemRepositoryTest.kt` — con `MockEngine` de Ktor, sin red ni emulador:

```kotlin
import io.ktor.client.engine.mock.*
import io.ktor.http.*
import kotlinx.coroutines.test.runTest
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

private fun motor(estado: HttpStatusCode, cuerpo: String) = MockEngine {
    respond(cuerpo, estado, headersOf(HttpHeaders.ContentType, "application/json"))
}

class ItemRepositoryTest {

    @Test
    fun `un 401 se traduce a Fallo Autenticacion`() = runTest {
        val client = crearHttpClient(motor(HttpStatusCode.Unauthorized, "{}"), "http://t", false)
        val e = assertFailsWith<FalloException> { /* repositorio con dao vacío */ }
        assertEquals(Fallo.Autenticacion, e.fallo)
    }

    @Test
    fun `un 400 conserva el mensaje del servidor`() = runTest {
        val cuerpo = """{"codigo":"VALIDACION","mensaje":"Falta el campo nombre"}"""
        // ... verificar Fallo.Validacion con ese mensaje
    }

    @Test
    fun `sin red devuelve la cache en lugar de fallar`() = runTest {
        // ... precargar el dao, motor que lanza IOException
    }
}
```

**Los tres casos obligatorios:** un `4xx` que no se reintenta, un `429` que respeta el reintento, y la degradación a caché sin red.

---

## Paso E — Inspección del tráfico real (10 min)

```bash
./gradlew :composeApp:installDebug
adb logcat -s HttpClient
```

| | Comprobación |
|---|---|
| ☐ | La cabecera `Authorization` aparece como `***` en el registro |
| ☐ | El cuerpo de la respuesta **no** aparece en el registro |
| ☐ | Un `500` provocado a propósito reintenta 3 veces y se detiene |
| ☐ | Un `400` provocado a propósito **no** reintenta |
| ☐ | Con el modo avión activo, la lista sigue mostrándose desde la caché |

---

## Errores frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `Connection refused` desde el emulador | Se usó `localhost` | Use **`10.0.2.2`** para llegar al anfitrión |
| `CLEARTEXT communication not permitted` | Android bloquea HTTP en claro | Solo para el simulador local, `usesCleartextTraffic` en el manifiesto de **depuración** |
| `SerializationException: unknown key` | El servidor trae campos de más | `Json { ignoreUnknownKeys = true }` |
| Los logs aparecen en release | `install(Logging)` sin condición | Envuélvalo en `if (esDebug)` |
| `NoTransformationFoundException` | Falta negociación de contenido | `install(ContentNegotiation) { json() }` |
| El reintento cubre `4xx` | `retryIf` mal escrito | Solo `429` y `>= 500` |

---

## Con Antigravity

> «Implementa el cliente Ktor en `commonMain` contra `docs/api/openapi.yaml`: `HttpTimeout` de 10 s, negociación de contenido con `kotlinx.serialization`, `Logging` con `LogLevel.HEADERS` y `sanitizeHeader` sobre `Authorization`, y `HttpRequestRetry` que **solo** reintente `429` y `5xx`. Mapea los códigos a `Fallo`. El motor entra por parámetro: `okhttp` en `androidMain`. **No agregues dependencias fuera de Ktor.** Muéstrame el plan antes de escribir código.»

**Verifique a mano** que el nivel de registro no es `ALL`, que ningún `4xx` distinto de `429` se reintenta, y que nada cayó en `androidMain` salvo el motor.

---

---

[Semana 04](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · [Flutter](3-TALLER-FLUTTER.md) · **Kotlin Multiplatform**

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
