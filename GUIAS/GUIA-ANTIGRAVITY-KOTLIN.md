<div align="center">
  <img src="../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Guía práctica · Kotlin Multiplatform con Google Antigravity</h1>

<p align="center">
  <strong>SI-988 · Soluciones Móviles II</strong> · Pista <strong>Kotlin Multiplatform (KMP)</strong><br>
  De cero a una app corriendo en el emulador, paso a paso
</p>

---

## Qué es esta guía y qué no es

Es la guía de arranque para **Kotlin Multiplatform**. Deja el entorno funcionando y construye el primer artefacto con asistencia de un agente de código, antes de la Semana 01.

**No** es un curso de Kotlin. Y no es una guía para que el agente escriba la app por usted: es para que aprenda a **dirigirlo** y a **rechazar** lo que produce mal. Esa es la competencia que el curso evalúa.

> **Verificación de vigencia.** Versiones y pasos contrastados con la documentación oficial en **septiembre de 2026**. Si un menú no coincide, gana la documentación oficial. Fuentes al final.

## Flutter o Kotlin Multiplatform: cómo se elige

Las dos stacks llegan al mismo destino —una app publicada— por caminos distintos. La elección se hace en la Semana 01, es **provisional**, y se somete a evaluación con datos medidos en la Semana 13 (`ADR-004`).

| | **Flutter** | **Kotlin Multiplatform** |
|---|---|---|
| Lenguaje | Dart | Kotlin |
| Interfaz | Una sola, propia del framework, idéntica en ambas plataformas | Compose Multiplatform compartida, o interfaz nativa por plataforma |
| Qué se comparte | Prácticamente todo | La lógica; la interfaz según se decida |
| Curva si viene de Android | Lenguaje nuevo | Continúa con Kotlin y Android que ya conoce |
| Acceso a lo nativo | Por canales de plataforma | Directo, sin puente |
| Requisitos del equipo | Ninguno especial | Ver la advertencia sobre iOS |

> **Si el equipo ya sabe Kotlin y Android, KMP evita aprender un lenguaje nuevo.** Si el equipo viene de cero y quiere el camino más corto a algo funcionando, Flutter suele serlo. Ninguna de las dos es «mejor»: lo que el curso califica es que la decisión esté **justificada y medida**, no cuál eligieron.

---

## Antes de empezar

| Requisito | Detalle |
|---|---|
| Sistema operativo | Windows, macOS o Linux para el destino **Android** |
| Espacio en disco | 25 GB libres como mínimo |
| Memoria | 8 GB funciona; 16 GB hace el emulador usable |
| Cuenta de Google | Para iniciar sesión en Antigravity |
| Navegador Chrome | Requerido por el comando `/browser` |

> **Advertencia sobre iOS, léala antes de elegir este stack.** El destino **iOS de KMP exige macOS con Xcode instalado y abierto al menos una vez**. Sin un Mac no hay compilación para iOS, y no existe alternativa. Si el equipo no tiene Mac, esto **no** impide trabajar con KMP: se desarrolla y publica para **Android en Google Play**, que es lo que el curso exige —al menos una tienda oficial— y el módulo `iosMain` queda preparado pero sin compilar. Esa restricción se declara en el `ADR-004` como lo haría cualquier equipo profesional.

---

## Parte 1 · Instalar Google Antigravity

Antigravity es el entorno de desarrollo con agentes de Google. Tiene dos vistas: el **Editor**, un editor de código convencional, y el **Agent Manager**, donde se lanzan y supervisan agentes en paralelo.

### 1.1 Descarga e instalación

1. Entre a **https://antigravity.google/download** y descargue la versión de su sistema.
2. Ejecute el instalador.
3. **Inicie sesión con su cuenta de Google** y complete la autenticación.
4. Pulse **Open Antigravity**.
5. Acepte la política de **Security and Data Use** con **Next**.
6. Elija tema y complementos opcionales.
7. Pulse **Finish**.

### 1.2 Elegir el modo de trabajo

