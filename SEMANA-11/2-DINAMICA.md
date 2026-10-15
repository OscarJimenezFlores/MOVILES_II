[Semana 11](README.md) · [Teoría](1-TEORIA.md) · **Dinámica de aula** · [Taller de laboratorio](3-TALLER.md)

# Dinámica de aula · El flujo de sesión completo

**SI-988 · Soluciones Móviles II** · Semana 11 · Actividad en aula, **dentro de la sesión de teoría** · calificación **cognitiva**

> ¿Un término no le resulta claro? Está definido en el [glosario técnico del curso](../GLOSARIO.md).

---

## Qué entregas

| | |
|---|---|
| **Archivo** | `SI988-S11-DINAMICA-Grupo<N>.pdf` |
| **Plantilla obligatoria** | [SI988-PLANTILLA-DINAMICA.docx](../PLANTILLAS/SI988-PLANTILLA-DINAMICA.docx) |
| **Formato** | PDF exportado desde la plantilla en Word, con la carátula de la UPT y los apellidos, nombres y códigos de todos los integrantes |
| **Qué va dentro** | Lo que el grupo resolvió en aula. Las tablas de la sección **Producto** van completas, con los textos redactados, y cada decisión va justificada |
| **Dónde se sube** | Aula virtual, tarea «Dinámica · Semana 11» |
| **Cuándo vence** | Según lo programado en el aula virtual. La tabla se resuelve en aula; el PDF se formatea y se sube después |
| **Exposición** | En la ronda de cierre de **esta misma sesión**. El grupo **lee y explica su resultado** ante el aula, con el documento a la vista. No se usan diapositivas |

> No se califica un trabajo entregado en `.docx`, sin carátula, sin los códigos de los integrantes o con las tablas del producto vacías.

---

## Consigna

> **«El flujo de sesión completo»**
> Cada equipo diseña el **flujo de autenticación de extremo a extremo** de su aplicación — primer inicio de sesión, sesiones siguientes con biometría, renovación del token, expiración, cierre de sesión y **los seis casos de fallo de la biometría**.

| | |
|---|---|
| **Su papel** | **Responsable de la autenticación** ante un usuario que estrena teléfono y perdió el anterior |
| **Misión** | Diseñar el flujo de sesión de extremo a extremo, incluidos los seis casos de fallo de la biometría |
| **Restricción** | **La app es un cliente público.** Ninguna parte del flujo puede depender de un secreto guardado en el dispositivo |

## Producto

**Producto 1 — El diagrama de secuencia.** Desde que el usuario abre la app hasta que realiza su primera operación autenticada, con las tres rutas. Primera vez, con biometría y con token expirado.

**Producto 2 — Matriz de casos.**

| Caso | Qué hace la app | Qué ve el usuario | ¿Requiere autenticación completa? |
|---|---|---|---|
| Primera vez | | | |
| Con biometría disponible | | | |
| Token de acceso expirado | | | |
| Token de renovación expirado | | | |
| Sin sensor biométrico | | | |
| **Biometría nueva registrada** | | | |
| Biometría fallida 3 veces | | | |
| Cierre de sesión | | | |

> **Dónde va.** Este producto se presenta en la **sección 2 de la [plantilla de dinámica](../PLANTILLAS/SI988-PLANTILLA-DINAMICA.docx)**, «El producto». No se copia la consigna ni la teoría. Solo el resultado y lo que lo sostiene.

## Ejemplo resuelto

*El caso de este ejemplo es distinto del que le toca a tu grupo. Sirve para que veas el nivel de detalle que se espera, no para copiarlo.*

**Una matriz de casos bien resuelta.** El flujo del ejemplo es de otra aplicación.

*El diagrama de secuencia, ruta «con biometría»*

```
Usuario        App                 Almacén seguro        Servidor de identidad
   │            │                        │                        │
   │ abre app   │                        │                        │
   ├───────────▶│                        │                        │
   │            │ ¿hay token de          │                        │
   │            │  renovación?           │                        │
   │            ├───────────────────────▶│                        │
   │            │◀── sí, protegido ──────┤                        │
   │            │                        │                        │
   │  solicita  │                        │                        │
   │  huella    │                        │                        │
   │◀───────────┤                        │                        │
   ├───────────▶│ huella válida          │                        │
   │            ├───────────────────────▶│                        │
   │            │◀── token liberado ─────┤                        │
   │            │                        │                        │
   │            │ POST /token (refresh_token)                     │
   │            ├────────────────────────────────────────────────▶│
   │            │◀─────────── access_token (15 min) ──────────────┤
   │            │                                                 │
   │◀── pantalla principal, sesión activa ──┤                     │
```

