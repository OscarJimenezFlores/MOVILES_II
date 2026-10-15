[Semana 09](README.md) · [Teoría](1-TEORIA.md) · **Dinámica de aula** · [Taller de laboratorio](3-TALLER.md)

# Dinámica de aula · El inventario que nadie quiere hacer

**SI-988 · Soluciones Móviles II** · Semana 09 · Actividad en aula, **dentro de la sesión de teoría** · calificación **cognitiva**

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

---

## Qué entregas

| | |
|---|---|
| **Archivo** | `SI988-S09-DINAMICA-Grupo<N>.pdf` |
| **Plantilla obligatoria** | [SI988-PLANTILLA-DINAMICA.docx](../PLANTILLAS/SI988-PLANTILLA-DINAMICA.docx) |
| **Formato** | PDF exportado desde la plantilla en Word, con la carátula de la UPT y los apellidos, nombres y códigos de todos los integrantes |
| **Qué va dentro** | Lo que el grupo resolvió en aula. Las tablas de la sección **Producto** van completas, con los textos redactados, y cada decisión va justificada |
| **Dónde se sube** | Aula virtual, tarea «Dinámica · Semana 09» |
| **Cuándo vence** | Según lo programado en el aula virtual. La tabla se resuelve en aula; el PDF se formatea y se sube después |
| **Exposición** | En la ronda de cierre de **esta misma sesión**. El grupo **lee y explica su resultado** ante el aula, con el documento a la vista. No se usan diapositivas |

> No se califica un trabajo entregado en `.docx`, sin carátula, sin los códigos de los integrantes o con las tablas del producto vacías.

---

## Consigna

> **«El inventario que nadie quiere hacer»**
> Cada equipo construye el **inventario completo de datos personales** de su aplicación — qué recoge, con qué base legal, para qué, dónde reside, a quién se envía, cuánto se conserva y **qué daño causaría su filtración**. Incluye **los datos que recogen sus dependencias de terceros**.

| | |
|---|---|
| **Su papel** | **Responsable de la app** que firma la declaración de datos ante la tienda |
| **Misión** | Inventariar todo dato personal con su base legal, su residencia y el daño que causaría su filtración |
| **Restricción** | **Lo que recogen las dependencias cuenta como propio.** «No sabíamos que el SDK lo enviaba» no es una respuesta ante la tienda |

## Producto

**Producto 1 — Inventario de datos.**

| Dato | ¿Sensible? | **Base legal** | Finalidad declarada | Dónde reside | ¿Se envía a terceros? | Retención | **Daño si se filtra** |
|---|---|---|---|---|---|---|---|

**Producto 2 — Las siete decisiones de privacidad por diseño.** Aplicadas a los **tres datos más sensibles** de la app, con la decisión tomada y su justificación, más la lista de **datos que el equipo decidió NO recoger** y por qué.

> **Dónde va.** Este producto se presenta en la **sección 2 de la [plantilla de dinámica](../PLANTILLAS/SI988-PLANTILLA-DINAMICA.docx)**, «El producto». No se copia la consigna ni la teoría. Solo el resultado y lo que lo sostiene.

## Ejemplo resuelto

*El caso de este ejemplo es distinto del que le toca a tu grupo. Sirve para que veas el nivel de detalle que se espera, no para copiarlo.*

**Dos filas bien resueltas.** La app del ejemplo es un registro de gastos personales.

*Inventario de datos*

| Dato | ¿Sensible? | **Base legal** | Finalidad declarada | Dónde reside | ¿Terceros? | Retención | **Daño si se filtra** |
|---|---|---|---|---|---|---|---|
| Correo electrónico | No | **Ejecución del contrato.** Es el identificador de la cuenta | Autenticar al usuario y recuperar la contraseña | Servidor propio, base de datos cifrada en reposo. En el dispositivo solo el token, no el correo | No | Mientras la cuenta esté activa, más 30 días tras la baja | Bajo por sí solo. Combinado con la contraseña permite tomar la cuenta |
| Fotografía del comprobante | **Sí, potencialmente** | Consentimiento específico, solicitado al adjuntar la primera foto | Adjuntar respaldo al registro de un gasto | Dispositivo, en almacenamiento privado de la app. Copia en servidor propio, cifrada | No | 12 meses, o hasta que el usuario elimine el gasto | **Alto.** Un comprobante puede mostrar el nombre completo, el documento de identidad, la dirección de un local de salud o el detalle de un medicamento. Revela hábitos, ubicación y, en algunos casos, datos de salud |
| Identificador de publicidad del dispositivo | No | **Ninguna base legal aplicable** | *(la recoge la biblioteca de análisis, sin que la app la haya declarado)* | Servidores del proveedor de análisis, fuera del país | **Sí**, el proveedor de análisis | Fuera de nuestro control | Permite correlacionar el uso de esta app con el de otras del mismo dispositivo |

