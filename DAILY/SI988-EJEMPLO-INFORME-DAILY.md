**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERÍA**

**ESCUELA DE INGENIERÍA DE SISTEMAS**

**TALLER**

INFORME DE DAILY – SEMANA 05

**CURSO:**

**SOLUCIONES MÓVILES II · SI-988**

**INTEGRANTES:**

Ccama Huanca, Rosa Milagros · 2021070981

Quispe Mamani, Diego Alonso · 2021071234

Flores Apaza, Kevin Rodrigo · 2021071108

Ticona Larico, Andrea Belén · 2021070877

Choque Nina, Renzo Martín · 2021071350

**DOCENTE:**

DR. OSCAR JUAN JIMENEZ FLORES

TACNA — PERÚ

**Ejemplo resuelto.** Muestra la profundidad que se espera. Los datos son de una aplicación del catálogo y de un equipo ficticio.

# 1. Identificación

| | |
|---|---|
| **Nombre de la aplicación** | Ruta Limpia |
| **Repositorio en GitHub** | `https://github.com/si988-2026-grupo4/ruta-limpia` |
| **Tablero en GitHub Projects** | `https://github.com/orgs/si988-2026-grupo4/projects/1` |
| **Grupo N.º** | 4 |
| **Sprint N.º** | 2 de 5 |
| **Semanas del sprint** | 04 a 06 |
| **Sprint Goal** | Que el vecino vea en el mapa dónde está el camión de su ruta, con la posición actualizándose sola mientras el operario tiene la aplicación minimizada |
| **Semana del curso** | 05 |
| **Daily N.º** | 2 |

# 2. Equipo y roles

| Integrante | Rol en el Daily |
|---|---|
| Ccama Huanca, Rosa Milagros | Product Owner. Asiste y resuelve dudas de criterios de aceptación |
| Quispe Mamani, Diego Alonso | Scrum Master. Facilita la sesión y redacta este informe |
| Flores Apaza, Kevin Rodrigo | Developer. Servicio de ubicación en segundo plano |
| Ticona Larico, Andrea Belén | Developer. Mapa y capa de presentación |
| Choque Nina, Renzo Martín | Developer. Persistencia local y sincronización diferida |

# 3. Datos de la sesión

| | |
|---|---|
| **Fecha** | Martes 29 de septiembre de 2026 |
| **Hora de inicio y de fin** | 19:05 a 19:23 |
| **Lugar o canal** | Canal `#daily` del servidor del equipo, con cámara encendida |
| **Convocados** | Los cinco integrantes |
| **Presentes** | Ccama, Quispe, Flores, Ticona |
| **Ausentes y motivo** | Choque Nina, Renzo Martín. Avisó a las 18:40 por el canal del equipo, práctica preprofesional |

# 4. Registro del daily

| Integrante | Qué realizó | ¿Algo lo bloquea? |
|---|---|---|
| Flores Apaza, Kevin | Terminó el servicio de ubicación en primer plano emitiendo cada 15 s, con la notificación persistente que exige Android 14. Hoy lo lleva a segundo plano y mide el consumo de batería en una ruta de 40 min. `#H07` · rama `feat/h07-ubicacion-fg` · Pull Request `#41` en revisión | Sí, IMP-03 |
| Ticona Larico, Andrea | Dejó el mapa con el marcador del camión leyendo del repositorio local, con datos de prueba. Hoy lo conecta a una fuente simulada con la misma interfaz, para avanzar sin esperar a que se cierre IMP-03. `#H08` · rama `feat/h08-mapa-ruta` | No |
| Ccama Huanca, Rosa | Escribió los criterios de aceptación de H07 y H08 en formato Gherkin y los revisó con dos vecinos del piloto. Hoy toma los de H10, el sello de última actualización. Pull Request `#39`, fusionado | No |
| Quispe Mamani, Diego | Dejó activa la verificación de secretos en la integración continua, que ahora falla el flujo de trabajo si aparece una clave de mapa en el código. Hoy desbloquea IMP-03 con el laboratorio y revisa el Pull Request `#41`. `#42` · Pull Request `#40`, fusionado | No |
| Choque Nina, Renzo | Ausente. Su rama no registra movimiento desde el 26 de septiembre | Ausente |

# 5. Estado del tablero al cerrar la sesión

| Columna | Historias | Límite de trabajo en curso | ¿Se respeta? |
|---|---|---|---|
| Sprint Backlog | H06, H09, H10 | — | — |
| En progreso | H08 | 3 | Sí |
| En revisión | H07 | 2 | Sí |
| En pruebas | — | 2 | Sí |
| Listo | — | — | — |

# 6. Impedimentos

| Id | Impedimento | Quién lo levanta | Quién lo remueve | Estado | Fecha de cierre |
|---|---|---|---|---|---|
| IMP-01 | El emulador no entrega posiciones simuladas de forma continua y no permite probar el seguimiento | Flores | Quispe | Cerrado | 26 de septiembre, con un archivo de rutas simuladas cargado por consola |
| IMP-02 | Nadie del equipo tiene acceso a macOS para la compilación en iOS | Quispe | Ccama | Abierto | Escalado al docente el 24 de septiembre. El Sprint 2 se mantiene solo en Android |
| IMP-03 | El dispositivo de pruebas se queda sin batería antes de terminar el recorrido de 40 min | Flores | Quispe | Abierto | Compromiso para el 1 de octubre, con un cargador vehicular del laboratorio |

# 7. Evidencia

Captura del tablero al cerrar la sesión — `docs/evidencias/S05/tablero-daily-02.png`
