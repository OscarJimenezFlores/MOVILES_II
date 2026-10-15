[Semana 10](README.md) · [Teoría](1-TEORIA.md) · **Dinámica de aula** · [Taller de laboratorio](3-TALLER.md)

# Dinámica de aula · El artefacto que habla

**SI-988 · Soluciones Móviles II** · Semana 10 · Actividad en aula, **dentro de la sesión de teoría** · calificación **cognitiva**

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

---

## Qué entregas

| | |
|---|---|
| **Archivo** | `SI988-S10-DINAMICA-Grupo<N>.pdf` |
| **Plantilla obligatoria** | [SI988-PLANTILLA-DINAMICA.docx](../PLANTILLAS/SI988-PLANTILLA-DINAMICA.docx) |
| **Formato** | PDF exportado desde la plantilla en Word, con la carátula de la UPT y los apellidos, nombres y códigos de todos los integrantes |
| **Qué va dentro** | Lo que el grupo resolvió en aula. Las tablas de la sección **Producto** van completas, con los textos redactados, y cada decisión va justificada |
| **Dónde se sube** | Aula virtual, tarea «Dinámica · Semana 10» |
| **Cuándo vence** | Según lo programado en el aula virtual. La tabla se resuelve en aula; el PDF se formatea y se sube después |
| **Exposición** | En la ronda de cierre de **esta misma sesión**. El grupo **lee y explica su resultado** ante el aula, con el documento a la vista. No se usan diapositivas |

> No se califica un trabajo entregado en `.docx`, sin carátula, sin los códigos de los integrantes o con las tablas del producto vacías.

---

## Consigna

> **«El artefacto que habla»**
> Cada equipo recibe el **artefacto de una aplicación real vulnerable** (una app intencionalmente vulnerable de la comunidad; ver **Material de trabajo**) y debe **encontrar todo lo que revela** — secretos embebidos, datos en texto claro, tráfico sin cifrar y errores criptográficos, clasificando cada hallazgo por categoría MASVS.

| | |
|---|---|
| **Su papel** | **Analista de seguridad** con el artefacto en la mano y sin acceso al código fuente |
| **Misión** | Encontrar todo lo que el artefacto revela y clasificarlo por categoría MASVS |
| **Restricción** | **Cada hallazgo se prueba con la salida del comando que lo encontró.** Una sospecha sin salida no se cuenta |

## Producto

**Producto 1 — Hallazgos.**

| # | Hallazgo | Dónde se encontró | **Categoría MASVS** | Qué permite hacer a un atacante | Severidad |
|---|---|---|---|---|---|

**Producto 2 — Corrección y autoevaluación.** Para los **tres hallazgos más graves**. La corrección concreta. Más la **autoevaluación**. ¿Cuál de esos hallazgos existe hoy en su propia app?

> **Dónde va.** Este producto se presenta en la **sección 2 de la [plantilla de dinámica](../PLANTILLAS/SI988-PLANTILLA-DINAMICA.docx)**, «El producto». No se copia la consigna ni la teoría. Solo el resultado y lo que lo sostiene.

## Ejemplo resuelto

*El caso de este ejemplo es distinto del que le toca a tu grupo. Sirve para que veas el nivel de detalle que se espera, no para copiarlo.*

**Dos hallazgos bien documentados.** El artefacto del ejemplo es de otra aplicación.

*Hallazgos*

| # | Hallazgo | Dónde se encontró | **Categoría MASVS** | Qué permite hacer a un atacante | Severidad |
|---|---|---|---|---|---|
| 1 | Clave de la interfaz de programación del proveedor de mapas embebida en texto claro | `res/values/strings.xml`, cadena `maps_api_key`, recuperada al descomprimir el artefacto sin ninguna herramienta especial | **MASVS-STORAGE** y **MASVS-CRYPTO** | Consumir el servicio de mapas con cargo a la cuenta del equipo. Con una clave sin restricción por aplicación, el gasto es ilimitado | **Crítica** |
| 2 | El token de sesión se guarda en las preferencias compartidas sin cifrar | `shared_prefs/session.xml`, legible en un dispositivo con acceso de superusuario | **MASVS-STORAGE** | Copiar el token y actuar como el usuario desde otro dispositivo hasta que expire | Alta |
| 3 | El tráfico hacia el servicio de análisis viaja por HTTP sin cifrar | Captura con proxy interceptor. La configuración de seguridad de red permite texto claro para ese dominio | **MASVS-NETWORK** | Leer y modificar los eventos enviados en una red no confiable | Media |

*Corrección de los tres más graves*

| # | Corrección concreta |
|---|---|
| 1 | La clave sale del artefacto. Las peticiones al proveedor de mapas pasan por el backend propio, que guarda la clave como variable de entorno del servidor. Además, se restringe la clave por huella del certificado de la aplicación y se rota la comprometida. **Ofuscar la clave no es una corrección:** sigue estando en el artefacto y se recupera con el mismo esfuerzo |
| 2 | El token se guarda en el almacén de claves del sistema —Keystore en Android, Keychain en iOS— y no en preferencias. Se reduce la vigencia del token de acceso a 15 minutos y se usa token de renovación |
| 3 | Se elimina la excepción de texto claro de la configuración de seguridad de red y se exige HTTPS para todos los dominios. Si el proveedor de análisis no ofrece HTTPS, se cambia de proveedor |

