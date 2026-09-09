<div align="center">
  <img src="../../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Ruta Limpia</h1>

<p align="center">
  Catálogo de dominios de ejemplo · <strong>App 01</strong> · Recojo de residuos sólidos<br>
  <strong>SI-988 · Soluciones Móviles II</strong>
</p>

---

> **Esto es un ejemplo, no una asignación.** Su equipo puede proponer su propia app. Este dominio está desarrollado hasta el nivel que el curso exige, para que vea **qué profundidad se espera** y pueda decidir con criterio. Si lo toma tal cual, tiene que llevarlo más lejos que lo que está aquí.

## 1. El problema

En los distritos de la periferia el camión recolector no tiene horario fijo. La gente saca la basura cuando cree que va a pasar, y si no pasa queda en la vereda hasta el día siguiente. Nadie sabe dónde está el camión.

**Segmento objetivo.** Vecinos de un distrito de 40 000 habitantes, y los operarios del camión

## 2. Por qué tiene que ser una app y no una página web

Es la pregunta de cierre de la Semana 01, y la que más propuestas hunde.

> El vecino necesita un aviso **cuando el camión está a diez minutos de su cuadra**. Eso exige notificación push y posición en tiempo real. Una página web no avisa a nadie.

**Capacidades del móvil que esta app usa de verdad.**

| Capacidad | Por qué la necesita |
|---|---|
| **Notificaciones push por proximidad** | Sin aviso previo, el vecino saca la basura a ciegas y el problema no se resuelve |
| **Ubicación en segundo plano del vehículo** | La posición del camión debe seguir enviándose con la app minimizada durante toda la ruta |
| **Mapa con la ruta en curso** | Ver el avance real es lo que permite decidir cuándo bajar los residuos |

## 3. Alcance del semestre — cinco sprints

El alcance está acotado a lo que **cabe en cinco sprints** con un equipo de estudiantes. Todo lo demás es trabajo futuro y se declara como tal.

| Sprint | Semanas | Objetivo del sprint |
|---|---|---|
| **1** | 01–03 | Autenticación, catálogo de rutas y mapa base |
| **2** | 04–06 | Posición del vehículo y ruta en curso |
| **3** | 07–09 | Notificación por proximidad |
| **4** | 10–12 | Reporte de punto no recogido con foto |
| **5** | 13–16 | Historial y panel del operario |

## 4. Modelo de dominio

Las entidades mínimas. Falta el detalle de atributos. Eso lo define el equipo.

| Entidad | Rol en el dominio |
|---|---|
| **Ruta** | Entidad central del dominio |
| **Vehículo** | Entidad central del dominio |
| **Punto de recojo** | Entidad central del dominio |
| **Reporte** | Entidad central del dominio |
| **Aviso** | Entidad central del dominio |

## 5. Datos personales y permisos

Es la sección que determina el trabajo de las Semanas 08, 09, 10 y 11.

**Sensibilidad de los datos que trata. Media**

| Dato personal que trata | Base legal a declarar |
|---|---|
| Dirección aproximada del vecino | Consentimiento previo, informado y expreso |
| Token de notificación | Consentimiento previo, informado y expreso |

| Permiso del sistema | Cuándo se solicita | Qué pasa si el usuario lo niega |
|---|---|---|
| **Ubicación aproximada y precisa** | Al abrir el mapa por primera vez | Se degrada a búsqueda manual por dirección |
| **Ubicación en segundo plano (solo la app del operario)** | Al usar la función que lo requiere | Se ofrece un modo alternativo |
| **Notificaciones** | Tras la primera acción que generará un aviso, no en el arranque | La app funciona, pero el usuario debe consultar a mano |

> **Ley 29733 y D. S. 016-2024-JUS.** Todo dato personal exige consentimiento previo, informado y expreso. Los datos de salud y los de menores de edad son **datos sensibles** y su tratamiento tiene exigencias reforzadas. La política de privacidad de la Semana 09 no es un trámite. Es lo que hace legal a la app.

## 6. API simulada

El equipo no depende de un servicio externo. Se levanta un servidor simulado con el contrato en `docs/api/openapi.yaml`.

**Recursos mínimos del contrato.**

| Recurso | Métodos |
|---|---|
| `/ruta` | `GET` · `POST` · `PUT` · `DELETE` |
| `/vehículo` | `GET` · `POST` · `PUT` · `DELETE` |
| `/punto-de-recojo` | `GET` · `POST` · `PUT` · `DELETE` |
| `/reporte` | `GET` · `POST` · `PUT` · `DELETE` |
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
