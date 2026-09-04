<div align="center">
  <img src="Logos/logo_universidad.png" alt="Universidad Privada de Tacna" height="62">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="Logos/logo_escuela_sistemas.jpeg" alt="Escuela Profesional de Ingeniería de Sistemas" height="62">
</div>

<p align="center">
  <strong>Universidad Privada de Tacna</strong><br>
  Facultad de Ingeniería · Escuela Profesional de Ingeniería de Sistemas
</p>

<h1 align="center">Glosario técnico</h1>

<p align="center">
  <strong>SI-988 · Soluciones Móviles II</strong><br>
  Todo término o sigla que aparece en el curso, con su significado
</p>

---

Los términos en inglés se conservan cuando así se usan en el trabajo profesional. Es como los va a encontrar en la documentación, en las ofertas de empleo y en el código de sus compañeros. Traducirlos dificultaría buscarlos.

## Proceso y gestión del proyecto

| Término | Significado |
|---|---|
| **Scrum** | Marco de trabajo para desarrollo iterativo. Define tres roles, cinco eventos y tres artefactos |
| **Sprint** | Periodo fijo de trabajo, en este curso de tres semanas, al final del cual debe existir software funcionando |
| **Product Owner** | Rol responsable del valor del producto y del orden del Product Backlog. Decide **qué** se construye |
| **Scrum Master** | Rol responsable de que el equipo trabaje con eficacia y de remover impedimentos |
| **Developer** | En Scrum, todo integrante que construye el incremento. No solo quien escribe código |
| **Product Backlog** | Lista ordenada de todo lo que el producto podría necesitar. Nunca está completa |
| **Sprint Backlog** | Subconjunto del Product Backlog que el equipo se compromete a terminar en el sprint |
| **Historia de usuario** | Descripción de una necesidad con el formato «Como \<rol\> quiero \<acción\> para \<beneficio\>» |
| **Épica** | Agrupación de historias relacionadas |
| **INVEST** | Criterio de calidad de una historia: **I**ndependiente, **N**egociable, **V**aliosa, **E**stimable, **S**mall (pequeña), **T**esteable |
| **Planning Poker** | Técnica de estimación en la que cada integrante estima en privado y luego se discuten las diferencias |
| **Punto de historia** | Unidad relativa de esfuerzo. No son horas: expresan tamaño comparado con otra historia |
| **Velocidad** | Puntos completados por sprint. Sirve para planificar el siguiente, no para comparar equipos |
| **DoD** | *Definition of Done*. Lista de condiciones que toda historia debe cumplir para considerarse terminada |
| **Daily** | Reunión diaria de 15 minutos del equipo para sincronizarse |
| **Review** | Evento de cierre de sprint donde se muestra el incremento a los interesados |
| **Retrospective** | Evento de cierre de sprint donde el equipo revisa **cómo** trabajó y acuerda una mejora |
| **WIP** | *Work In Progress*. Límite de cuántos elementos pueden estar en una columna del tablero a la vez |
| **Lean Canvas** | Plantilla de una página para formular un modelo de producto en nueve bloques |
| **ADR** | *Architecture Decision Record*. Documento breve que registra una decisión técnica, sus alternativas y sus consecuencias |

## Repositorio e integración continua

| Término | Significado |
|---|---|
| **Repositorio** | El proyecto versionado con Git, alojado en GitHub |
| **Rama** (*branch*) | Línea de trabajo paralela. Cada historia se desarrolla en la suya |
| **Commit** | Cambio registrado en el repositorio, con autor, fecha y mensaje |
| **Pull Request (PR)** | Solicitud de integrar una rama en otra. Es el punto donde otro integrante revisa el código |
| **Merge** | Integración de una rama en otra |
| **Tag** (etiqueta) | Marca fija sobre un commit. En este curso se usa `taller-NN` para señalar la entrega |
| **CI** | *Continuous Integration*. Verificación automática que corre en cada push y cada PR |
| **Pipeline** | La secuencia de pasos que ejecuta la CI: formato, análisis, pruebas, compilación |
| **GitHub Actions** | El servicio que ejecuta el pipeline. Se configura en `.github/workflows/` |
| **GitHub Projects** | El tablero Scrum del equipo, en el mismo repositorio. Obligatorio en este curso |
| **Issue** | Elemento de trabajo en GitHub. Cada historia del backlog es un issue |
| **Conventional Commits** | Convención de mensajes de commit con prefijo: `feat:`, `fix:`, `docs:`, `test:` |

