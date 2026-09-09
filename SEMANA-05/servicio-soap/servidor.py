#!/usr/bin/env python3
"""
Servicio SOAP 1.1 de prueba para el Taller 05 de SI-988.

Solo usa la librería estándar de Python: no instala nada, corre en cualquier
máquina del laboratorio y funciona sin internet.

    python3 servidor.py            # escucha en 0.0.0.0:8080

Endpoints:
    GET  /servicio?wsdl     Devuelve el WSDL
    POST /servicio          Acepta SOAP 1.1

Operaciones:
    ListarProductos   -> lista de productos
    ObtenerProducto   -> un producto por código
                         codigo = "ERR-404"  -> SOAP Fault con HTTP 500
                         codigo = "ERR-200"  -> SOAP Fault con HTTP 200  (el caso traicionero)
    ConsultarStock    -> stock por código, con retardo artificial de 700 ms
"""
import re, time, xml.sax.saxutils as sx
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST, PUERTO = "0.0.0.0", 8080
NS = "http://si988.upt.pe/servicio"

PRODUCTOS = [
    ("P-001", "Aceituna botija 1 kg",      18.50, 240),
    ("P-002", "Aceite de oliva extra 500 ml", 32.00, 85),
    ("P-003", "Orégano seleccionado 250 g", 12.90, 410),
    ("P-004", "Pisco quebranta 750 ml",     65.00, 32),
    ("P-005", "Damasco deshidratado 500 g", 21.40, 0),
]

WSDL = """<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/"
             xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
             xmlns:xsd="http://www.w3.org/2001/XMLSchema"
             xmlns:tns="{ns}" targetNamespace="{ns}">

  <types>
    <xsd:schema targetNamespace="{ns}" elementFormDefault="qualified">
      <xsd:element name="ListarProductosRequest"><xsd:complexType/></xsd:element>
      <xsd:element name="ListarProductosResponse">
        <xsd:complexType><xsd:sequence>
          <xsd:element name="producto" maxOccurs="unbounded">
            <xsd:complexType><xsd:sequence>
              <xsd:element name="codigo" type="xsd:string"/>
              <xsd:element name="nombre" type="xsd:string"/>
              <xsd:element name="precio" type="xsd:decimal"/>
              <xsd:element name="stock"  type="xsd:int"/>
            </xsd:sequence></xsd:complexType>
          </xsd:element>
        </xsd:sequence></xsd:complexType>
      </xsd:element>

      <xsd:element name="ObtenerProductoRequest">
        <xsd:complexType><xsd:sequence>
          <xsd:element name="codigo" type="xsd:string"/>
        </xsd:sequence></xsd:complexType>
      </xsd:element>
      <xsd:element name="ObtenerProductoResponse">
        <xsd:complexType><xsd:sequence>
          <xsd:element name="codigo" type="xsd:string"/>
          <xsd:element name="nombre" type="xsd:string"/>
          <xsd:element name="precio" type="xsd:decimal"/>
          <xsd:element name="stock"  type="xsd:int"/>
        </xsd:sequence></xsd:complexType>
      </xsd:element>

      <xsd:element name="ConsultarStockRequest">
        <xsd:complexType><xsd:sequence>
          <xsd:element name="codigo" type="xsd:string"/>
        </xsd:sequence></xsd:complexType>
      </xsd:element>
      <xsd:element name="ConsultarStockResponse">
        <xsd:complexType><xsd:sequence>
          <xsd:element name="codigo"     type="xsd:string"/>
          <xsd:element name="disponible" type="xsd:int"/>
        </xsd:sequence></xsd:complexType>
      </xsd:element>
    </xsd:schema>
  </types>

  <message name="ListarProductosIn"><part name="parameters" element="tns:ListarProductosRequest"/></message>
  <message name="ListarProductosOut"><part name="parameters" element="tns:ListarProductosResponse"/></message>
  <message name="ObtenerProductoIn"><part name="parameters" element="tns:ObtenerProductoRequest"/></message>
  <message name="ObtenerProductoOut"><part name="parameters" element="tns:ObtenerProductoResponse"/></message>
  <message name="ConsultarStockIn"><part name="parameters" element="tns:ConsultarStockRequest"/></message>
  <message name="ConsultarStockOut"><part name="parameters" element="tns:ConsultarStockResponse"/></message>

  <portType name="CatalogoPortType">
    <operation name="ListarProductos">
      <input message="tns:ListarProductosIn"/><output message="tns:ListarProductosOut"/>
    </operation>
    <operation name="ObtenerProducto">
      <input message="tns:ObtenerProductoIn"/><output message="tns:ObtenerProductoOut"/>
    </operation>
    <operation name="ConsultarStock">
      <input message="tns:ConsultarStockIn"/><output message="tns:ConsultarStockOut"/>
    </operation>
  </portType>

  <binding name="CatalogoBinding" type="tns:CatalogoPortType">
    <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="ListarProductos">
      <soap:operation soapAction="{ns}/ListarProductos"/>
      <input><soap:body use="literal"/></input><output><soap:body use="literal"/></output>
    </operation>
    <operation name="ObtenerProducto">
      <soap:operation soapAction="{ns}/ObtenerProducto"/>
      <input><soap:body use="literal"/></input><output><soap:body use="literal"/></output>
    </operation>
    <operation name="ConsultarStock">
      <soap:operation soapAction="{ns}/ConsultarStock"/>
      <input><soap:body use="literal"/></input><output><soap:body use="literal"/></output>
    </operation>
  </binding>

  <service name="CatalogoService">
    <port name="CatalogoPort" binding="tns:CatalogoBinding">
      <soap:address location="http://HOSTPORT/servicio"/>
    </port>
  </service>
</definitions>
""".replace("{ns}", NS)


