<div align="center">
  <img src="../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Guía práctica · Flutter con Google Antigravity</h1>

<p align="center">
  <strong>SI-988 · Soluciones Móviles II</strong> · Pista <strong>Flutter</strong><br>
  De cero a una app corriendo en el emulador, paso a paso
</p>

---

## Qué es esta guía y qué no es

Es la guía de arranque para **Flutter**. Sirve para dejar el entorno funcionando y construir el primer artefacto con asistencia de un agente de código, antes de la Semana 01.

**No** es un curso de Dart ni de Flutter. Y no es una guía para que el agente escriba la app por usted: es para que aprenda a **dirigir** al agente y a **rechazar** lo que produce mal. Esa es la competencia que el curso evalúa, no la velocidad de tecleo.

> **Verificación de vigencia.** Las versiones y pasos de esta guía se contrastaron con la documentación oficial en **septiembre de 2026**. Flutter y Antigravity cambian rápido: si un menú no coincide, gana la documentación oficial, no esta guía. Las fuentes están al final.

## Antes de empezar

| Requisito | Detalle |
|---|---|
| Sistema operativo | Windows, macOS o Linux |
| Espacio en disco | 25 GB libres como mínimo. Android Studio y los emuladores ocupan más de lo que parece |
| Memoria | 8 GB funciona; con 16 GB el emulador deja de ser una tortura |
| Cuenta de Google | Necesaria para iniciar sesión en Antigravity |
| Navegador Chrome | Requerido por el comando `/browser` de Antigravity |
| Conexión | La primera instalación descarga varios gigabytes |

> **En el laboratorio de la universidad** todo esto ya debería estar instalado. Esta guía es para su propia máquina, que es donde va a trabajar fuera de las sesiones.

---

## Parte 1 · Instalar Google Antigravity

Antigravity es el entorno de desarrollo con agentes de Google. Tiene dos vistas: el **Editor**, que es un editor de código convencional, y el **Agent Manager**, donde se lanzan y supervisan agentes que trabajan en paralelo.

### 1.1 Descarga e instalación

1. Entre a **https://antigravity.google/download** y descargue la versión de su sistema operativo.
2. Ejecute el instalador.
3. **Inicie sesión con su cuenta de Google** y complete la autenticación.
4. Pulse **Open Antigravity**.
5. Revise y acepte la política de **Security and Data Use** con **Next**.
6. Elija el tema y, si quiere, los complementos opcionales.
7. Pulse **Finish**.

### 1.2 Elegir el modo de trabajo

En la configuración inicial Antigravity pregunta *«¿quién conduce?»* y ofrece tres modos:

| Modo | Qué hace | Para este curso |
|---|---|---|
| **Autopilot** | El agente ejecuta el flujo completo por su cuenta | **No lo use al inicio.** Aprenderá poco y aceptará errores sin verlos |
| **Review-driven** | El agente pide permiso antes de cada acción | Útil las primeras semanas, aunque es lento |
| **Agent-assisted** | Usted conduce; el agente automatiza lo seguro | **El recomendado.** Es el que usará durante el curso |

> Puede cambiarlo cuando quiera en los ajustes del proyecto, en **Agent Behaviour**.

### 1.3 Crear el proyecto

1. **Select Project → New Project**.
2. **Add Folder** y elija la carpeta donde vivirá su app.
3. **Next**, y deje la seguridad en **Default**.
4. Póngale nombre y pulse **Create**.

### 1.4 Lo que hay que saber para trabajar

| Elemento | Para qué sirve |
|---|---|
| **Cmd+E** (macOS) o **Ctrl+E** (Windows/Linux) | Alterna entre **Editor** y **Agent Manager** |
| **Agent Manager** | Lanza hasta **cinco agentes en paralelo**, cada uno en su propio espacio de trabajo |
| **Auxiliary Pane**, arriba a la derecha | Muestra los artefactos que produce el agente |
| **`/browser`** | Lanza el navegador y le encarga algo. Requiere Chrome |
| **`/schedule`** | Programa tareas del agente, únicas o recurrentes |
| **Settings → Customizations** | Añade servidores MCP |
| Icono de engranaje del proyecto | **Security Preset**, **Agent Behaviour**, **Local Permissions** y **MCP Tools** |

### 1.5 Los artefactos: donde está el valor académico

Antigravity no solo escribe código. Produce artefactos que **usted debe leer y evaluar**:

