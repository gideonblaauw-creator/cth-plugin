# Deck workspace

Built with `tools/reveal`.

`deck-meta.json` → `"gated": true` is a **label only** (default for new decks). **Enforcement** is Caddy + oauth2-proxy on the decks server. Public on `decks.cleantechhub.net` needs **Gideon GO per slug** plus an Infra **Caddy** change — not something this repo metadata controls.

```bash
../../tools/reveal/build.sh <slug>
```

Output: `dist/` (static site) and `<slug>.pdf` in this folder.
