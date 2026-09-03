<div align="center">
  <img src="../../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Carga Sur</h1>

<p align="center">
  Catálogo de dominios de ejemplo · <strong>App 03</strong> · Transporte de carga Tacna–Ilo<br>
  <strong>SI-988 · Soluciones Móviles II</strong>
</p>

---

> **Esto es un ejemplo, no una asignación.** Su equipo puede proponer su propia app. Este dominio está desarrollado hasta el nivel que el curso exige, para que vea **qué profundidad se espera** y pueda decidir con criterio. Si lo toma tal cual, tiene que llevarlo más lejos que lo que está aquí.

## 1. El problema

El transportista independiente consigue carga por llamadas y grupos de WhatsApp. Vuelve vacío la mitad de los viajes porque no se entera de la carga de retorno hasta que ya salió.

**Segmento objetivo.** Transportistas independientes y pequeños generadores de carga del corredor sur

## 2. Por qué tiene que ser una app y no una página web

Es la pregunta de cierre de la Semana 01, y la que más propuestas hunde.

> La carga de retorno se decide **en la carretera**, no en una oficina. Necesita ubicación, aviso inmediato y funcionar con señal intermitente.

**Capacidades del móvil que esta app usa de verdad:**

| Capacidad | Por qué la necesita |
|---|---|
| **Ubicación para ofertar carga cercana** | La carga de retorno solo sirve si está sobre la ruta que ya va a recorrer |
| **Notificaciones push de nueva carga en ruta** | La decisión se toma en carretera, en minutos, no revisando una web |
| **Persistencia sin conexión en tramos sin señal** | El corredor Tacna–Ilo tiene tramos largos sin cobertura |

## 3. Alcance del semestre — cinco sprints

El alcance está acotado a lo que **cabe en cinco sprints** con un equipo de estudiantes. Todo lo demás es trabajo futuro y se declara como tal.

| Sprint | Semanas | Objetivo del sprint |
|---|---|---|
| **1** | 01–03 | Autenticación y perfil de transportista |
| **2** | 04–06 | Publicación y búsqueda de carga |
| **3** | 07–09 | Ofertas y aceptación |
| **4** | 10–12 | Seguimiento del viaje y guía con foto |
| **5** | 13–16 | Historial, calificación y panel del generador |

## 4. Modelo de dominio

Las entidades mínimas. Falta el detalle de atributos: eso lo define el equipo.

| Entidad | Rol en el dominio |
|---|---|
| **Viaje** | Entidad central del dominio |
| **Carga** | Entidad central del dominio |
| **Transportista** | Entidad central del dominio |
| **Oferta** | Entidad central del dominio |
| **Guía** | Entidad central del dominio |

## 5. Datos personales y permisos

Es la sección que determina el trabajo de las Semanas 08, 09, 10 y 11.

**Sensibilidad de los datos que trata: Media**

| Dato personal que trata | Base legal a declarar |
|---|---|
| Placa y licencia del conductor | Consentimiento previo, informado y expreso |
| Ubicación del vehículo | Consentimiento previo, informado y expreso |
| Datos del generador de carga | Consentimiento previo, informado y expreso |

| Permiso del sistema | Cuándo se solicita | Qué pasa si el usuario lo niega |
|---|---|---|
| **Ubicación precisa** | Al usar por primera vez la función que la necesita, no al abrir la app | La función principal deja de operar. Debe explicarse antes de pedirlo y ofrecer un modo degradado |
| **Notificaciones** | Tras la primera acción que generará un aviso, no en el arranque | La app funciona, pero el usuario debe consultar a mano |
| **Cámara para la guía de remisión** | Al usar la función que lo requiere | Se ofrece un modo alternativo |

> **Ley 29733 y D. S. 016-2024-JUS.** Todo dato personal exige consentimiento previo, informado y expreso. Los datos de salud y los de menores de edad son **datos sensibles** y su tratamiento tiene exigencias reforzadas. La política de privacidad de la Semana 09 no es un trámite: es lo que hace legal a la app.

## 6. API simulada

El equipo no depende de un servicio externo. Se levanta un servidor simulado con el contrato en `docs/api/openapi.yaml`.

**Recursos mínimos del contrato:**

| Recurso | Métodos |
|---|---|
| `/viaje` | `GET` · `POST` · `PUT` · `DELETE` |
| `/carga` | `GET` · `POST` · `PUT` · `DELETE` |
| `/transportista` | `GET` · `POST` · `PUT` · `DELETE` |
| `/oferta` | `GET` · `POST` · `PUT` · `DELETE` |
| `/guía` | `GET` · `POST` · `PUT` · `DELETE` |

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
