# Deck workspace

Built with `tools/reveal`.

`deck-meta.json` → `"gated": true` is a **label only** (default for new decks). **Enforcement** is Caddy + oauth2-proxy on the decks server. Public on `decks.cleantechhub.net` needs **Gideon GO per slug** plus an Infra **Caddy** change — not something this repo metadata controls.

## Build (this deck)

Install once (QR on the closing slide):

```bash
python3 -m pip install 'qrcode[pil]'
```

```bash
../../tools/reveal/outline.sh --force --skip-build "$(pwd)/deck.yaml"
./post-process.sh   # strips catalog Example placeholders, QR, Spanish fuente
../../tools/reveal/build.sh cth-advisory-board-4q26
../../tools/reveal/lint.sh cth-advisory-board-4q26
```

Output: `dist/` (static site) and `cth-advisory-board-4q26.pdf` in this folder.