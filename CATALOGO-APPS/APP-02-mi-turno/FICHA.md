<div align="center">
  <img src="../../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Mi Turno</h1>

<p align="center">
  Catálogo de dominios de ejemplo · <strong>App 02</strong> · Turnos en establecimiento de salud<br>
  <strong>SI-988 · Soluciones Móviles II</strong>
</p>

---

> **Esto es un ejemplo, no una asignación.** Su equipo puede proponer su propia app. Este dominio está desarrollado hasta el nivel que el curso exige, para que vea **qué profundidad se espera** y pueda decidir con criterio. Si lo toma tal cual, tiene que llevarlo más lejos que lo que está aquí.

## 1. El problema

En el centro de salud la gente hace cola desde las cinco de la mañana para conseguir un cupo que se agota a las siete. Muchos viajan desde el valle para volverse sin atención.

**Segmento objetivo.** Pacientes de un centro de salud del primer nivel y su personal de admisión

## 2. Por qué tiene que ser una app y no una página web

Es la pregunta de cierre de la Semana 01, y la que más propuestas hunde.

> El paciente necesita saber **desde su casa** si le queda cupo, y que le avisen cuando falten tres turnos para el suyo. Sin notificación, la cola física no desaparece.

**Capacidades del móvil que esta app usa de verdad.**

| Capacidad | Por qué la necesita |
|---|---|
| **Notificaciones push de turno próximo** | Es lo que sustituye a la cola física desde las cinco de la mañana |
| **Funcionamiento sin conexión para el carné digital** | El paciente debe poder mostrar su turno aunque no tenga datos en el establecimiento |
| **Cámara para el documento de identidad** | Evita digitar mal el número de documento en la afiliación |

## 3. Alcance del semestre — cinco sprints

El alcance está acotado a lo que **cabe en cinco sprints** con un equipo de estudiantes. Todo lo demás es trabajo futuro y se declara como tal.

| Sprint | Semanas | Objetivo del sprint |
|---|---|---|
| **1** | 01–03 | Autenticación y registro del paciente |
| **2** | 04–06 | Consulta de cupos disponibles por consultorio |
| **3** | 07–09 | Reserva y cancelación de turno |
| **4** | 10–12 | Aviso de turno próximo y carné sin conexión |
| **5** | 13–16 | Panel de admisión y reprogramación |

## 4. Modelo de dominio

Las entidades mínimas. Falta el detalle de atributos. Eso lo define el equipo.

| Entidad | Rol en el dominio |
|---|---|
| **Paciente** | Entidad central del dominio |
| **Turno** | Entidad central del dominio |
| **Consultorio** | Entidad central del dominio |
| **Profesional** | Entidad central del dominio |
| **Aviso** | Entidad central del dominio |

## 5. Datos personales y permisos

Es la sección que determina el trabajo de las Semanas 08, 09, 10 y 11.

**Sensibilidad de los datos que trata.**Alta — dato de salud****

| Dato personal que trata | Base legal a declarar |
|---|---|
| Nombre y documento de identidad | Consentimiento previo, informado y expreso |
| Motivo de consulta | Consentimiento previo, informado y expreso |
| Historial de turnos | Consentimiento previo, informado y expreso |

| Permiso del sistema | Cuándo se solicita | Qué pasa si el usuario lo niega |
|---|---|---|
| **Notificaciones** | Tras la primera acción que generará un aviso, no en el arranque | La app funciona, pero el usuario debe consultar a mano |
| **Cámara** | Al pulsar el botón de tomar foto | Se permite adjuntar desde la galería como alternativa |

> **Ley 29733 y D. S. 016-2024-JUS.** Todo dato personal exige consentimiento previo, informado y expreso. Los datos de salud y los de menores de edad son **datos sensibles** y su tratamiento tiene exigencias reforzadas. La política de privacidad de la Semana 09 no es un trámite. Es lo que hace legal a la app.

## 6. API simulada

El equipo no depende de un servicio externo. Se levanta un servidor simulado con el contrato en `docs/api/openapi.yaml`.

**Recursos mínimos del contrato.**

| Recurso | Métodos |
|---|---|
| `/paciente` | `GET` · `POST` · `PUT` · `DELETE` |
| `/turno` | `GET` · `POST` · `PUT` · `DELETE` |
| `/consultorio` | `GET` · `POST` · `PUT` · `DELETE` |
| `/profesional` | `GET` · `POST` · `PUT` · `DELETE` |
| `/aviso` | `GET` · `POST` · `PUT` · `DELETE` |

> Los códigos de estado que el contrato debe contemplar — `200`, `201`, `400`, `401`, `403`, `404`, `409`, `429` con `Retry-After`, y `500`. El manejo diferenciado de cada uno es lo que se evalúa en la Semana 04.

## 7. Product Backlog semilla

**25 historias**, cinco por sprint, en [`backlog-semilla.csv`](backlog-semilla.csv).

> **No es el backlog final.** Es el punto de partida para que el Taller 03 no empiece en una hoja en blanco. En ese taller el equipo lo refina — aplica INVEST, divide lo que supere 13 puntos, escribe los criterios de aceptación en Gherkin, y **ordena por valor y riesgo**, no por número de historia. Las historias marcadas con dato personal necesitan además los cuatro escenarios de la Semana 09.

| Columna | Contenido |
|---|---|
| `id` | Identificador de la historia |
| `sprint` | Sprint propuesto, 1 a 5 |
| `epica` | Agrupación funcional |
| `historia` | Formato «Como… quiero… para…» |
| `puntos` | Estimación inicial en la escala de Fibonacci. **El equipo la reestima con Planning Poker** |
| `riesgo` | Alto, Medio o Bajo. Ordena el backlog junto con el valor |
| `dato_personal` | Si la historia trata datos personales |
| `criterio_aceptacion` | **Vacío a propósito.** Se escribe en el Taller 03 |

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
