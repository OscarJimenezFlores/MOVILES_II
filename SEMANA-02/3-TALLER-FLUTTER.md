[Semana 02](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · **Flutter** · [Kotlin Multiplatform](3-TALLER-KOTLIN.md)

# Taller 02 · Implementación en **Flutter**

**SI-988 · Soluciones Móviles II** · Semana 02 · Laboratorio · 100 min

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

> Implementación del [Taller 02](3-TALLER.md) en la Flutter. El enunciado y la evaluación están en el taller; aquí está el código.

---

## Paso A — Evaluar los stacks y decidir (25 min)

Sin código es la matriz de decisión del [taller](3-TALLER.md). Lo que sí se mide aquí, para que la decisión tenga datos:

```bash
# Tamaño del artefacto de referencia
flutter build apk --release
ls -lh build/app/outputs/flutter-apk/app-release.apk

# Tiempo de compilación limpia
flutter clean && time flutter build apk --debug
```

Anote ambos en la matriz. En la Semana 13 se vuelven a medir y se comparan.

---

## Paso B — Redactar los ADR (20 min)

Sin código. `ADR-001` lenguaje y framework, `ADR-002` arquitectura, `ADR-003` gestión de estado.

> **En `ADR-003` no basta con «usamos Riverpod».** Debe decir qué alternativas se descartaron y con qué criterio. Un ADR (*Architecture Decision Record*, registro de decisión de arquitectura) sin alternativas no es una decisión, es un anuncio.

---

## Paso C — Esqueleto y funcionalidad vertical (40 min)

El objetivo es una **rebanada vertical**. Una pantalla que atraviesa las cuatro capas y muestra un dato. Sin red todavía.

### C.1 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter
  get_it: ^8.0.0          # inyección de dependencias
  equatable: ^2.0.5       # comparación por valor en entidades

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0
  mocktail: ^1.0.4        # test doubles
```

```bash
flutter pub get
```

### C.2 La capa de dominio — sin Flutter dentro

> **`Item` es un marcador de posición.** Sustitúyalo por la entidad principal de su dominio — `Estudiante`, `Turno`, `Carga`, `Reporte`, la que corresponda a la app que su equipo propuso. Los nombres de archivos, clases y endpoints siguen a su dominio, no a este ejemplo.

`lib/domain/entities/<entidad>.dart`:

```dart
import 'package:equatable/equatable.dart';

class Item extends Equatable {
  const Item({required this.id, required this.nombre});

  final String id;
  final String nombre;

  @override
  List<Object?> get props => [id, nombre];
}
```

`lib/domain/repositories/item_repository.dart` — el contrato, no la implementación:

```dart
import '../entities/item.dart';

abstract interface class ItemRepository {
  Future<List<Item>> obtenerItems();
}
```

`lib/domain/usecases/obtener_items.dart`:

```dart
import '../entities/item.dart';
import '../repositories/item_repository.dart';

class ObtenerItems {
  const ObtenerItems(this._repo);
  final ItemRepository _repo;

  Future<List<Item>> call() => _repo.obtenerItems();
}
```

> **Ninguno de estos tres archivos importa `package:flutter`.** Compruébelo. Es la regla que permite probar la lógica sin emulador.

### C.3 La capa de datos — implementación falsa por ahora

`lib/data/repositories/item_repository_fake.dart`:

```dart
import '../../domain/entities/item.dart';
import '../../domain/repositories/item_repository.dart';

class ItemRepositoryFake implements ItemRepository {
  @override
  Future<List<Item>> obtenerItems() async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    return const [
      Item(id: '1', nombre: 'Primer elemento'),
      Item(id: '2', nombre: 'Segundo elemento'),
    ];
  }
}
```

> En la Semana 04 esta clase se reemplaza por la que consume la API. **La pantalla no cambia**, porque depende del contrato y no de la implementación. El repositorio depende del contrato, no de la implementación.

### C.4 Inyección de dependencias

`lib/core/di.dart`:

```dart
import 'package:get_it/get_it.dart';
import '../data/repositories/item_repository_fake.dart';
import '../domain/repositories/item_repository.dart';
import '../domain/usecases/obtener_items.dart';

final sl = GetIt.instance;

void configurarDependencias() {
  sl.registerLazySingleton<ItemRepository>(ItemRepositoryFake.new);
  sl.registerFactory(() => ObtenerItems(sl()));
}
```

### C.5 La capa de presentación

`lib/presentation/items/items_controller.dart`:

```dart
import 'package:flutter/foundation.dart';
import '../../domain/entities/item.dart';
import '../../domain/usecases/obtener_items.dart';

sealed class ItemsEstado {
  const ItemsEstado();
}

class ItemsCargando extends ItemsEstado { const ItemsCargando(); }
class ItemsError    extends ItemsEstado { const ItemsError(this.mensaje); final String mensaje; }
class ItemsListos   extends ItemsEstado { const ItemsListos(this.items); final List<Item> items; }

class ItemsController extends ChangeNotifier {
  ItemsController(this._obtenerItems);
  final ObtenerItems _obtenerItems;