| Modo | Qué hace | Para este curso |
|---|---|---|
| **Autopilot** | El agente ejecuta el flujo completo solo | **No al inicio.** Aceptará errores sin verlos |
| **Review-driven** | Pide permiso antes de cada acción | Útil las primeras semanas, lento |
| **Agent-assisted** | Usted conduce; el agente automatiza lo seguro | **El recomendado** |

Se cambia en los ajustes del proyecto, en **Agent Behaviour**.

### 1.3 Crear el proyecto y moverse

1. **Select Project → New Project** → **Add Folder** → **Next** → seguridad **Default** → nombre → **Create**.

| Elemento | Para qué |
|---|---|
| **Cmd+E** / **Ctrl+E** | Alterna **Editor** ↔ **Agent Manager** |
| **Agent Manager** | Hasta **cinco agentes en paralelo**, cada uno en su espacio |
| **Auxiliary Pane**, arriba a la derecha | Los artefactos del agente |
| **`/browser`** | Lanza Chrome y le encarga algo |
| **`/schedule`** | Tareas programadas |
| **Settings → Customizations** | Servidores MCP |
| Engranaje del proyecto | **Security Preset**, **Agent Behaviour**, **Local Permissions**, **MCP Tools** |

### 1.4 Los artefactos: donde está el valor académico

| Artefacto | Qué contiene | Qué debe hacer usted |
|---|---|---|
| **Task List** | El plan antes de implementar | Leerlo **antes** de que ejecute |
| **Implementation Plan** | Los detalles técnicos | Verificar que respeta la arquitectura del equipo |
| **Task** | Lista paso a paso con su estado | Seguir el avance |
| **Walkthrough** | Los cambios y cómo probarlos | **Probarlo.** Si no se puede probar, no está hecho |
| **Code diffs** | Los cambios revisables | Revisar línea por línea lo de seguridad y datos |
| **Screenshots** | Interfaz antes y después | Comparar con lo pedido |

> **Regla del curso.** El `Implementation Plan` y el `Walkthrough` de cada historia se guardan en `docs/agentes/`. Son evidencia evaluable.

---

## Parte 2 · Instalar el entorno Kotlin Multiplatform

### 2.1 El IDE

KMP necesita un IDE con su complemento. **Antigravity no lo reemplaza**: se usa Android Studio o IntelliJ IDEA para el proyecto y el emulador, y Antigravity como entorno de agentes sobre la misma carpeta.

| Herramienta | Versión mínima |
|---|---|
| **Android Studio** | **Otter 2025.2.1** o posterior |
| **IntelliJ IDEA** | **2025.2.2** o posterior |

