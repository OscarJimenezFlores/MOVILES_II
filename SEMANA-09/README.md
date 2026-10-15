<div align="center">
  <img src="../Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="../Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Semana 09 · Manejo de Datos Sensibles · Privacidad por Diseño</h1>

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
| **Semana** | 09 de 17 |
| **Duración** | 4 horas académicas de 50 min · 100 min de teoría con la dinámica incluida en aula · 100 min de taller en laboratorio |
| **Resultados de aprendizaje** | **RA1** Desarrolla la geolocalización en una app móvil · **RA2** Implementa y gestiona los permisos de geolocalización en una app móvil |
| **Artefacto del proyecto** | **Sprint 3 Planning** · Inventario de datos · Política de privacidad · Consentimiento |

### Lo que indica el sílabo

**Contenido conceptual.** Manejo de datos sensibles.

**Contenido procedimental.** Controla el manejo de datos sensibles y cumplimiento con normas de seguridad (GDPR).

## Materiales de esta semana

| | Documento | Qué encontrarás | Dónde y cuánto dura |
|---|---|---|---|
| 1 | **[Teoría](1-TEORIA.md)** | Qué es un dato personal y qué lo hace sensible · El marco normativo aplicable · Privacidad por diseño en siete decisiones | Aula · 100 min |
| 2 | **[Dinámica de aula](2-DINAMICA.md)** | El inventario que nadie quiere hacer, con su material, su ejemplo resuelto y su rúbrica | Aula · dentro de los 100 min de la sesión de teoría |
| 3 | **[Taller de laboratorio](3-TALLER.md)** | Inventario de datos, minimización, política de privacidad y consentimiento | Laboratorio · 100 min |

## Ruta de la semana

```mermaid
flowchart LR
    A["<b>Sesión 1 · Aula</b><br/>Teoría · 100 min"]
    B["<b>Dinámica de aula</b><br/>El inventario que nadie<br/>quiere hacer<br/><i>nota cognitiva</i>"]
    C["<b>Sesión 2 · Laboratorio</b><br/>Inventario de datos,<br/>minimización, política de<br/>privacidad y consentimiento<br/><i>nota procedimental</i>"]
    D["<b>Entregables</b><br/>de la semana 09"]
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
| **Dinámica de aula** · El inventario que nadie quiere hacer | PDF desde la [plantilla de dinámica](../PLANTILLAS/SI988-PLANTILLA-DINAMICA.docx) · `SI988-S09-DINAMICA-Grupo<N>.pdf` | Según lo programado en el aula virtual |
| **Informe del taller de laboratorio N.º 09** | PDF en formato EPIS desde la [plantilla de taller](../PLANTILLAS/SI988-PLANTILLA-TALLER.docx) · `SI988-S09-TALLER-Grupo<N>.pdf` | Según lo programado en el aula virtual |
| Política de privacidad publicada y consentimiento implementado | URL + commit | Según lo programado en el aula virtual |

> La dinámica y el informe del taller se entregan en **PDF**, con la carátula de la UPT y los códigos de todos los integrantes. Las plantillas obligatorias están en [`PLANTILLAS/`](../PLANTILLAS/).

## Cómo se evalúa

| Criterio | Instrumento | Peso |
|---|---|---|
| Cognitivo | Rúbrica del inventario + exposición de 10 min en la Semana 10 | 25 % |
| Procedimental | Lista de cotejo de los 16 resultados del laboratorio | 35 % |
| Actitudinal | Veracidad de la política publicada y corrección de lo detectado en la auditoría | 15 % |

## Preparación para la Semana 10

- **Leer.** [OWASP MASVS](https://mas.owasp.org/MASVS/) completo — son pocas páginas — y las categorías MASVS-STORAGE y MASVS-CRYPTO.
- **Leer.** [Android Keystore](https://developer.android.com/privacy-and-security/keystore) y [Apple Keychain](https://developer.apple.com/documentation/security/keychain-services).
- Revisar dónde guarda hoy su app los tokens y los datos del usuario — **es probable que estén en texto claro**.
- Continuar el **Sprint 3**.

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