| Artefacto | Qué contiene | Qué debe hacer usted |
|---|---|---|
| **Task List** | El plan estructurado antes de implementar | Leerlo **antes** de dejar que ejecute. Aquí se detectan los malentendidos baratos |
| **Implementation Plan** | Los detalles técnicos de la revisión | Verificar que respeta la arquitectura acordada por el equipo |
| **Task** | La lista paso a paso con su estado | Seguir el avance |
| **Walkthrough** | Resumen de los cambios y cómo probarlos | **Probar lo que dice.** Si no se puede probar, no está hecho |
| **Code diffs** | Los cambios revisables | Revisar línea por línea lo que toca seguridad o datos |
| **Screenshots** | La interfaz antes y después | Comparar con lo que pidió |

> **Regla del curso.** El `Implementation Plan` y el `Walkthrough` de cada historia se guardan en el repositorio, en `docs/agentes/`. Son evidencia evaluable: demuestran que usted dirigió el trabajo y no solo lo aceptó.

---

## Parte 2 · Instalar Flutter

**Versión estable actual: Flutter 3.47.**

### 2.1 El SDK

Siga la ruta oficial en **https://docs.flutter.dev/get-started/install** y elija su sistema operativo. Hay dos caminos:

- **Quick start** — con VS Code o un editor basado en Code OSS. Es el más rápido.
- **Custom setup** — instala el SDK a mano y configura las plataformas destino. Es el que da más control y el que conviene si va a usar Antigravity como editor principal.

Al terminar, verifique que `flutter` está en el `PATH`:

```bash
flutter --version
```

### 2.2 Android Studio y el SDK de Android

Aunque no vaya a programar en Android Studio, **hace falta** para el SDK, el emulador y las licencias.

1. Instale la **última versión estable** desde https://developer.android.com/studio
2. Abra el **SDK Manager**:
   - Desde el diálogo de bienvenida: **More Actions → SDK Manager**
   - Con un proyecto abierto: **Tools → SDK Manager**
3. En la pestaña **SDK Platforms**, marque **API Level 36** y pulse **Apply**.
4. En la pestaña **SDK Tools**, asegúrese de tener instalados:

| Componente | Para qué |
|---|---|
| Android SDK Build-Tools | Compilación |
| Android SDK Command-line Tools | Herramientas de consola y licencias |
| Android Emulator | El emulador |
| Android SDK Platform-Tools | `adb` y utilidades de dispositivo |
| CMake | Compilación de código nativo |
| NDK (Side by side) | Kit nativo |

### 2.3 Aceptar las licencias

```bash
flutter doctor --android-licenses
```

Acepte todas. Debe terminar con:

```
All SDK package licenses accepted.
```

### 2.4 Crear el emulador

1. En Android Studio, **More Actions → Virtual Device Manager**, o **Tools → Device Manager**.
2. **Create Virtual Device** (+).
3. Elija **Phone** y una definición de dispositivo.
4. **Next**.
5. Elija **x86 Images** o **ARM Images**, según la arquitectura de su computadora.
6. Elija una imagen del sistema y descárguela si hace falta.
7. **Additional settings → Emulated Performance** y ponga **Graphics** en la opción que diga **Hardware**.
8. **Finish**.

> **Dispositivo de referencia del curso.** Todo el equipo mide sobre el **mismo perfil de emulador**, de gama media, no sobre el mejor teléfono de un integrante. Las métricas de arranque y consumo de la Semana 15 no significan nada si cada quien mide en un aparato distinto. Acuerden el perfil en la Semana 01 y anótenlo en `docs/entorno/`.

Para arrancarlo, pulse **Run** junto al dispositivo en el Device Manager.

### 2.5 Verificar todo

```bash
flutter doctor
flutter emulators && flutter devices
```

Todo lo relacionado con Android debe salir **sin errores**, y debe aparecer al menos un dispositivo con plataforma **android**.

> **Sobre iOS.** Compilar y publicar para iOS exige **macOS con Xcode**. Si su equipo no tiene un Mac, publique en **Google Play**, que es lo que el curso exige: al menos una tienda oficial. No es una versión reducida del trabajo; es la decisión de alcance que tomaría cualquier equipo con esa restricción, y así debe justificarse en el `ADR`.

---

## Parte 3 · El primer artefacto, dirigiendo al agente

Aquí empieza lo que el curso evalúa.

### 3.1 Crear el proyecto

En el terminal de Antigravity:

```bash
flutter create --org pe.edu.upt.<equipo> --platforms=android <nombre_app>
cd <nombre_app>
flutter run
```

Debe ver la app de ejemplo corriendo en el emulador. Si llegó hasta aquí, el entorno está listo.

### 3.2 La primera tarea al agente: cómo se pide

Un encargo mal formulado produce código plausible y equivocado. Compare:

