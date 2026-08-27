[Semana 02](README.md) · **Teoría** · [Dinámica de aula](2-DINAMICA.md) · [Taller de laboratorio](3-TALLER.md)

# Teoría · Arquitectura de Aplicaciones Móviles

**SI-988 · Soluciones Móviles II** · Semana 02 · Sesión 1 en aula · 2 h, con la dinámica incluida

---

## Qué se trabaja en esta sesión

- Por qué la arquitectura es una decisión económica.
- Los patrones de presentación MVC, MVP, MVVM y MVI.
- Clean Architecture aplicada a móviles.
- La Definition of Done y el ADR.

## Mapa de la sesión

```mermaid
flowchart TD
    AR["Arquitectura<br/>decisión económica, no estética"]
    PR["Capa de presentación"]
    DO["Capa de dominio"]
    DA["Capa de datos"]
    MV["Patrones de presentación<br/>MVC, MVP, MVVM y MVI"]
    DE["Regla de dependencia<br/>el dominio no conoce<br/>ni la interfaz ni la red"]
    ADR["Registro de decisión<br/>de arquitectura"]
    DOD["Definition of Done"]
    AR --> PR
    AR --> DO
    AR --> DA
    MV --> PR
    DE --> DO
    AR --> ADR
    ADR --> DOD
    class AR nucleo
    class PR,DO,DA,MV concepto
    class DE alerta
    class ADR,DOD producto
    classDef nucleo fill:#16285C,stroke:#16285C,stroke-width:1px,color:#FFFFFF;
    classDef concepto fill:#E8F1FB,stroke:#16285C,stroke-width:1px,color:#16285C;
    classDef producto fill:#E9F6F2,stroke:#0F766E,stroke-width:1px,color:#0F4C46;
    classDef alerta fill:#FDF2E2,stroke:#B45309,stroke-width:1px,color:#7C3E00;
```

---

## Exposición de la dinámica de la Semana 01 (20 min)

Exposiciones de 10 minutos sobre «Tres apps que no debieron existir». Cierre. **la app que no aprovecha ninguna capacidad del dispositivo compite contra una página web que no hay que instalar, no hay que actualizar y no ocupa espacio. Esa competencia se pierde siempre.**

Revisión pública del veredicto de validación de cada equipo. Los que obtuvieron menos de 3 de 5 reformulan su propuesta esta semana.

## Por qué la arquitectura es una decisión económica (20 min)

**El costo de no decidir.** Una app sin arquitectura definida funciona igual de bien en el sprint 1 y cuesta el triple en el sprint 4. Los síntomas son predecibles:

| Síntoma | Causa arquitectónica | Costo |
|---|---|---|
| «Cambiar el color del botón rompió el guardado» | Lógica de negocio dentro de la vista | Cada cambio requiere probar toda la app |
| «No podemos probar esto sin ejecutar la app» | Dependencias concretas, sin abstracción | Sin pruebas automatizadas viables |
| «Hay tres formas de pedir el mismo dato» | Sin capa de datos única | Comportamiento inconsistente |
| «Si cambiamos de proveedor de backend hay que reescribir todo» | El detalle de infraestructura filtrado a toda la app | Bloqueo tecnológico |
| «Nadie entiende esta pantalla salvo quien la hizo» | Sin patrón consistente | Factor bus = 1 por pantalla |

> **La arquitectura no se juzga por su elegancia sino por el costo del próximo cambio.** La pregunta que la valida es: *¿cuánto cuesta agregar una pantalla nueva? ¿Y cambiar el origen de un dato?*

## Los patrones de presentación MVC, MVP, MVVM y MVI (30 min)

Todos separan **datos**, **presentación** y **vista**. Difieren en quién habla con quién.

| Patrón | Flujo | Quién conoce a quién | Prueba unitaria | Cuándo se usa hoy |
|---|---|---|---|---|
| **MVC** | Vista → Controlador → Modelo → Vista | El controlador conoce la vista | Difícil: el controlador depende de la vista | Base histórica; el «MVC» de iOS clásico degenera en controladores enormes |
| **MVP** | Vista ↔ Presentador → Modelo | El presentador conoce una **interfaz** de la vista | Buena: se sustituye la vista por un doble | Android pre-2018; aún vigente en código legado |
| **MVVM** | Vista **observa** al ViewModel → Modelo | **El ViewModel no conoce la vista** | Muy buena: se prueba el ViewModel sin interfaz | **Estándar actual** en Android, SwiftUI y Flutter |
| **MVI** | Intención → Estado inmutable único → Vista | Flujo unidireccional | Excelente: estado predecible y reproducible | Pantallas con estado complejo; equipos con experiencia |

**MVVM en detalle** —el patrón que este curso exige como mínimo:

```
   ┌──────────┐   observa el estado   ┌───────────────┐   solicita   ┌────────────┐
   │  VISTA   │ ◄──────────────────── │   VIEWMODEL   │ ───────────► │ REPOSITORIO│
   │(Composable│                      │               │              │            │
   │ /SwiftUI/ │ ──── eventos ──────► │ · estado      │ ◄─── datos ──│ · red      │
   │  Widget)  │   del usuario        │ · lógica de   │              │ · local    │
   └──────────┘                       │   presentación│              └────────────┘
                                      └───────────────┘
   La vista NO tiene lógica.          El ViewModel NO importa nada de la interfaz.
   Solo dibuja el estado y            Es una clase que se prueba sin emulador.
   emite eventos.
```

