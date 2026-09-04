[Semana 01](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · **Flutter** · [Kotlin Multiplatform](3-TALLER-KOTLIN.md)

# Taller 01 · Implementación en **Flutter**

**SI-988 · Soluciones Móviles II** · Semana 01 · Laboratorio · 100 min

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

> Esta es la **implementación** del [Taller 01](3-TALLER.md) en la Flutter. El enunciado, los objetivos, los resultados exigidos y la evaluación están en el taller; aquí está el código. Trabaje con los dos abiertos.
>
> Si su equipo eligió Kotlin Multiplatform, use la [Kotlin Multiplatform](3-TALLER-KOTLIN.md).

---

## Antes de la sesión

El entorno se instala **antes**, siguiendo la [Guía práctica · Flutter con Google Antigravity](../GUIAS/GUIA-ANTIGRAVITY-FLUTTER.md). A la sesión se llega con `flutter doctor` sin errores.

---

## Paso A — Verificar el entorno (20 min)

### A.1 Comprobación por integrante

Cada integrante ejecuta y guarda la salida en `docs/entorno/<apellido>.txt`:

```bash
flutter --version
flutter doctor -v
dart --version
git --version
```

**Criterio de conformidad.** `flutter doctor` sin errores en las secciones de Flutter, Android toolchain y Android Studio. Los avisos de Xcode se ignoran si el equipo no tiene Mac; se anota en `docs/entorno/README.md`.

### A.2 Crear el proyecto

```bash
flutter create --org pe.edu.upt.si988 \
               --project-name <nombre_app> \
               --platforms=android \
               .
flutter run
```

> `--org` fija el identificador del paquete (`pe.edu.upt.si988.<nombre_app>`). **Se decide ahora y no se cambia**. Cambiarlo después de publicar significa una app nueva en la tienda.

### A.3 Fijar la versión del SDK

Para que los cinco integrantes compilen igual, se fija la versión en `pubspec.yaml`:

```yaml
environment:
  sdk: ^3.9.0
  flutter: ">=3.47.0"
```

Y se registra el dispositivo de referencia acordado:

```bash
flutter emulators          # lista los AVD disponibles
flutter emulators --launch <id_del_avd>
flutter devices
```

**Anote en `docs/entorno/README.md`** el AVD que el equipo usará para todas las mediciones del semestre. Sin un dispositivo común, las métricas de la Semana 15 no son comparables.

---

## Paso B — Conformar el equipo Scrum (15 min)

Sin código. Se completan `docs/equipo/EQUIPO.md` y `docs/equipo/ACUERDOS.md` según el [taller](3-TALLER.md).

**Lo único técnico.** Cada integrante confirma que puede clonar, compilar y ejecutar.

```bash
git clone <url> && cd <repo> && flutter pub get && flutter run
```

Si a alguien le falla aquí, se resuelve **ahora**. Un integrante que no compila en la Semana 01 no contribuye en la 04.

---

## Paso C — Lean Canvas y validación del problema (35 min)

Sin código. Se completan `LEAN_CANVAS.md`, `VALIDACION.md` y `VISION.md`.

> Si el equipo aún no tiene idea, el [catálogo de dominios](../CATALOGO-APPS/README.md) trae diez ejemplos desarrollados con su backlog semilla.

---

## Paso D — Repositorio e integración continua (30 min)

### D.1 Estructura de carpetas

```
lib/
├── main.dart
├── core/                 Utilidades transversales: errores, constantes, extensiones
├── data/                 Fuentes de datos, modelos y repositorios
├── domain/               Entidades y casos de uso — sin dependencias de Flutter
└── presentation/         Pantallas, widgets y gestión de estado
test/
docs/
```

> **`domain/` no importa nada de Flutter.** Es la regla que hace comprobable la lógica sin emulador, y la que se verifica en la Semana 15.

### D.2 `.gitignore`

`flutter create` ya genera uno. Se añade:

```gitignore
# Secretos — NUNCA versionar
*.jks
*.keystore
key.properties
.env
**/google-services.json

# Compilación
build/
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
```

### D.3 Análisis estático

En `analysis_options.yaml`:

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    avoid_print: true
    prefer_const_constructors: true
    always_declare_return_types: true
    avoid_dynamic_calls: true

analyzer:
  errors:
    invalid_annotation_target: ignore
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
```

```bash
flutter analyze
```

**El análisis debe salir limpio antes de cada Pull Request.**

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
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.47.0'
          channel: stable
          cache: true

      - name: Dependencias
        run: flutter pub get

      - name: Formato
        run: dart format --set-exit-if-changed .

      - name: Análisis estático
        run: flutter analyze --fatal-infos

      - name: Pruebas
        run: flutter test --coverage

      - name: Compilar APK de depuración
        run: flutter build apk --debug
```

> **El pipeline falla el Pull Request si el formato, el análisis o las pruebas fallan.** Impide que entre a `main` código sin revisar.

### D.5 Primera prueba, para que el pipeline tenga qué ejecutar

`test/smoke_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('el proyecto compila y las pruebas se ejecutan', () {
    expect(2 + 2, 4);
  });
}
```

```bash
flutter test
```

### D.6 Tablero en GitHub Projects

Según el [taller](3-TALLER.md) tablero `Board`, columnas con su límite de WIP, y el docente agregado con permiso de lectura.

---

## Verificación de cierre

Antes de salir del laboratorio:

| | Comprobación | Comando |
|---|---|---|
| ☐ | `flutter doctor` sin errores en todos los equipos | `flutter doctor -v` |
| ☐ | La app de ejemplo corre en el emulador acordado | `flutter run` |
| ☐ | Todos los integrantes clonan y compilan | `flutter pub get && flutter run` |
| ☐ | El análisis estático sale limpio | `flutter analyze` |
| ☐ | El pipeline de CI está en verde | Pestaña **Actions** del repositorio |
| ☐ | El tablero existe y el docente tiene acceso | Pestaña **Projects** |

---

## Errores frecuentes en Flutter

| Síntoma | Causa | Solución |
|---|---|---|
| `flutter: command not found` | El SDK no está en el `PATH` | Ver la guía de instalación, sección 2.1 |
| `Android licenses not accepted` | Licencias sin aceptar | `flutter doctor --android-licenses` |
| `No devices found` | El emulador no está corriendo | `flutter emulators --launch <id>` |
| `dart format` falla en CI y en local no | Fin de línea distinto en Windows | `git config --global core.autocrlf input` |
| La CI tarda más de 10 min | Sin caché | `cache: true` en `subosito/flutter-action` |
| `Gradle task assembleDebug failed` | Versión de Java incompatible | Use el JDK que incluye Android Studio |

---

## Con Antigravity

Encargo sugerido para el Paso D, **después** de crear el proyecto a mano:

> «Configura la integración continua en `.github/workflows/ci.yml` para este proyecto Flutter. Debe verificar formato, análisis estático y pruebas, y compilar el APK de depuración. Usa `subosito/flutter-action@v2` con caché. **No agregues dependencias nuevas** ni toques `pubspec.yaml`. Muéstrame el plan antes de crear archivos.»

Guarde el `Implementation Plan` y el `Walkthrough` en `docs/agentes/`.

---

---

[Semana 01](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · **Flutter** · [Kotlin Multiplatform](3-TALLER-KOTLIN.md)

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