## Arquitectura de la aplicación

| Término | Significado |
|---|---|
| **Capa de dominio** | Entidades y reglas de negocio. No conoce ni la red ni la interfaz |
| **Capa de datos** | Repositorios, fuentes de datos y modelos de transporte |
| **Capa de presentación** | Pantallas y gestión del estado que muestran |
| **Regla de dependencia** | El dominio no depende de nada; las demás capas dependen de él, nunca al revés |
| **Repositorio** (patrón) | Clase que oculta de dónde vienen los datos: red, base local o memoria |
| **Caso de uso** | Una operación del negocio, con un solo propósito. Ejemplo: `ObtenerItems` |
| **DTO** | *Data Transfer Object*. Modelo que refleja el formato del servicio, no el del dominio |
| **Inyección de dependencias** | Entregar a una clase lo que necesita en lugar de que ella lo construya |
| **ViewModel** | Clase que sostiene el estado de una pantalla y sobrevive a la rotación |
| **Estado** | Lo que la pantalla muestra en un momento. En este curso siempre tiene al menos tres: cargando, error y listo |
| **`sealed`** | Modificador que restringe qué subtipos existen. Permite que el compilador exija cubrir todos los casos |
| **`expect` / `actual`** | Mecanismo de Kotlin Multiplatform: `expect` declara qué se necesita, `actual` lo implementa en cada plataforma |
| **`commonMain`** | En KMP, el código compartido por todas las plataformas |
| **`androidMain` / `iosMain`** | En KMP, el código específico de cada plataforma |

## Red y servicios

| Término | Significado |
|---|---|
| **API** | *Application Programming Interface*. El conjunto de operaciones que un servicio expone |
| **REST** | Estilo de API sobre HTTP donde cada recurso tiene su URL y se opera con `GET`, `POST`, `PUT`, `DELETE` |
| **SOAP** | Protocolo de mensajería basado en XML, anterior a REST. Frecuente en sistemas heredados |
| **Endpoint** | La URL concreta donde vive una operación. Ejemplo: `GET /api/productos` |
| **Request / Response** | La petición que envía la app y la respuesta que devuelve el servicio |
| **Body** | El contenido del request o del response. En REST suele ser JSON; en SOAP, XML |
| **Payload** | Los datos útiles que viajan en el body, sin contar cabeceras ni envoltorio |
| **Header** (cabecera) | Metadato de la petición o la respuesta: `Content-Type`, `Authorization`, `Retry-After` |
| **JSON** | Formato de datos en texto, el habitual en APIs REST |
| **XML** | Formato de datos con etiquetas, el que usa SOAP |
| **OpenAPI** | Estándar para describir una API REST en un archivo `.yaml`. Es el contrato |
| **WSDL** | *Web Services Description Language*. El equivalente de OpenAPI para SOAP: describe operaciones, tipos y dirección del servicio |
| **Envelope** (sobre) | La estructura XML fija que SOAP exige alrededor de cada mensaje: `<Envelope><Body>…` |
| **`SOAPAction`** | Cabecera HTTP que indica qué operación del WSDL se está invocando |
| **`soap:Fault`** | El error de SOAP. Viaja dentro del body y **puede llegar con HTTP 200** |
| **Namespace** | Prefijo que identifica a qué vocabulario pertenece un elemento XML |
| **BFF** | *Backend For Frontend*. Servicio intermedio que habla el protocolo del sistema heredado por un lado y REST/JSON con la app por el otro |
| **Mock server** | Servidor de prueba que responde según el contrato, sin lógica real. Permite trabajar sin el servicio verdadero |
| **Interceptor** | Función que se ejecuta antes de enviar el request o después de recibir el response: añade cabeceras, registra, reintenta |
| **Timeout** | Tiempo máximo de espera antes de dar la petición por fallida |
| **Retry / backoff** | Reintento de una petición fallida, esperando cada vez más entre intentos |
| **Idempotencia** | Propiedad de una operación que produce el mismo resultado se ejecute una o varias veces |
| **Paginación** | Devolver los resultados por partes en lugar de todos juntos |
| **Cache-first** | Estrategia que devuelve primero lo guardado localmente y actualiza después contra la red |
| **TTL** | *Time To Live*. Cuánto tiempo se considera válido un dato en caché |

## Seguridad

