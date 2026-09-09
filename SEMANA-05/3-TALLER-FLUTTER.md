[Semana 05](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · **Flutter** · [Kotlin Multiplatform](3-TALLER-KOTLIN.md)

# Taller 05 · Implementación en **Flutter**

**SI-988 · Soluciones Móviles II** · Semana 05 · Laboratorio · 100 min

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

> Código del **Paso C** del [Taller 05](3-TALLER.md). Los pasos A, B, D y E no dependen del stack elegido y están en el taller.
>
> **Requisito.** El servicio SOAP debe estar corriendo (`python3 servicio-soap/servidor.py`) y usted ya debe haber hecho las llamadas con `curl` del Paso B. Si no lo hizo, hágalo primero. Depurar XML desde la app sin haberlo visto en la terminal es innecesariamente difícil.

---

## C.1 — Dependencias

```yaml
dependencies:
  dio: ^5.7.0
  xml: ^6.5.0
```

```bash
flutter pub get
```

## C.2 — La URL, según dónde corra

```dart
// lib/core/config.dart
const bool _enEmulador = bool.fromEnvironment('EMULADOR', defaultValue: true);

/// En el emulador de Android, 10.0.2.2 es la máquina anfitriona.
/// 'localhost' apuntaría al propio emulador y la conexión sería rechazada.
const String soapBaseUrl = _enEmulador
    ? 'http://10.0.2.2:8080'
    : 'http://localhost:8080';
```

Android bloquea HTTP en claro desde API 28. Solo para el build de depuración, en `android/app/src/debug/AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application android:usesCleartextTraffic="true" />
</manifest>
```

> Va en `src/debug/`, **no** en `src/main/`. El build de release no debe permitir tráfico en claro.

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

`lib/data/soap/envelope.dart`:

```dart
import 'package:xml/xml.dart';

const String nsServicio = 'http://si988.upt.pe/servicio';

/// Genera el XML del request SOAP para una operación del WSDL.
///
/// Ejemplo: construirEnvelope('ObtenerProducto', {'codigo': 'P-002'})
/// produce el envelope completo, listo para enviar como body del POST.
String construirEnvelope(String operacion, Map<String, String> parametros) {
  final builder = XmlBuilder();
  builder.processing('xml', 'version="1.0" encoding="UTF-8"');

  builder.element('soap:Envelope', nest: () {
    builder.attribute('xmlns:soap', 'http://schemas.xmlsoap.org/soap/envelope/');

    builder.element('soap:Body', nest: () {
      builder.element('${operacion}Request', nest: () {
        builder.attribute('xmlns', nsServicio);

        parametros.forEach((clave, valor) {
          // builder.text() escapa el valor: < se convierte en &lt;, etc.
          builder.element(clave, nest: () => builder.text(valor));
        });
      });
    });
  });

  return builder.buildDocument().toXmlString();
}
```

**Por qué con `XmlBuilder` y no armando el string a mano.** Si el código de producto llega con `<` o `&`, un string interpolado produce XML inválido y el servicio responde error. Si llega con `</codigo><otro>`, el atacante inserta elementos en el request. Es **inyección de XML**, el equivalente a un `SQL injection`. `builder.text()` escapa el contenido antes de insertarlo.

Compruébelo:

```dart
print(construirEnvelope('ObtenerProducto', {'codigo': 'P-002'}));
print(construirEnvelope('ObtenerProducto', {'codigo': 'A & B <script>'}));
// el segundo produce &amp; y &lt;script&gt;, no XML roto
```

## C.4 — Análisis seguro de la respuesta

El paquete `xml` de Dart **no resuelve entidades externas**, así que no es vulnerable a XXE por omisión. Aun así se valida el tamaño antes de analizar, para no quedar expuesto a una bomba de expansión:

```dart
import 'package:xml/xml.dart';

const int _maxBytesRespuesta = 2 * 1024 * 1024;   // 2 MB

XmlDocument analizarSeguro(String cuerpo) {
  if (cuerpo.length > _maxBytesRespuesta) {
    throw const FormatException('Respuesta demasiado grande');
  }
  return XmlDocument.parse(cuerpo);
}
```

## C.5 — Detectar el Fault, sin mirar el código HTTP

Es el punto que decide el taller:

```dart
// lib/data/soap/fault.dart
import 'package:xml/xml.dart';

class SoapFault implements Exception {
  const SoapFault({required this.codigo, required this.razon});
  final String codigo;
  final String razon;

  @override
  String toString() => 'SoapFault($codigo): $razon';
}

/// Devuelve el Fault si lo hay. Se llama SIEMPRE, aunque el status sea 200.
SoapFault? detectarFault(XmlDocument doc) {
  final fault = doc.findAllElements('Fault', namespace: '*').firstOrNull;
  if (fault == null) return null;
  return SoapFault(
    codigo: fault.findAllElements('CodigoNegocio', namespace: '*').firstOrNull?.innerText
        ?? 'DESCONOCIDO',
    razon: fault.findAllElements('faultstring', namespace: '*').firstOrNull?.innerText
        ?? 'Error del servicio',
  );
}
```

## C.6 — El cliente completo, con medición

`lib/data/soap/catalogo_soap.dart`:

```dart
import 'package:dio/dio.dart';
import 'package:xml/xml.dart';
import '../../core/config.dart';
import 'envelope.dart';
import 'fault.dart';

class MedicionSoap {
  const MedicionSoap({required this.bytesRequest, required this.bytesResponse,
                      required this.milisegundos, required this.statusHttp});
  final int bytesRequest, bytesResponse, milisegundos, statusHttp;
}

class CatalogoSoap {
  CatalogoSoap(this._dio);
  final Dio _dio;

  MedicionSoap? ultimaMedicion;

  Future<List<Map<String, dynamic>>> listarProductos() async {
    final doc = await _invocar('ListarProductos', const {});
    return doc.findAllElements('producto', namespace: '*').map((p) => {
          'codigo': _texto(p, 'codigo'),
          'nombre': _texto(p, 'nombre'),
          'precio': double.tryParse(_texto(p, 'precio') ?? '0') ?? 0,
          'stock': int.tryParse(_texto(p, 'stock') ?? '0') ?? 0,
        }).toList();
  }

  Future<Map<String, dynamic>> obtenerProducto(String codigo) async {
    final doc = await _invocar('ObtenerProducto', {'codigo': codigo});
    final r = doc.findAllElements('ObtenerProductoResponse', namespace: '*').first;
    return {
      'codigo': _texto(r, 'codigo'),
      'nombre': _texto(r, 'nombre'),
      'precio': double.tryParse(_texto(r, 'precio') ?? '0') ?? 0,
      'stock': int.tryParse(_texto(r, 'stock') ?? '0') ?? 0,
    };
  }

  Future<XmlDocument> _invocar(String operacion, Map<String, String> params) async {
    final envelope = construirEnvelope(operacion, params);
    final crono = Stopwatch()..start();

    final r = await _dio.post<String>(
      '$soapBaseUrl/servicio',
      data: envelope,
      options: Options(
        headers: {
          'Content-Type': 'text/xml; charset=utf-8',
          'SOAPAction': '"$nsServicio/$operacion"',
        },
        responseType: ResponseType.plain,
        // Se acepta cualquier status: el Fault puede venir con 200 o con 500.
        validateStatus: (_) => true,
      ),
    );
    crono.stop();

    final cuerpo = r.data ?? '';
    ultimaMedicion = MedicionSoap(
      bytesRequest: envelope.length,
      bytesResponse: cuerpo.length,
      milisegundos: crono.elapsedMilliseconds,
      statusHttp: r.statusCode ?? 0,
    );

    final doc = analizarSeguro(cuerpo);

    // SIEMPRE antes de leer datos, sin importar el status HTTP.
    final fault = detectarFault(doc);
    if (fault != null) throw fault;

    return doc;
  }

  String? _texto(XmlElement e, String nombre) =>
      e.findAllElements(nombre, namespace: '*').firstOrNull?.innerText;
}
```

## C.7 — Probarlo

`test/soap/catalogo_soap_test.dart`, sin red ni emulador:

```dart
import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:http_mock_adapter/http_mock_adapter.dart';

const _faultCon200 = '''<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body>
<soap:Fault><faultcode>soap:Server</faultcode>
<faultstring>Error de negocio devuelto con HTTP 200</faultstring>
<detail><CodigoNegocio>FAULT_CON_200</CodigoNegocio></detail>
</soap:Fault></soap:Body></soap:Envelope>''';

void main() {
  test('detecta el Fault aunque el status sea 200', () async {
    final dio = Dio();
    DioAdapter(dio: dio).onPost('/servicio', (s) => s.reply(200, _faultCon200));

    expect(
      () => CatalogoSoap(dio).obtenerProducto('ERR-200'),
      throwsA(isA<SoapFault>().having((f) => f.codigo, 'codigo', 'FAULT_CON_200')),
    );
  });
}
```

```bash
flutter test test/soap/
flutter run --dart-define=EMULADOR=true
```

## C.8 — Registrar las mediciones

```dart
final catalogo = CatalogoSoap(Dio());
for (var i = 0; i < 3; i++) {
  await catalogo.listarProductos();
  final m = catalogo.ultimaMedicion!;
  debugPrint('req=${m.bytesRequest}B  res=${m.bytesResponse}B  ${m.milisegundos}ms');
}
```

Se registra la **mediana de tres** en `docs/api/MEDICIONES.md`.

---

## Verificación de cierre

| | Comprobación |
|---|---|
| ☐ | El servicio responde desde la app en el emulador |
| ☐ | `ERR-404` lanza `SoapFault` con código `PROD_NO_ENCONTRADO` |
| ☐ | **`ERR-200` lanza `SoapFault` pese a llegar con HTTP 200** |
| ☐ | El envelope se construye con `XmlBuilder`, sin interpolación |
| ☐ | La prueba del Fault con 200 pasa |
| ☐ | Las mediciones están tomadas tres veces |

---

## Errores frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| `Connection refused` | Se usó `localhost` en el emulador | Use `10.0.2.2` |
| `CLEARTEXT communication not permitted` | Android bloquea HTTP | `usesCleartextTraffic` solo en `src/debug/` |
| `XmlParserException: Expected name` | La respuesta no es XML | Imprima `r.data` crudo antes de analizar |
| `findAllElements` devuelve vacío | Namespace | Use `namespace: '*'` |
| El Fault con 200 no se detecta | Se comprobó el status antes que el cuerpo | Analice el cuerpo **siempre** |
| Dio lanza antes de leer el 500 | `validateStatus` por omisión | `validateStatus: (_) => true` |

---

## Con Antigravity

> «Implementa `CatalogoSoap` para el servicio de `docs/api/catalogo.wsdl`. El envelope se construye con `XmlBuilder` del paquete `xml`, **nunca por interpolación**. El cliente debe usar `validateStatus: (_) => true` y **detectar `<soap:Fault>` inspeccionando el cuerpo antes de leer datos, sin importar el código HTTP**. Registra bytes de request, bytes de response y milisegundos. Muéstrame el plan antes de escribir código.»

**Verifique a mano** que el Fault se detecta con HTTP 200. Es el error que el agente comete aquí, porque asume la convención de REST.

---

---

[Semana 05](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · [Taller](3-TALLER.md) · **Flutter** · [Kotlin Multiplatform](3-TALLER-KOTLIN.md)

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
