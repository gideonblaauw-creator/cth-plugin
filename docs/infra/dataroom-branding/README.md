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

Site file: `docs/infra/caddy/dataroom.cleantechhub.net.caddy` — serves branded shell for `/` and `/login`, overrides `/icons/*`, and serves `rein-debrand.js` (MutationObserver text/title patch). No `replace_response` module required.