Se recomienda instalarlos con **JetBrains Toolbox App** (https://www.jetbrains.com/toolbox/app/), que facilita mantener varias versiones.

### 2.2 El complemento de Kotlin Multiplatform

Instale el **Kotlin Multiplatform IDE plugin** desde https://plugins.jetbrains.com/plugin/14936-kotlin-multiplatform

El complemento instala por su cuenta las dependencias necesarias. Verifique que quedó activo en **Plugins → Installed**.

### 2.3 El JDK

Use **JetBrains Runtime (JBR)**, no un JDK cualquiera. Viene incluido en toda distribución de IntelliJ IDEA y trae correcciones importantes de compatibilidad para aplicaciones KMP de escritorio.

### 2.4 La variable `ANDROID_HOME`

Es obligatoria. Sin ella el proyecto no compila para Android.

**macOS o Linux** — añádalo a `.profile` o `.zprofile`:

```bash
export ANDROID_HOME=~/Library/Android/sdk
```

**Windows, PowerShell:**

```powershell
[Environment]::SetEnvironmentVariable('ANDROID_HOME', '<ruta del SDK>', 'Machine')
```

**Windows, CMD:**

```cmd
setx ANDROID_HOME "<ruta del SDK>"
```

### 2.5 El SDK de Android y el emulador

En Android Studio, **More Actions → SDK Manager**, o **Tools → SDK Manager**:

- **SDK Platforms**: marque el nivel de API vigente y aplique.
- **SDK Tools**: **Build-Tools**, **Command-line Tools**, **Emulator**, **Platform-Tools**.

Para el emulador: **More Actions → Virtual Device Manager** → **Create Virtual Device** → **Phone** → definición del dispositivo → **Next** → imagen del sistema (**x86** o **ARM** según su procesador) → **Additional settings → Emulated Performance → Graphics: Hardware** → **Finish**.

> **Dispositivo de referencia del curso.** Todo el equipo mide sobre **el mismo perfil de emulador**, de gama media. Las métricas de la Semana 15 no significan nada si cada quien mide en un aparato distinto. Acuerden el perfil en la Semana 01 y anótenlo en `docs/entorno/`.

### 2.6 Comprobación en macOS: KDoctor

Solo en macOS, y solo si va a intentar el destino iOS. Se instala con Homebrew y se ejecuta desde el terminal:

```bash
kdoctor
```

Reporta lo que falta. El fallo más común es `JAVA_HOME`, que indica dónde está el binario de Java que necesitan Xcode y Gradle. Siga las indicaciones que el propio KDoctor imprime.

### 2.7 iOS, si el equipo tiene Mac

- Instale **Xcode** y **ábralo al menos una vez** antes de trabajar con el proyecto KMP.
- Vuelva a abrirlo manualmente después de cada actualización.

---

## Parte 3 · Crear el proyecto

### 3.1 Con el asistente del IDE

**En Android Studio:**

1. **File → New → New project**
2. En la plantilla **Phone and Tablet**, elija **Kotlin Multiplatform**
3. Seleccione las plataformas y pulse **Finish**

**En IntelliJ IDEA:**

1. **File → New → Project**
2. Elija **Kotlin Multiplatform**
3. Seleccione las plataformas: Android, iOS, Desktop, Web, Server
4. Elija **JetBrains Runtime** como JDK
5. **Create**

### 3.2 La estructura, y por qué importa

```
<proyecto>/
├── commonMain/     Código compartido por todas las plataformas — aquí vive la lógica
├── androidMain/    Lo específico de Android
├── iosMain/        Lo específico de iOS
└── ...
```

> **La decisión de diseño de todo el semestre es qué va en `commonMain`.** Cuanto más suba ahí, menos se duplica, pero más se aleja de lo nativo. Esa decisión, con su costo, es exactamente lo que el `ADR-004` de la Semana 13 debe justificar con datos medidos.

### 3.3 Ejecutar

| Destino | Configuración de ejecución |
|---|---|
| Android | `androidApp` — usa el primer dispositivo virtual disponible |
| iOS | `iosApp` — solo macOS, compila con Xcode por debajo |
| Escritorio | `desktopApp [hot] 🔥` — incluye Compose Hot Reload |
| Web | `webApp [wasmJs]`, o la tarea Gradle `wasmJsBrowserDevelopmentRun` |

Para el curso, el destino obligatorio es **`androidApp`**.

---

## Parte 4 · El primer artefacto, dirigiendo al agente

### 4.1 Cómo se pide una tarea

Un encargo mal formulado produce código plausible y equivocado:

| Así no | Así sí |
|---|---|
| «Hazme una pantalla de login.» | «Crea la pantalla de inicio de sesión con correo y contraseña en `commonMain` con Compose Multiplatform. Valida el formato del correo antes de enviar. La contraseña nunca va a logs. Distingue el error 401 del error de red. No agregues dependencias sin decírmelo.» |
| «Conecta la API.» | «Implementa el cliente Ktor contra `docs/api/openapi.yaml`, en `commonMain`. Tiempo de espera de 10 s. Ante 429 respeta `Retry-After`. Ante 4xx no reintentes. Errores tipados con `sealed class`, no `Exception`.» |
| «Arregla el bug.» | «La lista se duplica al rotar. Sospecho del `ViewModel` en `androidMain`. Muéstrame el plan primero; no cambies nada hasta que lo apruebe.» |

**Las tres reglas del encargo:**

1. **Diga la restricción, no solo la funcionalidad.**
2. **Pida el plan antes que el código** cuando toque arquitectura, datos personales o seguridad.
3. **Prohíba explícitamente lo que no quiere.**

Y una propia de KMP:

4. **Diga en qué fuente va el código.** Si no lo dice, el agente tenderá a poner en `androidMain` cosas que debían ir en `commonMain`, y el proyecto deja de ser multiplataforma sin que nadie lo note.

### 4.2 Qué revisar siempre antes de aceptar

| Revisar | Por qué |
|---|---|
| **Ubicación del código** | ¿Puso en `androidMain` lo que debía ir en `commonMain`? |
| **Claves y secretos** | El artefacto es descompilable |
| **Validación de certificados** | Desactivar TLS «para que funcione» es el atajo más común y el más grave |
| **Permisos** | ¿Pidió permisos que la funcionalidad no necesita? |
| **Datos sensibles en logs** | ¿Registra el cuerpo completo de las respuestas? |
| **Dependencias nuevas** | ¿Son multiplataforma o solo de Android? |
| **`expect`/`actual`** | ¿Declaró un `expect` sin su `actual` en cada destino? |
| **Pruebas** | ¿Comprueban algo o solo que no explota? |

> **Lo que se entrega no es lo que el agente produjo: es lo que usted aprobó.**

### 4.3 Dejar rastro

```
docs/agentes/
├── AG-<historia>.md      Encargo, plan recibido, qué se aceptó y qué se rechazó, con la razón
└── walkthroughs/         Los Walkthrough de Antigravity
```

```markdown
# Historia: <ID y título>

## Encargo dado al agente
<el texto exacto>

## Plan que devolvió
<resumen del Implementation Plan>

## Qué acepté
- ...

## Qué rechacé y por qué
- ...

## Qué verifiqué a mano
- [ ] El código compartido quedó en `commonMain`
- [ ] Sin secretos en el código
- [ ] Validación TLS intacta
- [ ] Sin permisos de más
- [ ] Sin datos sensibles en logs
- [ ] Todo `expect` tiene su `actual`
- [ ] Las pruebas fallan si rompo el código a propósito
```

Carpeta **evaluable** en las Semanas 13, 15 y 17.

---

## Parte 5 · Problemas frecuentes

| Síntoma | Causa habitual | Qué hacer |
|---|---|---|
| El proyecto no compila para Android | Falta `ANDROID_HOME` | Defínala como indica 2.4 y reinicie el IDE |
| El asistente de KMP no aparece | Complemento no instalado o IDE antiguo | Revise **Plugins → Installed** y la versión mínima del IDE |
| El emulador arranca lentísimo | Aceleración por software | **Emulated Performance → Graphics: Hardware**; verifique la virtualización en la BIOS |
| Gradle falla con errores de Java | `JAVA_HOME` mal apuntado | En macOS, ejecute `kdoctor` y siga sus indicaciones. Use JetBrains Runtime |
| `iosApp` no compila | Sin Mac, o Xcode nunca abierto | Abra Xcode una vez. Sin Mac, siga con `androidApp` y declárelo en el `ADR` |
| El agente pone todo en `androidMain` | No se le dijo la fuente | Nómbrela en el encargo y revise el diff |
| Falta el `actual` de un `expect` | Implementación incompleta | Complete el `actual` en cada destino activo |

---

## Fuentes

- Google. *Getting Started with Google Antigravity* — Google Codelabs. https://codelabs.developers.google.com/getting-started-google-antigravity
- Google. *Antigravity — descarga*. https://antigravity.google/download
- Kotlin. *Kotlin Multiplatform quickstart*. https://kotlinlang.org/docs/multiplatform/quickstart.html
- Kotlin. *Set up an environment*. https://kotlinlang.org/docs/multiplatform-mobile-setup.html
- JetBrains. *Kotlin Multiplatform IDE plugin*. https://plugins.jetbrains.com/plugin/14936-kotlin-multiplatform
- JetBrains. *Toolbox App*. https://www.jetbrains.com/toolbox/app/
- Android Developers. *Set up your environment for Kotlin Multiplatform*. https://developer.android.com/kotlin/multiplatform/setup

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
