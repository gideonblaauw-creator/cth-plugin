# Nexus CO₂ impact deck (draft)

Interactive CleantechHUB deck for self-reported startup CO₂ figures from `research/nexus-co2/co2.csv`.

- **Format:** CTH interactive deck protocol (same house as [cth-clp26-rein](https://decks.cleantechhub.net/cth-clp26-rein/)): 1920×1080 stage, glass cards, index, dots, optional questions toggle. Shell copied from in-repo reference `decks/meetings-2026-10-13/b4b` on branch `meetings-2026-10-13-b4b` (live CLP26 REIN source is on VPS, not vendored here).
- **Brand:** CleantechHUB HTML deck tokens (`--deep`, `--cyan`, `--green`, Open Sans) per `skills/cth-html-deck` / Manual de Marca — not the WordPress green block.
- **Publish:** Do not deploy to `decks.cleantechhub.net/nexus-co2/` without Gideon's GO.

## Build

```bash
cd decks/nexus-co2 && ./build.sh
```

## Local preview

Open `index.html` in a browser. Print-all slides: `?print=1`.

## Screenshots (1440×900)

```bash
python3 capture-slides.py
```
