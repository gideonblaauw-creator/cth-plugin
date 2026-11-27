# Run 5 diff notes

Start SHA: `e60ec3bf5e436d9fb3f4394600737e33a2b5b4ee`. Head SHA (run 5 tip): `ac65166fa4e7ec7818a71c6e8873c53121e28ec0` (pack rebuild in `f1bd1f15c72f67f55f9e6778dc2ebb90e65a8def`).

## pdffonts q_pdf
```
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
BAAAAA+OpenSans-Bold                 TrueType          WinAnsi          yes yes yes    548  0
CAAAAA+OpenSans-Regular              TrueType          WinAnsi          yes yes yes    558  0
DAAAAA+OpenSans-Italic               TrueType          WinAnsi          yes yes yes    553  0
EAAAAA+NotoColorEmoji                Type 3            Custom           yes yes yes    561  0
```
## pdffonts ej_pdf
```
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
BAAAAA+OpenSans-Bold                 TrueType          WinAnsi          yes yes yes    496  0
CAAAAA+OpenSans-Regular              TrueType          WinAnsi          yes yes yes    501  0
DAAAAA+NotoColorEmoji                Type 3            Custom           yes yes yes    504  0
```
## pdffonts guia_pdf
```
name                                 type              encoding         emb sub uni object ID
------------------------------------ ----------------- ---------------- --- --- --- ---------
BAAAAA+OpenSans-Bold                 TrueType          WinAnsi          yes yes yes   1637  0
CAAAAA+OpenSans-Regular              TrueType          WinAnsi          yes yes yes   1652  0
DAAAAA+OpenSans-Italic               TrueType          WinAnsi          yes yes yes   1647  0
EAAAAA+OpenSans-BoldItalic           TrueType          WinAnsi          yes yes yes   1642  0
```
## Glyph scan (OpenSans-Regular cmap)
Script: `scripts/run5_self_check.py` (this file).
Result: 0 out-of-cmap glyphs in all PDF pages and docx (except emoji + whitespace).
## Embedded font proof (guia.pdf OpenSans-Regular 'g')
- Font name table: `Open Sans Regular`
- Subset glyph(s) with same contour topology as committed `g`: **['glyph00026']** (match=True)
- Any subset glyph matching DejaVu `g` topology: **False** (expect False)
- 200 dpi crop: `_png/run5/glyph-g-line-200dpi.png` (page 19)
## Character counts
```
q_docx docx: {'arrow': 0, 'checkbox': 0, 'sgl': 2, 'boxdraw': 0, 'tri': 0}
ej_docx docx: {'arrow': 0, 'checkbox': 0, 'sgl': 2, 'boxdraw': 0, 'tri': 0}
guia_docx docx: {'arrow': 0, 'checkbox': 0, 'sgl': 22, 'boxdraw': 0, 'tri': 0}
q_pdf pdf text: {'arrow': 0, 'checkbox': 0, 'sgl': 2, 'boxdraw': 0, 'tri': 0}
ej_pdf pdf text: {'arrow': 0, 'checkbox': 0, 'sgl': 2, 'boxdraw': 0, 'tri': 0}
guia_pdf pdf text: {'arrow': 0, 'checkbox': 0, 'sgl': 18, 'boxdraw': 0, 'tri': 0}
total › in docx (python-docx; merged Word cells counted once per cell): 26
total › in pdftotext (q+ej+guía): 22 (20 arrow swaps + 2 in puente table line)
```
## fc-match
```
OpenSans-Regular.ttf: "Open Sans" "Regular"
OpenSans-Bold.ttf: "Open Sans" "Bold"
```
Resolved paths (after `fonts/install-fonts.sh`): `~/.local/share/fonts/cth-open-sans/OpenSans-Regular.ttf`, `OpenSans-Bold.ttf`.

