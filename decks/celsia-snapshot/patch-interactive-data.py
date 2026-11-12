#!/usr/bin/env python3
"""Add interactive chart/coverage/CTH blocks to celsia data.json (one-time patch)."""
import json
from pathlib import Path

p = Path(__file__).parent / "data.json"
data = json.loads(p.read_text())
pdf = data["report"]["pdf_url"]

data["interactive"] = {
    "coverage_sites": [
        {
            "id": "supply_chain",
            "label": {"en": "Supply chain (scope 3)", "es": "Cadena de suministro (alcance 3)"},
            "gaps": [1],
            "gri": ["GRI 305-3"],
        },
        {
            "id": "biodiversity_ops",
            "label": {"en": "Biodiversity on operations", "es": "Biodiversidad en operaciones"},
            "gaps": [2],
            "gri": ["GRI 304-2"],
        },
        {
            "id": "hydro_assets",
            "label": {"en": "Hydro reservoirs & rivers", "es": "Embalses e hidrología"},
            "gaps": [3],
            "gri": ["GRI 303-1"],
        },
        {
            "id": "nc_renewables",
            "label": {"en": "Non-conventional renewables", "es": "Renovables no convencionales"},
            "gaps": [4],
            "gri": ["GRI 302-1"],
        },
        {
            "id": "packaging",
            "label": {"en": "Own-brand packaging", "es": "Empaque de marca propia"},
            "gaps": [5],
            "gri": ["GRI 306-3"],
        },
    ]
}

charts = {
    1: {
        "source": {"en": f"Celsia Reporte Integrado 2024, PDF p. 60", "es": f"Reporte Integrado Celsia 2024, PDF p. 60"},
        "bars": [
            {"label": {"en": "SBTi approval indicator progress", "es": "Avance indicador aprobación SBTi"}, "value": 20, "unit": "%", "max": 100},
        ],
    },
    2: {
        "source": {"en": "Celsia Reporte Integrado 2024, PDF p. 60", "es": "Reporte Integrado Celsia 2024, PDF p. 60"},
        "bars": [
            {"label": {"en": "Net-positive indicator progress", "es": "Avance indicador neto positivo"}, "value": 23, "unit": "%", "max": 100},
            {"label": {"en": "ReverdeC trees planted", "es": "Árboles ReverdeC plantados"}, "value": 18005015, "unit": "", "max": 50000000, "display": "18,005,015 / 50,000,000"},
        ],
    },
    3: {
        "source": {"en": "Celsia Reporte Integrado 2024, PDF p. 22 — qualitative physical-risk mapping (no % KPI in report)", "es": "Reporte Integrado Celsia 2024, PDF p. 22 — mapeo cualitativo (sin KPI % en el reporte)"},
        "bars": [],
        "note": {"en": "Report uses TCS climate data linked to assets; no target/actual percentage on this page.", "es": "El reporte usa datos TCS ligados a activos; no hay porcentaje meta/actual en esta página."},
    },
    4: {
        "source": {"en": "Celsia Reporte Integrado 2024, PDF p. 61", "es": "Reporte Integrado Celsia 2024, PDF p. 61"},
        "bars": [
            {"label": {"en": "2024 installed NC renewables share", "es": "Participación renovables NC 2024"}, "value": 19, "unit": "%", "max": 35},
            {"label": {"en": "2025 target", "es": "Meta 2025"}, "value": 25, "unit": "%", "max": 35},
            {"label": {"en": "2030 expectation (report)", "es": "Expectativa 2030 (reporte)"}, "value": 35, "unit": "%", "max": 35},
        ],
    },
    5: {
        "source": {"en": "Celsia Reporte Integrado 2024, PDF p. 61", "es": "Reporte Integrado Celsia 2024, PDF p. 61"},
        "bars": [
            {"label": {"en": "Reusable/compostable/recyclable own-brand packaging", "es": "Empaque reutilizable/compostable/reciclable"}, "value": 10, "unit": "%", "max": 100},
            {"label": {"en": "2030 target", "es": "Meta 2030"}, "value": 100, "unit": "%", "max": 100},
            {"label": {"en": "Circular-economy policy progress", "es": "Avance política economía circular"}, "value": 20, "unit": "%", "max": 100},
        ],
    },
}

