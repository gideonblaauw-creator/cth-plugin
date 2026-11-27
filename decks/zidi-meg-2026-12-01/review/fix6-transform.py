#!/usr/bin/env python3
"""One-shot Fix-6 HTML transform: drop photo bleed, add hero rails, insert GIZ slides."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
text = INDEX.read_text(encoding="utf-8")

# Remove full-bleed backgrounds and scrims
text = re.sub(
    r'\n\s*<div class="fp-photo-bg"[^>]*></div>',
    "",
    text,
)
text = re.sub(
    r'\n\s*<div class="fp-photo-scrim[^"]*"[^>]*></div>',
    "",
    text,
)
text = re.sub(r'\n\s*<div class="fp-programme-card__scrim"></div>', "", text)

HERO_BY_FRAGMENT = [
    ("fp-cover", "assets/bg/highway-electric.jpg"),
    ('data-cth-type="statement"', "assets/bg/wind-energy.jpg", 0),  # first statement only
    ("Speaker path", "assets/bg/andes-colombia.jpg"),
    ('data-cth-type="process"', "assets/bg/solar-energy.jpg"),
    ("MubOn is where", "assets/bg/ev-station.jpg"),
    ("In 18 months", "assets/bg/ev-station.jpg"),
    ("Participant Q3", "assets/bg/solar-energy.jpg"),
    ("Investors can diligence", "assets/bg/andes-colombia.jpg"),
    ("Market context", "assets/ev-charging.jpg"),
    ("Zidi thesis checklist", "assets/bg/highway-electric.jpg"),
    ("Participant Q1", "assets/bg/ev-station.jpg"),
    ("Participant Q2", "assets/bg/agriculture.jpg"),
    ("Participant Q4", "assets/bg/solar-energy.jpg"),
    ("Participant Q5", "assets/bg/wind-energy.jpg"),
    ("Participant Q6", "assets/bg/wind-energy.jpg"),
]

statement_seen = 0


def hero_for_section(section: str) -> str | None:
    global statement_seen
    if "fp-closing" in section:
        return None
    if 'data-cth-type="cover"' in section:
        return "assets/bg/highway-electric.jpg"
    if 'data-cth-type="statement"' in section:
        statement_seen += 1
        return "assets/bg/wind-energy.jpg" if statement_seen == 1 else "assets/ev-charging.jpg"
    for needle, img in (
        ("Speaker path", "assets/bg/andes-colombia.jpg"),
        ('data-cth-type="process"', "assets/bg/solar-energy.jpg"),
        ("MubOn is where", "assets/bg/ev-station.jpg"),
        ("In 18 months", "assets/bg/ev-station.jpg"),
        ("Participant Q3", "assets/bg/solar-energy.jpg"),
        ("Investors can diligence", "assets/bg/andes-colombia.jpg"),
        ("Zidi thesis checklist", "assets/bg/highway-electric.jpg"),
        ("Participant Q1", "assets/bg/ev-station.jpg"),
        ("Participant Q2", "assets/bg/agriculture.jpg"),
        ("Participant Q4", "assets/bg/solar-energy.jpg"),
        ("Participant Q5", "assets/bg/wind-energy.jpg"),
        ("Participant Q6", "assets/bg/wind-energy.jpg"),
        ("GIZ growth", "assets/bg/growth.jpg"),
        ("GIZ · CATAL", "assets/bg/incubation.jpg"),
    ):
        if needle in section:
            return img
    return "assets/bg/solar-energy.jpg"


def wrap_section(section: str) -> str:
    section = section.replace(" fp--bleed", "")
    section = section.replace(" fp--photo", "")
    if "fp-closing" in section:
        section = re.sub(
            r'<section class="([^"]+)"',
            r'<section class="\1 fp--fix6 fp--navy fp--no-hero"',
            section,
            count=1,
        )
        return section
    if 'data-cth-type="cover"' in section:
        section = re.sub(
            r'<section class="([^"]+)"',
            r'<section class="\1 fp--fix6 fp--navy"',
            section,
            count=1,
        )
    elif "fp--dark" in section or 'data-cth-type="statement"' in section:
        section = section.replace(" fp--dark", "")
        section = re.sub(
            r'<section class="([^"]+)"',
            r'<section class="\1 fp--fix6 fp--navy"',
            section,
            count=1,
        )
    else:
        section = re.sub(
            r'<section class="([^"]+)"',
            r'<section class="\1 fp--fix6"',
            section,
            count=1,
        )
    hero = hero_for_section(section)
    if not hero:
        return section
    # Strip glass wrappers on cover/statement
    section = section.replace(" fp-text-glass fp-text-glass--cover", "")
    section = section.replace(" fp-text-glass fp-text-glass--statement", "")
    section = section.replace(" fp-text-glass fp-text-glass--caption", "")
    section = section.replace(' class="cth-source fp-text-glass"', ' class="cth-source"')
    # Insert shell + hero after opening section tag
    open_m = re.match(r"(<section[^>]*>\s*)", section, re.DOTALL)
    if not open_m:
        return section
    rest = section[open_m.end() :]
    hero_html = (
        f'<aside class="fp-hero-rail" aria-hidden="true">'
        f'<img src="{hero}" alt="" /></aside>\n  <div class="fp-slide-shell">\n'
    )
    close_footer = rest.rfind("</section>")
    inner = rest[:close_footer].strip()
    # Remove decorative plant on statement
    inner = re.sub(
        r'<img class="fp-deco fp-statement__plant"[^>]*/>\s*',
        "",
        inner,
    )
    # Remove inline z-index styles from cover
    inner = re.sub(r'\s*style="position:relative;z-index:2"', "", inner)
    inner = re.sub(r'\s*style="grid-template-columns:1fr;position:relative;z-index:2"', "", inner)
    inner = re.sub(r'\s*style="z-index:2"', "", inner)
    section = (
        open_m.group(1)
        + hero_html
        + inner
        + "\n  </div>\n</section>"
    )
    return section


parts = re.split(r"(<section[\s\S]*?</section>)", text)
out: list[str] = []
giz_inserted = False
for part in parts:
    if part.startswith("<section"):
        wrapped = wrap_section(part)
        out.append(wrapped)
        if not giz_inserted and 'data-cth-type="process"' in part:
            giz1 = """
