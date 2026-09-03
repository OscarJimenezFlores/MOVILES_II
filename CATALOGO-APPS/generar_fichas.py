# -*- coding: utf-8 -*-
"""Genera la ficha y el Product Backlog semilla de cada dominio de ejemplo."""
import os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dominios import D
from roles import V
R = os.path.dirname(os.path.abspath(__file__))

# 25 historias: 5 por sprint. Plantilla común, entidades propias de cada dominio.
PLANTILLA = [
 # (sprint, épica, "como / quiero / para", puntos, riesgo, dato_personal)
 (1,"Acceso","Como {u} quiero registrarme con correo y contraseña para tener mi cuenta",5,"Medio","Sí"),
 (1,"Acceso","Como {u} quiero iniciar sesión y que mi sesión se mantenga para no escribir la clave cada vez",3,"Medio","Sí"),
 (1,"Acceso","Como {u} quiero recuperar mi contraseña para no perder el acceso",3,"Bajo","Sí"),
 (1,"{e0}","Como {u} quiero ver la lista de {e0p} registrados para ubicar el que me corresponde",5,"Bajo","No"),
 (1,"{e0}","Como {u} quiero ver el detalle de un {e0l} para conocer toda su información",3,"Bajo","No"),
 (2,"{e2}","Como {u} quiero consultar el estado actual de mi {e2l} para actuar a tiempo",8,"Alto","No"),
 (2,"{e1}","Como {u} quiero que la información se actualice sola para no recargar a mano",5,"Alto","No"),
 (2,"Ubicación","Como {u} quiero ver la ubicación en el mapa para orientarme",8,"Alto","Sí"),
 (2,"Datos","Como {u} quiero que la app funcione sin conexión para seguir usándola con mala señal",8,"Alto","No"),
 (2,"Datos","Como {u} quiero saber cuándo se actualizaron los datos para no confiar en información vieja",3,"Bajo","No"),
 (3,"{e2}","Como {u} quiero registrar un {e2l} para dejar constancia de lo ocurrido",8,"Alto","Sí"),
 (3,"{e2}","Como {u} quiero adjuntar una foto al {e2l} para respaldarlo",5,"Medio","Sí"),
 (3,"{e2}","Como {u} quiero editar o anular un {e2l} propio para corregir errores",5,"Medio","Sí"),
 (3,"{e2}","Como {u} quiero ver el historial de mis {e2p} para revisar lo que hice",5,"Bajo","Sí"),
 (3,"Privacidad","Como {u} quiero leer qué datos míos se guardan y para qué antes de aceptar",3,"Alto","Sí"),
 (4,"Avisos","Como {u} quiero recibir un aviso cuando {ev} para no estar revisando",8,"Alto","Sí"),
 (4,"Avisos","Como {u} quiero elegir qué avisos recibir para que no me molesten de más",5,"Bajo","Sí"),
 (4,"Avisos","Como {u} quiero ver los avisos pasados para no perderme ninguno",3,"Bajo","No"),
 (4,"Seguridad","Como {u} quiero que mis datos viajen cifrados para que nadie los intercepte",5,"Alto","Sí"),
 (4,"Seguridad","Como {u} quiero cerrar sesión en todos mis dispositivos si pierdo el teléfono",5,"Alto","Sí"),
 (5,"{e3}","Como {a} quiero un panel con el resumen de {e3l} para tomar decisiones",8,"Medio","No"),
 (5,"{e3}","Como {a} quiero filtrar por fecha y por estado para encontrar lo que busco",5,"Bajo","No"),
 (5,"{e3}","Como {a} quiero exportar el reporte para usarlo fuera de la app",5,"Bajo","Sí"),
 (5,"Calidad","Como {u} quiero que la app abra en menos de 2 segundos para no perder tiempo",5,"Medio","No"),
 (5,"Privacidad","Como {u} quiero eliminar mi cuenta y mis datos para ejercer mi derecho de supresión",5,"Alto","Sí"),
]

