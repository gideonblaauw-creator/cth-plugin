# Prompts de IA para el Datatón (copiar y pegar)

Cada prompt pide a la IA que **marque lo desconocido como U** y **no invente números**. Revise siempre la salida con su equipo.

---

## Paso 0 — BMC desde el pitch

```
Eres asistente de un equipo en un datatón de calidad del aire en Bogotá.
A partir del siguiente texto de pitch (pegue aquí), arme un Lienzo de Modelo de Negocio de 9 bloques en español colombiano, breve.
Reglas:
- No invente cifras de ventas, clientes ni impacto; cite solo lo que el texto dice.
- Lo que falte, marque «U — validar con el equipo».
- No use nombres personales ni teléfonos; use roles (ej. «productor», «comprador corporativo»).
- Liste VP1, VP2… al inicio del bloque Propuestas de valor.
Salida: markdown con los 9 bloques.
```

---

## Paso 1 — Hoja 1 mapa de calor

```
Ayúdeme a diligenciar la Hoja 1 (mapa de calor de datos) del datatón CTH.
Adjunto: nuestro BMC en markdown.

Para cada bloque del BMC, proponga hasta 3 conjuntos de datos (D1, D2, D3) con códigos S, R, H, F, A, Q, G, M, L según las definiciones de la hoja.
Reglas:
- Si el pitch no dice dónde se guarda, use S=N, R=1, A=0 y etiqueta REO.
- No invente meses de historia, frecuencia ni exportaciones.
- Marque U donde falte evidencia.
- Separe fundador vs operador solo si yo pegue dos versiones de respuestas.

Salida: tabla por bloque en markdown, más lista de etiquetas (REO, acceso legal, acceso técnico, calidad, copia maestra).
```

---

## Paso 2 — Hoja 2 escalera Medallion

```
Con base en nuestra Hoja 1 diligenciada (pegue abajo), ayúdeme con la Hoja 2:
1) Elija el flujo VP principal o justifique tarjeta de arranque.
2) Complete A1–A14 en español breve.
3) Evalúe Bronce, Plata y Oro con S/N; U cuenta como N.
4) Indique nivel alcanzado y el siguiente ítem «N» a trabajar esta tarde.

Reglas: no invente contratos, exportaciones CSV ni consentimientos. Marque ABIERTO en A12 si hay datos personales sin base escrita.
Salida: tarjeta de flujo en el formato de plantilla de la hoja.
```

---

## Paso 3 — Hoja 3 de dato a valor

```
Usando nuestra tarjeta Hoja 2 (pegue abajo), complete la Hoja 3:
- Un usuario (rol), una decisión, 2–3 preguntas, 2–3 números.
- Cada número: grada Medallion real, mostrar como firme solo si Plata/Oro, si no «estimado».
- Panel sandbox: Línea base, Delta o Paisaje.
- Boceto ASCII de tres paneles.

Reglas: no invente valores de sensores ni PM2.5. Si no hay número en los datos, escriba «valor no declarado (estimado)».
Si derechos abiertos, tablero público = No.
```

---

## Paso 4 — Boceto de tablero (refinar)

```
Tome mi Hoja 3 (abajo) y mejore el boceto de una pantalla para impresión A4:
- Tres columnas: Línea base, Delta, Paisaje.
- Cada métrica con (firme) o (estimado) y la grada [Ninguno/Bronce/Plata/Oro].
- Una línea de decisión y una de valor.
- Texto en español colombiano, sin nombres de clientes.
No agregue números nuevos; solo reorganice lo que ya está.
```

---

**Equipo:** _______________  **Fecha:** _______________