*Autoevaluación*

| Pregunta | Respuesta honesta |
|---|---|
| ¿Cuál de estos hallazgos existe hoy en nuestra propia app? | El hallazgo 2. Nuestro token está en preferencias compartidas sin cifrar. Lo verificamos extrayendo el artefacto de depuración y leyendo el archivo |
| ¿Qué haremos y cuándo? | Migrar al almacén de claves del sistema en el Sprint 4. Queda registrado como deuda técnica con identificador DT-07 |

**Por qué la autoevaluación puntúa más que el análisis.** Encontrar fallos en el artefacto de otro es un ejercicio. Reconocer que el mismo fallo está en la app propia, verificarlo y comprometerse a corregirlo es lo que la rúbrica premia. Un equipo que declara «ninguno de estos hallazgos existe en nuestra app» sin mostrar cómo lo verificó no se califica.

**La diferencia entre aprobar y no aprobar.**

| Así no | Así sí |
|---|---|
| «Se encontró una clave de API en el código.» | «`res/values/strings.xml`, cadena `maps_api_key`, recuperada al descomprimir el artefacto sin herramientas especiales.» |
| «Corrección: ofuscar la clave.» | «La clave sale del artefacto. Las peticiones pasan por el backend, que la guarda como variable de entorno. Ofuscar no corrige: sigue ahí.» |
| «Categoría: seguridad.» | «MASVS-STORAGE y MASVS-CRYPTO.» |

## Reglas

- Cada hallazgo debe indicar **dónde exactamente** se encontró — archivo, ruta, cadena.
- Cada uno debe clasificarse en su **categoría MASVS**.
- **Obligatorio** responder la autoevaluación con honestidad. Es el insumo del laboratorio.
- La exposición es la ronda de cierre de esta misma sesión. El grupo **lee y explica su resultado**. No se usan diapositivas.

## Rúbrica cognitiva (20 puntos)

| Criterio | 5 | 3 | 1 |
|---|---|---|---|
| **Cantidad y precisión** | Al menos 6 hallazgos, con su ubicación exacta | 4 o 5 hallazgos | Menos de 4, o sin ubicación |
| **Clasificación MASVS** | Categoría correcta en todos | En la mayoría | Clasificación incorrecta |
| **Impacto** | Describe qué permite hacer al atacante, concretamente | Impacto general | «Es inseguro» |
| **Autoevaluación** | Honesta, identifica los propios problemas | Parcial | Declara no tener ninguno sin verificarlo |

## Anexo · Material de trabajo

Trabaja sobre una aplicación **intencionalmente vulnerable**, de las que la comunidad publica para practicar. Son legales, gratuitas y están hechas para esto.

**Aplicaciones admitidas**

| Aplicación | Plataforma | Dónde obtenerla |
|---|---|---|
| **OWASP (*Open Worldwide Application Security Project*) MASTG Hacking Playground** | Android e iOS | https://github.com/OWASP/MASTG-Hacking-Playground |
| **InsecureBankv2** | Android | https://github.com/dineshshetty/Android-InsecureBankv2 |
| **DIVA Android** | Android | https://github.com/payatu/diva-android |
| **OWASP iGoat** | iOS | https://github.com/OWASP/iGoat-Swift |

Se asigna una por equipo en la sesión de laboratorio de la Semana 10, para que los hallazgos no se repitan.

> **Regla de alcance que no se negocia.** El análisis se hace **solo** sobre la aplicación asignada, en el dispositivo o emulador del laboratorio. Analizar la aplicación de un tercero sin su autorización escrita constituye acceso no autorizado, tipificado en la Ley 30096. No se analiza la app de otra empresa, ni la de un compañero sin su permiso por escrito.

**Qué vas a buscar y con qué**

| Qué se busca | Cómo se busca |
|---|---|
| Secretos embebidos | Descomprimir el artefacto y revisar los recursos de cadenas, los archivos de configuración y el código descompilado |
| Datos en texto claro | Extraer el almacenamiento privado de la app tras usarla, y revisar preferencias, base de datos local y archivos |
| Tráfico sin cifrar | Proxy interceptor con el certificado instalado, y revisión de la configuración de seguridad de red del artefacto |
| Errores criptográficos | Buscar algoritmos obsoletos, claves fijas en el código y vectores de inicialización constantes |

**Las categorías MASVS con las que clasificas cada hallazgo**

| Categoría | Qué cubre |
|---|---|
| MASVS-STORAGE | Almacenamiento de datos en el dispositivo |
| MASVS-CRYPTO | Uso correcto de la criptografía |
| MASVS-AUTH | Autenticación y gestión de sesión |
| MASVS-NETWORK | Seguridad de las comunicaciones |
| MASVS-PLATFORM | Interacción con la plataforma y con otras apps |
| MASVS-CODE | Calidad del código y dependencias |
| MASVS-RESILIENCE | Resistencia a la manipulación del artefacto |
| MASVS-PRIVACY | Tratamiento de datos personales |

**La parte que más puntúa.** La autoevaluación final sobre tu propia app. Hay que **verificarlo**, no suponerlo. Extrae el artefacto de depuración de tu app y revisa lo mismo que revisaste en la vulnerable.

---

---

[Semana 10](README.md) · [Teoría](1-TEORIA.md) · **Dinámica de aula** · [Taller de laboratorio](3-TALLER.md)

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