  ItemsEstado estado = const ItemsCargando();

  Future<void> cargar() async {
    estado = const ItemsCargando();
    notifyListeners();
    try {
      estado = ItemsListos(await _obtenerItems());
    } catch (e) {
      estado = const ItemsError('No se pudieron cargar los elementos');
    }
    notifyListeners();
  }
}
```

> **Los tres estados son obligatorios. Cargando, error y listo.** Una pantalla que solo contempla el caso de éxito falla en la Semana 04, al incorporar la red.

`lib/presentation/items/items_page.dart`:

```dart
import 'package:flutter/material.dart';
import '../../core/di.dart';
import '../../domain/usecases/obtener_items.dart';
import 'items_controller.dart';

class ItemsPage extends StatefulWidget {
  const ItemsPage({super.key});
  @override
  State<ItemsPage> createState() => _ItemsPageState();
}

class _ItemsPageState extends State<ItemsPage> {
  late final ItemsController _c = ItemsController(sl<ObtenerItems>())..cargar();

  @override
  void dispose() { _c.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(title: const Text('Elementos')),
        body: AnimatedBuilder(
          animation: _c,
          builder: (context, _) => switch (_c.estado) {
            ItemsCargando() => const Center(child: CircularProgressIndicator()),
            ItemsError(:final mensaje) => Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(mensaje),
                    const SizedBox(height: 12),
                    FilledButton(onPressed: _c.cargar, child: const Text('Reintentar')),
                  ],
                ),
              ),
            ItemsListos(:final items) => ListView.builder(
                itemCount: items.length,
                itemBuilder: (_, i) => ListTile(title: Text(items[i].nombre)),
              ),
          },
        ),
      );
}
```

`lib/main.dart`:

```dart
import 'package:flutter/material.dart';
import 'core/di.dart';
import 'presentation/items/items_page.dart';

void main() {
  configurarDependencias();
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
        title: 'SI-988',
        theme: ThemeData(colorSchemeSeed: Colors.indigo, useMaterial3: true),
        home: const ItemsPage(),
      );
}
```

### C.6 Prueba de la rebanada

`test/domain/obtener_items_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:<nombre_app>/domain/entities/item.dart';
import 'package:<nombre_app>/domain/repositories/item_repository.dart';
import 'package:<nombre_app>/domain/usecases/obtener_items.dart';

class _RepoFalso extends Mock implements ItemRepository {}

void main() {
  test('devuelve los elementos del repositorio', () async {
    final repo = _RepoFalso();
    when(repo.obtenerItems).thenAnswer((_) async => const [Item(id: '1', nombre: 'A')]);

    final resultado = await ObtenerItems(repo)();

    expect(resultado, hasLength(1));
    expect(resultado.first.nombre, 'A');
  });
}
```

```bash
flutter test
flutter run
```

---

## Paso D — Definition of Done y CI ampliada (15 min)

Se añade a el pipeline de la Semana 01 la verificación de la regla de dependencia:

```yaml
      - name: La capa de dominio no depende de Flutter
        run: |
          if grep -rn "package:flutter" lib/domain/; then
            echo "ERROR: lib/domain/ importa Flutter. Rompe la regla de dependencia."
            exit 1
          fi
          echo "OK: la capa de dominio está limpia."
```

> La verificación evita que la capa de dominio acumule dependencias de framework. Sin ella, una importación de `BuildContext` en un caso de uso pasa inadvertida hasta que el refactor es costoso.

---

## Verificación de cierre

| | Comprobación | Comando |
|---|---|---|
| ☐ | La app muestra la lista con datos falsos | `flutter run` |
| ☐ | Los tres estados se ven: cargando, error y listo | Fuerce el error en el repositorio falso |
| ☐ | `lib/domain/` no importa Flutter | `grep -rn "package:flutter" lib/domain/` |
| ☐ | La prueba del caso de uso pasa | `flutter test` |
| ☐ | Análisis limpio | `flutter analyze` |
| ☐ | La CI está en verde con la nueva verificación | Pestaña **Actions** |

---

## Errores frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `Bad state: GetIt: Object not registered` | Falta `configurarDependencias()` | Llámelo en `main()` antes de `runApp` |
| El `switch` sobre el estado no compila | Falta `sealed` en la clase base | Declare `sealed class ItemsEstado` |
| La pantalla no se actualiza | Falta `notifyListeners()` | Llámelo tras cada cambio de estado |
| `import` no resuelve | Nombre del paquete distinto | Use el `name:` de `pubspec.yaml` |

---

## Con Antigravity

> «Implementa la rebanada vertical descrita en `docs/adr/ADR-002.md` — entidad, contrato de repositorio, caso de uso, repositorio falso, controlador con tres estados y pantalla. **La capa de dominio no puede importar `package:flutter`.** Escribe la prueba del caso de uso con `mocktail`. Muéstrame el plan antes de escribir código.»

Después **verifique usted mismo** el `grep` de la regla de dependencia. Es el error que el agente comete con más frecuencia.

---

---

[Semana 02](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · **Flutter** · [Kotlin Multiplatform](3-TALLER-KOTLIN.md)

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
