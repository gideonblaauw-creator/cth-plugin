#!/usr/bin/env python3
import csv
from pathlib import Path

THEMES = [
    ("Logistics / org GHG total", "GHG logistics-related or S1+2 total", "32.31 m t CO2e (DHL steering)", "10,151.38 t CO2 eq (AGV S1+S2)", "DHL Group", "AGV Colombia", "no", "DHL:25-26", "AGV:23-25"),
    ("Scope 1 GHG", "Direct / Scope 1", "6.46 m t CO2e logistics S1", "8,918.40–9,129.67 t CO2 eq", "DHL Group", "AGV Colombia", "partial AGV", "DHL:25", "AGV:24;95"),
    ("Scope 2 GHG", "Market-based Scope 2", "0.06 m t CO2e", "1,232.95 t CO2 eq", "DHL Group", "AGV Colombia", "yes AGV", "DHL:25", "AGV:25"),
    ("Scope 3 GHG", "Scope 3 inventory", "25.79 m t (logistics S3)", "not reported (en desarrollo)", "DHL Group", "AGV", "AGV gap", "DHL:25", "AGV:25"),
    ("GHG intensity", "per ton or per shipment", "not reported (DHL deck)", "0.0584 t CO2/ton; 1.210 kg CO2eq/km", "DHL Group", "AGV Colombia", "yes AGV", "1-105", "AGV:25"),
    ("Non-diesel fleet share (AGV)", "PUD e-vehicle % vs no-diesel %", "46.2% (66% target 2030)", "13.6% no diésel (gasolina+gas+eléctrico; p.26)", "DHL Group", "AGV Colombia", "yes AGV", "DHL:24", "AGV:26"),
    ("E-vehicle count / km", "Fleet electrification", "50,604 e-vehicles (Group)", "69,461 km eléctricos 2025", "DHL Group", "AGV Colombia", "yes AGV", "DHL:5;37", "AGV:26"),
    ("CNG / GNV / gas fleet", "Alternative fuels road", "20.5% sustainable fuels road (own)", "868,532 km GNV; 2 GNV bought", "DHL Group", "AGV Colombia", "yes AGV", "DHL:24", "AGV:26"),
    ("Avoided emissions vs diesel", "Baseline comparison", "2.1 m t decarb effects (Group)", "21.95 t eléctrico; 33 t GNV", "DHL Group", "AGV Colombia", "yes AGV", "DHL:10", "AGV:23;26"),
    ("Air pollutants NOx/PM", "Scope 1 tonnage", "NOx 39,247 t; PM10 552 t", "not reported (qualitative only)", "DHL Group", "AGV", "DHL only", "DHL:45", "AGV:44;106"),
    ("Per-shipment / client footprint", "Customer dashboard", "GoGreen per shipment (p.42)", "Dashboard diesel vs gas p.27-28 (gráfico, confirmar AGV)", "DHL Group", "AGV Colombia", "yes AGV", "DHL:42", "AGV:27"),
    ("Colombia / Bogotá split", "Country granularity", "not reported", "Colombia-focused; Brasil sin split GEI", "DHL Group", "AGV", "AGV partial", "DHL:66", "AGV:3;37"),
    ("Third-party fleet", "Subcontracted transport", "Scope 3 upstream (categories)", "85% combustible flota tercerizada", "DHL Group", "AGV Colombia", "yes AGV", "DHL:26", "AGV:44"),
    ("Climate targets", "SBTi / net zero", "SBTi validated; <29m by 2030; NZ 2050", "Zero Waste meta; bajo carbono (narrativa)", "DHL Group", "AGV Colombia", "DHL stronger", "DHL:23", "AGV:4;63"),
    ("Renewable electricity", "Buildings / Scope 2", "96.9% renewable electricity", "Alcance 2 down via grid Colombia (XM)", "DHL Group", "AGV Colombia", "both", "DHL:24", "AGV:25"),
    ("Cold chain / packaging CO2", "Circular packaging", "not in DHL air pack", "1,400 t CO2 avoided reusables", "—", "AGV Colombia", "AGV only", "—", "AGV:4;63"),
]

HEADER = ["theme", "metric_family", "dhl_group_value", "agv_value", "dhl_source_label", "agv_source_label", "colombia_granularity", "dhl_pages", "agv_pages", "notes"]


def main():
    base = Path(__file__).resolve().parent
    rows = []
    for t in THEMES:
        rows.append({
            "theme": t[0],
            "metric_family": t[1],
            "dhl_group_value": t[2],
            "agv_value": t[3],
            "dhl_source_label": t[4],
            "agv_source_label": t[5],
            "colombia_granularity": t[6],
            "dhl_pages": t[7],
            "agv_pages": t[8],
            "notes": "Never merge AGV and DHL entities; overlay is comparative only.",
        })
    with (base / "overlay.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(rows)
    md = [
        "# Overlay AGV × DHL Group (temas alineados)\n",
        "**source: AGV Open Market Informe de Sostenibilidad 2025** | **source: DHL Group 2025 public report**\n",
        "Comparación temática; **no** implica que AGV sea DHL.\n",
        "| theme | DHL Group | AGV Open Market | Colombia flag | DHL p. | AGV p. |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        md.append(
            f"| {r['theme']} | {r['dhl_group_value']} | {r['agv_value']} | {r['colombia_granularity']} | {r['dhl_pages']} | {r['agv_pages']} |"
        )
    (base / "overlay.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("overlay", len(rows))


if __name__ == "__main__":
    main()