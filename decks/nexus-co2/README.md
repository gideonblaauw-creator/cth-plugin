# Nexus CO₂ impact deck (draft)

Interactive CleantechHUB deck for self-reported startup CO₂ figures from `research/nexus-co2/co2.csv`.

- **Format:** Same slide shell as in-repo client decks (`decks/rein-academic-city-ghana`); live [CTH CLP26 deck](https://decks.cleantechhub.net/cth-clp26/) is hosted on VPS (Appwrite) and is not vendored in this repo.
- **Brand:** CleantechHUB tokens (`#2D6A4F`, `#1B4332`, `#95D5B2`, Inter).
- **Publish:** Do not deploy to `decks.cleantechhub.net/nexus-co2/` without Gideon's GO.

## Local preview

Open `index.html` in a browser, or from repo root:

```bash
google-chrome-stable --headless --no-sandbox --disable-gpu \
  --screenshot=/tmp/nexus-co2.png --window-size=1920,1080 \
  "file://$(pwd)/decks/nexus-co2/index.html#3"
```

Print-all slides: append `?print=1` to the URL.
