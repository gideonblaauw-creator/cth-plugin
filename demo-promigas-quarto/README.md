# Promigas Energy Coop demo (Quarto)

Quarto rebuild of `services/energy-coop/demo-promigas/` (live: `https://decks.cleantechhub.net/demo-promigas/`). The original static demo is unchanged; this folder is a parallel site for review.

## Build

```bash
cd demo-promigas-quarto
quarto render
```

Output: `_site/index.html` plus `www/` assets (`i18n.js`, `app.js`).

## Preview

```bash
quarto preview
```

## Deploy (not in this PR)

Would publish `_site/` to e.g. `https://decks.cleantechhub.net/demo-promigas-quarto/` behind the same Google login (`auth.cleantechhub.net` → Caddy `rd=` redirect), matching the gating on `/demo-promigas/`. No Caddy, gating, or DNS changes in this PR.

## Quarto vs static

Interactive behaviour (Leaflet maps, hash navigation, i18n, CEOF wizard) uses the same client JS as the live demo, embedded via `include-after-body`. No OJS rewrite — full parity over Quarto-native widgets.
