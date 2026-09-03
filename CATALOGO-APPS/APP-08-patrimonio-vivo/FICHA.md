<div align="center">
  <img src="../../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Patrimonio Vivo</h1>

<p align="center">
  Catálogo de dominios de ejemplo · <strong>App 08</strong> · Guía turística de patrimonio<br>
  <strong>SI-988 · Soluciones Móviles II</strong>
</p>

---

> **Esto es un ejemplo, no una asignación.** Su equipo puede proponer su propia app. Este dominio está desarrollado hasta el nivel que el curso exige, para que vea **qué profundidad se espera** y pueda decidir con criterio. Si lo toma tal cual, tiene que llevarlo más lejos que lo que está aquí.

## 1. El problema

El visitante llega al centro histórico sin saber qué está viendo. Los paneles informativos están deteriorados y no hay guía disponible fuera de temporada.

**Segmento objetivo.** Turistas nacionales y chilenos que visitan el centro histórico de Tacna

## 2. Por qué tiene que ser una app y no una página web

Es la pregunta de cierre de la Semana 01, y la que más propuestas hunde.

> El contenido debe estar disponible **caminando y sin datos móviles**, porque el visitante extranjero suele no tener plan local. Exige descarga previa y ubicación.

**Capacidades del móvil que esta app usa de verdad:**

| Capacidad | Por qué la necesita |
|---|---|
| **Contenido descargado para uso sin conexión** | El visitante chileno suele no tener plan de datos peruano |
| **Ubicación para detectar el punto cercano** | El contenido debe aparecer solo, caminando, sin buscar nada |
| **Notificación al acercarse a un hito** | Es lo que reemplaza al panel informativo deteriorado |

## 3. Alcance del semestre — cinco sprints

El alcance está acotado a lo que **cabe en cinco sprints** con un equipo de estudiantes. Todo lo demás es trabajo futuro y se declara como tal.

| Sprint | Semanas | Objetivo del sprint |
|---|---|---|
| **1** | 01–03 | Catálogo de hitos y contenido base |
| **2** | 04–06 | Descarga para uso sin conexión |
| **3** | 07–09 | Mapa y detección de proximidad |
| **4** | 10–12 | Recorridos guiados y multilenguaje |
| **5** | 13–16 | Estadísticas de visita y panel de contenidos |

## 4. Modelo de dominio

Las entidades mínimas. Falta el detalle de atributos: eso lo define el equipo.

| Entidad | Rol en el dominio |
|---|---|
| **Hito** | Entidad central del dominio |
| **Recorrido** | Entidad central del dominio |
| **Contenido** | Entidad central del dominio |
| **Visita** | Entidad central del dominio |
| **Idioma** | Entidad central del dominio |

## 5. Datos personales y permisos

Es la sección que determina el trabajo de las Semanas 08, 09, 10 y 11.

**Sensibilidad de los datos que trata: Baja**

| Dato personal que trata | Base legal a declarar |
|---|---|
| Recorridos del visitante | Consentimiento previo, informado y expreso |
| Idioma preferido | Consentimiento previo, informado y expreso |

| Permiso del sistema | Cuándo se solicita | Qué pasa si el usuario lo niega |
|---|---|---|
| **Ubicación precisa** | Al usar por primera vez la función que la necesita, no al abrir la app | La función principal deja de operar. Debe explicarse antes de pedirlo y ofrecer un modo degradado |
| **Almacenamiento** | Al descargar contenido por primera vez | No se puede usar sin conexión; se advierte al usuario |
| **Notificaciones** | Tras la primera acción que generará un aviso, no en el arranque | La app funciona, pero el usuario debe consultar a mano |

> **Ley 29733 y D. S. 016-2024-JUS.** Todo dato personal exige consentimiento previo, informado y expreso. Los datos de salud y los de menores de edad son **datos sensibles** y su tratamiento tiene exigencias reforzadas. La política de privacidad de la Semana 09 no es un trámite: es lo que hace legal a la app.

## 6. API simulada

El equipo no depende de un servicio externo. Se levanta un servidor simulado con el contrato en `docs/api/openapi.yaml`.

**Recursos mínimos del contrato:**

| Recurso | Métodos |
|---|---|
| `/hito` | `GET` · `POST` · `PUT` · `DELETE` |
| `/recorrido` | `GET` · `POST` · `PUT` · `DELETE` |
| `/contenido` | `GET` · `POST` · `PUT` · `DELETE` |
| `/visita` | `GET` · `POST` · `PUT` · `DELETE` |
| `/idioma` | `GET` · `POST` · `PUT` · `DELETE` |

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