def sobre(cuerpo):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
            '<soap:Body>%s</soap:Body></soap:Envelope>' % cuerpo)


def fault(codigo, mensaje, detalle=""):
    return sobre(
        '<soap:Fault><faultcode>soap:%s</faultcode>'
        '<faultstring>%s</faultstring>'
        '<detail><CodigoNegocio>%s</CodigoNegocio></detail></soap:Fault>'
        % (codigo, sx.escape(mensaje), sx.escape(detalle)))


def producto_xml(p, tag="producto"):
    c, n, pr, st = p
    return ('<%s><codigo>%s</codigo><nombre>%s</nombre>'
            '<precio>%.2f</precio><stock>%d</stock></%s>'
            % (tag, c, sx.escape(n), pr, st, tag))


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *a):
        print("  %s  %s" % (self.command, fmt % a))

    def _responder(self, estado, cuerpo, tipo="text/xml; charset=utf-8"):
        datos = cuerpo.encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
        if self.path.startswith("/servicio") and "wsdl" in self.path.lower():
            host = self.headers.get("Host", "localhost:%d" % PUERTO)
            return self._responder(200, WSDL.replace("HOSTPORT", host))
        self._responder(404, "No encontrado", "text/plain; charset=utf-8")

    def do_POST(self):
        if not self.path.startswith("/servicio"):
            return self._responder(404, "No encontrado", "text/plain; charset=utf-8")

        n = int(self.headers.get("Content-Length", 0))
        cuerpo = self.rfile.read(n).decode("utf-8", "replace")

        if "ListarProductos" in cuerpo:
            items = "".join(producto_xml(p) for p in PRODUCTOS)
            return self._responder(200, sobre(
                '<ListarProductosResponse xmlns="%s">%s</ListarProductosResponse>' % (NS, items)))

        if "ObtenerProducto" in cuerpo:
            m = re.search(r"<(?:\w+:)?codigo>([^<]*)</(?:\w+:)?codigo>", cuerpo)
            cod = (m.group(1) if m else "").strip()

            # Caso didáctico 1: Fault con HTTP 500 — el esperado
            if cod == "ERR-404":
                return self._responder(500, fault("Client", "El producto no existe", "PROD_NO_ENCONTRADO"))
            # Caso didáctico 2: Fault con HTTP 200 — el que rompe a quien confía en el código HTTP
            if cod == "ERR-200":
                return self._responder(200, fault("Server", "Error de negocio devuelto con HTTP 200",
                                                  "FAULT_CON_200"))
            for p in PRODUCTOS:
                if p[0] == cod:
                    return self._responder(200, sobre(
                        '<ObtenerProductoResponse xmlns="%s">%s</ObtenerProductoResponse>'
                        % (NS, producto_xml(p, "x").replace("<x>", "").replace("</x>", ""))))
            return self._responder(500, fault("Client", "El producto no existe", "PROD_NO_ENCONTRADO"))

        if "ConsultarStock" in cuerpo:
            time.sleep(0.7)                      # retardo artificial, para que la medición se note
            m = re.search(r"<(?:\w+:)?codigo>([^<]*)</(?:\w+:)?codigo>", cuerpo)
            cod = (m.group(1) if m else "").strip()
            st = next((p[3] for p in PRODUCTOS if p[0] == cod), None)
            if st is None:
                return self._responder(500, fault("Client", "El producto no existe", "PROD_NO_ENCONTRADO"))
            return self._responder(200, sobre(
                '<ConsultarStockResponse xmlns="%s"><codigo>%s</codigo>'
                '<disponible>%d</disponible></ConsultarStockResponse>' % (NS, cod, st)))

        return self._responder(500, fault("Client", "Operación no reconocida", "OP_DESCONOCIDA"))


if __name__ == "__main__":
    print("Servicio SOAP del Taller 05 escuchando en http://%s:%d/servicio" % (HOST, PUERTO))
    print("WSDL: http://localhost:%d/servicio?wsdl" % PUERTO)
    print("Desde el emulador de Android use  http://10.0.2.2:%d/servicio\n" % PUERTO)
    ThreadingHTTPServer((HOST, PUERTO), Handler).serve_forever()