## pdfinfo pages
- q.pdf: 7
- ej.pdf: 6
- guía.pdf: 55
## sha256
| id | file | sha256 |
|---|---|---|
| q_docx | Cuestionario-Dataton-24nov-equipos.docx | `0ed244fa80725d0c26ace921c08bf243927ddfa916dd4b8ac989ef13d4ae8a5a` |
| ej_docx | Cuestionario-ejemplo-Air4U.docx | `c0294707fa982d9eee32626797738d34a3d4dff985cdb352b91b8dcf145dfea6` |
| guia_docx | Guia-tecnica-mentores.docx | `443a9fffa0465aaa9c8434a4f2d78c5a33d355dcd068b4a6f807717f436c91fe` |
| q_pdf | Cuestionario-Dataton-24nov-equipos.pdf | `df28f7a25159f7dc516fc171329081a6c86fc75aea3d051bf7cb39debadc503d` |
| ej_pdf | Cuestionario-ejemplo-Air4U.pdf | `ea4bfa7a19bdc0e475268e11ac00d3ac0278305b245ec16e71a100fe40d245da` |
| guia_pdf | Guia-tecnica-mentores.pdf | `c680b8a268f45e58e6047c319af9ae7af5f9127ce94a845f42c7a52642656ac6` |
| prompts | prompts.txt | `e325f2f5e8d60547a5ffd1047dbe241b23e071d2e763e7149f5a77f186424015` |
| zip | team-pack-es-pdfs-v0.4.zip | `7bc0e8fbe4b2cc6a6318c4239df3df525ee7ad8cf8bd3bf733c03eda0059e6b0` |
| OpenSans-Bold.ttf | OpenSans-Bold.ttf | `27da758f4dcac9a65abe914c13b463b42982b9909bc65713424099f4810bd1e6` |
| OpenSans-BoldItalic.ttf | OpenSans-BoldItalic.ttf | `d672a770037104b6af45e1336b3d3c1729c8aea940f81e010f5a8a7319c29a21` |
| OpenSans-Italic.ttf | OpenSans-Italic.ttf | `93bc1bb6abf4e6b7c75d7131714061d5b57cc478abcabe4cb3519bb38fb917aa` |
| OpenSans-Regular.ttf | OpenSans-Regular.ttf | `c53aceea2dcf5b4098099c0c4d0a061d17e178a049317b42a422b1a9f7f8eb59` |
| OpenSans-SemiBold.ttf | OpenSans-SemiBold.ttf | `4a413711684a9dd564ef0f1c10cb62b5d9f7eb6df2cff962f5341a6ecd5f64ae` |
| OpenSans-SemiBoldItalic.ttf | OpenSans-SemiBoldItalic.ttf | `c646a9aefc0e964f66487260639e375685328a6280856faea3e012c43fe9c56d` |

## Docx text diff vs e60ec3bf

Only swaps, checkbox text, and the two Word table rebuilds are expected.

### decks/dataton-2026-team-pack/cuestionario/Cuestionario-Dataton-24nov-equipos.docx
```diff
--- e60ec3bf/Cuestionario-Dataton-24nov-equipos.docx
+++ run5/Cuestionario-Dataton-24nov-equipos.docx
@@ -181,7 +181,7 @@
 
 
 ¿Cuáles son los pasos en orden?
-Ejemplo: Medición → guardado en plataforma → aviso al gestor si hay alerta.
+Ejemplo: Medición › guardado en plataforma › aviso al gestor si hay alerta.
 
 
 
```

### decks/dataton-2026-team-pack/cuestionario/Cuestionario-ejemplo-Air4U.docx
```diff
--- e60ec3bf/Cuestionario-ejemplo-Air4U.docx
+++ run5/Cuestionario-ejemplo-Air4U.docx
@@ -113,7 +113,7 @@
 ¿Qué pasa para crear un registro nuevo?
 El sensor mide y la plataforma registra la lectura.
 ¿Cuáles son los pasos en orden?
-Medición → guardado en plataforma → aviso al gestor si hay alerta.
+Medición › guardado en plataforma › aviso al gestor si hay alerta.
 ¿Quién participa en cada paso?
 Sensor automático; gestor revisa y avisa a mantenimiento.
 ¿Qué herramienta usan?
```