| Término | Significado |
|---|---|
| **TLS** | *Transport Layer Security*. El cifrado del canal. Es la `s` de HTTPS |
| **Certificate pinning** | Fijar en la app qué certificado se acepta, para que un certificado falso no funcione |
| **Cleartext** | Tráfico HTTP sin cifrar. Android lo bloquea desde API 28 |
| **Proxy interceptor** | Herramienta que se pone entre la app y el servidor para leer el tráfico. Se usa para auditar la propia app |
| **OAuth 2.0** | Estándar de autorización: la app obtiene un token sin manejar la contraseña del usuario |
| **PKCE** | *Proof Key for Code Exchange*. Extensión de OAuth obligatoria en apps móviles, evita que otra app robe el código de autorización |
| **Token** | Credencial temporal que la app envía en la cabecera `Authorization` |
| **JWT** | *JSON Web Token*. Formato de token que lleva datos firmados en su interior |
| **Keystore / Keychain** | Almacén seguro del sistema operativo, donde se guardan claves y tokens. No es el almacenamiento normal de la app |
| **MASVS** | *Mobile Application Security Verification Standard*, de OWASP. La lista de verificación de seguridad móvil que usa el curso |
| **OWASP** | *Open Worldwide Application Security Project*. Organización que publica MASVS y otras guías de seguridad |
| **XXE** | *XML External Entity*. Ataque en el que un XML malicioso hace que el parser lea archivos del sistema. Se previene desactivando entidades externas |
| **Inyección de XML** | Insertar etiquetas en un XML aprovechando que los valores no se escaparon. Equivalente al `SQL injection` |
| **Minimización** | Principio de tratar solo los datos personales estrictamente necesarios |
| **Dato sensible** | Categoría de la Ley 29733 con protección reforzada: salud, biometría, origen étnico, datos de menores |
| **Descompilable** | Que el artefacto publicado puede abrirse y leerse. Por eso nunca se embeben secretos en el código |

## Construcción y publicación

| Término | Significado |
|---|---|
| **SDK** | *Software Development Kit*. El conjunto de herramientas y librerías de una plataforma |
| **NDK** | *Native Development Kit*. Herramientas para compilar código nativo en Android |
| **AVD** | *Android Virtual Device*. Un emulador configurado con un modelo y una versión concretos |
| **Emulador** | Dispositivo Android simulado que corre en la computadora del laboratorio |
| **`10.0.2.2`** | Dirección con la que el emulador alcanza la máquina anfitriona. `localhost` apuntaría al propio emulador |
| **`adb`** | *Android Debug Bridge*. Herramienta de línea de comandos para hablar con un dispositivo o emulador |
| **Gradle** | Sistema de construcción de los proyectos Android y KMP |
| **`pub` / `pubspec.yaml`** | Gestor de dependencias de Dart y su archivo de configuración |
| **Version catalog** | En Gradle, el archivo `libs.versions.toml` donde se declaran todas las versiones una sola vez |
| **APK** | *Android Package*. El archivo instalable de una app Android |
| **AAB** | *Android App Bundle*. El formato que Google Play exige para publicar |
| **Firma** (*signing*) | Proceso criptográfico que acredita quién publicó la app. Sin la misma clave no se puede actualizar |
| **Keystore de firma** | Archivo con la clave de firma. **Si se pierde, no se puede volver a actualizar la app publicada** |
| **Prueba cerrada** | Fase de Google Play con testers invitados, previa a producción. Exige 12 testers durante 14 días continuos |
| **Ficha de tienda** | La descripción, capturas e íconos que el usuario ve antes de instalar |

## Pruebas y calidad

| Término | Significado |
|---|---|
| **Prueba unitaria** | Verifica una clase o función aislada, sin red ni base de datos |
| **Prueba de integración** | Verifica que varias piezas funcionen juntas, con dependencias reales |
| **Prueba de extremo a extremo** | Recorre un flujo completo como lo haría el usuario |
| **Test double** | Objeto que sustituye a una dependencia real en una prueba |
| **Mock** | Test double que además verifica que se le llamó como se esperaba |
| **Cobertura** | Porcentaje de líneas ejecutadas por las pruebas. Alta cobertura no garantiza buenas pruebas |
| **Gherkin** | Formato de criterios de aceptación: `Dado… Cuando… Entonces…` |
| **Linter** | Herramienta que revisa el código sin ejecutarlo. `flutter analyze`, `ktlint`, `detekt` |
| **Análisis estático** | Revisión automática del código en busca de defectos y desviaciones de estilo |

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