**Lo que este diagrama deja claro.** La biometría **no autentica ante el servidor**. Solo libera un token que ya estaba en el dispositivo. El servidor nunca ve la huella y no sabe que se usó. Confundir esto es el error más frecuente de la dinámica.

*Matriz de casos*

| Caso | Qué hace la app | Qué ve el usuario | ¿Requiere autenticación completa? |
|---|---|---|---|
| Primera vez | Flujo de código de autorización con PKCE en el navegador del sistema. Guarda el token de renovación en el almacén seguro, protegido por biometría | Pantalla del proveedor de identidad, luego «¿Quieres usar tu huella para ingresar la próxima vez?» | **Sí** |
| Con biometría disponible | Solicita la huella, libera el token de renovación, obtiene token de acceso | Diálogo de huella, luego la pantalla principal | No |
| Token de acceso expirado | Renueva en silencio con el token de renovación. Si hay una petición en curso, la reintenta una vez tras renovar | Nada. El usuario no se entera | No |
| Token de renovación expirado | Borra el token del almacén y lleva al flujo de inicio de sesión completo | «Tu sesión venció. Ingresa de nuevo.» | **Sí** |
| Sin sensor biométrico | Ofrece un PIN propio de la app de 6 dígitos como protección del almacén | «Crea un PIN para ingresar más rápido» | No, tras crear el PIN |
| **Biometría nueva registrada en el dispositivo** | El sistema invalida la clave asociada. La app detecta la invalidación, **borra el token de renovación** y exige inicio de sesión completo | «Detectamos un cambio en la biometría de tu dispositivo. Por seguridad, ingresa de nuevo.» | **Sí** |
| Biometría fallida 3 veces | El sistema bloquea el sensor temporalmente. La app ofrece el PIN o el inicio de sesión completo | «Intenta con tu PIN o ingresa con tu contraseña» | No, si usa el PIN |
| Cierre de sesión | Borra el token de renovación del almacén, revoca el token en el servidor y limpia la caché de datos del usuario | Vuelve a la pantalla de inicio de sesión | — |

**El caso que separa un buen trabajo de uno mediocre.** «Biometría nueva registrada». Si alguien añade su huella al dispositivo de otra persona y la app no invalida la credencial, esa persona entra a la cuenta ajena. El sistema ofrece la invalidación automática; hay que activarla explícitamente al crear la clave.

**La diferencia entre aprobar y no aprobar.**

| Así no | Así sí |
|---|---|
| «La biometría autentica al usuario ante el servidor.» | «La biometría libera un token que ya estaba en el dispositivo. El servidor nunca ve la huella.» |
| «Si se registra una huella nueva, no pasa nada.» | «El sistema invalida la clave. La app borra el token y exige inicio de sesión completo.» |
| «Al cerrar sesión se borra el token.» | «Se borra del almacén, se revoca en el servidor y se limpia la caché de datos del usuario.» |

## Reglas

- El diagrama debe mostrar **dónde se guarda cada token** y **quién verifica qué**.
- **Obligatorio** indicar que la biometría desbloquea la clave y **no autentica ante el servidor**.
- **Obligatorio** cubrir el caso de biometría nueva registrada.
- El cierre de sesión debe incluir la **revocación en el servidor**.
- La exposición es la ronda de cierre de esta misma sesión. El grupo **lee y explica su resultado**. No se usan diapositivas.

## Rúbrica cognitiva (20 puntos)

| Criterio | 5 | 3 | 1 |
|---|---|---|---|
| **Corrección del flujo** | PKCE con navegador del sistema; sin secreto de cliente; `state` verificado | Flujo correcto con alguna omisión | Usa un flujo obsoleto o vista web embebida |
| **Rol de la biometría** | Explica que desbloquea la clave y no autentica ante el servidor | Lo usa correctamente sin explicarlo | La presenta como sustituto de la autenticación |
| **Gestión de tokens** | Vidas útiles, ubicación de almacenamiento y rotación definidas | Definidas parcialmente | Un solo token sin expiración |
| **Casos cubiertos** | Los ocho, incluida la invalidación por biometría nueva | Seis o siete | Solo el camino feliz |

---

---

[Semana 11](README.md) · [Teoría](1-TEORIA.md) · **Dinámica de aula** · [Taller de laboratorio](3-TALLER.md)

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