<section class="fp fp-title-bullets fp-slide-fill fp--fix6" data-cth-type="title-bullets">
  <aside class="fp-hero-rail" aria-hidden="true"><img src="assets/bg/growth.jpg" alt="" /></aside>
  <div class="fp-slide-shell">
  <header class="fp-head">
    <div class="fp-head__text">
      <p class="fp-eyebrow">GIZ growth · CATAL1.5°T</p>
      <h2 class="fp-title fp-title--sm">We take climate SMEs from a four-area diagnosis to investor conversations, a programme we built and ran with GIZ for CATAL1.5°T in 2025.</h2>
      <p class="fp-giz-kicker">GIZ · CATAL1.5°T · May–Nov 2025 · GIZ Mexico technical counterpart, contracted via GIZ Bogotá · regional LatAm cohort of four climate-tech ventures.</p>
    </div>
    <img class="fp-head__logo" src="assets/cth-logo.png" alt="CleantechHUB" />
  </header>
  <div class="fp-body">
    <div class="fp-flip-grid fp-flip-grid--giz">
      <div class="fp-flip fragment fade-up" data-fp-flip><div class="fp-flip__inner"><div class="fp-flip__face fp-flip__face--front"><p class="fp-flip__title">Select and diagnose</p></div><div class="fp-flip__face fp-flip__face--back">Document review plus interviews across business, finance, impact and legal, ending in an individual diagnostic and gap analysis.</div></div></div>
      <div class="fp-flip fragment fade-up" data-fp-flip><div class="fp-flip__inner"><div class="fp-flip__face fp-flip__face--front"><p class="fp-flip__title">Co-create area by area</p></div><div class="fp-flip__face fp-flip__face--back">Four working sessions per venture, one per area, to stress-test the story and sharpen the pitch.</div></div></div>
      <div class="fp-flip fragment fade-up" data-fp-flip><div class="fp-flip__inner"><div class="fp-flip__face fp-flip__face--front"><p class="fp-flip__title">Capital-raising plan</p></div><div class="fp-flip__face fp-flip__face--back">Investor roadmap, tailored investor list for Europe and LatAm, market-access strategy.</div></div></div>
      <div class="fp-flip fragment fade-up" data-fp-flip><div class="fp-flip__inner"><div class="fp-flip__face fp-flip__face--front"><p class="fp-flip__title">Open investor doors</p></div><div class="fp-flip__face fp-flip__face--back">Activate the CTH network, up to four strategic introductions per venture, meeting prep and follow-up.</div></div></div>
    </div>
  </div>
  <p class="cth-source">CTH × GIZ CATAL1.5°T capital-raising accompaniment, 2025. · CATAL1.5°T LatAm initiative (giz.de): 8 countries, 90 climate ventures.</p>
  <footer class="fp-foot"><span class="fp-conf">Confidential</span><span>ZidiCircle × GIZ MEG · 1 Dec 2026</span></footer>
  </div>