### decks/dataton-2026-team-pack/guia-tecnica/Guia-tecnica-mentores.docx
```diff
--- e60ec3bf/Guia-tecnica-mentores.docx
+++ run5/Guia-tecnica-mentores.docx
@@ -25,7 +25,7 @@
 • Puntaje del mentor: utilidad 0–5 más honestidad 0–5, más 1 por cada número firme en plata u oro (máximo +3). En empate gana honestidad.
 • Los mentores contrastan 2–3 números con la carpeta del equipo en Drive.
 • Las finales a las 16:00 usan las mismas dos notas (utilidad, honestidad). Si hay empate, gana la mayor nota de honestidad.
-• 14 equipos → 6 finalistas → 3 ganadores, quienes entran al Datalab CTH en 2027. Todos reciben certificado.
+• 14 equipos › 6 finalistas › 3 ganadores, quienes entran al Datalab CTH en 2027. Todos reciben certificado.
 • Ningún equipo queda fuera después del Bloque 1: las etiquetas advierten, no excluyen.
 • La lista de los 6 finalistas se anuncia antes de las 16:00.
 
@@ -55,7 +55,7 @@
 2 | Al menos mensual, menos que diario |
 3 | Diario o más (incluye tiempo real) |
 Acceso técnico (A)
-0 | No recuperable en 1 semana, o U. REO → A = 0 |
+0 | No recuperable en 1 semana, o U. REO › A = 0 |
 1 | Recuperable en 1 semana, pero no como tabla; o sin responsable nombrado |
 2 | Archivo exportable (CSV, XLSX) y responsable nombrado |
 3 | Exportación automática o API y responsable nombrado |
@@ -99,7 +99,7 @@
 
 Hoja 2 — Flujo que genera datos y escalera Medallion (¿QUÉ?) · Bloque 2
 Para qué sirve
-En la mañana ubicó dónde están los datos. Ahora describe qué flujo los produce y sube la escalera Medallion: Bronce → Plata → Oro.
+En la mañana ubicó dónde están los datos. Ahora describe qué flujo los produce y sube la escalera Medallion: Bronce › Plata › Oro.
 Empezar por debajo de Bronce es normal. La tarde es la siguiente grada, no un reproche.
 Parte A — Preguntas del flujo (una tarjeta por bloque elegido)
 Parte B — Escalera Medallion
@@ -114,8 +114,8 @@
 Bloque(s) / ID datos : ______________________
 Flujo              : ______________________________
 Disparador         : ______________________________
-Línea de flujo de datos   : Disparador → Captura [sistema] → Almacén [Bronce]
-                     → Limpiar [Plata] → Referencia [Oro] → Tarea + audiencia [A14]
+Línea de flujo de datos   : Disparador › Captura [sistema] › Almacén [Bronce]
+                     › Limpiar [Plata] › Referencia [Oro] › Tarea + audiencia [A14]
 Nivel alcanzado    : Ninguno / Bronce / Plata / Oro
 Siguiente grada    : Los «N» de la siguiente grada: ______________
 
@@ -154,19 +154,14 @@
 Valor: _________________________________________________
 6. Audiencia y límites
 7. Boceto de una pantalla (tres paneles)
-┌─────────────────────┬─────────────────────┬─────────────────────┐
-│ LÍNEA BASE          │ DELTA               │ PAISAJE             │
-│  [N1] (firme/est.)  │  [N2]               │  [N3]               │
-│  nota breve         │  nota breve         │  nota breve         │
-└─────────────────────┴─────────────────────┴─────────────────────┘
-        Decisión esta semana: [una línea]
-        Usuario: [rol]          Valor: [una línea]
+Decisión esta semana: [una línea]
+Usuario: [rol] Valor: [una línea]
 8. Autocontrol antes de finales
-☐ Cada número tiene ID de datos y tarjeta Hoja 2.
-☐ Ningún número firme sin Plata u Oro.
-☐ Cada número tiene panel sandbox.
-☐ Si hay derechos abiertos: sin tablero público.
-☐ Si combina paneles en un mapa: revisó reidentificación (G9).
+[ ] Cada número tiene ID de datos y tarjeta Hoja 2.
+[ ] Ningún número firme sin Plata u Oro.
+[ ] Cada número tiene panel sandbox.
+[ ] Si hay derechos abiertos: sin tablero público.
+[ ] Si combina paneles en un mapa: revisó reidentificación (G9).
 
 Equipo: _______________ Fecha: _______________
 
@@ -182,15 +177,6 @@
 
 
 Tres paneles + puente de valor
-                    ┌──────────────────────────────────────┐
-                    │ Delta: donde el dato se vuelve valor  │
-                    │  entradas ──► salida ──► línea valor  │
-                    └──────────────────────────────────────┘
-           ▲                    ▲                    ▲
-           │                    │                    │
-  Línea base          Delta innovador         Panorama datos
-  del cliente         (su intervención)       abiertos
-     (entrada)              (salida)              (entrada)
 Panel 1 — Línea base del cliente
 Panel 2 — Delta del innovador
 Panel 3 — Panorama de datos abiertos
@@ -210,7 +196,7 @@
 Referencia de redacción: ¿Qué decisión concreta enfrentan esta semana?
 
 Tres paneles + puente de valor
-Delta: donde el dato se vuelve valor — Línea base + Paisaje → Delta → valor
+Delta: donde el dato se vuelve valor — Línea base + Paisaje › Delta › valor
 Panel 1 — Línea base del cliente · N1
 Supuestos (N1): sin lecturas de interior almacenadas en el piloto.
 Panel 2 — Delta del innovador · N2
@@ -366,7 +352,7 @@
 Estructura obligatoria:
 - Encabezado: Usuario (rol, no nombre) y Decisión «¿Debe [acción] antes de [cuándo]?».
 - Panel 1 Línea base del cliente, Panel 2 Delta del innovador, Panel 3 Panorama de datos abiertos. En cada panel: Valor, Rango (o +/-), Unidad, Fuente (ID datos / tarjeta Hoja 2), Grada (Ninguno/Bronce/Plata/Oro), Confianza (firme/estimado), Por qué (una línea).
-- Puente de valor: entradas = línea base + panorama; salida = delta; hacia el pie = delta → línea de valor.
+- Puente de valor: entradas = línea base + panorama; salida = delta; hacia el pie = delta › línea de valor.
 - Mapa o antes/después con notas de confidencialidad.
 - Pie: línea de valor + texto fijo: «sin tablero público mientras los derechos de datos estén abiertos».
 
@@ -390,7 +376,7 @@
 - Cifra firme solo con Plata u Oro.
 - Sin tablero público si derechos abiertos.
 - Marque **BORRADOR** en la salida si falta evidencia en las hojas.
-(6) Prompt transversal — cuestionario → hoja diligenciada
+(6) Prompt transversal — cuestionario › hoja diligenciada
 Propósito. La IA toma nuestra hoja en blanco y la información del proyecto, y devuelve la hoja diligenciada en la estructura exacta.
 Entradas. (1) Texto de la hoja 1, 2, 3 o 4 o BMC; (2) notas del equipo, pitch o tablas (sin datos personales).
 Formato de salida. La misma estructura de la hoja pegada, más lista (a) campos con evidencia y (b) campos U o ABIERTO a validar en sala.
@@ -424,7 +410,7 @@
 Y
 Puede decir dónde están los registros hoy
 N
-Sabe que existen pero no dónde → REO
+Sabe que existen pero no dónde › REO
 0–3
 Significado (resumen)
 0
@@ -734,6 +720,15 @@
 
 ¿Tablero público?
 No mientras haya derechos abiertos
+LÍNEA BASE
+DELTA
+PAISAJE
+[N1] (firme/est.)
+[N2]
+[N3]
+nota breve
+nota breve
+nota breve
 Campo
 Valor
 Versión equipo
@@ -756,6 +751,15 @@
 
 
 
+Delta: donde el dato se vuelve valor
+entradas › salida › línea valor
+Delta: donde el dato se vuelve valor
+entradas › salida › línea valor
+Delta: donde el dato se vuelve valor
+entradas › salida › línea valor
+Línea base del cliente (entrada)
+Delta innovador (su intervención) (salida)
+Panorama datos abiertos (entrada)
 Campo
 Respuesta
 Valor
@@ -811,7 +815,7 @@
 Salida
 Delta del innovador
 Hacia el pie
-Delta innovador → línea de valor (abajo)
+Delta innovador › línea de valor (abajo)
 Antes / sitio A
 Después / sitio B o mismo sitio tras intervención
 
```

