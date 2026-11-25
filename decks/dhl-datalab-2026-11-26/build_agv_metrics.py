#!/usr/bin/env python3
"""Build agv-metrics.csv — source: AGV Open Market Informe de Sostenibilidad 2025."""
import csv
from pathlib import Path

SOURCE = "AGV Open Market Informe de Sostenibilidad 2025"
HEADER = ["metric", "value", "unit", "year", "geo", "target", "page", "quote", "source"]

ROWS = [
    ("Empresa (identidad)", "AGV Open Market", "—", "2025", "Colombia y Brasil (grupo)", "", "3", "Informe de Sostenibilidad AGV Open Market, año 2025.", SOURCE),
    ("Ingresos operacionales", "513543", "millones COP", "2025", "Colombia (consolidado informe)", "+12,2 % vs 2024", "23", "Crecimiento del doce coma dos por ciento en ingresos operacionales.", SOURCE),
    ("Colaboradores", "4000", "personas (más de)", "2025", "Colombia", "", "3", "Más de cuatro mil colaboradores encuentran en AGV una oportunidad.", SOURCE),
    ("Clientes activos", "400", "clientes (más de)", "2025", "Colombia", "", "3", "Beneficiando a más de cuatrocientos clientes que confían en nosotros.", SOURCE),
    ("Presencia geográfica", "Colombia y Brasil", "—", "2025", "Colombia; Brasil", "", "3;7", "Más de cuarenta años de trayectoria en Colombia y Brasil.", SOURCE),
    ("Desglose Brasil vs Colombia (GEI)", "not reported", "—", "2025", "Brasil", "", "1-124", "Sin cifras de emisiones separadas por país en este informe.", SOURCE),
    ("Alcance 1 — combustibles (huella total)", "8918.40", "t CO2 eq", "2025", "Colombia", "", "24", "Total, huella de carbono por consumo de combustibles.", SOURCE),
    ("Alcance 1 — emisiones directas GEI (bruto)", "8918.40", "t métricas CO2", "2025", "Colombia", "", "24", "Valor bruto de las emisiones directas de GEI alcance 1.", SOURCE),
    ("Alcance 1 — consumo refrigerantes", "188", "t CO2 eq", "2025", "Colombia", "", "24;95", "Consumo de refrigerantes reportado en inventario GEI.", SOURCE),
    ("Alcance 1 — CO2 biogénico (aparte)", "749.06", "t CO2", "2025", "Colombia", "", "24", "Emisiones biogénicas reportadas separadas del total alcances.", SOURCE),
    ("Alcance 1 — ACPM (diesel)", "8022.23", "t CO2 eq", "2025", "Colombia", "", "95", "Huella por ACPM con factor diez coma quince kg CO2 eq por galón.", SOURCE),
    ("Alcance 1 — GNV (gas)", "896.20", "t CO2 eq", "2025", "Colombia", "", "95", "Huella por gas natural vehicular en flota propia.", SOURCE),
    ("Alcance 1 — total inventario (GRI 305-1)", "9129.67", "t CO2 eq", "2025", "Colombia", "", "95", "TOTAL emisiones directas GEI según tabla GRI 305-1.", SOURCE),
    ("Alcance 2 — energía eléctrica centros", "1232.95", "t CO2 eq", "2025", "Colombia", "−53,57 % vs 2024", "25", "Emisiones indirectas de GEI asociadas a la energía, alcance 2.", SOURCE),
    ("Alcance 2 — factor XM", "0.097", "t CO2 eq/MWh", "2025", "Colombia (red nacional)", "", "25", "Factor de emisión XM usado para electricidad en centros.", SOURCE),
    ("Alcance 1 y 2 — emisiones totales", "10151.38", "t CO2 eq", "2025", "Colombia", "−12,78 % vs 2024", "23;25", "Diez mil ciento cincuenta y un toneladas CO2 eq alcances 1 y 2.", SOURCE),
    ("Intensidad GEI — por tonelada movilizada", "0.0584", "t CO2 / ton", "2025", "Colombia", "−4,7 % vs 2024", "25", "Emisiones por tonelada movilizada en la organización.", SOURCE),
    ("Intensidad GEI — por distancia", "1.210", "kg CO2 eq/km", "2025", "Colombia", "−9,8 % vs 2024", "25", "Emisiones por kilómetro recorrido en operación.", SOURCE),
    ("Alcance 3 — inventario", "not reported", "—", "2025", "Colombia", "en desarrollo", "25", "Estamos desarrollando el inventario de Alcance 3.", SOURCE),
    ("Flota tercerizada — participación combustible", "85", "%", "2025", "Colombia", "", "44", "Consumo de combustible de la flota tercerizada ochenta y cinco por ciento.", SOURCE),
    ("Flota propia vs terceros (GEI cuantificado)", "propia", "Alcance 1+2 reportado", "2025", "Colombia", "terceros excluidos intensidad", "24;73", "ACPM y GNV flota propia; subcontratados fuera del ratio energético.", SOURCE),
    ("GNV — km recorridos", "868532", "km", "2025", "Colombia", "", "26", "En 2025, con ochocientos sesenta y ocho mil quinientos treinta y dos km.", SOURCE),
    ("GNV — emisiones evitadas vs diésel", "33.00", "t CO2 eq", "2025", "Colombia", "", "26", "Ahorro de treinta y tres toneladas CO2 eq frente a diésel.", SOURCE),
    ("GNV — emisiones evitadas 2024", "112.14", "t CO2 eq", "2024", "Colombia", "", "26", "Diferencia frente a diésel en 2024: ciento doce coma catorce toneladas.", SOURCE),
    ("Vehículos GNV adquiridos (cierre 2025)", "2", "vehículos", "2025", "Colombia", "", "26", "Al cierre de 2025, adquirimos dos vehículos a gas natural vehicular.", SOURCE),
    ("Eléctricos última milla — km", "69461", "km", "2025", "Colombia", "", "26", "En 2025, con sesenta y nueve mil cuatrocientos sesenta y un km recorridos.", SOURCE),
    ("Eléctricos — emisiones evitadas vs diésel", "21.95", "t CO2 eq", "2025", "Colombia", "", "26", "Reducción neta de veintiún coma noventa y cinco toneladas CO2 eq.", SOURCE),
    ("Eléctricos — evitadas 2024", "19.94", "t CO2 eq", "2024", "Colombia", "", "26", "Reducción neta de diecinueve coma noventa y cuatro toneladas en 2024.", SOURCE),
    ("Emisiones evitadas — total gas+eléctrico (resumen)", "54.95", "t CO2 eq", "2025", "Colombia", "", "23", "Cincuenta y cuatro coma noventa y cinco tCO2e evitadas (gas y eléctrico).", SOURCE),
    ("Mix flota gasolina, gas y eléctrica", "13.6", "%", "2025", "Colombia", "", "26", "Porcentaje de flota a gasolina, gas y eléctrica: trece coma seis por ciento.", SOURCE),
    ("Flota mitigación — eléctricos (mención GRI)", "5", "vehículos", "2025", "Colombia", "", "106", "Flota de cinco vehículos eléctricos y diez a gas para reducir emisiones.", SOURCE),
    ("Flota mitigación — gas (mención GRI)", "10", "vehículos", "2025", "Colombia", "", "106", "Diez vehículos a gas en líneas de mitigación de material particulado.", SOURCE),
    ("Huella por movimiento — dashboard transporte CO2", "9860.46", "t CO2", "2025", "Colombia", "", "27", "Datos en tiempo real del año 2025 — total tablero transporte.", SOURCE),
    ("Huella por movimiento — toneladas movilizadas (tablero)", "291076.03", "ton", "2025", "Colombia", "", "27", "Total toneladas movilizadas en tablero huella de carbono transporte.", SOURCE),
    ("Huella por movimiento — diesel vs gas (etiqueta)", "reported", "dashboard", "2025", "Colombia", "", "27", "Huella clientes por movimiento diésel y huella evitada vehículos GAS.", SOURCE),
    ("Cadena frío — CO2 evitado embalajes reutilizables", "1400", "t CO2", "2025", "Colombia", "", "4", "Reduciendo más de mil cuatrocientas toneladas de CO₂ en cadena de frío.", SOURCE),
    ("Embalajes reutilizables — emisiones vs un solo uso", "96", "%", "menos", "2025", "Colombia", "", "63", "Embalajes reutilizables emiten noventa y seis por ciento menos.", SOURCE),
    ("Estibas remanufacturadas", "39510", "unidades", "2025", "Colombia", "+12 % vs 2024", "63", "Treinta y nueve mil quinientas diez estibas remanufacturadas en 2025.", SOURCE),
    ("Red logística nacional — sitios", "30", "sitios", "2025", "Colombia", "15 bodegas + 15 cross-docks", "23;37", "Red nacional de treinta sitios operativos en Colombia.", SOURCE),
    ("Red logística — área almacenamiento", "160115", "m²", "2025", "Colombia", "", "23;37", "Ciento sesenta mil ciento quince metros cuadrados de red nacional.", SOURCE),
    ("Posiciones de paletización", "120000", "posiciones", "2025", "Colombia", "", "23", "Ciento veinte mil posiciones de paletización en la red.", SOURCE),
    ("CILOG Bogotá — viajes camión evitados/día", "94", "viajes/día", "2025", "Bogotá D.C.", "", "37", "Eliminó noventa y cuatro trayectos de camiones diarios en CILOG.", SOURCE),
    ("CILOG — CO2 evitado", "955", "kg CO2/mes", "2025", "Bogotá D.C.", "", "37", "Redujo novecientos cincuenta y cinco kilogramos CO₂ por mes.", SOURCE),
    ("Consumo energético consolidado", "173188.70", "GJ", "2025", "Colombia", "+0,80 % vs 2024", "73", "Consumo de energía consolidado 2025 en gigajulios.", SOURCE),
    ("Intensidad energética", "0.9921", "GJ/ton transportada", "2025", "Colombia", "+10,28 % vs 2024", "73", "Ratio de intensidad energética de la organización.", SOURCE),
    ("Carga total movilizada", "174557.05", "ton", "2025", "Colombia", "−8,61 % vs 2024", "73", "Carga total movilizada para indicador de intensidad energética.", SOURCE),
    ("NOx / SOx / PM2.5 / PM10 (inventario)", "not reported", "—", "2025", "Colombia", "", "44;59;106", "Mención cualitativa calidad del aire; sin toneladas NOx o PM.", SOURCE),
    ("Meta Zero Waste", "certificación", "objetivo", "—", "Colombia (Bogotá)", "", "63", "Meta: certificación Zero Waste en operación responsable.", SOURCE),
    ("Metodología huella carbono", "ICONTEC validada", "—", "2025", "Colombia", "", "23;26", "Metodología de huella de carbono validada con ICONTEC.", SOURCE),
    ("Proveedores activos", "652", "proveedores", "2025", "Colombia", "", "23", "Seiscientos cincuenta y dos proveedores activos en cadena.", SOURCE),
]


def main():
    out = Path(__file__).resolve().parent / "agv-metrics.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(ROWS)
    print(len(ROWS), "rows ->", out)


if __name__ == "__main__":
    main()