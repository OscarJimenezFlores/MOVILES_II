[Semana 02](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · [Flutter](3-TALLER-FLUTTER.md) · **Kotlin Multiplatform**

# Taller 02 · Implementación en **Kotlin Multiplatform**

**SI-988 · Soluciones Móviles II** · Semana 02 · Laboratorio · 100 min

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

> Implementación del [Taller 02](3-TALLER.md) en la Kotlin Multiplatform. El enunciado y la evaluación están en el taller; aquí está el código.

---

## Paso A — Evaluar los stacks y decidir (25 min)

Sin código: es la matriz de decisión del [taller](3-TALLER.md). Lo que sí se mide aquí:

```bash
# Tamaño del artefacto de referencia
./gradlew :composeApp:assembleRelease
ls -lh composeApp/build/outputs/apk/release/

# Tiempo de compilación limpia
./gradlew clean && time ./gradlew :composeApp:assembleDebug
```

Anote ambos en la matriz. En la Semana 13 se vuelven a medir y se comparan.

---

## Paso B — Redactar los ADR (20 min)

Sin código. `ADR-001` lenguaje y framework, `ADR-002` arquitectura, `ADR-003` gestión de estado.

> **`ADR-002` debe declarar qué va en `commonMain` y qué no.** Es la decisión que define el proyecto: cuanto más suba al código compartido menos se duplica, pero más se aleja de lo nativo. Sin ese criterio escrito, el proyecto deriva solo.

---

## Paso C — Esqueleto y funcionalidad vertical (40 min)

El objetivo es una **rebanada vertical**. Una pantalla que atraviesa las cuatro capas y muestra un dato. Sin red todavía.

### C.1 Dependencias

En `gradle/libs.versions.toml`:

```toml
[versions]
koin = "4.0.0"
coroutines = "1.9.0"
lifecycle = "2.8.4"

[libraries]
koin-core = { module = "io.insert-koin:koin-core", version.ref = "koin" }
koin-compose = { module = "io.insert-koin:koin-compose", version.ref = "koin" }
coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }
coroutines-test = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-test", version.ref = "coroutines" }
viewmodel-compose = { module = "org.jetbrains.androidx.lifecycle:lifecycle-viewmodel-compose", version.ref = "lifecycle" }
```

En `composeApp/build.gradle.kts`:

```kotlin
kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation(libs.koin.core)
            implementation(libs.koin.compose)
            implementation(libs.coroutines.core)
            implementation(libs.viewmodel.compose)
        }
        commonTest.dependencies {
            implementation(libs.kotlin.test)
            implementation(libs.coroutines.test)
        }
    }
}
```

### C.2 La capa de dominio — en `commonMain`, sin plataforma dentro

> **`Item` es un marcador de posición.** Sustitúyalo por la entidad principal de su dominio: `Estudiante`, `Turno`, `Carga`, `Reporte`, la que corresponda a la app que su equipo propuso. Los nombres de archivos, clases y endpoints siguen a su dominio, no a este ejemplo.

`commonMain/.../domain/model/Item.kt`:

```kotlin
package pe.edu.upt.si988.app.domain.model

data class Item(
    val id: String,
    val nombre: String,
)
```

`commonMain/.../domain/repository/ItemRepository.kt` — el contrato:

```kotlin
package pe.edu.upt.si988.app.domain.repository

import pe.edu.upt.si988.app.domain.model.Item

interface ItemRepository {
    suspend fun obtenerItems(): List<Item>
}
```

`commonMain/.../domain/usecase/ObtenerItems.kt`:

```kotlin
package pe.edu.upt.si988.app.domain.usecase

import pe.edu.upt.si988.app.domain.model.Item
import pe.edu.upt.si988.app.domain.repository.ItemRepository

class ObtenerItems(private val repo: ItemRepository) {
    suspend operator fun invoke(): List<Item> = repo.obtenerItems()
}
```

> **Ninguno de estos tres archivos importa nada de `android.*` ni de Compose.** Compruébelo. Es la regla que permite probar la lógica sin emulador y compartirla con iOS.

### C.3 La capa de datos — implementación falsa por ahora

`commonMain/.../data/repository/ItemRepositoryFake.kt`:

```kotlin
package pe.edu.upt.si988.app.data.repository

import kotlinx.coroutines.delay
import pe.edu.upt.si988.app.domain.model.Item
import pe.edu.upt.si988.app.domain.repository.ItemRepository

class ItemRepositoryFake : ItemRepository {
    override suspend fun obtenerItems(): List<Item> {
        delay(300)
        return listOf(
            Item("1", "Primer elemento"),
            Item("2", "Segundo elemento"),
        )
    }
}
```

> En la Semana 04 esta clase se reemplaza por la que consume la API con Ktor. **La pantalla no cambia**, porque depende del contrato y no de la implementación. El repositorio depende del contrato, no de la implementación.

### C.4 Inyección de dependencias

`commonMain/.../core/di/Modules.kt`:

```kotlin
package pe.edu.upt.si988.app.core.di

import org.koin.dsl.module
import pe.edu.upt.si988.app.data.repository.ItemRepositoryFake
import pe.edu.upt.si988.app.domain.repository.ItemRepository
import pe.edu.upt.si988.app.domain.usecase.ObtenerItems

val appModule = module {
    single<ItemRepository> { ItemRepositoryFake() }
    factory { ObtenerItems(get()) }
}
```

### C.5 La capa de presentación

`commonMain/.../presentation/items/ItemsViewModel.kt`:

```kotlin
package pe.edu.upt.si988.app.presentation.items

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import pe.edu.upt.si988.app.domain.model.Item
import pe.edu.upt.si988.app.domain.usecase.ObtenerItems

sealed interface ItemsEstado {
    data object Cargando : ItemsEstado
    data class Error(val mensaje: String) : ItemsEstado
    data class Listos(val items: List<Item>) : ItemsEstado
}

class ItemsViewModel(private val obtenerItems: ObtenerItems) : ViewModel() {

    private val _estado = MutableStateFlow<ItemsEstado>(ItemsEstado.Cargando)
    val estado: StateFlow<ItemsEstado> = _estado.asStateFlow()

    init { cargar() }

    fun cargar() {
        viewModelScope.launch {
            _estado.value = ItemsEstado.Cargando
            _estado.value = runCatching { ItemsEstado.Listos(obtenerItems()) }
                .getOrElse { ItemsEstado.Error("No se pudieron cargar los elementos") }
        }
    }
}
```

> **Los tres estados son obligatorios: cargando, error y listo.** Una pantalla que solo contempla el caso de éxito falla en la Semana 04, al incorporar la red.

`commonMain/.../presentation/items/ItemsScreen.kt`:

```kotlin
package pe.edu.upt.si988.app.presentation.items

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle

@Composable
fun ItemsScreen(vm: ItemsViewModel) {
    val estado by vm.estado.collectAsStateWithLifecycle()

    Scaffold(topBar = { TopAppBar(title = { Text("Elementos") }) }) { padding ->
        Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
            when (val e = estado) {
                is ItemsEstado.Cargando -> CircularProgressIndicator()
                is ItemsEstado.Error -> Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(e.mensaje)
                    Spacer(Modifier.height(12.dp))
                    Button(onClick = vm::cargar) { Text("Reintentar") }
                }
                is ItemsEstado.Listos -> LazyColumn(Modifier.fillMaxSize()) {
                    items(e.items) { item -> ListItem(headlineContent = { Text(item.nombre) }) }
                }
            }
        }
    }
}
```

### C.6 Prueba de la rebanada

`commonTest/.../ObtenerItemsTest.kt`:

```kotlin
import kotlinx.coroutines.test.runTest
import pe.edu.upt.si988.app.domain.model.Item
import pe.edu.upt.si988.app.domain.repository.ItemRepository
import pe.edu.upt.si988.app.domain.usecase.ObtenerItems
import kotlin.test.Test
import kotlin.test.assertEquals

private class RepoFalso(private val datos: List<Item>) : ItemRepository {
    override suspend fun obtenerItems() = datos
}

class ObtenerItemsTest {
    @Test
    fun `devuelve los elementos del repositorio`() = runTest {
        val resultado = ObtenerItems(RepoFalso(listOf(Item("1", "A"))))()
        assertEquals(1, resultado.size)
        assertEquals("A", resultado.first().nombre)
    }
}
```

```bash
./gradlew :composeApp:testDebugUnitTest
./gradlew :composeApp:installDebug
```

---

## Paso D — Definition of Done y CI ampliada (15 min)

Se añade a el pipeline de la Semana 01 la verificación de la regla de dependencia:

```yaml
      - name: La capa de dominio no depende de la plataforma
        run: |
          RUTA=composeApp/src/commonMain/kotlin/pe/edu/upt/si988/app/domain
          if grep -rn "import android\.\|androidx\.compose" "$RUTA"; then
            echo "ERROR: la capa de dominio importa plataforma. Rompe la regla de dependencia."
            exit 1
          fi
          echo "OK: la capa de dominio está limpia."
```

> La verificación evita que `commonMain` acumule dependencias de plataforma. Sin ella, una importación de `Context` en un caso de uso rompe la portabilidad sin que el compilador lo advierta.

---

## Verificación de cierre

| | Comprobación | Comando |
|---|---|---|
| ☐ | La app muestra la lista con datos falsos | `./gradlew :composeApp:installDebug` |
| ☐ | Los tres estados se ven: cargando, error y listo | Fuerce el error en el repositorio falso |
| ☐ | `domain/` no importa plataforma | `grep -rn "import android\." .../domain` |
| ☐ | La prueba del caso de uso pasa | `./gradlew :composeApp:testDebugUnitTest` |
| ☐ | Formato y análisis limpios | `./gradlew ktlintCheck detekt` |
| ☐ | La CI está en verde con la nueva verificación | Pestaña **Actions** |

---

## Errores frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `NoBeanDefFoundException` de Koin | Módulo no arrancado | `startKoin { modules(appModule) }` en el arranque de la app |
| `when` exige rama `else` | La interfaz no es `sealed` | Declare `sealed interface ItemsEstado` |
| La pantalla no se recompone | Se leyó el `StateFlow` sin `collectAsStateWithLifecycle` | Use el `by` con esa función |
| `Unresolved reference: dp` | Falta el import | `import androidx.compose.ui.unit.dp` |
| Gradle no ve la dependencia nueva | No se sincronizó | **Sync Project with Gradle Files** |

---

## Con Antigravity

> «Implementa la rebanada vertical descrita en `docs/adr/ADR-002.md`: modelo, interfaz de repositorio, caso de uso, repositorio falso, ViewModel con tres estados y pantalla Compose. **Todo en `commonMain`; la capa de dominio no puede importar `android.*` ni Compose.** Escribe la prueba del caso de uso en `commonTest` con `runTest`. Muéstrame el plan antes de escribir código.»

Después **verifique usted mismo** el `grep` de la regla de dependencia y que nada haya caído en `androidMain`. Son los dos errores que el agente comete con más frecuencia en KMP.

---

---

[Semana 02](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · [Flutter](3-TALLER-FLUTTER.md) · **Kotlin Multiplatform**

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