headlines = {
    1: {
        "en": "Scope 3 and SBTi still in progress — SBTi indicator at 20%.",
        "es": "Alcance 3 y SBTi en curso — indicador SBTi al 20 %.",
    },
    2: {
        "en": "Net-positive at 23%; ReverdeC at 18,005,015 of 50 million trees by 2030.",
        "es": "Neto positivo al 23 %; ReverdeC con 18.005.015 de 50 millones de árboles al 2030.",
    },
    3: {
        "en": "Physical water and climate risks mapped to assets (GRI 303).",
        "es": "Riesgos físicos hídricos y climáticos mapeados a activos (GRI 303).",
    },
    4: {
        "en": "NC renewables: 19% in 2024 vs 25% target in 2025; 35% expected by 2030.",
        "es": "Renovables NC: 19 % en 2024 vs meta 25 % en 2025; 35 % esperado en 2030.",
    },
    5: {
        "en": "Own-brand circular packaging at 10% vs 100% by 2030; circular policy at 20%.",
        "es": "Empaque circular propio al 10 % vs 100 % en 2030; política circular al 20 %.",
    },
}

for g in data["gaps"]:
    r = g["rank"]
    g["headline"] = headlines[r]
    g["chart"] = charts[r]
    for lang in ("en", "es"):
        dl = g.get("datalab", {}).get(lang, {})
        if dl:
            dl["reported_missing"] = headlines[r][lang]
            dl["deliverable"] = (
                f"L2/L3 Datalab export mapped to gap {r} standards — next report cycle."
                if lang == "en"
                else f"Exportación Datalab L2/L3 mapeada a estándares de la brecha {r} — próximo ciclo de reporte."
            )

data["ui"]["en"]["datalab.intro"] = "CleantechHUB Datalab: data steward, L1→L2→L3 flow, reporting-ready outputs."
data["ui"]["es"]["datalab.intro"] = "Datalab CleantechHUB: administrador de datos, flujo L1→L2→L3, salidas listas para reporte."
data["ui"]["en"]["nav.history"] = "CTH track record"
data["ui"]["es"]["nav.history"] = "Trayectoria CTH"
data["ui"]["en"]["history.title"] = "CleantechHUB history & achievements"
data["ui"]["es"]["history.title"] = "Historia y logros CleantechHUB"
data["ui"]["en"]["history.lead"] = "Public facts only — each item links to its source."
data["ui"]["es"]["history.lead"] = "Solo hechos públicos — cada ítem enlaza su fuente."
data["ui"]["en"]["nav.gaps"] = "Gaps"
data["ui"]["es"]["nav.gaps"] = "Brechas"
data["ui"]["en"]["nav.compare"] = "Compare"
data["ui"]["es"]["nav.compare"] = "Comparar"
data["ui"]["en"]["nav.coverage"] = "Coverage"
data["ui"]["es"]["nav.coverage"] = "Cobertura"
data["ui"]["en"]["compare.title"] = "Startup comparison"
data["ui"]["es"]["compare.title"] = "Comparación de startups"
data["ui"]["en"]["coverage.title"] = "Data coverage explorer"
data["ui"]["es"]["coverage.title"] = "Explorador de cobertura de datos"

data["cth_history"] = {
    "timeline": [
        {
            "year": "2019",
            "text": {
                "en": "CleantechHUB begins driving climate entrepreneurship and cleantech innovation ecosystems in Latin America.",
                "es": "CleantechHUB comienza a impulsar el emprendimiento climático y ecosistemas de innovación cleantech en América Latina.",
            },
            "source_url": "https://cleantechhub.net",
            "source_label": "cleantechhub.net",
        },
        {
            "year": "",
            "text": {
                "en": "CleantechHUB runs early-stage programmes (IDEAS hackathon, START-UPS, SCALE-UPS, tailor-made growth tracks).",
                "es": "CleantechHUB ejecuta programas de etapa temprana (hackathon IDEAS, START-UPS, SCALE-UPS, rutas a medida).",
            },
            "source_url": "https://cleantechhub.net",
            "source_label": "cleantechhub.net — Programs",
        },
        {
            "year": "",
            "text": {
                "en": "CleantechHUB is National Organizer for ClimateLaunchpad in Colombia, Peru, El Salvador, Guatemala, and Costa Rica.",
                "es": "CleantechHUB es Organizador Nacional de ClimateLaunchpad en Colombia, Perú, El Salvador, Guatemala y Costa Rica.",
            },
            "source_url": "https://github.com/gideonblaauw-creator/cth-plugin/blob/main/skills/clp26-brand/SKILL.md",
            "source_label": "cth-plugin skills/clp26-brand/SKILL.md",
        },
    ],
    "metrics": [
        {
            "value": "+50M",
            "label": {"en": "Capital leveraged (site headline)", "es": "Capital apalancado (titular del sitio)"},
            "source_url": "https://cleantechhub.net",
            "source_label": "cleantechhub.net",
        },
        {
            "value": "6+",
            "label": {"en": "Years of impact (site section)", "es": "Años de impacto (sección del sitio)"},
            "source_url": "https://cleantechhub.net",
            "source_label": "cleantechhub.net",
        },
    ],
}

p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
print("patched", p)
