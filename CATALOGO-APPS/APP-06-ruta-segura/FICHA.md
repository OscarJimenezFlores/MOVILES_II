<div align="center">
  <img src="../../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Ruta Segura</h1>

<p align="center">
  Catálogo de dominios de ejemplo · <strong>App 06</strong> · Transporte escolar<br>
  <strong>SI-988 · Soluciones Móviles II</strong>
</p>

---

> **Esto es un ejemplo, no una asignación.** Su equipo puede proponer su propia app. Este dominio está desarrollado hasta el nivel que el curso exige, para que vea **qué profundidad se espera** y pueda decidir con criterio. Si lo toma tal cual, tiene que llevarlo más lejos que lo que está aquí.

## 1. El problema

Los padres no saben si el movilidad escolar recogió a su hijo ni por dónde va. Cuando llaman, el conductor está manejando y no contesta.

**Segmento objetivo.** Padres de familia, conductores de movilidad escolar y el colegio

## 2. Por qué tiene que ser una app y no una página web

Es la pregunta de cierre de la Semana 01, y la que más propuestas hunde.

> El padre necesita la confirmación **en el momento del recojo**, y el conductor no puede operar nada complejo mientras maneja. Push y ubicación en segundo plano son obligatorios.

**Capacidades del móvil que esta app usa de verdad:**

| Capacidad | Por qué la necesita |
|---|---|
| **Ubicación en segundo plano del vehículo** | La ruta dura 40 minutos con la app minimizada; sin segundo plano no hay seguimiento |
| **Notificación de recojo y llegada** | Es la confirmación que hoy el padre intenta conseguir llamando al conductor que va manejando |
| **Registro con un solo toque para el conductor** | Cualquier interfaz compleja al volante es un riesgo de seguridad vial |

## 3. Alcance del semestre — cinco sprints

El alcance está acotado a lo que **cabe en cinco sprints** con un equipo de estudiantes. Todo lo demás es trabajo futuro y se declara como tal.

| Sprint | Semanas | Objetivo del sprint |
|---|---|---|
| **1** | 01–03 | Autenticación por rol y padrón de estudiantes |
| **2** | 04–06 | Ruta y mapa en vivo |
| **3** | 07–09 | Registro de recojo y llegada |
| **4** | 10–12 | Notificaciones a los apoderados |
| **5** | 13–16 | Historial, incidencias y panel del colegio |

## 4. Modelo de dominio

Las entidades mínimas. Falta el detalle de atributos: eso lo define el equipo.

| Entidad | Rol en el dominio |
|---|---|
| **Estudiante** | Entidad central del dominio |
| **Vehículo** | Entidad central del dominio |
| **Ruta** | Entidad central del dominio |
| **Evento de recojo** | Entidad central del dominio |
| **Apoderado** | Entidad central del dominio |

## 5. Datos personales y permisos

Es la sección que determina el trabajo de las Semanas 08, 09, 10 y 11.

**Sensibilidad de los datos que trata: **Muy alta — menores de edad****

| Dato personal que trata | Base legal a declarar |
|---|---|
| **Datos de menores de edad** | Consentimiento previo, informado y expreso |
| Ubicación del vehículo | Consentimiento previo, informado y expreso |
| Dirección de recojo | Consentimiento previo, informado y expreso |

| Permiso del sistema | Cuándo se solicita | Qué pasa si el usuario lo niega |
|---|---|---|
| **Ubicación en segundo plano** | Solo tras conceder la ubicación en primer plano, con pantalla explicativa propia | **El caso más delicado.** Requiere justificación explícita ante la tienda y una pantalla previa que lo explique |
| **Notificaciones** | Tras la primera acción que generará un aviso, no en el arranque | La app funciona, pero el usuario debe consultar a mano |

> **Ley 29733 y D. S. 016-2024-JUS.** Todo dato personal exige consentimiento previo, informado y expreso. Los datos de salud y los de menores de edad son **datos sensibles** y su tratamiento tiene exigencias reforzadas. La política de privacidad de la Semana 09 no es un trámite: es lo que hace legal a la app.

## 6. API simulada

El equipo no depende de un servicio externo. Se levanta un servidor simulado con el contrato en `docs/api/openapi.yaml`.

**Recursos mínimos del contrato:**

| Recurso | Métodos |
|---|---|
| `/estudiante` | `GET` · `POST` · `PUT` · `DELETE` |
| `/vehículo` | `GET` · `POST` · `PUT` · `DELETE` |
| `/ruta` | `GET` · `POST` · `PUT` · `DELETE` |
| `/evento-de-recojo` | `GET` · `POST` · `PUT` · `DELETE` |
| `/apoderado` | `GET` · `POST` · `PUT` · `DELETE` |

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