</section>
"""
            giz2 = """
<section class="fp fp-title-bullets fp--fix6" data-cth-type="title-bullets">
  <aside class="fp-hero-rail" aria-hidden="true"><img src="assets/bg/incubation.jpg" alt="" /></aside>
  <div class="fp-slide-shell">
  <header class="fp-head">
    <div class="fp-head__text">
      <p class="fp-eyebrow">GIZ · CATAL1.5°T · outcomes</p>
      <h2 class="fp-title fp-title--sm">What each side gets from the accompaniment</h2>
    </div>
    <img class="fp-head__logo" src="assets/cth-logo.png" alt="CleantechHUB" />
  </header>
  <div class="fp-body">
    <div class="fp-giz-compare">
      <article class="fp-card">
        <p class="fp-card__title">For the SME</p>
        <p class="fp-card__text">Diagnosis, revised pitch, capital plan, investor shortlist, supported outreach.</p>
      </article>
      <article class="fp-card">
        <p class="fp-card__title">For the investor</p>
        <p class="fp-card__text">A company pre-examined on business, finance, impact and legal with a clear ask and documented roadmap.</p>
      </article>
    </div>
  </div>
  <p class="cth-source">CTH × GIZ CATAL1.5°T capital-raising accompaniment, 2025.</p>
  <footer class="fp-foot"><span class="fp-conf">Confidential</span><span>ZidiCircle × GIZ MEG · 1 Dec 2026</span></footer>
  </div>
</section>
"""
            out.append(giz1)
            out.append(giz2)
            giz_inserted = True
    else:
        out.append(part)

text = "".join(out)
text = text.replace(
    "ZidiCircle-MEG-Gideon-Blaauw-MubOn-1Dec2026-v5-REVIEW.pdf",
    "ZidiCircle-MEG-Gideon-Blaauw-MubOn-1Dec2026-v6-REVIEW.pdf",
)
text = text.replace("<body>", '<body class="fix6-deck">')
# Statement market context: remove absolute source positioning
text = re.sub(
    r'<p class="cth-source" style="position:absolute;left:96px;bottom:68px;[^"]*">',
    '<p class="cth-source">',
    text,
)
text = re.sub(
    r'<p class="fp-statement__text" style="font-size:52px">',
    '<p class="fp-statement__text">',
    text,
)
INDEX.write_text(text, encoding="utf-8")
print("transformed", INDEX)