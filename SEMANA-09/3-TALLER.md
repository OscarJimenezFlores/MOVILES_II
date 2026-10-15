[Semana 09](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · **Taller de laboratorio**

# Taller de laboratorio 09 · Inventario de datos, minimización, política de privacidad y consentimiento

**SI-988 · Soluciones Móviles II** · Semana 09 · Sesión 2 en laboratorio · calificación **procedimental**

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

---

## Qué entregas

| | |
|---|---|
| **Archivo** | `SI988-S09-TALLER-Grupo<N>.pdf` |
| **Plantilla obligatoria** | [SI988-PLANTILLA-TALLER.docx](../PLANTILLAS/SI988-PLANTILLA-TALLER.docx) |
| **Formato** | PDF exportado desde la plantilla en Word, con la carátula de la UPT, el índice actualizado y las capturas numeradas |
| **Qué va dentro** | Las secciones de la plantilla. La **5. Resultados y evidencias** se califica contra la tabla de resultados esperados de esta guía, y **cada resultado necesita la evidencia que lo demuestre**. No se copian de aquí los objetivos, la duración ni los resultados de aprendizaje |
| **Dónde se sube** | Aula virtual, tarea «Taller · Semana 09» |
| **Cuándo vence** | Según lo programado en el aula virtual |

> No se califica un informe entregado en `.docx`, sin carátula, sin los códigos de los integrantes o con resultados declarados sin evidencia.

---

El avance de Sprint 3 lo ejecuta el equipo fuera de la sesión.

## 1. Información sobre el evento práctico

### 1.1. Título del evento práctico

Implementación de las medidas de privacidad de la aplicación — auditoría de los datos que recogen las dependencias, aplicación de la minimización, redacción de la política de privacidad, implementación del consentimiento granular con registro, y de la pantalla de derechos ARCO con eliminación de cuenta.

### 1.2. Objetivos

- **Auditar las dependencias** para descubrir qué datos recogen sin que el equipo lo sepa.
- Construir el **registro de actividades de tratamiento** de la aplicación.
- Aplicar la **minimización**. Eliminar del código la recolección de datos innecesarios.
- Redactar la **política de privacidad** y publicarla en una URL accesible.
- Implementar el **consentimiento granular por finalidad**, con registro demostrable.
- Implementar la **pantalla de privacidad** con acceso, exportación y **eliminación de cuenta**.
- Completar las **declaraciones de las tiendas** en borrador.

### 1.3. Resultados de Aprendizaje (RA)

- **RA1** Desarrolla la geolocalización en una app móvil.
- **RA2** Implementa y gestiona los permisos de geolocalización en una app móvil.

### 1.4. Recursos

| Recurso | Detalle |
|---|---|
| **Ley 29733** y **D. S. 016-2024-JUS** | https://www.gob.pe/institucion/anpd |
| **RGPD** | https://gdpr-info.eu/ |
| **OWASP MASVS-PRIVACY** | https://mas.owasp.org/MASVS/ |
| **Google Play — Data safety** | https://support.google.com/googleplay/android-developer/answer/10787469 |
| **Apple — App privacy details** | https://developer.apple.com/app-store/app-privacy-details/ |
| **MobSF** (Docker) | Análisis estático del artefacto: https://mobsf.github.io/docs/ |
| **mitmproxy** | Verificación del tráfico real de la app |
| GitHub Pages o similar | Publicación de la política de privacidad |

### 1.5. Seguridad

> **Dónde se trabaja.** El taller se hace en el **laboratorio de la universidad, sobre el emulador**. Cuando un escenario no se reproduce fielmente en el emulador, la verificación en un teléfono real la hace el equipo **fuera de la sesión** y adjunta el video como anexo. Ningún resultado del taller depende de tener un teléfono en clase.

1. El inventario de datos **es en sí mismo información sensible**. Describe dónde reside cada dato de los usuarios. Se guarda en el repositorio privado.
2. **No se usan datos personales reales en pruebas.** Se generan datos sintéticos.
3. Si durante la auditoría se descubre que la app envía datos no declarados, **se corrige antes de continuar**. Publicar así sería una infracción.
4. La política de privacidad publicada debe ser **veraz**. Un documento que declara prácticas que la app no cumple agrava la infracción en lugar de protegerla.

---

## 2. Procedimiento o Metodología

### Paso A — Auditar lo que la app realmente envía

**A.1 — Auditoría de dependencias.** Qué recoge cada biblioteca:

```bash
# Inventario de dependencias del proyecto
<comando del stack: ./gradlew dependencies | flutter pub deps | npm ls --all> > docs/privacidad/dependencias.txt

# Análisis estático del artefacto con MobSF
docker run -d --name mobsf -p 127.0.0.1:8000:8000 opensecurity/mobile-security-framework-mobsf:latest
# Se sube el .apk generado y se revisan las secciones:
#   · Permisos declarados vs. usados
#   · Trackers detectados
#   · Dominios y URL embebidas
#   · Cadenas sensibles
```

`docs/privacidad/AUDITORIA_DEPENDENCIAS.csv`:

| Dependencia | Para qué la usamos | **Qué datos recoge por su cuenta** | ¿Los envía a un tercero? | ¿A qué país? | ¿Es necesaria? | Decisión |
|---|---|---|---|---|---|---|
| Biblioteca de reporte de errores | Diagnóstico de fallos | Identificador de dispositivo, modelo, versión del sistema, traza | Sí | EE. UU. | Sí | Se mantiene · se declara · **se anonimiza el identificador** |
| Biblioteca de análisis de uso | Métricas del producto | Identificador de usuario, eventos, ubicación aproximada | Sí | EE. UU. | Revisar | **Se desactiva la recolección de ubicación** |
| Biblioteca de mapas | Mostrar el mapa | Consultas de teselas con coordenadas | Sí | Variable | Sí | Se mantiene · se declara |

**A.2 — Verificación del tráfico real** con mitmproxy. La auditoría estática dice qué **puede** enviar; el tráfico dice qué **envía**:

| Verificación | Resultado |
|---|---|
| Dominios contactados por la app en 10 minutos de uso | Lista completa |
| **Dominios no esperados** | ¿Cuáles y de qué dependencia provienen? |
| Datos enviados a cada dominio | ¿Coinciden con lo declarado? |
| ¿Se envía ubicación a algún servicio de análisis? | Si sí, **se corrige** |
| ¿Todo el tráfico es HTTPS? | Sin excepciones |

> **Resultado esperado del laboratorio.** Casi todos los equipos descubren **al menos un dato que envían sin saberlo**. Encontrarlo y corregirlo es el objetivo.

### Paso B — Registro de tratamiento y minimización

`docs/privacidad/REGISTRO_TRATAMIENTO.csv`:

| id | Dato | Categoría | ¿Sensible? | **Base legal** | Finalidad | Origen | Almacenamiento local | Almacenamiento remoto | **País del servidor** | Encargados | Retención | Medidas de seguridad | ¿Se declara en las tiendas? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D-01 | Correo electrónico | Identificación | No | Ejecución de contrato | Autenticación y notificaciones | Registro | Almacenamiento seguro | Base de datos del backend | | — | Hasta eliminar la cuenta | Cifrado en tránsito y en reposo, control de acceso | Sí |
| D-02 | Ubicación precisa | Localización | No (**pero puede inferir sensibles**) | Consentimiento | Mostrar puntos cercanos | Sensor | **No se almacena** | **No se envía** | — | — | **En memoria, durante la sesión** | Procesamiento local | Sí |
| D-03 | Foto de comprobante | Contenido | No | Ejecución de contrato | Evidencia de entrega | Cámara | Caché temporal | Almacenamiento del backend | | — | 90 días | Cifrado, URL firmada de acceso temporal | Sí |
| D-04 | Identificador de dispositivo | Técnico | No | Interés legítimo | Diagnóstico de fallos | Sistema | — | Servicio de reporte de errores | EE. UU. | Proveedor del servicio | 90 días | Anonimizado | Sí |

**Aplicación de la minimización** —cambios concretos en el código:

| Antes | Después | Justificación |
|---|---|---|
| Se enviaba la ubicación precisa al backend en cada consulta | **Se procesa en el dispositivo**; al backend solo se envía el identificador de la zona | **Decisión 3.** El dato no sale del dispositivo |
| Se guardaba el historial completo de ubicaciones | **No se guarda** | **Decisión 1.** No es necesario para la función |
| El servicio de análisis recibía la ubicación | **Desactivada** esa recolección | **Decisión 6.** El servicio no la necesita |
| Se pedía la fecha de nacimiento en el registro | **Se pide solo si el usuario activa una función que la requiere** | Decisión 1 y 2 |
| Las fotos se conservaban indefinidamente | **Depuración automática a los 90 días** | Decisión 4 |

### Paso C — Política de privacidad y consentimiento

**C.1 — Política de privacidad** (`docs/privacidad/POLITICA_PRIVACIDAD.md`), publicada en URL accesible. Estructura mínima:

```markdown
# Política de Privacidad de <app>
Versión <n> · Última actualización: <fecha>

## 1. Quiénes somos
Responsable del tratamiento, con datos de contacto y correo de privacidad.

## 2. Qué datos recogemos y para qué
| Dato | Para qué lo usamos | Base legal | Cuánto lo conservamos |
(tabla derivada del registro de tratamiento — en lenguaje claro, no jurídico)

## 3. Qué NO recogemos
Declaración explícita de lo que la app no recoge. Genera confianza y es verificable.

## 4. Con quién compartimos
Lista de encargados del tratamiento, para qué y en qué país están sus servidores.

## 5. Transferencia internacional
Si aplica: qué datos salen del Perú, hacia dónde y con qué garantías.

## 6. Tus derechos
Cómo ejercer acceso, rectificación, cancelación y oposición **desde la propia app**,
y el plazo de respuesta.

## 7. Cómo protegemos tus datos
Medidas técnicas y organizativas, en lenguaje comprensible.

## 8. Menores de edad
Si la app no se dirige a menores, declararlo. Ambas tiendas lo revisan.

## 9. Cambios en esta política
Cómo se comunican y desde cuándo rigen.

## 10. Contacto y reclamos
Correo del responsable y referencia a la Autoridad Nacional de Protección de
Datos Personales para presentar un reclamo.
```

**C.2 — Consentimiento granular con registro demostrable.**

```
// Finalidades SEPARADAS: el usuario consiente cada una por su cuenta
enum class Finalidad {
  ESENCIAL,              // no requiere consentimiento: es necesario para el servicio
  UBICACION_CERCANOS,    // consentimiento
  ANALITICA_USO,         // consentimiento — POR DEFECTO DESACTIVADO
  COMUNICACIONES,        // consentimiento — POR DEFECTO DESACTIVADO
}

// El registro DEMOSTRABLE del consentimiento
@Entity
data class RegistroConsentimiento(
  @PrimaryKey val id: String,
  val finalidad: Finalidad,
  val otorgado: Boolean,
  val momentoUtc: Instant,
  val versionPolitica: String,      // ← a QUÉ texto consintió
  val versionApp: String,
  val metodo: String,               // "pantalla de bienvenida" | "ajustes de privacidad"
)

// Pantalla de consentimiento — REGLAS
//  · Ninguna casilla premarcada salvo la ESENCIAL, que se explica y no se puede desactivar
//  · Un interruptor por finalidad, con su explicación en una línea
//  · Enlace visible a la política completa
//  · Botones equivalentes: "Aceptar todo" y "Solo lo esencial" con el MISMO peso visual
//  · Revocable en cualquier momento desde Ajustes > Privacidad
```

> **La igualdad de peso visual entre «Aceptar todo» y «Solo lo esencial» no es estética**. Un botón destacado frente a otro apagado convierte el consentimiento en inducido, y eso lo invalida.

**C.3 — Pantalla de privacidad con derechos ARCO.**

| Opción | Qué hace | Requisito |
|---|---|---|
| **Ver mis datos** | Muestra qué datos tiene la organización sobre el usuario | Derecho de acceso |
| **Descargar mis datos** | Exporta en formato legible por máquina (JSON o CSV) | Acceso y portabilidad |
| **Corregir mis datos** | Edición de los datos rectificables | Rectificación |
| **Preferencias de privacidad** | Los interruptores por finalidad, revocables | Oposición |
| **Eliminar mi cuenta** | **Elimina la cuenta y sus datos**, con confirmación y explicación de qué se conserva por obligación legal | Cancelación · **exigido por ambas tiendas** |

### Paso D — Declaraciones de las tiendas

`docs/privacidad/DECLARACION_TIENDAS.md`, en borrador para la Semana 16:

| Categoría de dato | ¿Se recoge? | ¿Se comparte? | Finalidad | ¿Opcional? | ¿Se cifra en tránsito? | ¿El usuario puede solicitar su eliminación? |
|---|---|---|---|---|---|---|
| Ubicación aproximada | | | | | | |
| Ubicación precisa | | | | | | |
| Correo electrónico | | | | | | |
| Fotos | | | | | | |
| Identificadores de dispositivo | | | | | | |
| Datos de diagnóstico de fallos | | | | | | |
| Interacciones con la app | | | | | | |

> **Verificación cruzada obligatoria.** La declaración debe coincidir con **el registro de tratamiento** y con **el tráfico observado en mitmproxy**. Las tres fuentes deben decir lo mismo. Si difieren, la app no está lista para publicarse.

### Trabajo del equipo fuera de la sesión — Sprint 3

> Lo que no alcance a completarse en la sesión lo ejecuta el equipo durante la semana, y llega al siguiente taller con el incremento listo. El docente lo revisa en el repositorio y en el tablero, no en clase.

**Sprint 3 Planning** — Sprint Goal orientado a privacidad y seguridad, con las historias marcadas en la Semana 03. Luego, el equipo continúa el desarrollo fuera de la sesión.

---

### Paso E — Validar y corregir

El resultado no vale por estar hecho, sino por resistir una comprobación. Se ejecutan estas tres y **se corrige lo que falle antes de cerrar la sesión**.

1. Volver a capturar el tráfico con el proxy después de las correcciones y comprobar que la lista de dominios contactados coincide con la declarada.
2. Verificar que el consentimiento es **granular por finalidad**, sin casillas premarcadas y con botones de igual peso visual.
3. Comprobar que la sección «Qué NO recogemos» de la política es veraz contrastándola contra el registro de tratamiento.

> Lo que no se pueda corregir hoy se anota en la sección **Problemas y mejoras** de la evidencia, con lo que faltó y por qué. Un resultado parcial documentado con honestidad vale más que uno declarado sin prueba.

### Paso F — Registrar la evidencia y cerrar

Se versiona lo producido, se anota la URL de cada resultado y se responde en dos frases la pregunta de transferencia — **qué riesgo correría una organización real si esto se hiciera mal**.

---

## 3. Resultados

> **Evidencia obligatoria en GitHub.** Todo resultado de este taller se versiona en el repositorio del equipo. El informe **no consigna capturas sueltas**. Consigna la **URL** del artefacto en GitHub. Una captura no permite verificar autoría, fecha ni contenido; un enlace sí.
>
> | Qué se entrega | Dónde vive | Qué se escribe en el informe |
> |---|---|---|
> | Código y archivos de configuración | Rama del taller, fusionada a `develop` vía Pull Request | URL del Pull Request |
> | Documentos y matrices | `docs/`, en formato de texto versionable | URL del archivo en la rama |
> | Capturas y videos que el taller exija | `docs/evidencias/S09/` | URL del archivo |
> | Salida de comandos | `docs/evidencias/S09/salidas/*.txt` | URL del archivo |
>
> **Etiqueta del taller.** Al cerrar el taller se crea la etiqueta `taller-09` sobre el commit entregado:
>
> ```bash
> git tag -a taller-09 -m "Taller 09 · SI988"
> git push origin taller-09
> ```
>
> La URL que se consigna en el informe apunta a esa etiqueta:
> `https://github.com/<organizacion>/<repositorio>/tree/taller-09`
>
> **El informe es lo que se califica; el repositorio es lo que lo prueba.** Cada resultado de la sección 3 del informe lleva la URL con la que se verifica, y **un resultado sin su URL se califica como no logrado**, por bien redactado que esté. Lo que no se puede abrir no se puede dar por hecho.

### 3.1. Los tres resultados que se califican

Son los que la rúbrica evalúa. El resto de la lista tiene que existir, pero no se califica fila por fila.

| Resultado | Qué demuestra | Dónde está |
|---|---|---|
| **El dato que se enviaba sin saberlo** | Detectado en el tráfico real, corregido, con el antes y el después | Capturas de mitmproxy y *commits* |
| **El registro de tratamiento** | Las catorce columnas, coincidente con el tráfico observado | `REGISTRO_TRATAMIENTO.csv` |
| **El consentimiento granular** | Por finalidad, sin premarcados, con registro demostrable y versión de la política | Demostración y base de datos |

### 3.2. Lista de comprobación del taller

Todo esto debe existir al cerrar la sesión.

| # | Resultado esperado | Verificación |
|---|---|---|
| 1 | Auditoría de dependencias con **qué recoge cada una** | `AUDITORIA_DEPENDENCIAS.csv` |
| 2 | Análisis con MobSF ejecutado, con trackers y dominios identificados | Reporte |
| 3 | **Tráfico real verificado con mitmproxy**, con la lista completa de dominios contactados | Capturas |
| 4 | **Al menos un dato enviado sin saberlo, detectado y corregido** | Antes y después |
| 5 | Registro de actividades de tratamiento con las 14 columnas | `REGISTRO_TRATAMIENTO.csv` |
| 6 | **Al menos cuatro cambios de minimización aplicados al código** | Tabla antes/después y *commits* |
| 7 | **Al menos un dato procesado localmente** que antes se enviaba | Código |
| 8 | Política de retención con **depuración automática** implementada | Código |
| 9 | Política de privacidad con las 10 secciones, publicada en URL accesible | URL |
| 10 | Sección «Qué NO recogemos» presente y veraz | Política |
| 11 | Consentimiento **granular por finalidad**, sin casillas premarcadas | Demostración |
| 12 | **Botones de igual peso visual**; analítica y comunicaciones desactivadas por defecto | Captura |
| 13 | **Registro demostrable del consentimiento**, con versión de la política | Base de datos y código |
| 14 | Pantalla de privacidad con las cinco opciones, incluida **eliminación de cuenta** | Demostración |
| 15 | Declaración de las tiendas en borrador, **coincidente con el registro y con el tráfico** | Verificación cruzada |
| 16 | Sprint 3 planificado con Sprint Goal de privacidad y seguridad | Tablero |

## Rúbrica procedimental (20 puntos)

Se aplica sobre el informe entregado y la evidencia enlazada en el repositorio. **Cada criterio se califica de forma independiente.**

| Criterio | 4 — Logrado | 2 — En proceso | 0 — Insuficiente |
|---|---|---|---|
| **Auditar lo que la app realmente envía** | Completo y correcto, con la evidencia que lo respalda | Completo con errores menores, o correcto pero sin toda la evidencia | Incompleto, o entregado sin ejecutar |
| **Política de privacidad y consentimiento** | Completo y correcto, con la evidencia que lo respalda | Completo con errores menores, o correcto pero sin toda la evidencia | Incompleto, o entregado sin ejecutar |
| **Evidencia verificable en el repositorio** | Cada resultado tiene su URL sobre la etiqueta `taller-NN`, y el enlace abre lo que dice | La mayoría tiene URL; alguna evidencia es una captura suelta | Se declaran resultados sin enlace, o el enlace no corresponde |
| **Rigor técnico de la implementación** | El código compila, las pruebas pasan y el análisis estático sale limpio | Compila y funciona, con avisos del análisis sin resolver | No compila, o se entregó sin ejecutar |
| **La evidencia entregada** | Las secciones de la plantilla completas; los resultados se sustentan con la evidencia enlazada | Secciones completas con sustento parcial | Faltan secciones o los resultados se afirman sin evidencia |

| Puntaje | Equivalencia |
|---|---|
| 18 – 20 | Destacado |
| 14 – 17 | Logrado |
| 6 – 13 | En proceso |
| 0 – 5 | Insuficiente |

> **Un resultado declarado sin evidencia enlazada no se califica**, aunque el trabajo se haya hecho. La tabla de la sección 3.1 es la lista de cotejo; esta rúbrica es lo que determina la nota.

## 4. Conclusiones

Mínimo tres. Líneas argumentales esperadas:

1. La auditoría del tráfico real revela lo que las dependencias envían sin que el equipo lo sepa; desconocerlo no exime de responsabilidad ante la autoridad ni ante la tienda, porque el responsable es quien publica la app.
2. La medida de privacidad más eficaz es no recoger el dato, y la segunda es procesarlo en el dispositivo. Un dato que nunca sale no puede filtrarse, no requiere garantías de transferencia y no aparece en la etiqueta de la tienda.
3. Un consentimiento con casillas premarcadas o con botones de peso visual desigual es un consentimiento inducido, y por tanto inválido; la igualdad visual entre aceptar y rechazar es un requisito, no una preferencia de diseño.

## 5. Referencias Bibliográficas

- Ley 29733, Ley de Protección de Datos Personales (Perú). https://www.gob.pe/institucion/congreso-de-la-republica/normas-legales/243470-29733
- Decreto Supremo 016-2024-JUS, Reglamento de la Ley 29733, vigente. https://www.gob.pe/institucion/anpd
- Autoridad Nacional de Protección de Datos Personales. https://www.gob.pe/institucion/anpd
- Reglamento General de Protección de Datos (UE) 2016/679. https://gdpr-info.eu/
- OWASP (*Open Worldwide Application Security Project*) Foundation. *MASVS-PRIVACY*. https://mas.owasp.org/MASVS/
- OWASP Foundation. *MASTG — pruebas de privacidad*. https://mas.owasp.org/MASTG/
- Google Play. *Provide information for Google Play's Data safety section*. https://support.google.com/googleplay/android-developer/answer/10787469
- Apple. *App privacy details on the App Store*. https://developer.apple.com/app-store/app-privacy-details/
- Google. *Android privacy best practices*. https://developer.android.com/privacy-and-security/best-practices
- Cavoukian, A. *Privacy by Design: The 7 Foundational Principles*. https://iapp.org/resources/article/privacy-by-design-the-7-foundational-principles/
- MobSF. *Mobile Security Framework documentation*. https://mobsf.github.io/docs/

## 6. Anexos

- `anexo_A_auditoria_dependencias.xlsx`
- `anexo_B_mobsf.pdf` — reporte del análisis estático
- `anexo_C_trafico_real.pdf` — dominios contactados y su análisis
- `anexo_D_registro_tratamiento.xlsx` — **repositorio privado**
- `anexo_E_politica_privacidad.pdf` y su URL
- `anexo_F_consentimiento.mp4` — flujo completo demostrado
- `anexo_G_declaracion_tiendas.xlsx`

---

---

[Semana 09](README.md) · [Teoría](1-TEORIA.md) · [Dinámica de aula](2-DINAMICA.md) · **Taller de laboratorio**

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
