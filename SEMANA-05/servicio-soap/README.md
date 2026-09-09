# Servicio SOAP y BFF del Taller 05

Servicios de prueba para el Taller 05 de **SI-988 · Soluciones Móviles II**. Solo requieren **Python 3.8 o superior**. No instalan dependencias y funcionan sin internet.

## Arranque

```bash
# Terminal 1 — servicio SOAP heredado
python3 servidor.py          # http://localhost:8080/servicio

# Terminal 2 — BFF que traduce SOAP a REST/JSON
python3 bff.py               # http://localhost:8081/api/productos
```

Desde el emulador de Android, la máquina anfitriona es `10.0.2.2`, no `localhost`.

## `servidor.py` — servicio SOAP 1.1

| Endpoint | Método | Descripción |
|---|---|---|
| `/servicio?wsdl` | `GET` | Devuelve el WSDL |
| `/servicio` | `POST` | Acepta SOAP 1.1 |

| Operación | Parámetro | Comportamiento |
|---|---|---|
| `ListarProductos` | — | Devuelve 5 productos |
| `ObtenerProducto` | `codigo` | Devuelve el producto |
| `ObtenerProducto` | `codigo = ERR-404` | `soap:Fault` con **HTTP 500** |
| `ObtenerProducto` | `codigo = ERR-200` | `soap:Fault` con **HTTP 200** |
| `ConsultarStock` | `codigo` | Devuelve el stock, con 700 ms de retardo |

Los dos casos de `Fault` son deliberados. El de HTTP 200 reproduce el comportamiento real de servicios SOAP que devuelven errores de negocio con código de éxito. Obliga a inspeccionar el cuerpo en toda respuesta.

El retardo de `ConsultarStock` hace que la medición de latencia del Paso B arroje diferencias observables.

## `bff.py` — Backend For Frontend

Consume el SOAP de `servidor.py` y expone REST/JSON.

| Endpoint | Respuesta |
|---|---|
| `GET /api/productos` | `200` con el arreglo de productos |
| `GET /api/productos/<codigo>` | `200`, `404` si no existe, `502` ante otro Fault |
| `GET /api/productos/<codigo>/stock` | `200` con `{ codigo, disponible }` |

El BFF realiza tres funciones que el cliente móvil no debe asumir:

1. Construir y analizar XML.
2. Traducir el `soap:Fault` a un código HTTP correcto — `PROD_NO_ENCONTRADO` pasa a `404`, el resto a `502`.
3. Reducir el payload a los campos que la app consume.

## Comparación de payload

```bash
curl -s -o /dev/null -w 'SOAP: %{size_download} bytes\n' -X POST http://localhost:8080/servicio \
  -H 'Content-Type: text/xml' \
  -d '<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ListarProductosRequest xmlns="http://si988.upt.pe/servicio"/></soap:Body></soap:Envelope>'
curl -s -o /dev/null -w 'REST: %{size_download} bytes\n' http://localhost:8081/api/productos
```

Valores de referencia medidos con estos servicios. **SOAP 855 bytes · REST 444 bytes**.