def backlog(d):
    e = d["entidades"]; v = V[d["id"]]
    ctx = dict(u=v["rol"], a=v["admin"], ev=v["evento"],
               e0=e[0], e0l=v["obj"], e0p=v["objp"], e1=e[1], e1l=e[1].lower(),
               e2=v["reg"][0].upper()+v["reg"][1:], e2l=v["reg"], e2p=v["regp"],
               e3=e[2], e3l=v["panel"])
    filas = []
    for i, (sp, ep, hist, pt, ri, dp) in enumerate(PLANTILLA, 1):
        filas.append(dict(id="H%02d" % i, sprint=sp, epica=ep.format(**ctx),
                          historia=hist.format(**ctx), puntos=pt, riesgo=ri,
                          dato_personal=dp, estado="Pendiente",
                          criterio_aceptacion="Por refinar en la Semana 03 con formato Gherkin"))
    return filas

FICHA = """<div align="center">
  <img src="../../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">{nombre}</h1>

<p align="center">
  Catálogo de dominios de ejemplo · <strong>App {id}</strong> · {tag}<br>
  <strong>SI-988 · Soluciones Móviles II</strong>
</p>

---

> **Esto es un ejemplo, no una asignación.** Su equipo puede proponer su propia app. Este dominio está desarrollado hasta el nivel que el curso exige, para que vea **qué profundidad se espera** y pueda decidir con criterio. Si lo toma tal cual, tiene que llevarlo más lejos que lo que está aquí.

## 1. El problema

{problema}

**Segmento objetivo.** {segmento}

## 2. Por qué tiene que ser una app y no una página web

Es la pregunta de cierre de la Semana 01, y la que más propuestas hunde.

> {por_que_movil}

**Capacidades del móvil que esta app usa de verdad:**

{tabla_movil}

## 3. Alcance del semestre — cinco sprints

El alcance está acotado a lo que **cabe en cinco sprints** con un equipo de estudiantes. Todo lo demás es trabajo futuro y se declara como tal.

| Sprint | Semanas | Objetivo del sprint |
|---|---|---|
{tabla_sprints}

## 4. Modelo de dominio

Las entidades mínimas. Falta el detalle de atributos: eso lo define el equipo.

{tabla_entidades}

## 5. Datos personales y permisos

Es la sección que determina el trabajo de las Semanas 08, 09, 10 y 11.

**Sensibilidad de los datos que trata: {sensibles}**

| Dato personal que trata | Base legal a declarar |
|---|---|
{tabla_datos}

| Permiso del sistema | Cuándo se solicita | Qué pasa si el usuario lo niega |
|---|---|---|
{tabla_permisos}

> **Ley 29733 y D. S. 016-2024-JUS.** Todo dato personal exige consentimiento previo, informado y expreso. Los datos de salud y los de menores de edad son **datos sensibles** y su tratamiento tiene exigencias reforzadas. La política de privacidad de la Semana 09 no es un trámite: es lo que hace legal a la app.

## 6. API simulada

El equipo no depende de un servicio externo. Se levanta un servidor simulado con el contrato en `docs/api/openapi.yaml`.

**Recursos mínimos del contrato:**

{tabla_api}

> Los códigos de estado que el contrato debe contemplar: `200`, `201`, `400`, `401`, `403`, `404`, `409`, `429` con `Retry-After`, y `500`. El manejo diferenciado de cada uno es lo que se evalúa en la Semana 04.

## 7. Product Backlog semilla

**25 historias**, cinco por sprint, en [`backlog-semilla.csv`](backlog-semilla.csv).

> **No es el backlog final.** Es el punto de partida para que el Taller 03 no empiece en una hoja en blanco. En ese taller el equipo lo refina: aplica INVEST, divide lo que supere 13 puntos, escribe los criterios de aceptación en Gherkin, y **ordena por valor y riesgo**, no por número de historia. Las historias marcadas con dato personal necesitan además los cuatro escenarios de la Semana 09.

| Columna | Contenido |
|---|---|
| `id` | Identificador de la historia |
| `sprint` | Sprint propuesto, 1 a 5 |
| `epica` | Agrupación funcional |
| `historia` | Formato «Como… quiero… para…» |
| `puntos` | Estimación inicial en la escala de Fibonacci. **El equipo la reestima con Planning Poker** |
| `riesgo` | Alto, Medio o Bajo. Ordena el backlog junto con el valor |
| `dato_personal` | Si la historia trata datos personales |
| `criterio_aceptacion` | Vacío a propósito: se escribe en el Taller 03 |

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
"""

