/* CTH Living lab · inlined data (ported from livinglab/cth-living-lab-skeleton-v2.html, 4 Oct 2026).
   L1 = REAL provisional RMCAB snapshot 2026-10-04 09:00 COT + IDEAM SISAIRE 2024 annual means. L2/L3 = EXAMPLE placeholders. */
export const RAW_BASELINE = {
  datasetId: 'cth-ll-baseline-bogota',
  version: 'v2026.10.04-01',
  snapshotHour: '2026-10-04T09:00:00-05:00',
  retrievedAt: '2026-10-04T09:36:23-05:00',
  status: 'REAL — provisional real-time hourly data as published by RMCAB (not yet validated by SDA)',
  sources: [
    {lane:'L1 live hourly', owner:'Secretaría Distrital de Ambiente (SDA) — Red de Monitoreo de Calidad del Aire de Bogotá (RMCAB)',
     url:'http://rmcab.ambientebogota.gov.co/ajax/getAllStations/', page:'http://rmcab.ambientebogota.gov.co/home/map',
     note:'Public endpoint behind the RMCAB map page (no login). Station names, coordinates, PM2.5 (µg/m³), O3 (ppb), PM10, hour label 2026-10-04 09:00.'},
    {lane:'L1 reference (annual)', owner:'IDEAM — SISAIRE, “Calidad del Aire en Colombia (Promedio Anual)”, datos.gov.co kekd-7v7h',
     url:'https://www.datos.gov.co/resource/kekd-7v7h.json', page:'https://www.datos.gov.co/d/kekd-7v7h',
     note:'2024 annual means: PM2.5 (24-h basis) and O3 (8-h basis), µg/m³. Used as each station’s historical reference in the anomaly processor.'}
  ],
  stations: [
 {
  "id": "RMCAB-01",
  "rmcabSerial": 1,
  "name": "Usaquén",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.71035,
  "lon": -74.030417,
  "address": "TV-9 No 133-95",
  "pm25": 2.2,
  "o3_ppb": null,
  "pm10": 14.6,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "USAQUÉN",
   "pm25_24h_annual_mean": 12.2,
   "pm25_repr_pct": 99.0,
   "o3_8h_annual_mean_ugm3": 40.3
  }
 },
 {
  "id": "RMCAB-03",
  "rmcabSerial": 3,
  "name": "Carvajal - Sevillana",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.595833,
  "lon": -74.1485,
  "address": "Auto Sur No 61-40",
  "pm25": 19.9,
  "o3_ppb": null,
  "pm10": null,
  "o3_monitored": false,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "CARVAJAL - SEVILLANA",
   "pm25_24h_annual_mean": 33.3,
   "pm25_repr_pct": 96.0,
   "o3_8h_annual_mean_ugm3": null
  }
 },
 {
  "id": "RMCAB-04",
  "rmcabSerial": 4,
  "name": "Tunal",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.57619,
  "lon": -74.13093,
  "address": "Carrera 24 N° 49-86 sur",
  "pm25": 7.0,
  "o3_ppb": 16.7,
  "pm10": 44.0,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "TUNAL",
   "pm25_24h_annual_mean": 17.2,
   "pm25_repr_pct": 95.0,
   "o3_8h_annual_mean_ugm3": 30.3
  }
 },
 {
  "id": "RMCAB-05",
  "rmcabSerial": 5,
  "name": "Centro de Alto Rendimiento",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.658333,
  "lon": -74.083889,
  "address": "Cl 63 No 47-06",
  "pm25": 19.1,
  "o3_ppb": 16.0,
  "pm10": 16.1,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "C. ALTO RENDIMIENTO",
   "pm25_24h_annual_mean": 13.4,
   "pm25_repr_pct": 96.0,
   "o3_8h_annual_mean_ugm3": 29.2
  }
 },
 {
  "id": "RMCAB-06",
  "rmcabSerial": 6,
  "name": "Las Ferias",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.6907,
  "lon": -74.082483,
  "address": "AV Calle 80 N° 69Q - 50",
  "pm25": 11.0,
  "o3_ppb": 18.6,
  "pm10": 21.0,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "LAS FERIAS",
   "pm25_24h_annual_mean": 16.3,
   "pm25_repr_pct": 91.0,
   "o3_8h_annual_mean_ugm3": 29.8
  }
 },
 {
  "id": "RMCAB-08",
  "rmcabSerial": 8,
  "name": "Guaymaral",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.78375,
  "lon": -74.044139,
  "address": "Auto Norte KM 13",
  "pm25": 11.0,
  "o3_ppb": 13.2,
  "pm10": 31.0,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "GUAYMARAL",
   "pm25_24h_annual_mean": 15.1,
   "pm25_repr_pct": 95.0,
   "o3_8h_annual_mean_ugm3": 20.6
  }
 },
 {
  "id": "RMCAB-09",
  "rmcabSerial": 9,
  "name": "Kennedy",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.62505,
  "lon": -74.161333,
  "address": "Cr 86 No 40-55 Sur",
  "pm25": 22.2,
  "o3_ppb": 6.3,
  "pm10": 50.2,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "KENNEDY",
   "pm25_24h_annual_mean": 19.5,
   "pm25_repr_pct": 94.0,
   "o3_8h_annual_mean_ugm3": 23.1
  }
 },
 {
  "id": "RMCAB-11",
  "rmcabSerial": 11,
  "name": "Suba",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.761247,
  "lon": -74.093461,
  "address": "Ave Corpas Km 13 / KR 111 157-45",
  "pm25": 15.0,
  "o3_ppb": 11.2,
  "pm10": 53.8,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "SUBA",
   "pm25_24h_annual_mean": 16.7,
   "pm25_repr_pct": 99.0,
   "o3_8h_annual_mean_ugm3": 27.7
  }
 },
 {
  "id": "RMCAB-13",
  "rmcabSerial": 13,
  "name": "Puente Aranda",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.631767,
  "lon": -74.117483,
  "address": "Cr 65 No 10-95",
  "pm25": 5.7,
  "o3_ppb": 4.6,
  "pm10": 30.0,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "PUENTE ARANDA",
   "pm25_24h_annual_mean": 15.1,
   "pm25_repr_pct": 99.0,
   "o3_8h_annual_mean_ugm3": 20.5
  }
 },
 {
  "id": "RMCAB-17",
  "rmcabSerial": 17,
  "name": "MinAmbiente",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.625486,
  "lon": -74.066981,
  "address": "CL 37 No. 8 - 40",
  "pm25": 14.0,
  "o3_ppb": 13.1,
  "pm10": 20.0,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "MINAMBIENTE",
   "pm25_24h_annual_mean": 15.6,
   "pm25_repr_pct": 97.0,
   "o3_8h_annual_mean_ugm3": 28.1
  }
 },
 {
  "id": "RMCAB-24",
  "rmcabSerial": 24,
  "name": "San Cristóbal",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.572553,
  "lon": -74.083814,
  "address": "Carrera 2 Este No. 12-78 Sur",
  "pm25": 9.0,
  "o3_ppb": 10.9,
  "pm10": 29.0,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "SAN CRISTÓBAL",
   "pm25_24h_annual_mean": 12.8,
   "pm25_repr_pct": 97.0,
   "o3_8h_annual_mean_ugm3": 22.5
  }
 },
 {
  "id": "RMCAB-26",
  "rmcabSerial": 26,
  "name": "Móvil 7ma",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.645,
  "lon": -74.061556,
  "address": "AV boyaca calle 63",
  "pm25": 9.1,
  "o3_ppb": null,
  "pm10": 22.1,
  "o3_monitored": false,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "MÓVIL 7MA",
   "pm25_24h_annual_mean": 14.7,
   "pm25_repr_pct": 98.0,
   "o3_8h_annual_mean_ugm3": null
  }
 },
 {
  "id": "RMCAB-27",
  "rmcabSerial": 27,
  "name": "Bolivia",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.735806,
  "lon": -74.125889,
  "address": "Avenida Calle 80  # 121-98",
  "pm25": 7.4,
  "o3_ppb": 11.3,
  "pm10": 29.4,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "BOLIVIA",
   "pm25_24h_annual_mean": 11.4,
   "pm25_repr_pct": 70.0,
   "o3_8h_annual_mean_ugm3": 12.5
  }
 },
 {
  "id": "RMCAB-30",
  "rmcabSerial": 30,
  "name": "Fontibón",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.678242,
  "lon": -74.143819,
  "address": "KR 96G 17B 49",
  "pm25": 9.1,
  "o3_ppb": null,
  "pm10": 33.2,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "FONTIBÓN",
   "pm25_24h_annual_mean": 20.7,
   "pm25_repr_pct": 99.0,
   "o3_8h_annual_mean_ugm3": 27.8
  }
 },
 {
  "id": "RMCAB-32",
  "rmcabSerial": 32,
  "name": "Usme",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.531206,
  "lon": -74.111714,
  "address": "Carrera 11 # 65 D 50 Sur",
  "pm25": 19.2,
  "o3_ppb": 23.0,
  "pm10": 36.0,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "USME",
   "pm25_24h_annual_mean": 13.7,
   "pm25_repr_pct": 100.0,
   "o3_8h_annual_mean_ugm3": 31.1
  }
 },
 {
  "id": "RMCAB-34",
  "rmcabSerial": 34,
  "name": "Jazmín",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.6085,
  "lon": -74.114944,
  "address": "Calle 1 G # 41 A 39",
  "pm25": 15.7,
  "o3_ppb": 4.0,
  "pm10": 28.1,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "EL JAZMÍN",
   "pm25_24h_annual_mean": 16.4,
   "pm25_repr_pct": 100.0,
   "o3_8h_annual_mean_ugm3": 26.6
  }
 },
 {
  "id": "RMCAB-37",
  "rmcabSerial": 37,
  "name": "Ciudad Bolívar",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.577806,
  "lon": -74.166278,
  "address": "Calle 70 Sur # 56 - 11",
  "pm25": 18.9,
  "o3_ppb": 12.4,
  "pm10": 53.4,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "CIUDAD BOLIVAR",
   "pm25_24h_annual_mean": 17.4,
   "pm25_repr_pct": 99.0,
   "o3_8h_annual_mean_ugm3": 27.6
  }
 },
 {
  "id": "RMCAB-38",
  "rmcabSerial": 38,
  "name": "Colina",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.737194,
  "lon": -74.069472,
  "address": "Avenida Boyacá No 142ª-55",
  "pm25": 11.9,
  "o3_ppb": 9.8,
  "pm10": 11.1,
  "o3_monitored": true,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "COLINA",
   "pm25_24h_annual_mean": 12.5,
   "pm25_repr_pct": 99.0,
   "o3_8h_annual_mean_ugm3": 19.4
  }
 },
 {
  "id": "RMCAB-39",
  "rmcabSerial": 39,
  "name": "Móvil Fontibón",
  "operator": "SDA",
  "network": "RMCAB",
  "lat": 4.668,
  "lon": -74.1485,
  "address": "Cra. 98 #16 B 50",
  "pm25": 28.0,
  "o3_ppb": null,
  "pm10": 51.8,
  "o3_monitored": false,
  "hour": "2026-10-04 09:00",
  "sisaire2024": {
   "stationName": "MÓVIL FONTIBÓN",
   "pm25_24h_annual_mean": 20.8,
   "pm25_repr_pct": 96.0,
   "o3_8h_annual_mean_ugm3": 20.1
  }
 },
 {
  "id": "CAR-MOCHUELO",
  "rmcabSerial": null,
  "name": "Mochuelo",
  "operator": "CAR",
  "network": "CAR (via IDEAM SISAIRE)",
  "lat": 4.530864,
  "lon": -74.142125,
  "address": "—",
  "pm25": null,
  "o3_ppb": null,
  "pm10": null,
  "o3_monitored": false,
  "hour": null,
  "sisaire2024": {
   "stationName": "MOCHUELO",
   "pm25_24h_annual_mean": 35.7,
   "pm25_repr_pct": 90.0,
   "o3_8h_annual_mean_ugm3": null
  }
 }
],
  notices: {
    'RMCAB-03': 'RMCAB site notice (4 Oct 2026): Carvajal station data not updating (communication failure) — this value may be stale.',
    'RMCAB-26': 'RMCAB site notice: the Móvil 7ma PM2.5 monitor has been moved to Puente Aranda — treat this PM2.5 value with caution.',
    'RMCAB-32': 'Coordinates from the RMCAB feed differ by ~0.6 km from the SDA GIS station layer (4.53206, −74.11714).'
  },
  coordCheck: '19 of 19 live stations cross-checked against the SDA GIS layer (mapas.ambientebogota.gov.co … Estacion_calidad_aire/MapServer/0): 18 within 50 m, Usme ~0.6 km apart.'
};

