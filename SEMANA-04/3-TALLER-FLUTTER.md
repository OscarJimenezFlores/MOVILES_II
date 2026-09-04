[Semana 04](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · **Flutter** · [Kotlin Multiplatform](3-TALLER-KOTLIN.md)

# Taller 04 · Implementación en **Flutter**

**SI-988 · Soluciones Móviles II** · Semana 04 · Laboratorio · 100 min

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

> Implementación del [Taller 04](3-TALLER.md) en la Flutter. El contrato OpenAPI, los objetivos y la evaluación están en el taller; aquí está el código.

---

## Dependencias

```yaml
dependencies:
  dio: ^5.7.0
  connectivity_plus: ^6.1.0

dev_dependencies:
  http_mock_adapter: ^0.6.1
```

---

## Paso A — Contrato en OpenAPI (15 min)

> **El contrato es el de su app.** `/items` es un marcador de posición. El equipo define los recursos de su propio dominio en `docs/api/openapi.yaml`. El mock server sirve **ese** contrato, no uno genérico.


Sin código específico del stack el contrato está en el [taller](3-TALLER.md), en `docs/api/openapi.yaml`. Levante el mock server:

```bash
docker run --rm -p 4010:4010 -v "$PWD/docs/api:/api" \
  stoplight/prism:4 mock -h 0.0.0.0 /api/openapi.yaml
curl -i http://localhost:4010/items
```

> En el emulador, `localhost` es el propio emulador. La máquina anfitriona es **`10.0.2.2`**. Es la causa más frecuente de `Connection refused` en este taller.

---

## Paso B — Cliente HTTP e interceptores (25 min)

`lib/core/network/dio_client.dart`:

```dart
import 'package:dio/dio.dart';

Dio crearDio({required String baseUrl}) {
  final dio = Dio(BaseOptions(
    baseUrl: baseUrl,
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
    headers: {'Accept': 'application/json'},
  ));

  dio.interceptors.addAll([
    _AutenticacionInterceptor(),
    _RegistroInterceptor(),
    _ReintentoInterceptor(dio),
  ]);
  return dio;
}
```

### B.1 Autenticación

```dart
class _AutenticacionInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    // En la Semana 11 el token sale del almacén seguro. Hoy basta el marcador.
    const token = String.fromEnvironment('API_TOKEN');
    if (token.isNotEmpty) options.headers['Authorization'] = 'Bearer $token';
    handler.next(options);
  }
}
```

> **El token nunca se escribe en el código.** Entra por `--dart-define=API_TOKEN=...`. Un token en el fuente viaja al repositorio y al artefacto, que es descompilable.

### B.2 Registro — el interceptor que más daño hace mal escrito

```dart
class _RegistroInterceptor extends Interceptor {
  static const _sensibles = {'authorization', 'cookie', 'set-cookie'};

  @override
  void onRequest(RequestOptions o, RequestInterceptorHandler h) {
    assert(() {
      final cabeceras = {
        for (final e in o.headers.entries)
          e.key: _sensibles.contains(e.key.toLowerCase()) ? '***' : e.value,
      };
      print('→ ${o.method} ${o.uri} $cabeceras');
      return true;
    }());
    h.next(o);
  }

  @override
  void onResponse(Response r, ResponseInterceptorHandler h) {
    assert(() {
      print('← ${r.statusCode} ${r.requestOptions.uri}');   // sin cuerpo
      return true;
    }());
    h.next(r);
  }
}
```

> **Dos reglas.** El `assert` hace que el registro **desaparezca en release**, no solo se silencie. Y **nunca se registra el cuerpo de la respuesta** ahí van los datos personales. Este es uno de los siete puntos que se auditan en la Semana 10.

### B.3 Reintento — solo donde corresponde

```dart
class _ReintentoInterceptor extends Interceptor {
  _ReintentoInterceptor(this._dio);
  final Dio _dio;
  static const _maxIntentos = 3;

  @override
  Future<void> onError(DioException e, ErrorInterceptorHandler h) async {
    final estado = e.response?.statusCode;
    final reintentable = estado == null || estado == 429 || estado >= 500;
    final intentos = (e.requestOptions.extra['intentos'] as int? ?? 0);

    if (!reintentable || intentos >= _maxIntentos) return h.next(e);

    // 429 con Retry-After manda; si no, backoff exponencial
    final retryAfter = int.tryParse(e.response?.headers.value('retry-after') ?? '');
    final espera = retryAfter != null
        ? Duration(seconds: retryAfter)
        : Duration(milliseconds: 400 * (1 << intentos));

    await Future<void>.delayed(espera);
    e.requestOptions.extra['intentos'] = intentos + 1;
    try {
      h.resolve(await _dio.fetch(e.requestOptions));
    } on DioException catch (nuevo) {
      h.next(nuevo);
    }
  }
}
```

> **No se reintenta ningún `4xx` salvo el `429`.** Un `400` se repetiría con el mismo request mal formado; un `401` repetido puede bloquear la cuenta.

---

## Paso C — Mapeo de errores y repositorio (30 min)

### C.1 Fallos de dominio

`lib/domain/failures.dart`:

```dart
sealed class Fallo {
  const Fallo(this.mensaje);
  final String mensaje;
}

class FalloRed        extends Fallo { const FalloRed()        : super('Sin conexión. Revise su red.'); }
class FalloTiempo     extends Fallo { const FalloTiempo()     : super('El servidor tardó demasiado.'); }
class FalloAutenticacion extends Fallo { const FalloAutenticacion() : super('Su sesión expiró.'); }
class FalloPermiso    extends Fallo { const FalloPermiso()    : super('No tiene permiso para esta acción.'); }
class FalloNoEncontrado extends Fallo { const FalloNoEncontrado() : super('No se encontró lo solicitado.'); }
class FalloValidacion extends Fallo { const FalloValidacion(super.mensaje); }
class FalloConflicto  extends Fallo { const FalloConflicto()  : super('El recurso cambió. Actualice e intente de nuevo.'); }
class FalloLimite     extends Fallo { const FalloLimite()     : super('Demasiadas solicitudes. Espere un momento.'); }
class FalloServidor   extends Fallo { const FalloServidor()   : super('Error del servidor. Intente más tarde.'); }
```

> **El usuario no ve códigos HTTP.** La capa de datos traduce el código de estado a un fallo de dominio con un mensaje accionable.

### C.2 El mapeador

`lib/data/error_mapper.dart`:

```dart
import 'package:dio/dio.dart';
import '../domain/failures.dart';

Fallo mapearError(DioException e) => switch (e.type) {
      DioExceptionType.connectionTimeout ||
      DioExceptionType.receiveTimeout ||
      DioExceptionType.sendTimeout => const FalloTiempo(),
      DioExceptionType.connectionError => const FalloRed(),
      _ => switch (e.response?.statusCode) {
          400 => FalloValidacion(
              (e.response?.data as Map?)?['mensaje'] as String? ?? 'Datos inválidos'),
          401 => const FalloAutenticacion(),
          403 => const FalloPermiso(),
          404 => const FalloNoEncontrado(),
          409 => const FalloConflicto(),
          429 => const FalloLimite(),
          _   => const FalloServidor(),
        },
    };
```

### C.3 El repositorio con caché

`lib/data/repositories/item_repository_impl.dart`:

```dart
import 'package:dio/dio.dart';
import '../../domain/entities/item.dart';
import '../../domain/failures.dart';
import '../../domain/repositories/item_repository.dart';
import '../error_mapper.dart';
import '../local/item_dao.dart';

class ItemRepositoryImpl implements ItemRepository {
  ItemRepositoryImpl(this._dio, this._dao);
  final Dio _dio;
  final ItemDao _dao;

  @override
  Future<List<Item>> obtenerItems({bool forzarRed = false}) async {
    final enCache = await _dao.leerTodos();
    if (enCache.isNotEmpty && !forzarRed) {
      _refrescarEnSegundoPlano();            // devuelve rápido, actualiza después
      return enCache;
    }
    try {
      final r = await _dio.get<List<dynamic>>('/items');
      final items = r.data!.map((e) => _desdeJson(e as Map<String, dynamic>)).toList();
      await _dao.guardarTodos(items);
      return items;
    } on DioException catch (e) {
      if (enCache.isNotEmpty) return enCache;   // degradación: dato viejo antes que nada
      throw mapearError(e);
    }
  }

  Future<void> _refrescarEnSegundoPlano() async {
    try {
      final r = await _dio.get<List<dynamic>>('/items');
      await _dao.guardarTodos(
          r.data!.map((e) => _desdeJson(e as Map<String, dynamic>)).toList());
    } on DioException {
      // silencioso: ya se devolvió la caché
    }
  }

  Item _desdeJson(Map<String, dynamic> j) =>
      Item(id: j['id'] as String, nombre: j['nombre'] as String);
}
```

> **Estrategia *cache-first*.** La app abre con datos aunque no haya red. Esperar siempre a la red produce pantallas vacías en el arranque.

---

## Paso D — Pruebas con mock server (20 min)

`test/data/item_repository_test.dart`:

```dart
import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http_mock_adapter/http_mock_adapter.dart';

void main() {
  late Dio dio;
  late DioAdapter adapter;

  setUp(() {
    dio = Dio(BaseOptions(baseUrl: 'https://api.test'));
    adapter = DioAdapter(dio: dio);
  });

  test('un 401 se traduce a FalloAutenticacion', () async {
    adapter.onGet('/items', (s) => s.reply(401, {'codigo': 'NO_AUTORIZADO'}));
    // ... construir el repositorio y verificar que lanza FalloAutenticacion
  });

  test('un 400 conserva el mensaje del servidor', () async {
    adapter.onGet('/items', (s) => s.reply(400, {'mensaje': 'Falta el campo nombre'}));
    // ... verificar FalloValidacion con ese mensaje
  });

  test('sin red devuelve la caché en lugar de fallar', () async {
    // ... precargar el DAO, simular DioExceptionType.connectionError
  });
}
```

**Los tres casos obligatorios.** Un `4xx` que no se reintenta, un `429` que respeta `Retry-After`, y la degradación a caché sin red.

---

## Paso E — Inspección del tráfico real (10 min)

```bash
flutter run --dart-define=API_BASE=http://10.0.2.2:4010
```

Con las DevTools abiertas, pestaña **Network**, compruebe:

| | Comprobación |
|---|---|
| ☐ | La cabecera `Authorization` aparece enmascarada en el registro |
| ☐ | El cuerpo de la respuesta **no** aparece en la consola |
| ☐ | Un `500` provocado a propósito reintenta 3 veces y se detiene |
| ☐ | Un `400` provocado a propósito **no** reintenta |
| ☐ | Con el modo avión activo, la lista sigue mostrándose desde la caché |

---

## Errores frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `Connection refused` desde el emulador | Se usó `localhost` | Use **`10.0.2.2`** para llegar al anfitrión |
| El reintento entra en bucle | No se cuenta el intento | Guarde el contador en `options.extra` |
| `type 'Null' is not a subtype` | El JSON no trae el campo | Valide antes de mapear; no confíe en el contrato |
| Los logs aparecen en release | Se usó `print` suelto | Envuélvalo en `assert(() { ... return true; }())` |
| `CERTIFICATE_VERIFY_FAILED` en el emulador | Certificado del simulador | **No desactive la validación.** Use HTTP en local; en la Semana 12 se fija el certificado |

---

## Con Antigravity

> «Implementa el cliente HTTP con `dio` contra `docs/api/openapi.yaml` — tiempo de espera de 10 s, interceptor de autenticación que lee el token de `String.fromEnvironment`, interceptor de registro que **enmascara `Authorization` y nunca registra el cuerpo**, e interceptor de reintento que solo reintenta `429` y `5xx`, respetando `Retry-After`. Mapea los códigos a los fallos de `lib/domain/failures.dart`. **No agregues dependencias fuera de `dio`.** Muéstrame el plan antes de escribir código.»

**Verifique a mano** que el registro no imprime cuerpos y que ningún `4xx` distinto de `429` se reintenta. Son los dos errores que el agente comete aquí.

---

---

[Semana 04](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · **Flutter** · [Kotlin Multiplatform](3-TALLER-KOTLIN.md)

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