SEM = ["01–03", "04–06", "07–09", "10–12", "13–16"]
NEG = {"Ubicación precisa": "La función principal deja de operar. Debe explicarse antes de pedirlo y ofrecer un modo degradado",
       "Ubicación aproximada y precisa": "Se degrada a búsqueda manual por dirección",
       "Ubicación en segundo plano": "**El caso más delicado.** Requiere justificación explícita ante la tienda y una pantalla previa que lo explique",
       "Notificaciones": "La app funciona, pero el usuario debe consultar a mano",
       "Cámara": "Se permite adjuntar desde la galería como alternativa",
       "Almacenamiento": "No se puede usar sin conexión; se advierte al usuario"}
CUANDO = {"Ubicación precisa": "Al usar por primera vez la función que la necesita, no al abrir la app",
          "Ubicación aproximada y precisa": "Al abrir el mapa por primera vez",
          "Ubicación en segundo plano": "Solo tras conceder la ubicación en primer plano, con pantalla explicativa propia",
          "Notificaciones": "Tras la primera acción que generará un aviso, no en el arranque",
          "Cámara": "Al pulsar el botón de tomar foto",
          "Almacenamiento": "Al descargar contenido por primera vez"}

for d in D:
    base = os.path.join(R, "APP-%s-%s" % (d["id"], d["slug"]))
    os.makedirs(base, exist_ok=True)
    filas = backlog(d)
    with open(os.path.join(base, "backlog-semilla.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys())); w.writeheader(); w.writerows(filas)
    tm = "| Capacidad | Por qué la necesita |\n|---|---|\n" + "\n".join("| **%s** | %s |" % (m, V[d["id"]]["razones"].get(m, "")) for m in d["movil"])
    ts = "\n".join("| **%d** | %s | %s |" % (i + 1, SEM[i], s) for i, s in enumerate(d["sprints"]))
    te = "| Entidad | Rol en el dominio |\n|---|---|\n" + "\n".join("| **%s** | Entidad central del dominio |" % e for e in d["entidades"])
    td = "\n".join("| %s | Consentimiento previo, informado y expreso |" % x for x in d["datos"])
    tp = "\n".join("| **%s** | %s | %s |" % (p, CUANDO.get(p, "Al usar la función que lo requiere"), NEG.get(p, "Se ofrece un modo alternativo")) for p in d["permisos"])
    ta = "| Recurso | Métodos |\n|---|---|\n" + "\n".join("| `/%s` | `GET` · `POST` · `PUT` · `DELETE` |" % e.lower().replace(" ", "-") for e in d["entidades"])
    open(os.path.join(base, "FICHA.md"), "w", encoding="utf-8").write(FICHA.format(
        nombre=d["nombre"], id=d["id"], tag=d["tag"], problema=d["problema"], segmento=d["segmento"],
        por_que_movil=d["por_que_movil"], tabla_movil=tm, tabla_sprints=ts, tabla_entidades=te,
        sensibles=d["sensibles"], tabla_datos=td, tabla_permisos=tp, tabla_api=ta))
    print("ok  APP-%s  %-18s %d historias" % (d["id"], d["nombre"], len(filas)))
