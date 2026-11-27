# Inventario del paquete para equipos — Datatón Observatorio de la Tierra

- **Evento:** martes 24 nov 2026, Universidad Externado (14 equipos Externado; Air4U es el ejemplo del sandbox).
- **Inventario:** 23 nov 2026, tarde (hora de Bogotá, America/Bogota). Solo lectura: sin ediciones, envíos ni pushes.
- **Pregunta de Gideon:** listar todo lo que se entrega a las startups (del BMC a los ejemplos Air4U) y un PDF de prompts para que generen, con su propia IA, los documentos y cuestionarios.

## Fuentes consultadas

| Fuente | Qué se encontró |
|---|---|
| Box `/workspace/air4u-deck-src/fix2/team-pack-es/` | Fuente maestra del paquete ES v0.3-es (21 nov 2026), con PDFs de comprobación en `/workspace/pack-check-fix1` y `/workspace/pack-check-fix2`. |
| Box `/workspace/datathon-questionnaires/` | Maestros en inglés Q1/Q2, rúbrica, ejemplo Air4U, CHANGELOG. Falta en esta copia local el `q3-data-to-value-card.md` (sí está en Drive). |
| Box `/workspace/air4u-bmc/` | BMC ilustrativo de Air4U (HTML/PDF; hay una versión anterior con tarifas de sandbox, ya superada). |
| Box `/workspace/pr172-check/` y `/workspace/air4u-datathon-teams-deck/` | Plantilla de pitch Hoja 5 (PR #172) y deck para equipos (commit publicado `7de09c90`). |
| GitHub `gideonblaauw-creator/cth-plugin` | PRs #167, #171, #172, #174, #175, #176 (y #163 ya fusionado: deck Observatorio). El paquete `team-pack-es` **no** está en `main` ni en un PR propio. |
| Google Drive carpeta padre `1DyKMgRcw1oG6WNqoxhLp0gNB8yds0oK4` y subcarpeta `team-pack-es` (`1kAasGLjutnSBeDMIOg4MVWxZjlT2Py_F`) | Docs/PDFs del paquete, maestros en inglés, BMC Air4U, PDFs del deck de equipos. Permisos: solo cuentas CTH (Gideon, Angie, Mónica, etc.). Sin “cualquiera con el enlace”, sin Marlene, sin equipos. |
| Gmail (últimas 3 semanas, consulta: pack / plantilla / BMC / cuestionario / mapa de calor / datatón) | No hay correo que envíe el paquete, las hojas o los prompts a equipos, monitores o Marlene. Lo enviado a invitados es la logística y, el 23 nov a las 15:11 (Bogotá), el mensaje de Luma con indicaciones de llegada (sin agenda ni pack). |
| Sitios en vivo | `https://decks.cleantechhub.net/datathon-2026-teams/` (público, noindex, 200). `https://datalab.cleantechhub.net/` enlaza Taller (`/app/#/taller`) y Datathon (`/datathon-demo/`). `programs.cleantechhub.net` redirige a un share; no es el paquete de equipos. |
| Memoria del workstream Datatón (23 nov) | Método del día: BMC → tablero en los dos bloques de hacking; BMC se hace el día (no viene prellenado); datasheet y tablero con herramientas abiertas o la IA del equipo; tablero a las 16:00; Air4U es el ejemplo; un PDF con marca CTH es la alternativa de baja tecnología a un cuestionario de IA en línea. |

**Lectura de “ya compartido con los equipos”:** solo cuenta un envío o una publicación que los 14 equipos (o los invitados de Luma) hayan podido abrir. Un archivo en Drive interno de CTH o un PR en borrador no cuenta.

---

## A. Tabla de inventario

### A1. Paquete de equipo v0.3-es (lo que las mesas deben usar)

Versión de equipo: **v0.3-es**, fecha en las hojas **2026-11-21**. Ticket de Hands del 21 nov: traducir los maestros en inglés a español imprimible; *“Nothing sent, shared or published.”* El diseño metodológico (entrada abierta en Bloque 1, subida estricta en Bloque 2) quedó aprobado por Gideon el 21 nov (CHANGELOG v0.2). No hay un GO posterior, en correo o en esta revisión, para entregar el zip o la carpeta Drive a los equipos. El deck publicado sí dice: “Cada equipo recibe hoy el paquete v0.3-es”.

| # | Nombre | Qué es | Formato | Dónde vive | Estado | ¿Ya compartido con equipos? |
|---|---|---|---|---|---|---|
| 1 | Agenda del día — equipos | Run-of-show de hacking (Bloque 1 mañana / Bloque 2 tarde). Horas en `[confirmar]` salvo finales 16:00. Embudo **20 → 6 → 3**. | MD + PDF A4 + Google Doc | Box `team-pack-es/agenda-equipos.md`; Drive `1yJ6fozXxGnaaNTPcR8-kwnSzvBu7QC9t` (PDF), Doc `1p8VMQPCnWHQM58zkQCXQWrzjBg4TIylCRFS-X2gCLOo` | Borrador de pack v0.3-es. **Desactualizada** frente a la agenda pública del 23 nov (ver C). | No |
| 2 | Hoja 1 — Mapa de calor de datos (¿DÓNDE?) | Cuestionario por los 9 bloques del BMC; hasta 3 conjuntos (D1–D3) por bloque; códigos S/R/H/F/A/Q/G/M/L; verificación de contexto; registro de desacuerdos fundador/operador. | MD + PDF A4 + Google Doc | `hoja-1-mapa-de-calor.md`; Drive PDF `18-i-G0PLwuq9RQVosVLG1-xn5TgQqJOF` | v0.3-es, alineada al maestro inglés Q1 v0.2. Sin GO de entrega. | No |
| 3 | Hoja 2 — Flujo y escalera Medallion (¿QUÉ?) | Preguntas de flujo A1–A15; escalera Bronce (B1–B7) / Plata (S1–S6) / Oro (G1–G9); plantilla de tarjeta de flujo; tarjeta de arranque si no hay bloque tibio. | MD + PDF A4 + Google Doc | `hoja-2-flujo-de-datos.md`; Drive PDF `1MUIc-9hM_-_Znpb1pBZC6JhkcrdjSdCR` | v0.3-es. Sin GO de entrega. | No |
| 4 | Hoja 3 — De dato a valor | Una decisión, un usuario, 2–3 preguntas, 2–3 números, valor, audiencia, boceto de tres paneles, autocontrol. | MD + PDF A4 + Google Doc | `hoja-3-dato-a-valor.md`; Drive PDF `19y9dg02mfDYkHcDrub_pGL-AXSxAopc7` | v0.3-es. El maestro inglés Q3 está en Drive (`1Eb2VG0BnGYDv-ImjR_y0bfs9rRBqJNlc`), no en la copia local de `/workspace/datathon-questionnaires/`. | No |
| 5 | Hoja 4 — Plantilla de tablero (una pantalla) | Plantilla imprimible de una pantalla: usuario, decisión, tres paneles (línea base / delta / panorama) + puente de valor, mapa o antes/después, pie de valor. | MD + PDF A4 + Google Doc | `hoja-4-plantilla-tablero.md`; Drive PDF canónico en el zip fix2 `1D_pYjA940q47m-xcrkE4MWLDos3u_ZcE` (sha256 del PDF en el manifiesto: `6a9abb1f…`). Hay **varias copias** del mismo PDF en la carpeta Drive (ver C). | v0.3-es, corrección fix2 de Hoja 4 (21 nov). | No |
| 6 | Hoja 4b — Ejemplo Air4U (relleno) | Misma plantilla de Hoja 4, llena con el ejemplo “una clínica en Bogotá (piloto)”. Números en **[sin dato]** / **estimado**, escalera **Ninguno**. | MD + PDF A4 + Google Doc | `hoja-4b-ejemplo-air4u.md`; Drive PDF `1676enEJL3Wts8bmQQ__-4e2zXxAmLewV` (también duplicado). | Ilustrativo; “la empresa piloto no ha diligenciado las hojas”. | No (el ejemplo también aparece en el deck publicado, ver #16) |
| 7 | Ejemplo trabajado Air4U (Hojas 1–3) | Recorrido corto de Hojas 1–3: D1 sensores indoor, tarjeta de flujo en Ninguno, tres números estimados, tablero público = No. | MD + PDF + Google Doc | `ejemplo-air4u.md`; Drive PDF `1ZJ6ESHnuJF4j6OuNFj6kfRGaMw0P3qU9` | Ilustrativo, v0.3-es. | No |
| 8 | Prompts de IA (`prompts-ia`) | 5 prompts para copiar y pegar (Paso 0 BMC desde el pitch; Pasos 1–4 hojas 1–3 y boceto). Ya pide marcar U y no inventar números. **No cubre Hoja 4 campo a campo ni Hoja 5.** | MD + PDF + Google Doc | `prompts-ia.md`; Drive PDF `1j2T5tKe0IeY1jULIPKXHKOi_vRe4OIz_`; Doc `1D8AiAaZiWB0qVyuVRzPBJwxjGEvTeLVR5rHy3vJTTY8` | Borrador dentro del pack v0.3-es. Es el antecedente del “PDF de prompts” que pide Gideon; hay que ampliarlo (sección D). | No |
| 9 | Fuentes de datos abiertos | Lista verificada (21 nov 2026) para el panel Paisaje; sobre todo calidad del aire en Bogotá/Colombia. datos.gov.co 200; DANE 403 en el entorno de verificación; IDEAM timeout. | MD + PDF + Google Doc | `fuentes-datos-abiertos.md`; Drive PDF `1PmohYXM0FeN_h2xT89nJgxI4OYw_CHSH` | v0.3-es. El propio pack avisa que otros sectores deben buscar fuentes propias. | No |
| 10 | Nota de derechos de datos | Reglas prácticas del piloto (no es asesoría legal; borrador para el Legal desk). Audiencias, datos personales, sitios de cliente, G9 reidentificación, licencias de datos abiertos, prohibición de afirmar ONAC. | MD + PDF + Google Doc | `nota-derechos-datos.md`; Drive PDF `1Z-Te4p85niD6_9Rt6v27ZpbY3kUtWPnD` | v0.3-es. Sigue marcado como borrador para Legal. | No |
| 11 | Guía de carpeta Drive | Plantilla de carpeta por equipo (`01_crudo` … `05_pitch`) y cómo compartirla con CTH en rol Lector. Dice expresamente: no crear ni compartir carpetas reales desde el documento. El correo CTH queda **[confirmar]**. | MD + PDF + Google Doc | `guia-carpeta-drive.md`; Drive PDF `1UlNYsNAKNJUDsGLNa35j58Y1DAjH2SvY` | Plantilla solamente. No hay carpetas reales de los 14 equipos. | No |
| 12 | `test-notes.md` | Notas internas de prueba de escritorio con material CurubaTech (fricciones F1–F6, tiempos). **No es un entregable de mesa.** | MD + PDF + Google Doc | En el mismo `team-pack-es/` y en el zip de PDFs | Herramienta de facilitación / QA. | No, y no debería ir en el zip que se entregue |
| 13 | Manifiesto + zip de PDFs | Inventario sha256 del pack (fix2 Hoja 4). Zip `team-pack-es-pdfs.zip` sha256 `eb84f2ae3d47591ceee978167f69d2705b5d355f90df854680a0a75c4b829540`. | MD + ZIP | Drive zip más reciente `1D_pYjA940q47m-xcrkE4MWLDos3u_ZcE` (282 KB, 22 nov 00:01 UTC). Hay zips anteriores más pequeños / vacíos (ver C). | Fix2 del 21–22 nov. | No |

### A2. BMC y plantilla de pitch (parte del método; aún no están en el zip del pack)

| # | Nombre | Qué es | Formato | Dónde vive | Estado | ¿Ya compartido? |
|---|---|---|---|---|---|---|
| 14 | Lienzo BMC (lo que el equipo produce el día) | Los 9 bloques, empezando por VP1, VP2…. El pack y la memoria del 23 nov coinciden: el BMC **se hace el día, no viene prellenado**. | Entregable del equipo (no hay plantilla en blanco en el pack) | Solo el Paso 0 de `prompts-ia.md` y la agenda-equipos (“BMC con VP1, VP2…”). No hay `hoja-0-bmc` ni PDF de lienzo en blanco. | **Falta la plantilla en blanco** (ver C y B). | No hay nada que entregar aún |
| 15 | Air4U · Business Model Canvas (ejemplo) | BMC ilustrativo en inglés (9 bloques + “Open questions and sources”). Título: *draft*. Versión vigente **sin** tarifas de sandbox CTH. | HTML + PDF + previews | Box `/workspace/air4u-bmc/Air4U_BMC.pdf`; Drive `1rh58NB7XS-EPcwInCigY98Rjp4nINn_A`. Superada: `1Kx_7brgwhtu9ympDM6WXdrT5_eqyQqNM` (“ZZZ SUPERSEDED — with sandbox fees”). | Borrador de ejemplo; no diligenciado por Air4U. El deck de equipos lo usa como ejemplo. | El PDF no consta enviado. El contenido aparece en el deck publicado (#16) |
| 16 | Deck para equipos — piloto Air4U | Presentación de 18 páginas (ES por defecto, hay EN): método, embudo 20→6→3, agenda con horas por confirmar, ejemplo Air4U (BMC → calor → escalera → tarjeta → Hoja 4), reglas de honestidad, qué incluye el paquete, derechos, contacto `info@cleantechhub.net`. | HTML reveal + PDF ES/EN | En vivo: https://decks.cleantechhub.net/datathon-2026-teams/ (publicado 22 nov ~22:14 hora de Bogotá, commit `7de09c90834d57d9d7c9849527d7406f32c3de87`, GO de Gideon en el chat Air4U). PR #167 sigue abierto en borrador (más adelante el PR cita PDFs de 21 páginas). Drive: `1TT2MGrEi2WPbyAC7grGViCoIm8CCO8JY` (ES). | Publicado en la URL de decks (público, noindex). El PR no está fusionado. | **URL pública sí.** No hay correo a los 14 equipos ni a Marlene con el enlace. Marcado CONFIDENCIAL — EQUIPOS DATATÓN |
| 17 | Hoja 5 — Plantilla pitch 5 min (5a) + ejemplo Air4U (5b) | Plantilla de pitch en 5 bloques (Problema, Datos usados, Tablero/hallazgo, Impacto, Próximo paso), con preguntas guía, caja para llenar, tiempo y “Cómo se evalúa”. Los jueces puntúan Parte A utilidad y Parte B honestidad (0–5 cada una). | HTML + PDF A4 (2 páginas) + diapositivas reveal | PR **#172** (borrador, abierto): `decks/datathon-2026-pitch-template/`. Box: `/workspace/pr172-check/review/hoja-5-pitch.pdf`. Ticket: Gideon, 22 nov 21:59 (Bogotá), “get pitch template ready for Team pack”. | Borrador de PR. Aún **no** está en `team-pack-es` ni en el zip. | No |

### A3. Maestros en inglés y material de staff (no son el handout de mesa)

| # | Nombre | Qué es | Formato | Dónde vive | Estado | ¿Para equipos? |
|---|---|---|---|---|---|---|
| 18 | Q1 / Q2 / Q3 maestros EN + rúbrica + hoja de jurados + guía del facilitador + methodology-v0.3 | Fuente de las hojas ES. Rúbrica: D = 2R+H+F+A+Q (0–18); bandas COLD 0–6 / WARM 7–12 / HOT 13–18; selección al Bloque 2. Finales: Parte A/B 0–5. | MD / Google Docs | Drive carpeta padre `1DyKMgRcw1oG6WNqoxhLp0gNB8yds0oK4`. Box (parcial): `/workspace/datathon-questionnaires/`. | Diseño v0.2/v0.3 aprobado por Gideon el 21 nov. Hay v0.1 conservada (escala distinta, no comparable). | No. La rúbrica la aplica CTH; la Hoja 5 ya traduce los criterios de finales al equipo. `test-notes` y `facilitator-guide` son de staff |
| 19 | Agenda pública del evento (v2–v5) | One-pager del programa (apertura, panel, sandbox Air4U, hacking, pitches). En revisión el 23 nov (v4 lista; v5 en curso: 9:10 Observatorio, 9:25 pausa, 9:40 conversación Díaz/Cortés, 9:55 Medina). | HTML/PDF/PNG; Word pedido para Marlene | PR **#176** (borrador). Box `/workspace/dataton-2026-11-24/agenda-v*.md` y `/workspace/dataton-agenda/`. | v4 comprobada internamente; v5 y Word en construcción. No fusionado. | El mensaje de Luma del 23 nov **no** llevó la agenda. Pendiente decisión de Gideon |
| 20 | Guía del panel / certificado / deck MentorXs + cuestionario de mentores | Material de escenario y de staff, no de mesa. | PDF / deck | PRs **#171** (panel), **#174** (certificado, 14 equipos Externado + monitores), **#175** (14 diapositivas + cuestionario de mentor, 55 ítems, sin Forms en vivo). | Borradores de PR. | No (el cuestionario de #175 es para mentores, no para startups) |
| 21 | Kit de comunicaciones `datathon-kit.zip` (4 nov) | Piezas de redes (agenda, EO, Datalab, Datathon, demo Air4U). | ZIP de PDF/JPG | `/workspace/datathon-assets/datathon-kit.zip`; PR #135 (borrador). | Comms, no pack de mesa. | No |
| 22 | App Taller / entorno Datathon en Datalab | Landing `datalab.cleantechhub.net` enlaza `#/taller` (app Air4U) y `/datathon-demo/` (entorno efímero; última modificación 6 oct 2026). La app es un SPA (el fetch solo devuelve la cáscara). | Web | https://datalab.cleantechhub.net/ y https://datalab.cleantechhub.net/datathon-demo/ | En vivo, pero no está descrito como el canal de entrega del pack v0.3-es. El pack en PDF es la alternativa de baja tecnología al cuestionario de IA en línea. | Público a nivel de URL; no consta como kit entregado a los 14 equipos |
| 23 | Página Luma + mensaje del 23 nov | Evento https://luma.com/7rhj57ax. Mensaje “Mañana nos vemos en el Datatón 🌍” (15:11 hora de Bogotá) a ~106 Going, con indicaciones de llegada al Bloque I piso 2. Un mensaje más corto está pendiente para el 24 nov a las 7:00, aún sin GO al texto. | Correo Luma | Luma; copia en `/workspace/dataton-2026-11-24/luma-blast-23nov.md` | Enviado el 23 nov. | **Sí** (indicaciones de llegada). No incluye pack, hojas, prompts ni agenda |

**Oferta adyacente, no está en el pack:** Croma (cris@usecroma.com) ofreció API/MCP y datasets SIATA/CREG/RMCAB, más una intro de 5 min. No aparece en `fuentes-datos-abiertos.md`.

---

## B. Campos y secciones exactos de lo que los equipos deben producir

Citas del paquete v0.3-es y, para el pitch, de la Hoja 5 del PR #172 (`hoja-5-pitch.txt`). No se inventan campos. Donde el pack no trae plantilla, se dice.

### B1. Business Model Canvas (se produce el día; no hay hoja en blanco)

La agenda-equipos pide, en el registro: «BMC con VP1, VP2…». El prompt Paso 0 pide: «un Lienzo de Modelo de Negocio de 9 bloques en español colombiano» y «Liste VP1, VP2… al inicio del bloque Propuestas de valor».

Los 9 bloques, en el orden y con las preguntas guía de **Hoja 1** (son a la vez la estructura del BMC y la entrada del mapa de calor):

1. **Propuestas de valor** — «Liste VP1, VP2… ¿Mide si el cliente recibe el beneficio prometido? ¿Guarda desempeño del producto/servicio?»
2. **Segmentos de clientes** — «¿Ventas por tipo de cliente? ¿Ubicación o sector? ¿Lista con campos de segmento?»
3. **Flujos de ingreso** — «¿Cada venta o factura? ¿Ingresos por producto? ¿Facturación electrónica?»
4. **Canales** — «¿Canal de cada venta? ¿Analítica web o redes? ¿Lugar de entrega?»
5. **Relaciones con clientes** — «¿Soporte, garantías, mantenimiento? ¿Reseñas o satisfacción? ¿Renovaciones?»
6. **Actividades clave** — «¿Producción, instalación, servicio con fechas y sitios? ¿Mediciones de equipos? ¿Control de calidad?»
7. **Recursos clave** — «¿Inventario, equipos en campo? ¿Datos propios (sensores)? ¿Tiempo de personal?»
8. **Socios clave** — «¿Órdenes y proveedores? ¿Datos que envían socios? ¿Contratos de propiedad de datos?»
9. **Estructura de costos** — «¿Costo por unidad o proyecto? ¿Categorías contables? ¿Margen bruto desde registros?»

El BMC de ejemplo Air4U (inglés, draft) usa los mismos nueve bloques: Key partners, Key activities, Key resources, Value propositions, Customer relationships, Channels, Customer segments, Cost structure, Revenue streams, más una segunda hoja “Open questions and sources”.

**No hay**, en el pack, cajas vacías por bloque ni un PDF de lienzo en blanco para imprimir.

### B2. Hoja 1 — Mapa de calor (cuestionario ¿DÓNDE?)

**Claves (iguales en todos los bloques):**

- **S** (¿Tiene almacenamiento nombrado?): Y = «Puede decir dónde están los registros hoy»; N = «Sabe que existen pero no dónde → REO».
- **R** Confiabilidad 0–3: 0 no registrado; 1 disperso (chat, papel, memoria) — «Todo REO usa R = 1»; 2 hoja de cálculo o documento a mano; 3 sistema con campos fijos.
- **H** Historia 0–3: 0 «< 3 meses o U»; 1 «3–11»; 2 «12–23»; 3 «24 o más».
- **F** Frecuencia 0–3: 0 ninguno en 12 meses / una sola vez / U; 1 al menos una vez en 12 meses, menos que mensual; 2 al menos mensual, menos que diario; 3 diario o más.
- **A** Acceso técnico 0–3: 0 no recuperable en 1 semana o U («REO → A = 0»); 1 recuperable en 1 semana pero no como tabla, o sin responsable; 2 archivo exportable (CSV, XLSX) y responsable nombrado; 3 exportación automática o API y responsable nombrado.
- **Q** Calidad = cantidad de «sí» (0–3): Q-a completitud (9 de 10 registros con campos clave); Q-b duplicados controlados o raros; Q-c sabe qué periodos o sitios faltan. «U cuenta como No.»
- **G** Acceso legal/ético 0–3: «Desconocido / verbal / base escrita / propósito documentado» — etiqueta, no suma al puntaje.
- **M** Modo de captura: «IoT · chat · hoja de cálculo · otro».
- **L** Vínculo a VP, 0–3: «Qué tan directo mide el beneficio que promete una propuesta de valor.»

**Columnas de la tabla por bloque** (hasta 3 conjuntos):

`ID | Conjunto de datos | S | R | Meses (texto) | H | Frecuencia (texto) | F | Formato / ubicación | Responsable (rol) | A | Q-a | Q-b | Q-c | Q | G | M | L | ¿VP?`

**Verificación de contexto (2 min, una vez):**

- «¿Algún conjunto tiene datos personales (nombre, correo, teléfono)?» S / N / U
- «¿Alguno describe un sitio confidencial de cliente?» S / N / U
- «¿Alguno lo produce o guarda un socio? ¿Quién es dueño?»
- «¿Contrato, asesoría o disputa que limite algún conjunto?»

**Registro de desacuerdos:** `Bloque | Conjunto | Ítem | Fundador | Operador | Nota`. Pie: Equipo, Fecha.

(La fórmula de puntaje D = 2R+H+F+A+Q y las bandas COLD/WARM/HOT viven en la rúbrica de staff, no en la Hoja 1 de equipo. La agenda sí menciona «Calificación CTH y mapa en el lienzo».)

### B3. Hoja 2 — Tarjeta de flujo + escalera (cuestionario ¿QUÉ?)

**Parte A — una tarjeta por bloque elegido:**

| # | Pregunta |
|---|---|
| A1 | Bloque(s) e ID de datos |
| A2 | Nombre del flujo (verbo + objeto) |
| A3 | Evento disparador |
| A4 | Pasos (3–8 numerados) |
| A5 | Actores (roles, no nombres) |
| A6 | Sistemas / dispositivos |
| A7 | Campos que produce un registro |
| A8 | Unidad y granularidad |
| A9 | Frecuencia y volumen (U si no sabe) |
| A10 | Controles de calidad / calibración |
| A11 | Huecos y pasos manuales |
| A12 | Propiedad, consentimiento, límites legales («Escriba **ABIERTO** si hay duda») |
| A13 | Capa sandbox: Delta / Línea base / Paisaje |
| A14 | **Tarea + audiencia (obligatorio)** — «[tarea] para [audiencia]» |
| A15 | Desacuerdos fundador / operador |

**Parte B — S o N; U = N.** El nivel es el más alto donde todo es S y las gradas inferiores también.

- Bronce: B1 registros crudos sin alterar; B2 fecha-hora; B3 ID de origen; B4 unidades en campos numéricos; B5 almacenamiento nombrado y responsable (sin REO); B6 derechos por escrito (G ≥ 2); B7 exportación estructurada (A ≥ 2).
- Plata: S1 reglas de limpieza escritas; S2 validación contra referencia; S3 unidades y zona horaria estandarizadas; S4 completitud, duplicados y huecos medidos (Q = 3); S5 diccionario de datos; S6 datos personales o confidenciales anonimizados.
- Oro: G1 tarea + audiencia en A14; G2 referencia o benchmark aplicado; G3 nivel de agregación fijo; G4 dueño aprobó compartir con esa audiencia; G5 pasos documentados para repetir; G6 capa sandbox etiquetada; G7 sin asuntos legales ABIERTOS en A12; G8 sin tablero público si derechos abiertos; G9 si combina capas: riesgo de reidentificación revisado.

Niveles: Ninguno / Bronce / Plata / Oro.

**Plantilla de tarjeta de flujo (cita):**

```
TARJETA DE FLUJO · Equipo: ______ · Fecha: ______
Bloque(s) / ID datos : ______________________
Flujo              : ______________________________
Disparador         : ______________________________
Línea Data Flows   : Disparador → Captura [sistema] → Almacén [Bronce]
                     → Limpiar [Plata] → Referencia [Oro] → Tarea + audiencia [A14]
Nivel alcanzado    : Ninguno / Bronce / Plata / Oro
Siguiente grada    : Los «N» de la siguiente grada: ______________
```

Hay una **tarjeta de arranque** aparte, «solo si en Bloque 1 ningún bloque quedó tibio/caliente con vínculo VP ≥ 2».

### B4. Hoja 3 — De dato a valor

Reglas previas: un usuario, una decisión; «Número firme solo con Plata»; tres paneles sandbox (Línea base / Delta / Paisaje); «Sin tablero público» si derechos abiertos; cada número apunta a un ID (D1…) y a la tarjeta de Hoja 2.

1. Usuario: Rol / cargo; Tipo de organización; Qué debe decidir esta semana.
2. Decisión, una frase: «¿Debe [acción] antes de [cuándo]?»
3. Dos o tres preguntas: P1, P2, P3 (opcional).
4. Dos o tres números — columnas: `Métrica (unidad) | Responde | ID datos | Grada Medallion | Mostrar como | Panel`. Mostrar como: «firme / **estimado**». Panel: «Línea base / Delta / Paisaje».
5. Valor (una frase): «Dinero, riesgo, tiempo o salud».
6. Audiencia: Quién puede ver; Quién no debe ver; ¿Tablero público? — «**No** mientras haya derechos abiertos».
7. Boceto ASCII de tres paneles + «Decisión esta semana» + Usuario + Valor.
8. Autocontrol (cinco casillas): ID y tarjeta Hoja 2; ningún firme sin Plata u Oro; cada número con panel; derechos abiertos ⇒ sin tablero público; si combina paneles en un mapa, revisó G9.

### B5. Hoja 4 — Plantilla de tablero (y 4b ejemplo)

Encabezado: Usuario (rol, no nombre); Decisión («¿debe [acción] antes de [cuándo]?»).

Cada uno de los tres paneles (1 Línea base del cliente, 2 Delta del innovador, 3 Panorama de datos abiertos) pide: Valor; Rango (o +/-); Unidad; Fuente (ID datos / tarjeta Hoja 2, o enlace en el panel 3); Grada escalera (Ninguno / Bronce / Plata / Oro); Confianza (firme / estimado); Por qué (una línea).

Puente: Entradas = «Línea base del cliente **+** Panorama de datos abiertos»; Salida = «Delta del innovador»; Hacia el pie = «Delta innovador **→** línea de valor».

Mapa o antes/después, con «Notas de confidencialidad (sin reidentificar)».

Pie: «Línea de valor (una frase: dinero, riesgo, tiempo o salud)». Texto fijo, no borrar: *«sin tablero público mientras los derechos de datos estén abiertos»*.

### B6. Hoja 5 — Pitch 5 min (PR #172; no está aún en el zip)

Intro 5a: «Complete cada bloque para las finales de las 16:00. Los jueces puntúan Parte A utilidad y Parte B honestidad (0–5 cada una). Marque estimado si la grada no es Plata+. Seis equipos presentan. Si empatan en utilidad y honestidad, desempata la historia.»

| Bloque | Preguntas guía | Caja | Tiempo |
|---|---|---|---|
| 1. Problema | «¿Quién es el usuario y qué decisión debe tomar esta semana?» «¿Qué costo tiene no decidir?» | «[Usuario] — [Decisión en una frase]» | ~0:45 |
| 2. Datos usados | «¿Qué fuentes enlazó en el mapa de calor y Hoja 4?» «¿Cobertura temporal/espacial y huecos?» | «Fuentes: … · Cobertura: … · Calidad (firme/estimado): …» | ~1:15 |
| 3. Tablero / hallazgo | «¿Qué ve el usuario en diez segundos?» «¿Cuál es la cifra clave y su confianza?» | «Pantalla: … · Cifra clave: …» | ~2:00 |
| 4. Impacto | «¿Quién se beneficia del delta?» «¿Magnitud u orden de magnitud con fuente?» | «Beneficiario: … · Magnitud: [dato del equipo]» | ~3:00 |
| 5. Próximo paso | «¿Qué piden a 30 días para subir grada?» «¿Qué validan a 90 días?» | «30 días: … · 90 días: …» | ~4:00 |

### B7. Carpeta Drive (cuando el facilitador la active)

```
01_crudo          ← exportaciones sin alterar (Bronce)
02_limpio         ← tablas ya limpiadas (Plata)
03_hojas_de_datos ← Hojas 1–4 diligenciadas (.md o Docs)
04_dashboard      ← Hoja 4 / boceto de pantalla
05_pitch          ← diapositivas o guion de finales (solo si avanzan)
```

No hay un “dataset card” como documento aparte: la **tarjeta de flujo** de Hoja 2 es esa pieza.

---

## C. Huecos, duplicados y versiones que chocan

### Huecos (se menciona o se necesita, y no está listo para entregar)

1. **Plantilla BMC en blanco.** El método arranca en el lienzo y el Paso 0 de prompts lo asume, pero no hay hoja/PDF/Doc de 9 bloques vacíos en español.
2. **Hoja 5 (pitch) fuera del pack.** Gideon la pidió el 22 nov «for Team pack»; sigue en el PR #172. El zip v0.3-es llega solo hasta Hoja 4. El deck publicado (diapositiva 15) enumera hojas 1–4, agenda, derechos, fuentes y prompts; no nombra Hoja 5.
3. **PDF de prompts completo.** Ya existe `prompts-ia.pdf` (5 prompts), pero no cubre Hoja 4 campo a campo, ni Hoja 5, ni un prompt específico de “pegue la hoja y la info de su proyecto, devuelva la hoja llena”. La prueba de escritorio ya había marcado F5: «`prompts-ia.md` sin paso “selección de bloques”».
4. **El pack no se ha entregado.** Drive solo CTH. Gmail de 3 semanas sin envío a equipos/Marlene. El deck en vivo dice que “cada equipo recibe hoy el paquete”, pero el zip sigue interno. Falta el GO de Gideon para enviar o imprimir.
5. **Agenda-equipos desfasada.** Horas `[confirmar]`, embudo **20 equipos**, mañana arranca en “Registro y revisión del BMC”. La agenda pública del 23 nov pone charlas hasta ~10:45/11:00, 14 equipos Externado, y un orden distinto (Observatorio, sandbox Air4U, etc.). El deck publicado repite el embudo 20→6→3 y las horas por confirmar.
6. **Carpeta Drive por equipo y correo CTH.** La guía es solo plantilla; el correo institucional para compartir está en `[confirmar]` (`test-notes` F, guía).
7. **Revisión Legal** de `nota-derechos-datos.md` (sigue como borrador).
8. **Fuentes abiertas de otros sectores.** La lista está centrada en aire (piloto Air4U). F6 de test-notes ya lo señaló. La oferta de Croma (SIATA/CREG/RMCAB) no está en la hoja de fuentes.
9. **Cuestionario de IA en línea.** La memoria del 23 nov habla de un PDF CTH como alternativa de baja tecnología. El PDF de hojas existe; no hay un cuestionario web listo como canal oficial para los 14 equipos.
10. **`test-notes` va dentro del zip de equipos** (incluye el recorrido CurubaTech). Conviene sacarlo antes de cualquier entrega.
11. El deck publicado incluye la frase «Sin costo de entrada en el piloto». La regla de copy del desk es no decir que el evento es gratis; conviene revisarlo antes de pasarlo a mesas.

### Duplicados o versiones en conflicto

1. **Tres zips** `team-pack-es-pdfs.zip` en Drive: uno de 142 B (21 nov 20:32 UTC, probablemente vacío), uno de 227 KB (23:35) y el canónico de 283 KB (22 nov 00:01, sha256 `eb84f2ae…`). Usar solo este último.
2. **PDFs de Hoja 4 y 4b repetidos** varias veces en la misma carpeta Drive (mismos tamaños 27213 / 29828 bytes).
3. **BMC Air4U vigente vs. “ZZZ SUPERSEDED — with sandbox fees”.** No reenviar la superada.
4. **Maestros EN v0.1 vs v0.2/v0.3.** El CHANGELOG avisa que v0.1 no es comparable (otra escala). El pack ES sigue a v0.2/v0.3.
5. **Deck de equipos:** build publicado `7de09c90` (18 páginas, en vivo) vs. PR #167, que más adelante habla de PDFs de 21 páginas. La URL en vivo es la de 18 páginas.
6. **Tres agendas:** `agenda-equipos` v0.3-es; `datathon-agenda.md` en inglés (Drive/box); agenda pública v2–v5 (PR #176). No coinciden en horas ni en el número de equipos.
7. **Prompts:** el PDF corto que ya existe vs. el PDF ampliado que pide Gideon (sección D, borrador).
8. Etiquetas EN en la rúbrica (HEARSAY, LEGAL ACCESS UNCLEAR…) vs. ES en las hojas (REO, acceso legal, acceso técnico, calidad). El deck mezcla “LEGAL? / TECH? / QUALITY?”. `test-notes` F2 ya lo había marcado.

---

## D. Esquema propuesto del «PDF de prompts» (borrador)

Un PDF CTH, en español, una sección por entregable. Cada sección: propósito, qué debe pegar el equipo, y un prompt para copiar y pegar (ChatGPT / Gemini / Claude). Todos los prompts de abajo son **borrador**; no se envían ni se publican con este inventario. Parten de `prompts-ia.md` v0.3-es y se completan con los campos exactos de las hojas 4 y 5.

**Portada / reglas comunes (repetir al inicio):** marcar lo desconocido como **U**; **no inventar números ni cifras**; usar roles, no nombres personales; si los derechos siguen abiertos, tablero público = No; firme solo con Plata u Oro; revisar siempre la salida en equipo.

### 0. Lienzo BMC (9 bloques)

- **Propósito:** armar el punto de partida del día (VP1, VP2… y los 9 bloques de B1).
- **El equipo pega:** pitch, web o notas de su proyecto (texto).
- **Prompt (borrador):** ampliar el Paso 0 actual, pidiendo salida en markdown con exactamente estos encabezados: Propuestas de valor (lista VP1, VP2…), Segmentos de clientes, Flujos de ingreso, Canales, Relaciones con clientes, Actividades clave, Recursos clave, Socios clave, Estructura de costos; y una lista final «U — validar con el equipo».

```
Eres asistente de un equipo en el Datatón del Observatorio de la Tierra (CleantechHUB, 24 nov 2026).
A partir del siguiente texto de nuestro proyecto o pitch (péguelo aquí), arme un Lienzo de Modelo de Negocio de 9 bloques en español colombiano, breve.

Use exactamente estos encabezados, en este orden:
1. Propuestas de valor (empiece listando VP1, VP2…)
2. Segmentos de clientes
3. Flujos de ingreso
4. Canales
5. Relaciones con clientes
6. Actividades clave
7. Recursos clave
8. Socios clave
9. Estructura de costos

Reglas:
- No invente cifras de ventas, clientes ni impacto; cite solo lo que el texto dice.
- Lo que falte, marque «U — validar con el equipo».
- No use nombres personales ni teléfonos; use roles (por ejemplo «gestor de instalaciones», «comprador corporativo»).
Salida: markdown con los 9 bloques y, al final, la lista de ítems U.
```

### 1. Hoja 1 — Mapa de calor

- **Propósito:** ubicar dónde hay datos en los 9 bloques, con códigos y etiquetas, sin excluir en la mañana.
- **El equipo pega:** su BMC en markdown (y, si hay, dos versiones fundador/operador).
- **Prompt (borrador):** el Paso 1 actual, más la tabla exacta de columnas de B2 y las cuatro preguntas de verificación de contexto. Etiquetas: REO, acceso legal, acceso técnico, calidad, copia maestra.

### 2. Hoja 2 — Flujo y escalera

- **Propósito:** describir el flujo que produce los datos y calcular (no declarar) el nivel Ninguno / Bronce / Plata / Oro.
- **El equipo pega:** Hoja 1 diligenciada, y si CTH ya eligió bloques, esa lista (cierra F5).
- **Prompt (borrador):** el Paso 2 actual, exigiendo A1–A15, las casillas B1–B7, S1–S6 y G1–G9, la plantilla «TARJETA DE FLUJO» al pie, y la tarjeta de arranque solo si ningún bloque quedó tibio/caliente con L ≥ 2. A12 = ABIERTO si hay duda.

### 3. Hoja 3 — De dato a valor

- **Propósito:** una decisión para un usuario, con 2 o 3 números trazables y un boceto de tres paneles.
- **El equipo pega:** la tarjeta de Hoja 2.
- **Prompt (borrador):** el Paso 3 actual, con las ocho secciones de B4 y el autocontrol de cinco casillas. Si no hay cifra en los datos: «valor no declarado (estimado)».

### 4. Hoja 4 — Plantilla de tablero

- **Propósito:** pasar la Hoja 3 a la plantilla imprimible de una pantalla (campos de valor, rango, unidad, fuente, grada, confianza, por qué).
- **El equipo pega:** Hoja 3 completa (no números nuevos).
- **Prompt (borrador):** sustituye el Paso 4 genérico («mejore el boceto») por una salida que llene, campo a campo, encabezado, tres paneles, puente, mapa o antes/después, y el pie con el texto fijo de derechos. No agregar números que no estén en la Hoja 3.

```
Tome nuestra Hoja 3 (péguela abajo) y llene la plantilla de tablero (Hoja 4) del Datatón CTH, en español colombiano.
No agregue números nuevos; solo reorganice lo que ya está.

Estructura obligatoria:
- Encabezado: Usuario (rol, no nombre) y Decisión en la forma «¿Debe [acción] antes de [cuándo]?».
- Panel 1 Línea base del cliente, Panel 2 Delta del innovador, Panel 3 Panorama de datos abiertos. En cada panel: Valor, Rango (o +/-), Unidad, Fuente (ID de datos / tarjeta Hoja 2, o enlace en el panel 3), Grada (Ninguno / Bronce / Plata / Oro), Confianza (firme / estimado), Por qué (una línea).
- Firme solo si la grada es Plata u Oro; si no, estimado.
- Puente de valor: entradas = línea base + panorama; salida = delta; hacia el pie = delta → línea de valor.
- Mapa (varios sitios) o antes/después (un sitio), con nota de confidencialidad (sin reidentificar).
- Pie: una frase de valor (dinero, riesgo, tiempo o salud). Incluya este texto fijo, sin borrarlo: «sin tablero público mientras los derechos de datos estén abiertos».
```

### 5. Hoja 5 — Pitch de 5 minutos

- **Propósito:** guion de finales (16:00) en los cinco bloques de la plantilla, alineado a utilidad y honestidad.
- **El equipo pega:** Hojas 1–4 (y el boceto).
- **Prompt (borrador, la hoja aún está en PR #172):**

```
Usando nuestras Hojas 1 a 4 (péguelas abajo), redacte el pitch de 5 minutos del Datatón CTH en español colombiano, con exactamente estos cinco bloques y sus cajas:

1. Problema (~0:45). Caja: «[Usuario] — [Decisión en una frase]». Deje claro qué costo tiene no decidir.
2. Datos usados (~1:15). Caja: «Fuentes: … · Cobertura: … · Calidad (firme/estimado): …».
3. Tablero / hallazgo (~2:00). Caja: «Pantalla: … · Cifra clave: …».
4. Impacto (~3:00). Caja: «Beneficiario: … · Magnitud: …». Si no hay magnitud en las hojas, escriba «[dato del equipo]» y no invente.
5. Próximo paso (~4:00). Caja: «30 días: … · 90 días: …» para subir grada. Si los derechos siguen abiertos, no proponga tablero público.

Reglas: no invente cifras; marque estimado si la grada no es Plata+; use roles, no nombres personales. Al final, una línea de autocontrol: qué sale de las hojas y qué quedó en U.
```

### 6. Prompt transversal: de las hojas-cuestionario a respuestas con datos del proyecto

- **Propósito:** lo que Gideon pidió de forma explícita: que la IA tome *nuestras* hojas (las preguntas) y la información del proyecto, y devuelva las hojas ya diligenciadas en la estructura exacta.
- **El equipo pega:** (a) el texto de la hoja (1, 2, 3 o 4) o el BMC; (b) pitch, notas, exportaciones o capturas (sin datos personales).
- **Prompt (borrador):**

```
Voy a pegar, en este orden: (1) una hoja o cuestionario del Datatón CleantechHUB, sin rellenar, y (2) información de nuestro proyecto (texto, tablas o notas).
Diligencie esa hoja en español colombiano, respetando el orden de secciones, tablas y códigos de la hoja. No cambie nombres de campos ni invente filas que la hoja no pida.

Reglas:
- Si un dato no está en (2), ponga U o «valor no declarado (estimado)». No invente meses de historia, frecuencias, exportaciones, contratos, consentimientos ni cifras de sensores.
- Códigos: use solo los de la hoja (S, R, H, F, A, Q, G, M, L, o S/N de la escalera). U cuenta como N en la escalera.
- Si hay duda de propiedad o consentimiento, ponga ABIERTO en A12 y tablero público = No.
- Firme solo con Plata u Oro.
- Sin nombres personales, teléfonos ni sitios exactos de hogar; use roles.
Al final, liste: (a) campos que llenó con evidencia de (2), y (b) campos U o ABIERTO que el equipo debe validar en sala.
```

**Cómo usarlo el día del evento:** mañana, prompts 0 y 1 (y el transversal con Hoja 1); tarde, 2, 3 y 4; a partir del anuncio de finalistas, prompt 5. El facilitador recuerda: la IA acelera la redacción; la grada se calcula con las casillas, no se declara.

**Siguiente paso sugerido (no hecho en este inventario):** con un GO, ampliar `prompts-ia.md` a este esquema, meter Hoja 5 en el pack cuando se apruebe el PR #172, sacar `test-notes` del zip de mesas, alinear `agenda-equipos` a la agenda pública, y recién entonces enviar o imprimir.

---

*Fin del inventario. 23 nov 2026, tarde, hora de Bogotá (America/Bogota).*
