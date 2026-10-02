<div align="center">
  <img src="../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Semana 08 · Permisos en Aplicaciones Móviles</h1>

<p align="center">
  <strong>SI-988 · Soluciones Móviles II</strong><br>
  4 horas académicas de 50 min · 100 min de teoría con la dinámica incluida en aula · 100 min de taller en laboratorio
</p>

---

## Datos de la asignatura

| | |
|---|---|
| **Asignatura** | SI-988 · Soluciones Móviles II |
| **Escuela** | Escuela Profesional de Ingeniería de Sistemas |
| **Ciclo** | IX · 04 horas semanales · 04 créditos · Electivo |
| **Prerrequisito** | SI-883 Soluciones Móviles I |
| **Unidad** | II — Geolocalización, seguridad y permisos |
| **Semana** | 08 de 17 |
| **Duración** | 4 horas académicas de 50 min · 100 min de teoría con la dinámica incluida en aula · 100 min de taller en laboratorio |
| **Resultados de aprendizaje** | **RA1** Desarrolla la geolocalización en una app móvil · **RA2** Implementa y gestiona los permisos de geolocalización en una app móvil |
| **Artefacto del proyecto** | **Sprint 2** · flujo completo de permisos con degradación · Incremento |

### Lo que indica el sílabo

**Contenido conceptual.** Permisos en aplicaciones móviles.

**Contenido procedimental.** Gestionar permisos en Android o iOS para acceso a localización, cámara, etc.

## Materiales de esta semana

| | Documento | Qué encontrarás | Dónde y cuánto dura |
|---|---|---|---|
| 1 | **[Teoría](1-TEORIA.md)** | El modelo de permisos y qué protege · Cómo se pide un permiso sin perder al usuario · Degradación de funciones cuando falta el permiso | Aula · 100 min |
| 2 | **[Dinámica de aula](2-DINAMICA.md)** | El flujo que convence, con su material, su ejemplo resuelto y su rúbrica | Aula · dentro de los 100 min de la sesión de teoría |
| 3 | **[Taller de laboratorio](3-TALLER.md)** | Flujo completo de permisos con degradación elegante | Laboratorio · 100 min |

## Ruta de la semana

```mermaid
flowchart LR
    A["<b>Sesión 1 · Aula</b><br/>Teoría · 100 min"]
    B["<b>Dinámica de aula</b><br/>El flujo que convence<br/><i>nota cognitiva</i>"]
    C["<b>Sesión 2 · Laboratorio</b><br/>Flujo completo de permisos con<br/>degradación elegante<br/><i>nota procedimental</i>"]
    D["<b>Entregables</b><br/>de la semana 08"]
    A --> B --> C --> D
    classDef aula fill:#E8F1FB,stroke:#16285C,stroke-width:1px,color:#16285C;
    classDef lab fill:#E9F6F2,stroke:#0F766E,stroke-width:1px,color:#0F4C46;
    classDef ent fill:#FDF2E2,stroke:#B45309,stroke-width:1px,color:#7C3E00;
    class A,B aula;
    class C lab;
    class D ent;
```

## Entregables

| Entregable | Formato y nombre del archivo | Vence |
|---|---|---|
| **Dinámica de aula** · El flujo que convence | PDF desde la [plantilla de dinámica](../PLANTILLAS/SI988-PLANTILLA-DINAMICA.docx) · `SI988-S08-DINAMICA-Grupo<N>.pdf` | Antes de cerrar la sesión de teoría |
| **Informe del taller de laboratorio N.º 08** | PDF en formato EPIS desde la [plantilla de taller](../PLANTILLAS/SI988-PLANTILLA-TALLER.docx) · `SI988-S08-TALLER-Grupo<N>.pdf` | 48 h después del taller |
| Flujo de permisos con degradación verificada | Commit, CI en verde, video de los 8 escenarios | 48 h después del taller |

> Ambos se entregan en **PDF**, con la carátula de la UPT y los códigos de todos los integrantes. Las plantillas obligatorias están en [`PLANTILLAS/`](../PLANTILLAS/).

## Cómo se evalúa

| Criterio | Instrumento | Peso |
|---|---|---|
| Cognitivo | Rúbrica del flujo de permisos + exposición de 10 min en la Semana 09 | 25 % |
| Procedimental | Lista de cotejo de los 14 resultados del laboratorio | 35 % |
| Actitudinal | Aplicación del privilegio mínimo y veracidad de los textos de propósito | 15 % |

## Preparación para la Semana 09

- **Leer.** Ley 29733 y el título sobre medidas de seguridad de su Reglamento, **D. S. 016-2024-JUS**.
- **Leer.** [OWASP MASVS-PRIVACY](https://mas.owasp.org/MASVS/) y las políticas de datos del usuario de ambas tiendas.
- Preparar el **inventario preliminar de datos** que trata la app. Qué recoge, dónde lo guarda y a quién lo envía.
- **Planificar el Sprint 3** e incluir en él las historias de privacidad y seguridad marcadas en la Semana 03.

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
