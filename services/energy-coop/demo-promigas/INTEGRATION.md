# Integrar `/demo-promigas` en la app Energy Coop

Objetivo: ruta nueva **`https://energiacoop.cleantechhub.net/demo-promigas/`** sin romper **`/casos`**.

## Opción A — estático en `public/` (Vite, CRA, o servidor estático)

1. Copiar la carpeta `demo-promigas/` completa al `public/` del repo de la app:
   - `public/demo-promigas/index.html`
   - `public/demo-promigas/assets/` (si se añaden más tarde)
2. En **Caddy/nginx** del sitio, servir `/demo-promigas/*` como archivos estáticos (igual que otros assets).
3. Enlazar desde el menú interno solo si Gideon aprueba (HITL); este PR no despliega.

## Opción B — ruta en framework

**Next.js (App Router):** `app/demo-promigas/page.tsx` que reexporte un iframe a `/demo-promigas/index.html` en `public`, o migre el markup a un componente React (Leaflet: `react-leaflet`, mismos tiles OSM).

**React Router:** ruta `<Route path="/demo-promigas/*" element={<StaticDemo />} />` sirviendo el HTML embebido o redirigiendo a `index.html`.

## Coexistencia con `/casos`

- No reutilizar el bundle de `/casos` para esta demo en el PR; la demo es **autocontenida** para revisión en GitHub.
- Tras integrar, compartir solo estilos/tokens CTH si el app ya los tiene; evitar duplicar lógica de pins rojos de `/casos` hasta un refactor explícito.

## Despliegue (fuera de alcance de este PR)

1. Merge del PR en el repo que **posee** la app Energy Coop (VPS / repo Lane B).
2. Build o copia estática al contenedor/servidor que sirve `energiacoop.cleantechhub.net`.
3. Verificar TLS y que `/casos` sigue respondiendo 200.
4. Ensayo en sala: ~2 min, teclado + clic, red solo para tiles OSM.
