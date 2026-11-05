# Dataroom branding (host Caddy, not Docmost image)

Docmost 0.96 ships a hardcoded product shell (`<title>Docmost</title>`, default favicons, navbar text in the client bundle). Workspace name/logo in Docmost settings cover the signed-in header but not the static shell.

## Deploy on VPS

```bash
sudo install -d -m 755 /opt/cth-dataroom-branding/{www,icons}
sudo cp -r docs/infra/dataroom-branding/* /opt/cth-dataroom-branding/
sudo chmod +x /opt/cth-dataroom-branding/sync-branded-shell.sh
sudo /opt/cth-dataroom-branding/sync-branded-shell.sh
```

Re-run `sync-branded-shell.sh` after Docmost upgrades (asset hash in `index.html` changes).

## Caddy

Site file: `docs/infra/caddy/dataroom.cleantechhub.net.caddy` — serves the branded SPA shell for all HTML routes including `/share/*` (Docmost assets still proxied), overrides `/icons/*`, and serves `rein-brand.css` + `rein-debrand.js` (REIN colors, logo header, hide “Powered by Docmost”). No `replace_response` module required.

After deploy, re-run `sync-branded-shell.sh` so `www/index.html` picks up new asset hashes if Docmost was upgraded.
