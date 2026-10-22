#!/usr/bin/env python3
"""Build decks/{slug}-teaser/data.json from cth-nexus docs/teasers sources."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

try:
    from deep_translator import MyMemoryTranslator
except ImportError:
    MyMemoryTranslator = None  # type: ignore

ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE = ROOT / "decks" / "teaser-template"
CELSIA = ROOT / "decks" / "celsia-teaser"
SOURCES = Path("/tmp/cth-nexus-teasers")
PORTFOLIO_URL = (
    "https://raw.githubusercontent.com/gideonblaauw-creator/cth-nexus/main/"
    "site/nexus-assets/previews/startups-redesign-20261016/portfolio-core.json"
)

SLUGS = [
    "isa",
    "geb",
    "enel",
    "epm",
    "alqueria",
    "nutresa",
    "juan-valdez",
    "alpina",
    "argos",
    "pavimentos-colombia",
    "interaseo",
    "ecopetrol",
    "parex",
    "terpel",
    "promigas",
    "bancolombia",
    "banco-popular",
    "sura",
]

LOG: dict[str, list[str]] = {s: [] for s in SLUGS}
_TR_CACHE: dict[tuple[str, str, str], str] = {}
_tr_en: MyMemoryTranslator | None = None
_tr_es: MyMemoryTranslator | None = None


def translators():
    global _tr_en, _tr_es
    if MyMemoryTranslator is None:
        return None, None
    if _tr_en is None:
        _tr_en = MyMemoryTranslator(source="es-ES", target="en-GB")
        _tr_es = MyMemoryTranslator(source="en-GB", target="es-ES")
    return _tr_en, _tr_es


def tr(text: str, direction: str) -> str:
    if not text or not text.strip():
        return ""
    key = (direction, text[:80], str(len(text)))
    if key in _TR_CACHE:
        return _TR_CACHE[key]
    tr_en, tr_es = translators()
    if not tr_en:
        return ""
    out = ""
    try:
        engine = tr_en if direction == "es-en" else tr_es
        out = " ".join(engine.translate(chunk) for chunk in _chunk(text))
        time.sleep(0.15)
    except Exception:
        out = ""
    _TR_CACHE[key] = out
    return out


def norm_key(name: str) -> str:
    n = unicodedata.normalize("NFKD", name)
    n = "".join(c for c in n if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", n.lower())


def _chunk(text: str, size: int = 4500) -> list[str]:
    if len(text) <= size:
        return [text]
    parts: list[str] = []
    cur: list[str] = []
    n = 0
    for sent in re.split(r"(?<=[.!?])\s+", text):
        if n + len(sent) > size and cur:
            parts.append(" ".join(cur))
            cur, n = [sent], len(sent)
        else:
            cur.append(sent)
            n += len(sent) + 1
    if cur:
        parts.append(" ".join(cur))
    return parts


def translate_es_to_en(text: str) -> str:
    return tr(text, "es-en")


def translate_en_to_es(text: str) -> str:
    return tr(text, "en-es")


def looks_spanish(text: str) -> bool:
    if re.search(r"[áéíóúñÁÉÍÓÚÑ¿¡]", text):
        return True
    low = text.lower()
    markers = (" de ", " la ", " el ", " en ", " que ", " por ", " con ", " emisiones", " alcance")
    return any(m in low for m in markers)


def split_pdf_url(url: str) -> tuple[str, int | None]:
    if not url:
        return "", None
    m = re.search(r"#page=(\d+)", url, re.I)
    page = int(m.group(1)) if m else None
    base = url.split("#")[0]
    return base, page


def parse_md(md: str) -> dict:
    out: dict = {}
    m = re.search(r"\*\*Company\.\*\*\s*(.+)", md)
    out["company_line"] = m.group(1).strip() if m else ""
    m = re.search(r"\*\*Report\.\*\*\s*(.+?)(?=\n\n|\n\*\*|\n>)", md, re.S)
    out["report_line"] = " ".join(m.group(1).split()) if m else ""
    m = re.search(r"\*\*Note\.\*\*\s*(.+?)(?=\n\n|\n>|$)", md, re.S)
    out["note"] = m.group(1).strip() if m else ""
    quotes = re.findall(r"^>\s*(.+)$", md, re.M)
    out["blockquotes"] = [q.strip() for q in quotes]
    scope_m = re.search(r"^Scope:\s*(.+)$", md, re.M | re.I)
    if not scope_m:
        scope_m = re.search(
            r"Environment, climate and nature only[^\n]*", md, re.I
        )
    out["scope_line"] = scope_m.group(0).strip() if scope_m else ""
    return out


def portfolio_index(raw: dict) -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for st in raw.get("startups", []):
        idx[norm_key(st["n"])] = st
        if st.get("w"):
            idx[norm_key(st["w"].split(".")[0])] = st
    aliases = {
        "carbonbox": "carbonbox",
        "cneutral": "cneutral",
        "sincarbono": "sincarbono",
        "o3smartcities": "o3smartcities",
        "apicultoresyrescatistassbic": "apicultoresyrescatistassasbic",
        "wero": "wero",
        "galaxy pack": "galaxypack",
    }
    for k, v in list(idx.items()):
        if v.get("n"):
            aliases.setdefault(norm_key(v["n"]), k)
    return idx


def lookup_portfolio(name: str, idx: dict[str, dict]) -> dict | None:
    keys = [norm_key(name)]
    if name.upper() == name and len(name) <= 6:
        keys.append(norm_key(name.lower()))
    for k in keys:
        if k in idx:
            return idx[k]
    return None


def nexus_entry(name: str, match: dict, idx: dict[str, dict]) -> dict | None:
    pf = lookup_portfolio(name, idx)
    if pf:
        entry = {"p": pf.get("p", ""), "t": pf.get("t", ""), "d": pf.get("d", ""), "ds": pf.get("ds", "")}
        if match.get("actor_kind") == "funder":
            entry["funder"] = True
        return entry
    desc = match.get("description") or match.get("why") or ""
    if not desc:
        return None
    ds = translate_en_to_es(desc) if desc else ""
    return {"p": "", "t": "", "d": desc, "ds": ds or desc}


def build_context(gap: dict, lang: str) -> str:
    parts: list[str] = []
    stmt = gap.get("statement") or ""
    page = gap.get("report_page_pdf")
    if page:
        parts.append(f"PDF page {page}." if lang == "en" else f"PDF página {page}.")
    gri = gap.get("gri_disclosure_in_report") or gap.get("gri_topic_standard") or ""
    if gri:
        parts.append(gri + ".")
    printed = gap.get("report_page_printed")
    if printed:
        parts.append(
            f"Printed page {printed}." if lang == "en" else f"Página impresa {printed}."
        )
    if stmt:
        parts.append(stmt if lang == "en" else (translate_en_to_es(stmt) or stmt))
    return " ".join(parts).strip()


def build_match(m: dict, gap: dict) -> dict:
    name = m.get("name") or ""
    url = m.get("website") or m.get("public_source_url") or ""
    why = m.get("why") or ""
    why_es = m.get("why_es") or translate_en_to_es(why) or why
    stage = m.get("startup_stage") or gap.get("startup_stage") or ""
    return {
        "match_id": m.get("match_id") or "",
        "name": name,
        "stage": "" if m.get("actor_kind") == "funder" else stage,
        "website": url,
        "why": why,
        "why_es": why_es,
        "public_quote": m.get("public_quote") or "",
        "public_source_url": m.get("public_source_url") or url,
        "funder": m.get("actor_kind") == "funder",
    }


def build_report_evidence(gap: dict, company: dict, slug: str) -> dict:
    quote = (gap.get("evidence_quote") or "").strip()
    url = gap.get("evidence_url") or company.get("gri_report_url") or ""
    pdf_url, page_from_url = split_pdf_url(url)
    page = gap.get("report_page_pdf") or page_from_url or 1
    if not pdf_url:
        pdf_url = company.get("gri_report_url") or ""
    ev = {"quote_es": quote, "quote_en": "", "pdf_url": pdf_url, "page": int(page)}
    if not quote:
        LOG[slug].append(f"gap {gap.get('rank')}: missing evidence_quote")
        return ev
    if looks_spanish(quote):
        en = translate_es_to_en(quote)
        if en:
            ev["quote_en"] = en
        else:
            LOG[slug].append(f"gap {gap.get('rank')}: quote_en translation failed")
    else:
        ev["quote_en"] = quote
        es = translate_en_to_es(quote)
        if es:
            ev["quote_es"] = es
        else:
            LOG[slug].append(f"gap {gap.get('rank')}: Spanish report quote unavailable (EN source)")
    return ev


def build_ui(company: dict, src: dict, md: dict, slug: str, n_gaps: int) -> dict:
    name = company.get("name") or slug
    accessed = src.get("accessed_on") or "2026-10-22"
    scope_en = src.get("scope") or (
        "Environment, climate and nature. Social and governance topics are out of scope."
    )
    if scope_en.lower().startswith("scope:"):
        scope_en = scope_en.split(":", 1)[1].strip()
    scope_es = translate_en_to_es(scope_en) or (
        "Medio ambiente, clima y naturaleza. Temas sociales y de gobernanza quedan fuera de alcance."
    )
    company_en = md.get("company_line") or f"{name}, {company.get('country', 'Colombia')}. Persona: CSO."
    company_es = translate_en_to_es(company_en) or company_en

    pdf = company.get("gri_report_url") or ""
    listing = company.get("report_listing_url") or ""
    prof_page = company.get("profile_page_pdf")
    report_label = company.get("report_title") or "Sustainability report"
    report_en_parts: list[str] = []
    if pdf:
        report_en_parts.append(f'{report_label} (<a href="{pdf}">PDF</a>)')
    elif md.get("report_line"):
        report_en_parts.append(md["report_line"])
    if listing:
        host = urlparse(listing).netloc or listing
        report_en_parts.append(f'linked from <a href="{listing}">{host}</a>')
    if prof_page:
        report_en_parts.append(f"PDF page {prof_page}.")
    report_en = " ".join(report_en_parts)
    report_es_parts = []
    if pdf:
        report_es_parts.append(f'{report_label} (<a href="{pdf}">PDF</a>)')
    if listing:
        host = urlparse(listing).netloc or listing
        report_es_parts.append(f'enlazado desde <a href="{listing}">{host}</a>')
    if prof_page:
        report_es_parts.append(f"PDF página {prof_page}.")
    report_es = " ".join(report_es_parts)

    hero_title_en = (
        f"{name} · environment, climate and nature — {n_gaps} material gaps from the latest sustainability report."
    )
    hero_title_es = (
        f"{name} · medio ambiente, clima y naturaleza — {n_gaps} brechas materiales del reporte de sostenibilidad."
    )

    snap_quote = company.get("profile_quote") or (md.get("blockquotes")[0] if md.get("blockquotes") else "")
    _, snap_page_url = split_pdf_url(company.get("profile_source_url") or "")
    snap_page = company.get("profile_page_pdf") or snap_page_url or 1

    bvc = ""
    if company.get("bvc_listed"):
        bvc = (
            f"BVC: {name} is listed on the Bolsa de Valores de Colombia."
            if company.get("bvc_listed") is True
            else ""
        )
    bvc_es = translate_en_to_es(bvc) if bvc else ""

    shortfall_gaps = [g for g in src.get("gaps", []) if g.get("shortfall")]
    sf_nums = ", ".join(str(g["rank"]) for g in shortfall_gaps)
    shortfall_en = (
        f"Shortfall: true on gap(s) {sf_nums}; false on others. csoReady: {src.get('csoReady', 'n/a')}. "
        "Every match is a theme match. None names the company."
        if sf_nums
        else "Every match is a theme match. None names the company. No shortfall gaps flagged in source."
    )
    shortfall_es = translate_en_to_es(shortfall_en) or shortfall_en

    foot_en = ""
    foot_es = ""

    def block(lang: str) -> dict:
        is_en = lang == "en"
        return {
            "nav.snapshot": "Snapshot" if is_en else "Panorama",
            "nav.g1": f"Gap 1" if is_en else "Brecha 1",
            "nav.g2": f"Gap 2" if is_en else "Brecha 2",
            "nav.g3": f"Gap 3" if is_en else "Brecha 3",
            "nav.g4": f"Gap 4" if is_en else "Brecha 4",
            "nav.g5": f"Gap 5" if is_en else "Brecha 5",
            "nav.team": "Team" if is_en else "Equipo",
            "nav.cta": "Next step" if is_en else "Siguiente paso",
            "hero.eyebrow": f"{name} · gap snapshot" if is_en else f"{name} · panorama de brechas",
            "hero.title": hero_title_en if is_en else hero_title_es,
            "hero.lead": "Draft. Not a CSO delivery." if is_en else "Borrador. No es una entrega CSO.",
            "hero.companyLbl": "Company" if is_en else "Empresa",
            "hero.company": company_en if is_en else company_es,
            "hero.scopeLbl": "Scope" if is_en else "Alcance",
            "hero.scope": scope_en if is_en else scope_es,
            "hero.reportLbl": "Report" if is_en else "Reporte",
            "hero.report": report_en if is_en else report_es,
            "snap.eyebrow": "Transparency frame" if is_en else "Marco de transparencia",
            "snap.title": (
                f"Reporting frame (PDF page {snap_page})"
                if is_en
                else f"Marco de reporte (PDF página {snap_page})"
            ),
            "snap.bvc": bvc if is_en else bvc_es,
            "snap.themeNote": (
                "Every match below is a theme match. None names the company. None is a graph relation."
                if is_en
                else "Cada coincidencia es temática. Ninguna nombra a la empresa. Ninguna es relación de grafo."
            ),
            "snap.shortfall": shortfall_en if is_en else shortfall_es,
            "team.eyebrow": "CleantechHUB team" if is_en else "Equipo CleantechHUB",
            "team.title": "Who shaped this teaser" if is_en else "Quién llevó este teaser",
            "team.intro": (
                "Angie (Angélica), Jenn (Jennifer) and Gideon — same team as the Air4U proposal deck."
                if is_en
                else "Angie (Angélica), Jenn (Jennifer) y Gideon — mismo equipo que la propuesta Air4U."
            ),
            "cta.title": "Discuss this gap snapshot" if is_en else "Conversemos este panorama de brechas",
            "cta.body": (
                "This page is a draft GTM hypothesis. Book a short call with the CleantechHUB team to explore next steps."
                if is_en
                else "Esta página es una hipótesis GTM en borrador. Agende una llamada breve con el equipo CleantechHUB."
            ),
            "cta.btn": "Book a call" if is_en else "Agenda una llamada",
            "foot.line": foot_en if is_en else foot_es,
        }

    return {"en": block("en"), "es": block("es")}


def build_slug(slug: str, pf_idx: dict[str, dict], celsia: dict) -> dict:
    src_path = SOURCES / slug / f"{slug}-teaser.json"
    md_path = SOURCES / slug / f"{slug}-teaser.md"
    src = json.loads(src_path.read_text())
    md = parse_md(md_path.read_text() if md_path.exists() else "")
    company = src.get("company") or {}
    gaps_src = src.get("gaps") or []
    nexus: dict = {}
    gaps_out = []

    for g in gaps_src:
        rank = int(g.get("rank") or len(gaps_out) + 1)
        title_en = g.get("title") or f"Gap {rank}"
        title_es = translate_en_to_es(title_en) or title_en
        matches = [build_match(m, g) for m in g.get("matches") or []]
        for m in g.get("matches") or []:
            nm = m.get("name")
            if nm and nm not in nexus:
                entry = nexus_entry(nm, m, pf_idx)
                if entry:
                    nexus[nm] = entry
        mc = len(matches)
        gap_out = {
            "id": f"gap-{rank}",
            "rank": rank,
            "shortfall": bool(g.get("shortfall")),
            "journey_step": g.get("journey_step") or "data",
            "match_count": mc,
            "title": {"en": f"{rank}. {title_en}", "es": f"{rank}. {title_es}"},
            "context": {"en": build_context(g, "en"), "es": build_context(g, "es")},
            "report_evidence": build_report_evidence(g, company, slug),
            "matches": matches,
        }
        if mc < 3 and g.get("shortfall"):
            note_en = f"Matches: {mc}."
            gap_out["note"] = {"en": note_en, "es": translate_en_to_es(note_en) or note_en}
        gaps_out.append(gap_out)

    snap_quote = company.get("profile_quote") or (md.get("blockquotes")[0] if md.get("blockquotes") else "")
    _, snap_page_url = split_pdf_url(company.get("profile_source_url") or "")
    snap_page = company.get("profile_page_pdf") or snap_page_url or 1
    pdf_url = company.get("gri_report_url") or ""
    snap_ev = {
        "quote_es": snap_quote,
        "quote_en": "",
        "pdf_url": pdf_url,
        "page": int(snap_page),
    }
    if snap_quote:
        if looks_spanish(snap_quote):
            snap_ev["quote_en"] = translate_es_to_en(snap_quote)
        else:
            snap_ev["quote_en"] = snap_quote
            snap_ev["quote_es"] = translate_en_to_es(snap_quote) or snap_quote
    else:
        LOG[slug].append("snapshot profile_quote missing")

    name = company.get("name") or slug
    total_matches = sum(len(g["matches"]) for g in gaps_out)
    footer = {
        "en": f"Match count: {total_matches}. {md.get('note') or 'Contact details omitted.'}",
        "es": translate_en_to_es(f"Match count: {total_matches}.") or f"Conteo de coincidencias: {total_matches}.",
    }

    data = {
        "meta": {
            "slug": f"{slug}-teaser",
            "company_key": slug,
            "public_url": f"https://proposals.cleantechhub.net/{slug}-teaser/",
            "title": {
                "en": f"{name} · gap snapshot · CleantechHUB",
                "es": f"{name} · panorama de brechas · CleantechHUB",
            },
        },
        "brand": {"logo": "img/cth-logo.png"},
        "report": {
            "pdf_url": pdf_url,
            "listing_url": company.get("report_listing_url") or "",
            "accessed_on": src.get("accessed_on") or "2026-10-22",
        },
        "ui": build_ui(company, src, md, slug, len(gaps_out)),
        "snapshot": {"report_evidence": snap_ev},
        "cta": {"url": "https://calendar.app.google/kzEv6jKdT4RxVeVu6"},
        "team": celsia["team"],
        "footer_note": footer,
        "nexus": nexus,
        "gaps": gaps_out,
    }
    return data


def sync_shell(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run([str(TEMPLATE / "sync-shell.sh"), str(dest)], check=True, cwd=TEMPLATE)


def copy_assets(dest: Path) -> None:
    img_dest = dest / "img"
    img_dest.mkdir(exist_ok=True)
    for name in (
        "cth-logo.png",
        "team-gideon.jpg",
        "team-angelica.jpg",
        "team-jennifer.jpg",
    ):
        shutil.copy2(CELSIA / "img" / name, img_dest / name)


def main() -> int:
    if MyMemoryTranslator is None:
        print("Install deep-translator: pip install deep-translator", file=sys.stderr)
        return 1

    import urllib.request

    pf_raw = json.loads(urllib.request.urlopen(PORTFOLIO_URL, timeout=60).read())
    pf_idx = portfolio_index(pf_raw)
    celsia = json.loads((CELSIA / "data.json").read_text())
    celsia_nexus = celsia.get("nexus") or {}

    summary = []
    for slug in SLUGS:
        dest = ROOT / "decks" / f"{slug}-teaser"
        sync_shell(dest)
        copy_assets(dest)
        data = build_slug(slug, pf_idx, celsia)
        for nm, entry in celsia_nexus.items():
            if nm in data["nexus"]:
                data["nexus"][nm] = {**entry, **{k: v for k, v in data["nexus"][nm].items() if v}}
        out = dest / "data.json"
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        subprocess.run(["python3", "-m", "json.tool", str(out)], check=True, stdout=subprocess.DEVNULL)
        ng = len(data["gaps"])
        nm = sum(len(g["matches"]) for g in data["gaps"])
        summary.append((slug, ng, nm, LOG[slug]))

    report_path = ROOT / "decks" / "teaser-template" / "build-log.json"
    report_path.write_text(json.dumps({s: {"gaps": g, "matches": m, "omitted": o} for s, g, m, o in summary}, indent=2))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
