# Docusaurus fallback (NCUK `/ncuk`)

Build on the VPS or CI, deploy `build/` to `NCUK_FALLBACK_ROOT`, set `NCUK_ROOM_MODE=fallback` in `caddy.env`.

```bash
npm ci
npm run build
```

Output: `build/` with `baseUrl` `/ncuk/`. Same Caddy Basic Auth as Docmost primary.

REIN colours: `#335d4f`, `#ff6633`, `#666666` in `src/css/custom.css`.
