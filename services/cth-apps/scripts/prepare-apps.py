#!/usr/bin/env python3
"""One-shot: copy uploaded HTML into slug dirs with CTH patches. Run from repo root."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SRC = Path("/tmp/ai-apps-src/ai-apps-src")
OUT = REPO / "services" / "cth-apps"

APPS = {
    "pitch-builder": ("pitchbuilder.html", "CC BY 4.0 (AI Apps for Good site-wide; no in-page licence text)"),
    "mel-builder": ("melbuilder.html", "CC BY-NC-SA 3.0 (in-page footer; BetterEvaluation-derived content)"),
    "compass": ("compass.html", "CC BY 4.0 (in-page footer)"),
    "tough-conversations": ("toughconversations.html", "CC BY-SA 4.0 (in-page footer)"),
}

CF_SCRIPT = re.compile(
    r'<script>\(function\(\)\{function c\(\)\{var b=a\.contentDocument.*?</script>',
    re.DOTALL,
)

FOOTER_STYLE = """
<style id="cth-adapt-footer-style">
#cth-adapt-footer{margin:24px auto 16px;max-width:960px;padding:12px 16px;font-size:12px;line-height:1.5;color:#475569;text-align:center;border-top:1px solid #e2e8f0;font-family:system-ui,sans-serif}
#cth-adapt-footer a{color:#2D6A4F}
</style>
"""


def footer_html(licence: str) -> str:
    return (
        f'<footer id="cth-adapt-footer">Adapted from '
        f'<a href="https://aiappsforgood.org/" rel="noopener">AI Apps for Good</a> / '
        f'<a href="https://nonprofitbuilder.org/" rel="noopener">Nonprofit Builder</a> '
        f"(licence: {licence}) — self-hosted by CleantechHUB</footer>"
    )


def patch_html(raw: str, licence: str) -> str:
    s = raw
    s = s.replace("https://proxy.aiappsforgood.org/api", "/api/llm")
    s = s.replace("https://proxy.org360.app/api/claude", "/api/llm")
    s = CF_SCRIPT.sub("", s)
    s = re.sub(
        r'<a class="sh-support" href="https://buy\.stripe\.com/[^"]*"[^>]*>[^<]*</a>\s*',
        "",
        s,
    )
    s = s.replace(
        "const ANTHROPIC_URL = 'https://proxy.aiappsforgood.org/api';",
        "const ANTHROPIC_URL = '/api/llm';",
    )
    # Disable web3forms feedback
    s = re.sub(
        r"async function sendFb\(\) \{[\s\S]*?\n\}",
        """async function sendFb() {
  alert('Feedback is disabled on this self-hosted copy. Contact your CleantechHUB admin.');
}""",
        s,
        count=1,
    )
    s = re.sub(
        r"async function submitFeedback\(\) \{[\s\S]*?\n\}",
        """async function submitFeedback() {
  alert('Feedback is disabled on this self-hosted copy. Contact your CleantechHUB admin.');
}""",
        s,
        count=1,
    )
    s = s.replace(
        "const res = await fetch('https://api.web3forms.com/submit',{method:'POST',body:formData});",
        "alert('Contact form is disabled on this CleantechHUB self-hosted copy.'); return;",
    )
    s = s.replace("https://api.web3forms.com/submit", "/api/llm-disabled-web3forms")
    s = s.replace("proxy.aiappsforgood.org is reachable.", "the /api/llm proxy is reachable.")
    # MEL perplexity → not available
    s = re.sub(
        r"async function callExamples\(\) \{[\s\S]*?\n\}",
        """async function callExamples() {
  const btn = $('ex-btn');
  const loading = $('ex-loading');
  const content = $('ex-content');
  const note = $('ex-note');
  btn.style.display = 'none';
  loading.style.display = 'none';
  content.style.display = 'block';
  note.style.display = 'block';
  content.innerHTML = '<p><strong>Real-world example search is not available</strong> on this CleantechHUB self-hosted copy (Perplexity step disabled).</p>';
}""",
        s,
        count=1,
    )
    if FOOTER_STYLE.strip() not in s:
        s = s.replace("</head>", FOOTER_STYLE + "\n</head>", 1)
    foot = footer_html(licence)
    if "cth-adapt-footer" not in s:
        s = s.replace("</body>", foot + "\n</body>", 1)
    return s


def _js_const(name: str, html: str):
    import subprocess

    m = re.search(rf"const {name} = ([\s\S]*?);\n", html)
    if not m:
        return None
    snippet = f"const {name} = {m.group(1)};\nconsole.log(JSON.stringify({name}));"
    out = subprocess.run(
        ["node", "-e", snippet],
        capture_output=True,
        text=True,
        check=False,
    )
    if out.returncode != 0:
        return None
    return json.loads(out.stdout.strip())


def extract_pitch_rubric(html: str) -> dict:
    questions = _js_const("QUESTIONS", html) or []
    return {
        "app": "pitch-builder",
        "framework": "10-question pitch intake + AI follow-up gap review + 10-slide deck generation",
        "questions": questions,
        "llm_steps": ["review_gaps", "generate_deck"],
    }


def extract_tough_rubric(html: str) -> dict:
    areas = _js_const("AREAS", html) or {}
    techniques = []
    for area_id, area in areas.items():
        for t in area.get("techniques", []):
            techniques.append(
                {
                    "area_id": area_id,
                    "area_label": area.get("label"),
                    "id": t.get("id"),
                    "name": t.get("name"),
                    "source": t.get("source"),
                    "keywords": t.get("keywords", []),
                    "steps": t.get("steps", []),
                }
            )
    return {
        "app": "tough-conversations",
        "framework": "Situation → support area → evidence-based technique (NVC, SCARF, etc.) + AI contextualisation",
        "support_areas": [
            {"id": k, "label": v.get("label"), "technique_count": len(v.get("techniques", []))}
            for k, v in areas.items()
        ],
        "techniques": techniques,
    }


def extract_mel_rubric(html: str) -> dict:
    intake = [
        {"id": "q0", "label": "Primary work type", "type": "single"},
        {"id": "q1", "label": "Current MEL situation", "type": "single"},
        {"id": "q2", "label": "Primary purpose of MEL", "type": "multi"},
        {"id": "q3", "label": "Number of programs", "type": "single"},
        {"id": "q4", "label": "MEL capacity", "type": "single"},
        {"id": "rc", "label": "Who will do MEL work", "type": "multi"},
        {"id": "rs", "label": "Organisation size", "type": "single"},
    ]
    approaches = []
    for line in html.splitlines():
        if "| slug:" in line and line.strip().startswith("-"):
            name, slug_part = line.split("| slug:", 1)
            name = name.lstrip("- ").strip()
            slug = slug_part.strip().split()[0]
            approaches.append({"name": name, "slug": slug})
    return {
        "app": "mel-builder",
        "framework": "BetterEvaluation MEL approach matching + design guide",
        "intake_questions": intake,
        "approach_catalog_slugs": approaches,
        "llm_steps": ["suggest_approaches", "build_design_guide"],
        "disabled_features": ["perplexity_real_world_examples"],
    }


def extract_compass_rubric(html: str) -> dict:
    services = _js_const("SERVICES_DATA", html) or []
    ask_three = [
        {
            "id": "ask_q1",
            "text": "Describe the organisation you are working to build.",
        },
        {
            "id": "ask_q2",
            "text": "What is currently holding you back?",
        },
        {
            "id": "ask_q3",
            "text": "Of those things holding you back, what is your top priority to work on right now?",
        },
    ]
    categories = sorted({s["category"] for s in services})
    return {
        "app": "compass",
        "framework": "Prioritisation game (80 projects / 14 themes) or Ask Claude three-question roadmap",
        "paths": ["prioritisation_game", "ask_claude_three_questions", "browse_catalog"],
        "ask_claude_questions": ask_three,
        "project_count": len(services),
        "categories": categories,
        "projects": [
            {
                "id": s["id"],
                "category": s["category"],
                "name": s["name"],
                "painPoint": s.get("painPoint"),
            }
            for s in services
        ],
    }


def main() -> None:
    for slug, (filename, licence) in APPS.items():
        src_path = SRC / filename
        dest_dir = OUT / slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        raw = src_path.read_text(encoding="utf-8")
        patched = patch_html(raw, licence)
        (dest_dir / "index.html").write_text(patched, encoding="utf-8")
        extractors = {
            "pitch-builder": extract_pitch_rubric,
            "mel-builder": extract_mel_rubric,
            "compass": extract_compass_rubric,
            "tough-conversations": extract_tough_rubric,
        }
        rubric = extractors[slug](patched)
        (dest_dir / "rubric.json").write_text(
            json.dumps(rubric, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print("Prepared", len(APPS), "apps under", OUT)


if __name__ == "__main__":
    main()