**El hallazgo que nadie espera.** La tercera fila es la razón por la que esta dinámica existe. Las dependencias de terceros recogen datos que el equipo no declaró y a veces ni conoce. Se detecta revisando el tráfico saliente y la documentación de cada biblioteca, no leyendo el propio código.

*Tres de las siete decisiones de privacidad por diseño*

| Decisión | Aplicada al comprobante fotográfico | Justificación |
|---|---|---|
| Minimización | La foto no se sube al servidor salvo que el usuario active «Respaldar mis comprobantes», que viene desactivado | Si el respaldo no es necesario para la función principal, el valor por defecto es no recogerlo |
| Privacidad por defecto | El respaldo en la nube viene **desactivado**, no activado | Un valor por defecto que favorece a la organización y no al usuario es lo que el principio prohíbe |
| Extremo a extremo con eliminación segura | Al eliminar un gasto se borra la foto del dispositivo y se envía la orden de borrado al servidor, con confirmación | Conservar la foto de un gasto eliminado no tiene finalidad que la sustente |

*Datos que el equipo decidió NO recoger*

| Dato | Por qué se descarta |
|---|---|
| Ubicación del gasto | Sería útil para agrupar por zona, pero la ubicación permanente revela dónde vive y trabaja el usuario. El beneficio no compensa el riesgo, y se sustituye por el nombre del comercio escrito a mano |
| Lista de contactos | Se consideró para dividir gastos entre amigos. Se descarta: la función se resuelve con un enlace para compartir, sin acceder a la agenda |
| Identificador de publicidad | Se retira la biblioteca de análisis que lo recogía y se sustituye por una que no lo requiere |

**La diferencia entre aprobar y no aprobar.**

| Así no | Así sí |
|---|---|
| «Foto del comprobante. Sensible: no.» | «Sí, potencialmente. Un comprobante puede mostrar el documento de identidad, la dirección de un local de salud o el detalle de un medicamento.» |
| «Base legal: consentimiento.» *(para todo)* | «Correo: ejecución del contrato. Foto: consentimiento específico. Identificador de publicidad: ninguna base aplicable, y por eso se retira.» |
| «Retención: la necesaria.» | «12 meses, o hasta que el usuario elimine el gasto, con orden de borrado confirmada al servidor.» |

## Reglas

- **Obligatorio** incluir los datos que recogen las bibliotecas de terceros. Hay que revisarlas.
- La base legal debe ser **específica**. «Consentimiento» exige indicar cuándo y cómo se obtiene.
- **Obligatorio** listar al menos **un dato que el equipo decidió no recoger** y el porqué.
- El daño debe describirse **desde la perspectiva de la persona**, no de la empresa.
- La exposición es la ronda de cierre de esta misma sesión. El grupo **lee y explica su resultado**. No se usan diapositivas.

## Rúbrica cognitiva (20 puntos)

| Criterio | 5 | 3 | 1 |
|---|---|---|---|
| **Completitud del inventario** | Incluye datos de terceros y datos inferidos | Incluye los datos propios | Solo los evidentes |
| **Base legal y finalidad** | Específicas y distintas por dato | Correctas de forma general | «Consentimiento» sin detalle |
| **Minimización** | Al menos un dato descartado, con justificación | Menciona la minimización | No la aplica |
| **Análisis del daño** | Desde la perspectiva de la persona, con consecuencia concreta | Daño identificado de forma general | «Riesgo de privacidad» |

---

---

[Semana 09](README.md) · [Teoría](1-TEORIA.md) · **Dinámica de aula** · [Taller de laboratorio](3-TALLER.md)

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