**La prueba de que el MVVM está bien implementado:** *¿puedo escribir una prueba unitaria del ViewModel sin arrancar un emulador ni instanciar una vista?* Si la respuesta es no, la separación no existe.

## Clean Architecture aplicada a móviles (30 min)

MVVM organiza la **presentación**; Clean Architecture organiza **toda la aplicación**.

```
  ┌───────────────────────────────────────────────────────────┐
  │  PRESENTACIÓN                                             │
  │  Vistas · ViewModels · Estados de interfaz · Navegación    │
  │  Conoce: dominio                                          │
  ├───────────────────────────────────────────────────────────┤
  │  DOMINIO           ← el corazón, sin dependencias externas │
  │  Entidades · Casos de uso · Interfaces de repositorio      │
  │  Conoce: NADA. Ni Android, ni iOS, ni HTTP, ni base de datos│
  ├───────────────────────────────────────────────────────────┤
  │  DATOS                                                     │
  │  Implementación de repositorios · Fuentes remota y local    │
  │  Modelos de transporte (DTO) · Mapeadores                  │
  │  Conoce: dominio                                          │
  └───────────────────────────────────────────────────────────┘

  REGLA DE DEPENDENCIA: las dependencias apuntan SIEMPRE hacia adentro.
  El dominio no importa nada de las capas externas. Se logra con
  inversión de dependencias: el dominio DEFINE la interfaz; datos la IMPLEMENTA.
```

**Qué vive en cada capa:**

| Capa | Elementos | Ejemplo |
|---|---|---|
| **Dominio** | Entidades del negocio · Casos de uso · Interfaces de repositorio · Errores de dominio | `Pedido`, `RegistrarPedido`, `PedidoRepository` (interfaz), `PedidoNoDisponible` |
| **Datos** | Implementación de repositorios · Cliente HTTP · Base de datos local · DTO · Mapeadores | `PedidoRepositoryImpl`, `PedidoApi`, `PedidoDao`, `PedidoDto`, `PedidoMapper` |
| **Presentación** | Vistas · ViewModels · Estados · Eventos · Navegación | `PedidoScreen`, `PedidoViewModel`, `PedidoUiState` |

**Por qué el modelo de dominio y el DTO deben ser distintos.** El DTO refleja lo que el backend envía; la entidad refleja lo que el negocio significa. Si son el mismo objeto, **cada cambio del backend obliga a tocar toda la aplicación**. El mapeador es el punto único donde se absorbe ese cambio.

**Proporcionalidad.** Clean Architecture completa en una app de 4 pantallas produce más carpetas que código útil. La regla del curso:

| Tamaño de la app | Arquitectura apropiada |
|---|---|
| ≤ 5 pantallas, sin lógica compleja | MVVM + repositorio, **sin capa de casos de uso** |
| 6 a 15 pantallas | MVVM + repositorio + casos de uso donde haya lógica de negocio real |
| > 15 pantallas o varios equipos | Clean completa, con modularización por funcionalidad |

## La Definition of Done y el ADR (20 min)

**Definition of Done (DoD).** El acuerdo del equipo sobre qué significa que algo está terminado. Sin ella, «terminado» significa cosas distintas para cada integrante y el incremento del sprint no es utilizable.

**La DoD debe ser verificable.** «Código de calidad» no es verificable; «pasa el linter sin advertencias» sí lo es. Ejemplo de DoD del curso:

| # | Criterio | Cómo se verifica |
|---|---|---|
| 1 | El código compila en Android **y** en iOS | CI en verde en ambos objetivos |
| 2 | Sin advertencias del analizador estático ni del linter | CI |
| 3 | Pruebas unitarias de la lógica nueva, con la CI en verde | CI |
| 4 | Cobertura de la capa de dominio ≥ 70 % | Reporte de cobertura |
| 5 | Revisado por un integrante distinto del autor | Pull Request aprobado |
| 6 | Sin secretos en el código | Verificación de la CI |
| 7 | Funciona en un **dispositivo físico**, no solo en emulador | Evidencia adjunta al PR |
| 8 | Estados de carga, error y vacío implementados | Revisión del PR |
| 9 | Textos externalizados, sin cadenas embebidas | Revisión del PR |
| 10 | Accesible: etiquetas de contenido y contraste suficiente | Revisión del PR |
| 11 | Documentado en el README si cambia el arranque o la configuración | Revisión del PR |
| 12 | Demostrable en la Review sin explicación previa | Ensayo del equipo |

**El ADR — Architecture Decision Record.** Registro breve de una decisión arquitectónica, su contexto, las alternativas evaluadas y sus consecuencias. **Su valor está en el futuro**: cuando dentro de un año alguien pregunte «¿por qué se eligió esto?», el ADR responde sin depender de la memoria de quien decidió.

---

---

[Semana 02](README.md) · **Teoría** · [Dinámica de aula](2-DINAMICA.md) · [Taller de laboratorio](3-TALLER.md)

---

**Docente** · Dr. Oscar Juan Jimenez Flores
[oscarjimenezflores@upt.pe](mailto:oscarjimenezflores@upt.pe) · [LinkedIn](https://www.linkedin.com/in/oscar-jimenez-flores/) · [CTI Vitae — CONCYTEC](https://ctivitae.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do?id_investigador=33398)

Escuela Profesional de Ingeniería de Sistemas · Universidad Privada de Tacna · Tacna, Perú
