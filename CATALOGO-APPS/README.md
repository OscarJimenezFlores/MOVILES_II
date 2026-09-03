<div align="center">
  <img src="../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="76">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="76">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Catálogo de dominios de app</h1>

<p align="center">
  Diez ejemplos desarrollados · <strong>SI-988 Soluciones Móviles II</strong><br>
  <em>Su equipo puede proponer el suyo. Esto existe para que sepa qué se espera.</em>
</p>

---

## La elección es libre

El curso **no le asigna** una app. Su equipo propone la suya en la Semana 01 y la construye durante todo el semestre.

Este catálogo existe por una razón concreta: para muchos estudiantes esta es la primera app que van a construir de principio a fin, y **una hoja en blanco en la primera semana no enseña nada**. Aquí hay diez dominios desarrollados hasta el nivel que el curso exige, para que vea la profundidad esperada antes de decidir.

| Puede | No puede |
|---|---|
| Proponer una app propia, distinta de todas estas | Entregar uno de estos ejemplos tal como está |
| Tomar uno de estos dominios y **llevarlo más lejos** | Copiar el backlog semilla sin refinarlo |
| Combinar la idea de dos dominios | Elegir un dominio que otro equipo ya tomó |
| Cambiar el segmento objetivo de un ejemplo | Proponer algo que no necesite ser una app |

## Los diez dominios

| N.º | App | Dominio | Usuario principal | Sensibilidad de los datos |
|---|---|---|---|---|
| **01** | [Ruta Limpia](APP-01-ruta-limpia/FICHA.md) | Recojo de residuos sólidos | vecino | Media |
| **02** | [Mi Turno](APP-02-mi-turno/FICHA.md) | Turnos en establecimiento de salud | paciente | **Alta — dato de salud** |
| **03** | [Carga Sur](APP-03-carga-sur/FICHA.md) | Transporte de carga Tacna–Ilo | transportista | Media |
| **04** | [Riego Justo](APP-04-riego-justo/FICHA.md) | Control de turnos de riego | regante | Baja |
| **05** | [Mi Farmacia](APP-05-mi-farmacia/FICHA.md) | Inventario y vencimientos de botica | responsable de local | Baja |
| **06** | [Ruta Segura](APP-06-ruta-segura/FICHA.md) | Transporte escolar | apoderado | **Muy alta — menores de edad** |
| **07** | [Reporta Tacna](APP-07-reporta-tacna/FICHA.md) | Reportes ciudadanos al municipio | vecino | Media |
| **08** | [Patrimonio Vivo](APP-08-patrimonio-vivo/FICHA.md) | Guía turística de patrimonio | visitante | Baja |
| **09** | [Campo Presente](APP-09-campo-presente/FICHA.md) | Asistencia de personal de campo | supervisor de cuadrilla | **Alta — dato laboral y biométrico si se usa rostro** |
| **10** | [Frontera Clara](APP-10-frontera-clara/FICHA.md) | Trámite de paso de frontera | usuario frecuente | Media |

Están escogidos para cubrir **capacidades móviles distintas**: notificación por proximidad, ubicación en segundo plano, funcionamiento sin conexión, cámara con coordenada, lectura de código de barras y contenido descargable. Y **niveles de exigencia legal distintos**: desde datos de baja sensibilidad hasta datos de salud y de menores de edad, que es el caso más exigente que trata la Ley 29733.

## Qué contiene cada ficha

| Sección | Para qué sirve |
|---|---|
| **1. El problema** | El dolor real y el segmento. Sin esto, lo demás es una ocurrencia |
| **2. Por qué tiene que ser una app** | La pregunta de cierre de la Semana 01, y la que más propuestas hunde |
| **3. Alcance del semestre** | Los cinco sprints. Lo que **cabe**, no lo que sería ideal |
| **4. Modelo de dominio** | Las entidades mínimas |
| **5. Datos personales y permisos** | Determina el trabajo de las Semanas 08 a 11 |
| **6. API simulada** | El contrato, para no depender de un servicio externo |
| **7. Product Backlog semilla** | 25 historias en CSV, listas para refinar en el Taller 03 |

## La pregunta que decide su propuesta

> **¿Por qué su idea tiene que ser una app y no una página web?**

Si la respuesta no nombra una **capacidad propia del móvil** —notificación push, ubicación en segundo plano, cámara con coordenada, funcionamiento sin conexión, sensores— la propuesta se reformula esa misma semana. No es un capricho: una app que podría ser una web no justifica un semestre de desarrollo móvil, y no da evidencia del atributo que el curso mide.

Los diez ejemplos responden esa pregunta en su sección 2. Léala antes de proponer la suya.

## El backlog semilla, y qué hacer con él

Cada dominio trae **25 historias en `backlog-semilla.csv`**, cinco por sprint, con épica, puntos, riesgo y marca de dato personal.

**No es el backlog final.** Es el punto de partida para que el Taller 03 no empiece en cero. En ese taller el equipo:

1. Aplica **INVEST** a cada historia y reescribe las que no lo cumplen
2. **Divide** toda historia de 13 puntos o más
3. Reestima con **Planning Poker** — los puntos del CSV son una referencia, no una verdad
4. Escribe los **criterios de aceptación en Gherkin**, que en el CSV están vacíos a propósito
5. **Ordena por valor y riesgo**, no por el número de historia
6. Añade los **cuatro escenarios de privacidad** a toda historia marcada con dato personal

> Si su equipo propone una app propia, use la estructura del CSV como formato y construya sus propias 25 historias. El formato es obligatorio; el contenido es suyo.

## Regenerar

```bash
cd CATALOGO-APPS
python3 generar_fichas.py
```

Solo requiere Python 3.8 o superior, sin librerías externas.

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
