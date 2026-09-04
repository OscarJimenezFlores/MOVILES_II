[Semana 01](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · [Flutter](3-TALLER-FLUTTER.md) · **Kotlin Multiplatform**

# Taller 01 · Implementación en **Kotlin Multiplatform**

**SI-988 · Soluciones Móviles II** · Semana 01 · Laboratorio · 100 min

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

> Esta es la **implementación** del [Taller 01](3-TALLER.md) en la Kotlin Multiplatform. El enunciado, los objetivos, los resultados exigidos y la evaluación están en el taller; aquí está el código. Trabaje con los dos abiertos.
>
> Si su equipo eligió Flutter, use la [Flutter](3-TALLER-FLUTTER.md).

---

## Antes de la sesión

El entorno se instala **antes**, siguiendo la [Guía práctica · KMP con Google Antigravity](../GUIAS/GUIA-ANTIGRAVITY-KOTLIN.md). A la sesión se llega con Android Studio, el complemento de KMP y `ANDROID_HOME` configurados.

---

## Paso A — Verificar el entorno (20 min)

### A.1 Comprobación por integrante

Cada integrante ejecuta y guarda la salida en `docs/entorno/<apellido>.txt`:

```bash
java -version
echo $ANDROID_HOME          # en Windows: echo %ANDROID_HOME%
adb --version
git --version
```

En macOS, además:

```bash
kdoctor
```

**Criterio de conformidad.** `ANDROID_HOME` definido, `adb` responde y Android Studio abre el asistente de Kotlin Multiplatform. Los avisos de Xcode se ignoran si el equipo no tiene Mac; se anota en `docs/entorno/README.md`.

### A.2 Crear el proyecto

En Android Studio **File → New → New project**, plantilla **Phone and Tablet → Kotlin Multiplatform**. Seleccione **Android** y, si el equipo tiene Mac, **iOS**. **Finish**.

> **Sin Mac no marque iOS.** El módulo quedaría sin poder compilar y ensuciaría el pipeline de CI desde el primer día. Se declara la restricción en el `ADR-004` de la Semana 13 y se publica en Google Play, que es lo que el curso exige.

Verifique que compila:

```bash
./gradlew :composeApp:assembleDebug
```

### A.3 Fijar las versiones

Para que los cinco integrantes compilen igual, todo se fija en `gradle/libs.versions.toml`:

```toml
[versions]
kotlin = "2.1.0"
agp = "8.7.3"
compose-multiplatform = "1.7.3"
android-compileSdk = "36"
android-minSdk = "26"
android-targetSdk = "36"

[libraries]
kotlin-test = { module = "org.jetbrains.kotlin:kotlin-test", version.ref = "kotlin" }

[plugins]
androidApplication = { id = "com.android.application", version.ref = "agp" }
kotlinMultiplatform = { id = "org.jetbrains.kotlin.multiplatform", version.ref = "kotlin" }
composeMultiplatform = { id = "org.jetbrains.compose", version.ref = "compose-multiplatform" }
```

> **El catálogo de versiones es obligatorio.** Nadie escribe una versión suelta en un `build.gradle.kts`. Se declara aquí una vez. Es lo que evita que dos integrantes compilen con dependencias distintas.

Registre el dispositivo de referencia:

```bash
emulator -list-avds
emulator -avd <nombre_del_avd> &
adb devices
```

**Anote en `docs/entorno/README.md`** el AVD que el equipo usará para todas las mediciones del semestre.

---

## Paso B — Conformar el equipo Scrum (15 min)

Sin código. Se completan `docs/equipo/EQUIPO.md` y `docs/equipo/ACUERDOS.md` según el [taller](3-TALLER.md).

**Lo único técnico.** Cada integrante confirma que puede clonar, sincronizar Gradle y ejecutar.

```bash
git clone <url> && cd <repo> && ./gradlew :composeApp:assembleDebug
```

Si a alguien le falla aquí, se resuelve **ahora**. La primera sincronización de Gradle descarga mucho y es el momento de hacerlo, no en la Semana 04.

---

## Paso C — Lean Canvas y validación del problema (35 min)

Sin código. Se completan `LEAN_CANVAS.md`, `VALIDACION.md` y `VISION.md`.

> Si el equipo aún no tiene idea, el [catálogo de dominios](../CATALOGO-APPS/README.md) trae diez ejemplos desarrollados con su backlog semilla.

---

## Paso D — Repositorio e integración continua (30 min)

### D.1 Estructura de fuentes

```
composeApp/src/
├── commonMain/kotlin/pe/edu/upt/si988/<app>/
│   ├── core/            Utilidades transversales: errores, constantes
│   ├── data/            Fuentes de datos, modelos y repositorios
│   ├── domain/          Entidades y casos de uso — sin dependencias de plataforma
│   └── presentation/    Pantallas Compose y gestión de estado
├── androidMain/kotlin/  Implementaciones `actual` de Android
├── iosMain/kotlin/      Implementaciones `actual` de iOS (si aplica)
└── commonTest/kotlin/   Pruebas del código compartido
```

> **`domain/` vive en `commonMain` y no importa nada de Android ni de iOS.** Esa es la regla que hace comprobable la lógica sin emulador, y la que se verifica en la Semana 15. Cada vez que algo «tiene que ir en `androidMain`», pregúntese si de verdad es específico de la plataforma o si es pereza.

### D.2 `.gitignore`

```gitignore
# Secretos — NUNCA versionar
*.jks
*.keystore
keystore.properties
local.properties
.env
**/google-services.json

# Compilación
build/
.gradle/
.kotlin/
```

### D.3 Análisis estático y formato

En `build.gradle.kts` de la raíz:

```kotlin
plugins {
    id("org.jlleitschuh.gradle.ktlint") version "12.1.1"
    id("io.gitlab.arturbosch.detekt") version "1.23.7"
}

subprojects {
    apply(plugin = "org.jlleitschuh.gradle.ktlint")
    apply(plugin = "io.gitlab.arturbosch.detekt")

    detekt {
        buildUponDefaultConfig = true
        allRules = false
    }
}
```

```bash
./gradlew ktlintCheck detekt
```

**Ambos deben salir limpios antes de cada Pull Request.**

### D.4 Integración continua

`.github/workflows/ci.yml`:

```yaml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  calidad:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - uses: gradle/actions/setup-gradle@v4

      - name: Formato
        run: ./gradlew ktlintCheck

      - name: Análisis estático
        run: ./gradlew detekt

      - name: Pruebas del código compartido
        run: ./gradlew :composeApp:testDebugUnitTest

      - name: Compilar APK de depuración
        run: ./gradlew :composeApp:assembleDebug
```

> **El pipeline falla el Pull Request si el formato, el análisis o las pruebas fallan.** Impide que entre a `main` código sin revisar.

### D.5 Primera prueba, para que el pipeline tenga qué ejecutar

`composeApp/src/commonTest/kotlin/SmokeTest.kt`:

```kotlin
import kotlin.test.Test
import kotlin.test.assertEquals

class SmokeTest {
    @Test
    fun `el proyecto compila y las pruebas se ejecutan`() {
        assertEquals(4, 2 + 2)
    }
}
```

```bash
./gradlew :composeApp:testDebugUnitTest
```

### D.6 Tablero en GitHub Projects

Según el [taller](3-TALLER.md) tablero `Board`, columnas con su límite de WIP, y el docente agregado con permiso de lectura.

---

## Verificación de cierre

| | Comprobación | Comando |
|---|---|---|
| ☐ | `ANDROID_HOME` definido en todos los equipos | `echo $ANDROID_HOME` |
| ☐ | El proyecto compila | `./gradlew :composeApp:assembleDebug` |
| ☐ | La app corre en el emulador acordado | Configuración `androidApp` |
| ☐ | Todos los integrantes clonan y compilan | `git clone && ./gradlew assembleDebug` |
| ☐ | Formato y análisis limpios | `./gradlew ktlintCheck detekt` |
| ☐ | El pipeline de CI está en verde | Pestaña **Actions** |
| ☐ | El tablero existe y el docente tiene acceso | Pestaña **Projects** |

---

## Errores frecuentes en Kotlin Multiplatform

| Síntoma | Causa | Solución |
|---|---|---|
| `SDK location not found` | Falta `ANDROID_HOME` o `local.properties` | Defina la variable como indica la guía, sección 2.4 |
| La primera compilación tarda 10 minutos | Gradle descarga todo la primera vez | Es normal. Hágalo **antes** de la sesión |
| `Unsupported class file major version` | JDK incompatible | Use **JDK 17**, o el JetBrains Runtime |
| `ktlintCheck` falla en CI y no en local | Fin de línea distinto en Windows | `git config --global core.autocrlf input` |
| El asistente de KMP no aparece | Complemento ausente o IDE antiguo | **Plugins → Installed**; Android Studio Otter 2025.2.1 o superior |
| `iosMain` rompe la compilación | Destino iOS activo sin Mac | Quite el destino iOS del `build.gradle.kts` |

---

## Con Antigravity

Encargo sugerido para el Paso D, **después** de crear el proyecto con el asistente:

> «Configura la integración continua en `.github/workflows/ci.yml` para este proyecto Kotlin Multiplatform. Debe ejecutar `ktlintCheck`, `detekt`, las pruebas del código compartido y compilar el APK de depuración, con JDK 17 y caché de Gradle. **No agregues dependencias nuevas** ni toques `libs.versions.toml`. Muéstrame el plan antes de crear archivos.»

Guarde el `Implementation Plan` y el `Walkthrough` en `docs/agentes/`.

---

---

[Semana 01](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · [Flutter](3-TALLER-FLUTTER.md) · **Kotlin Multiplatform**

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
