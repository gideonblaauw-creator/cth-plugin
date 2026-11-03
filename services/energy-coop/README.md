# Energy Coop — desk artifacts in `cth-plugin`

The live **Energy Coop** app (`energiacoop.cleantechhub.net`, map at `/casos`) is **not** in this repository. Per `docs/cursor-projects.md`, **CTH-Energy-Coop** is Lane B (`cth-matters` + VPS worker). Operational source lives on the VPS, not in GitHub from this agent’s access.

## Where the Promigas demo belongs in production

Copy or symlink:

```text
services/energy-coop/demo-promigas/   →   <energy-coop-app>/public/demo-promigas/
```

Then expose a static route **`/demo-promigas/`** (trailing slash) without changing `/casos`. See `demo-promigas/INTEGRATION.md`.

## Local preview (this PR)

```bash
cd services/energy-coop/demo-promigas
python3 -m http.server 8765
# open http://127.0.0.1:8765/  (Leaflet tiles need network; no API keys)
```

Navigation: **← →** arrow keys, **Espacio** / **Enter**, or on-screen controls.