/* Candidate client sites. Ramo and Bolívar positions are EXAMPLE locations (not verified addresses).
   Diaco pins are real public sites; coordinates geocoded approximately (OSM Nominatim, 4 Oct 2026). */
export const RAW_SITES = [
  {id:'ramo',    label:'Ramo',       lat:4.6555, lon:-74.1245, placed:true, kind:'example'},
  {id:'bolivar', label:'Bolívar',    lat:4.6650, lon:-74.0600, placed:true, kind:'example'},
  {id:'diaco-fontibon', label:'Diaco · Fontibón', lat:4.6782, lon:-74.1552, placed:true, kind:'real', ref:true,
   addr:'Calle 15F #112A-91, Barrio Moravia (Fontibón), Bogotá', what:{es:'Planta de desintegración vehicular (pública)',en:'Vehicle dismantling plant (public)'},
   note:{es:'Dirección pública; coordenadas aproximadas por cruce Calle 15F × Carrera 112A (OSM Nominatim).',en:'Public address; approximate coordinates from the Calle 15F × Carrera 112A intersection (OSM Nominatim).'}},
  {id:'diaco-muna', label:'Diaco · Muña (Sibaté)', lat:4.530, lon:-74.255, placed:true, kind:'real', ref:true,
   addr:'Planta Muña, Sibaté (Cundinamarca), al sur de Bogotá', what:{es:'Planta de laminación (Reporte Integrado 2022-2023)',en:'Rolling plant (2022-2023 Integrated Report)'},
   note:{es:'Ubicación aproximada en la zona del embalse del Muña; por verificar la dirección exacta.',en:'Approximate location near the Muña reservoir; exact address to verify.'}}
];

