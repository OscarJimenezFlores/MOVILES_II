#!/usr/bin/env python3
"""
BFF (Backend For Frontend) del Taller 05 de SI-988.

Habla SOAP con el servicio heredado de servidor.py y REST/JSON con la app.
Solo librería estándar de Python.

    python3 bff.py            # escucha en 0.0.0.0:8081

Endpoints REST:
    GET /api/productos            -> 200 [ {...}, ... ]
    GET /api/productos/<codigo>   -> 200 {...}  |  404  |  502
    GET /api/productos/<codigo>/stock -> 200 { codigo, disponible }

El BFF hace tres cosas que el móvil no debería hacer:
  1. Construir y analizar XML.
  2. Traducir el <soap:Fault> a un código HTTP correcto.
  3. Reducir el payload: entrega solo los campos que la app usa.
"""
import json, re, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SOAP_URL = "http://localhost:8080/servicio"
NS = "http://si988.upt.pe/servicio"
HOST, PUERTO = "0.0.0.0", 8081


def llamar_soap(operacion, cuerpo_interno=""):
    """Devuelve (texto_xml, http_status). Nunca lanza por código HTTP."""
    envelope = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
        '<soap:Body><%s xmlns="%s">%s</%s></soap:Body></soap:Envelope>'
        % (operacion + "Request", NS, cuerpo_interno, operacion + "Request")
    )
    req = urllib.request.Request(
        SOAP_URL, data=envelope.encode("utf-8"),
        headers={"Content-Type": "text/xml; charset=utf-8",
                 "SOAPAction": '"%s/%s"' % (NS, operacion)})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("utf-8"), r.status
    except urllib.error.HTTPError as e:
        return e.read().decode("utf-8"), e.code


def hay_fault(xml):
    """El Fault puede venir con HTTP 200: SIEMPRE se inspecciona el cuerpo."""
    return "<soap:Fault" in xml or ":Fault>" in xml or "<Fault" in xml


def leer_fault(xml):
    razon = re.search(r"<faultstring>([^<]*)</faultstring>", xml)
    codigo = re.search(r"<CodigoNegocio>([^<]*)</CodigoNegocio>", xml)
    return (codigo.group(1) if codigo else "DESCONOCIDO",
            razon.group(1) if razon else "Error del servicio")


def campo(bloque, nombre):
    m = re.search(r"<(?:\w+:)?%s>([^<]*)</(?:\w+:)?%s>" % (nombre, nombre), bloque)
    return m.group(1) if m else None


def productos_desde_xml(xml):
    salida = []
    for bloque in re.findall(r"<producto>(.*?)</producto>", xml, re.S):
        salida.append({
            "codigo": campo(bloque, "codigo"),
            "nombre": campo(bloque, "nombre"),
            "precio": float(campo(bloque, "precio") or 0),
            "stock": int(campo(bloque, "stock") or 0),
        })
    return salida


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *a):
        print("  %s  %s" % (self.command, fmt % a))

    def _json(self, estado, obj):
        datos = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def _error(self, estado, codigo, mensaje):
        self._json(estado, {"codigo": codigo, "mensaje": mensaje})

    def do_GET(self):
        # GET /api/productos
        if self.path == "/api/productos":
            xml, _ = llamar_soap("ListarProductos")
            if hay_fault(xml):
                cod, msg = leer_fault(xml)
                return self._error(502, cod, msg)
            return self._json(200, productos_desde_xml(xml))

        # GET /api/productos/<codigo>/stock
        m = re.fullmatch(r"/api/productos/([\w-]+)/stock", self.path)
        if m:
            xml, _ = llamar_soap("ConsultarStock", "<codigo>%s</codigo>" % m.group(1))
            if hay_fault(xml):
                cod, msg = leer_fault(xml)
                return self._error(404 if cod == "PROD_NO_ENCONTRADO" else 502, cod, msg)
            return self._json(200, {"codigo": campo(xml, "codigo"),
                                    "disponible": int(campo(xml, "disponible") or 0)})

        # GET /api/productos/<codigo>
        m = re.fullmatch(r"/api/productos/([\w-]+)", self.path)
        if m:
            xml, _ = llamar_soap("ObtenerProducto", "<codigo>%s</codigo>" % m.group(1))
            if hay_fault(xml):
                cod, msg = leer_fault(xml)
                # Aquí está el valor del BFF: el Fault se traduce a un código HTTP correcto.
                return self._error(404 if cod == "PROD_NO_ENCONTRADO" else 502, cod, msg)
            return self._json(200, {
                "codigo": campo(xml, "codigo"),
                "nombre": campo(xml, "nombre"),
                "precio": float(campo(xml, "precio") or 0),
                "stock": int(campo(xml, "stock") or 0),
            })

        self._error(404, "RUTA_NO_ENCONTRADA", "El recurso no existe")


if __name__ == "__main__":
    print("BFF escuchando en http://%s:%d" % (HOST, PUERTO))
    print("Consume el servicio SOAP en %s" % SOAP_URL)
    print("Desde el emulador de Android use  http://10.0.2.2:%d\n" % PUERTO)
    ThreadingHTTPServer((HOST, PUERTO), Handler).serve_forever()