| Así no | Así sí |
|---|---|
| «Hazme una pantalla de login.» | «Crea la pantalla de inicio de sesión con correo y contraseña. Valida el formato del correo antes de enviar. La contraseña nunca se registra en logs. Muestra un error legible si el servidor responde 401, distinto del error de red. No agregues dependencias nuevas sin decírmelo.» |
| «Conecta la API.» | «Implementa el cliente HTTP contra el contrato de `docs/api/openapi.yaml`. Usa un tiempo de espera de 10 s. Ante un 429 respeta la cabecera `Retry-After`. Ante 4xx no reintentes. Deja los errores tipados, no `Exception` genérica.» |
| «Arregla el bug.» | «La lista se duplica al rotar la pantalla. Sospecho del ciclo de vida del estado. Muéstrame primero el plan; no cambies nada hasta que lo apruebe.» |

**Las tres reglas del encargo:**

1. **Diga la restricción, no solo la funcionalidad.** El agente no adivina que la contraseña no va al log.
2. **Pida el plan antes que el código** cuando toque arquitectura, datos personales o seguridad.
3. **Prohíba explícitamente lo que no quiere.** Dependencias nuevas, cambios fuera del alcance, reescrituras.

### 3.3 Qué revisar siempre antes de aceptar

Un agente de código comete errores sistemáticos. Estos son los que aparecen en apps móviles, y los que se revisan en las Semanas 09 a 12:

| Revisar | Por qué |
|---|---|
| **Claves y secretos** | ¿Quedó alguna credencial escrita en el código? El artefacto es descompilable |
| **Validación de certificados** | ¿Desactivó la verificación TLS «para que funcione»? Es el atajo más común y el más grave |
| **Permisos** | ¿Pidió permisos que la funcionalidad no necesita? |
| **Datos sensibles en logs** | ¿Registra el cuerpo completo de las respuestas? |
| **Dependencias nuevas** | ¿Agregó paquetes sin avisar? ¿Están mantenidos? |
| **Manejo de errores** | ¿Captura todo con un `catch` genérico y sigue como si nada? |
| **Pruebas** | ¿Las pruebas que escribió comprueban algo, o solo que el código no explota? |

> **Lo que se entrega no es lo que el agente produjo: es lo que usted aprobó.** La rúbrica evalúa la decisión, no la generación.

### 3.4 Dejar rastro del trabajo con el agente

Cree en el repositorio:

```
docs/agentes/
├── AG-<historia>.md      Encargo dado, plan recibido, qué se aceptó y qué se rechazó, con la razón
└── walkthroughs/         Los Walkthrough que produjo Antigravity
```

Plantilla de `AG-<historia>.md`:

```markdown
# Historia: <ID y título>

## Encargo dado al agente
<el texto exacto que se le pidió>

## Plan que devolvió
<resumen del Implementation Plan, o enlace al artefacto>

## Qué acepté
- ...

## Qué rechacé y por qué
- ...

## Qué verifiqué a mano
- [ ] Sin secretos en el código
- [ ] Validación TLS intacta
- [ ] Sin permisos de más
- [ ] Sin datos sensibles en logs
- [ ] Las pruebas fallan si rompo el código a propósito
```

Esta carpeta es **evidencia evaluable** en las Semanas 13, 15 y 17.

---

## Parte 4 · Problemas frecuentes

| Síntoma | Causa habitual | Qué hacer |
|---|---|---|
| `flutter doctor` marca las licencias | No se aceptaron | `flutter doctor --android-licenses` y aceptar todas |
| El emulador arranca lentísimo | Aceleración por software | En el AVD, **Emulated Performance → Graphics: Hardware**. Verifique la virtualización en la BIOS |
| `flutter devices` no ve nada | El emulador no está corriendo | Arránquelo desde el Device Manager y repita |
| El agente cambia archivos que no pidió | Alcance abierto | Restrinja en **Local Permissions** y nombre los archivos en el encargo |
| El agente inventa una API | No tiene el contrato | Déle `openapi.yaml` como contexto antes de pedir el cliente |
| La compilación falla tras aceptar un cambio | Dependencia nueva sin instalar | `flutter pub get` y revise si esa dependencia debía existir |

---

## Fuentes

- Google. *Getting Started with Google Antigravity* — Google Codelabs. https://codelabs.developers.google.com/getting-started-google-antigravity
- Google. *Antigravity — descarga*. https://antigravity.google/download
- Flutter. *Install*. https://docs.flutter.dev/get-started/install
- Flutter. *Set up Android development*. https://docs.flutter.dev/platform-integration/android/setup
- Android Developers. *Android Studio*. https://developer.android.com/studio
- Android Developers. *Configure on-device developer options*. https://developer.android.com/studio/debug/dev-options

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