/* L2 — client proprietary context data. ALWAYS EXAMPLE placeholders. */
export const RAW_L2 = [
  {lane:'L2', id:'L2-RAMO-01', site:'ramo', owner:'Ramo (client)', pm25:27.0, ts:'2026-10-04T09:00:00-05:00', example:true,
   provenance:'EXAMPLE placeholder — client context slot, no real Ramo data received'},
  {lane:'L2', id:'L2-BOL-01', site:'bolivar', owner:'Bolívar (client)', pm25:16.0, ts:'2026-10-04T09:00:00-05:00', example:true,
   provenance:'EXAMPLE placeholder — client context slot, no real Bolívar data received'}
  /* Client TBD: empty slot */
];

/* L3 — startup proprietary measurement data. ALWAYS EXAMPLE placeholders.
   raw = uncalibrated low-cost sensor reading; before = pre-intervention period, after = post-intervention period. */
export const RAW_PARTNER_FEEDS = [
  {partner:'air4u', owner:'Air4U (partner)', status:'slot open · EXAMPLE values', example:true,
   provenance:'EXAMPLE — Air4U feed slot, no real data yet',
   sensors:[
    {id:'A4U-R1', site:'ramo', dLat: 0.0030, dLon:-0.0060, rawBefore:34.2, rawAfter:26.0, ts:'2026-10-04T09:00:00-05:00'},
    {id:'A4U-R2', site:'ramo', dLat:-0.0045, dLon:-0.0050, rawBefore:31.5, rawAfter:24.3, ts:'2026-10-04T09:00:00-05:00'},
    {id:'A4U-R3', site:'ramo', dLat:-0.0040, dLon: 0.0060, rawBefore:36.8, rawAfter:27.9, ts:'2026-10-04T09:00:00-05:00'}
   ]},
  {partner:'tbd', owner:'Partner TBD', status:'empty slot — awaiting partner onboarding', example:true, provenance:'Empty slot', sensors:[]}
];
