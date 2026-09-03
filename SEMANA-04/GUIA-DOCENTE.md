# Guía del docente · Semana 04 · «El pedido que se creó dos veces»

**SI-988 · Soluciones Móviles II** · Uso interno. No se publica: está excluida en el `.gitignore` del curso.

---

## Para qué sirve la dinámica

De toda la teoría de la semana, hay una frase que separa una app amateur de una profesional:

> *La conectividad móvil es intermitente. Si el usuario envía un pedido, pierde la señal antes de recibir la respuesta y la app reintenta, se crean dos pedidos.*

Casi ningún equipo lo tiene resuelto en su app, y casi todos lo van a descubrir hoy. Ese es el objetivo.

**Qué se quitó de esta dinámica.** La versión anterior pedía **tres** endpoints con ocho columnas, más una tabla de errores, más el formato JSON, más documentarlo en OpenAPI —y OpenAPI **no está en la teoría de la semana**, está en el taller—. No cabía en 35 minutos. Ahora es **un endpoint**, bien hecho.

---

## Paso 0 · Los 7 minutos de pizarra · guion

Es el mejor paso 0 de las tres asignaturas porque se puede **actuar**.

**Escriba:**

```
POST /reservas        →  201 Created
                         Location: /reservas/8417
```

**Lo que hace, en este orden:**

1. *«El usuario toca Reservar.»* Dibuje una flecha del teléfono al servidor. *«Llega. El servidor crea la reserva 8417.»*
2. Dibuje la flecha de vuelta y **córtela con una raya**. *«Aquí se cayó la señal. La respuesta nunca llegó.»*
3. *«¿Qué sabe la app en este momento?»* Espere. La respuesta correcta es: **nada**. *«No puede distinguir "no llegó" de "llegó y no me enteré". Son idénticas desde el teléfono.»*
4. *«¿Y qué hace toda app razonable? Reintenta.»* Dibuje la segunda flecha. *«Y el servidor crea la reserva 8418. Dos reservas. Dos cobros. Un cliente furioso.»*
5. *«¿Lo arreglamos poniendo un `if` en el servidor que busque reservas parecidas?»* Deje que lo intenten. Siempre aparece alguien proponiendo comparar fecha, hora y usuario. *«¿Y si el usuario de verdad quiere dos horas seguidas? Lo acaban de romper.»*
6. Escriba la solución: `Idempotency-Key: 7c2f...`. *«La app genera esta clave **una vez, cuando el usuario toca el botón**, no una por intento. El servidor guarda qué respondió a cada clave. Si la ve otra vez, devuelve lo mismo. No compara nada, no adivina nada.»*
7. Cierre del paso 0: *«La regla es de la teoría. `GET`, `PUT` y `DELETE` se reintentan solos. `POST` no. Ahora busquen su `POST`.»*

---

## Cómo arbitrar, ya que cada equipo trae su propia app

No hay una respuesta única, pero sí **cuatro preguntas que resuelven casi todo**:

| Pregunta | La respuesta correcta |
|---|---|
| «La clave de idempotencia, ¿cuándo se genera?» | Cuando el usuario **toca el botón**, y se reusa en los reintentos. Si se genera en cada intento, no sirve para nada. **Es el error más común** |
| «¿Qué devuelve el servidor si ve la clave repetida?» | **El mismo `201` y el mismo recurso.** No un `409`, no un `200` vacío. El cliente no debe notar la diferencia |
| «Ese mensaje de error, ¿se lo mostrarías a tu mamá?» | Si aparece «token», «servidor», «422», «campo», «null» o «request», no aprueba |
| «¿Por qué paginación por cursor y no por número de página?» | Porque la lista **crece por arriba**. Con `?page=2`, si entran filas nuevas mientras el usuario navega, se salta filas o las repite |

### Las seis apps de respaldo, resueltas

| App | Endpoint | Éxito | El `422` característico |
|---|---|---|---|
| **1** Canchas | `POST /reservas` | `201` + `Location` | «Esa cancha ya está reservada a las 7 p. m.» |
| **2** Visitas de campo | `POST /visitas/{id}/cierre` | `201` + `Location` | «Faltan las fotos del cierre.» |
| **3** Pedido a bodega | `POST /pedidos` | `201` + `Location` | «Solo quedan 3 unidades de arroz de 5 kg.» |
| **4** Reporte ciudadano | `POST /reportes` | `201` + `Location` | «La foto pesa demasiado. Tómala de nuevo.» |
| **5** Asistencia con QR | `POST /marcas` | `201` + `Location` | «Ya marcaste tu entrada hoy a las 8:02.» |
| **6** Pasajes | `POST /compras` | `201` + `Location` | «Ese asiento acaba de venderse. Elige otro.» |

> **La 5 es especial y vale la pena señalarla en la ronda.** Marcar asistencia **sí es idempotente por naturaleza**: marcar dos veces el mismo día debería dar el mismo resultado. Un equipo que llegue a eso solo merece el puntaje completo.

### Los errores que se repiten

| Lo que traerán | Qué decirles |
|---|---|
| `POST` que devuelve `200` con el objeto creado | `201` y la cabecera `Location`. El `200` no dice que se creó nada |
| `Failure` inventados: `SesionExpirada`, `StockInsuficiente` | Los seis de la teoría y ninguno más. `StockInsuficiente` es `ErrorValidacion` |
| `400` para todo error de negocio | `400` es petición malformada. Si el JSON está bien pero la regla de negocio falla, es `422` |
| «El `429` se reintenta enseguida» | Se espera lo que diga `Retry-After`. Reintentar de inmediato empeora el problema |
| `Cache-Control` en el `POST` | En una escritura va `no-store`. La caché es del `GET` |
| Mensajes con el nombre del campo: «items[2].cantidad inválido» | Ese detalle es para el desarrollador. Al usuario se le dice qué producto y qué hacer |

---

## Paso 4 · La ronda y el cierre · 6 minutos

Pida a tres equipos **solo el mensaje del `422`**, leído en voz alta. El aula vota si un usuario cualquiera lo entendería. Es rápido, es divertido y es donde más se aprende.

**Cierre, dos minutos:**

> *«Lo que hicieron hoy no es documentación: es la diferencia entre una app que se puede usar en un micro con mala señal y una que crea pedidos duplicados. En la Semana 15 va a aparecer un defecto que dice "al tocar enviar dos veces se crean dos pedidos". El equipo que hoy resolvió su clave de idempotencia no lo va a tener.»*

---

## Si el tiempo se acorta

| Situación | Qué se recorta |
|---|---|
| La teoría se pasó | Elimine el paso 3. El `GET`, la paginación y la caché se completan al formatear el PDF |
| Un equipo no tiene API definida | Que tome una de las seis de respaldo y lo diga. No resta: el objetivo es el concepto |
| Sobra tiempo | Pregunte cuál de las seis apps de respaldo tiene un endpoint que **ya es idempotente** sin necesidad de cabecera. Respuesta, la 5 |

---

**Docente** · Dr. Oscar Juan Jimenez Flores · Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna
