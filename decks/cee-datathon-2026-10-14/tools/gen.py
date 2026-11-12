#!/usr/bin/env python3
"""Generate slides/*.html for the CEE × CTH 14 oct 2026 deck."""
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "slides"
OUT.mkdir(exist_ok=True)
for f in OUT.glob("*.html"): f.unlink()

FOOT = '''  <footer class="footer">
    <span>CleantechHUB · Inspira. Actúa. Transforma.</span>
    <span>CEE Externado × CleantechHUB · 14 oct 2026</span>
    <span class="slide-num"></span>
  </footer>'''

def P(t):  # hidden PENDIENTE chip (visible only with ?review)
    return f'<span class="pendiente">{t}</span>'

S = {}

# 01 Portada ---------------------------------------------------------------
S["01-portada"] = f'''<style>
.s-01 .slide-inner{{justify-content:flex-end;padding-bottom:40px}}
.s-01 .logo-row{{position:absolute;top:0;left:0}}
.s-01 h1{{font-size:100px;margin:0 0 14px}}
.s-01 .subtitle{{font-size:42px;color:var(--cyan);margin-bottom:18px}}
.s-01 .meta{{font-size:32px;font-weight:600;margin-bottom:28px}}
.s-01 .cards{{display:grid;grid-template-columns:1.35fr 1fr;gap:24px}}
.s-01 .glass h3{{font-size:28px;color:var(--green);text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px}}
.s-01 .glass p{{font-size:30px;line-height:1.35;margin-bottom:8px}}
</style>
<section class="slide has-photo s-01 active" style="--bg: url('img/p-portada.jpg')">
  <div class="slide-inner">
    <div class="logo-row">
      <img class="logo-cth" src="img/logo-cth-white.svg" alt="CleantechHUB">
      <span class="logo-shield"><img src="img/logo-cee-externado.png" alt="Centro de Emprendimiento Externadista – CEE"></span>
    </div>
    <p class="tagline">Inspira. Actúa. Transforma.</p>
    <h1>CEE Externado × CleantechHUB</h1>
    <p class="subtitle">El tamaño del proyecto: actores, alianza y Datathon</p>
    <p class="meta">Miércoles 14 oct 2026 · 10:00 · Universidad Externado de Colombia, Edificio H</p>
    <div class="cards">
      <div class="glass">
        <h3>Universidad Externado de Colombia</h3>
        <p><strong>Marlene Díaz</strong> · Centro de Emprendimiento Externadista (CEE)</p>
        <p><strong>Diego Alejandro Díaz Malagón</strong> · Coordinador de Innovación</p>
      </div>
      <div class="glass">
        <h3>Presenta</h3>
        <p><strong>Gideon Blaauw</strong><br>CleantechHUB · CTH Foundation</p>
      </div>
    </div>
    {P("Uso del logo CEE en co-branding: tomado del paquete de marca Externado (Drive); confirmar con Marlene")}
  </div>
{FOOT}
</section>
'''

# 02 El proyecto en una mirada ---------------------------------------------
S["02-tamano"] = f'''<style>
.s-02 .norte{{font-size:46px;line-height:1.3;font-weight:700;max-width:1640px;margin:0 0 34px}}
.s-02 .norte em{{font-style:normal;color:var(--cyan)}}
.s-02 .kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin-bottom:30px}}
.s-02 .kpi{{padding:26px 24px}}
.s-02 .kpi .n{{font-size:84px;font-weight:700;color:var(--cyan);line-height:1;margin-bottom:12px}}
.s-02 .kpi p{{font-size:26px;line-height:1.35;margin:0}}
.s-02 .agenda{{display:flex;gap:16px;align-items:center;flex-wrap:wrap}}
.s-02 .agenda .lbl{{font-size:26px;font-weight:700;color:var(--green);margin-right:6px}}
.s-02 .agenda span.step{{font-size:28px;font-weight:600;padding:10px 22px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25)}}
</style>
<section class="slide has-photo s-02" style="--bg: url('img/p-norte.jpg')">
  <div class="slide-inner">
    <span class="block-badge">El proyecto en una mirada</span>
    <div style="margin-top:auto">
      <p class="kicker">Norte compartido</p>
      <p class="norte">Desarrollar <em>flujos de digitalización</em> que aceleren el desarrollo empresarial en clima, desde la Universidad y para América Latina.</p>
      <div class="kpis">
        <div class="glass kpi"><div class="n">5 años</div><p>Acuerdo de colaboración Fundación CleantechHUB × Universidad Externado, firmado el 3 jul 2024</p></div>
        <div class="glass kpi"><div class="n">4 + 1</div><p>Frentes del Otrosí: Datathon, Climate Data Week, Data Lab e Investigación, más HUB REIN Colombia</p></div>
        <div class="glass kpi"><div class="n">5</div><p>Entornos del Datalab ya en vivo: vitrina, Datathon, Living lab, Producto cliente y Taller</p></div>
        <div class="glass kpi"><div class="n">71</div><p>Corporativos colombianos en la vitrina, leídos desde su reporte de sostenibilidad</p></div>
      </div>
      <div class="agenda"><span class="lbl">Hoy</span><span class="step">1 · Actores</span><span class="step">2 · Alianza CEE–CTH</span><span class="step">3 · Datathon</span><span class="step">4 · Datalab en vivo</span><span class="step">5 · Próximos pasos</span></div>
      {P("Texto final del Otrosí y su estado en el trámite contractual de la Universidad")}
    </div>
  </div>
{FOOT}
</section>
'''

# 03 Actores ----------------------------------------------------------------
S["03-actores"] = f'''<style>
.s-03 .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;flex:1;min-height:0}}
.s-03 .glass{{padding:20px 24px;display:flex;flex-direction:column}}
.s-03 .role{{font-size:22px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--green);margin-bottom:6px}}
.s-03 h3{{font-size:36px;color:#fff;margin-bottom:10px}}
.s-03 p{{font-size:25px;line-height:1.36;margin-bottom:6px}}
.s-03 .pendiente{{font-size:19px}}
.s-03 .glass.pot{{border:2px dashed rgba(178,238,250,.45);background:rgba(255,255,255,.05)}}
</style>
<section class="slide slide-deep s-03">
  <span class="block-badge">1 · Actores</span>
  <h2 class="slide-title">Actores que vamos a articular</h2>
  <div class="slide-main" style="flex:1;display:flex;flex-direction:column;min-height:0">
    <div class="grid">
      <div class="glass"><div class="role">Academia · anfitrión</div><h3>CEE Externado</h3>
        <p>Investigación, academia y cupo de estudiantes y emprendedores.</p>
        <p class="cyan">Coordinación de Innovación: puente con gobierno y Estado.</p></div>
      <div class="glass"><div class="role">Método y plataforma</div><h3>CleantechHUB</h3>
        <p>Método, stack de datos abierto (n8n · Baserow · Metabase), Academy y Datathon.</p>
        <p class="cyan">Datalab en vivo: datalab.cleantechhub.net</p></div>
      <div class="glass"><div class="role">Capa de datos e investigación</div><h3>Observatorio · HUB REIN Colombia</h3>
        <p>Datos climáticos y de observación de la Tierra al servicio de la investigación sobre el entorno de negocios en LATAM.</p>
        {P("Nombre «Observatorio» y alcance de HUB REIN Colombia por validar con CEE; no figuran en el acuerdo de 2024")}</div>
      <div class="glass"><div class="role">Usuarios del flujo</div><h3>Startups y emprendedores</h3>
        <p>Primero negocios digitales; después datos e IA para startups climáticas.</p>
        <p class="muted">Ejemplos ilustrativos: Air4U (Externado Emprende+) y Biotalega.</p>
        {P("Biotalega: página oficial por confirmar; ambos solo como ejemplo")}</div>
      <div class="glass"><div class="role">Demanda</div><h3>Corporativos</h3>
        <p>71 empresas colombianas en la vitrina del Datalab, leídas desde su propio reporte de sostenibilidad, con código CIIU.</p>
        <p class="muted">Sus brechas se convierten en retos para la Datathon.</p></div>
      <div class="glass pot"><div class="role">Entorno habilitante · potencial</div><h3>Aliados por convocar</h3>
        <p>Atenea · APC Colombia · Innpulsa · Davivienda · SENA</p>
        <p class="muted">Otros mencionados: CAF (público) y ESRI (capa geo).</p>
        {P("Ningún aliado ha confirmado participación; roles exactos de APC/CAF/ESRI por mapear")}</div>
    </div>
  </div>
{FOOT}
</section>
'''

# 04 Alianza / triángulo ----------------------------------------------------
S["04-alianza"] = f'''<style>
.s-04 .wrap{{display:grid;grid-template-columns:900px 1fr;gap:44px;flex:1;min-height:0;align-items:center}}
.s-04 svg text{{font-family:'Open Sans',sans-serif}}
.s-04 .side .glass{{margin-bottom:18px;padding:22px 26px}}
.s-04 .side h3{{font-size:32px;margin-bottom:8px}}
.s-04 .side p{{font-size:27px;line-height:1.38;margin:0}}
</style>
<section class="slide slide-deep s-04">
  <span class="block-badge">2 · Alianza</span>
  <h2 class="slide-title">La alianza CEE Universidad – CleantechHUB</h2>
  <div class="slide-main wrap">
    <svg viewBox="0 0 900 700" width="900" height="700" role="img" aria-label="Triángulo de alianza">
      <defs><linearGradient id="tg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#69B5FA" stop-opacity=".28"/><stop offset="1" stop-color="#0C498A" stop-opacity=".15"/></linearGradient></defs>
      <polygon points="450,70 150,600 750,600" fill="url(#tg)" stroke="#B2EEFA" stroke-width="4"/>
      <circle cx="450" cy="70" r="16" fill="#B2EEFA"/><circle cx="150" cy="600" r="16" fill="#9DC384"/><circle cx="750" cy="600" r="16" fill="#9DC384"/>
      <text x="450" y="34" text-anchor="middle" font-size="30" font-weight="700" fill="#fff">Observatorio · HUB REIN Colombia</text>
      <text x="150" y="650" text-anchor="middle" font-size="30" font-weight="700" fill="#fff">CleantechHUB</text>
      <text x="150" y="684" text-anchor="middle" font-size="22" fill="#B2EEFA">Fundación</text>
      <text x="750" y="650" text-anchor="middle" font-size="30" font-weight="700" fill="#fff">CEE Externado</text>
      <text x="750" y="684" text-anchor="middle" font-size="22" fill="#B2EEFA">Universidad</text>
      <g font-weight="700" fill="#fff" font-size="28" text-anchor="middle">
        <rect x="335" y="250" width="230" height="56" rx="12" fill="#0C498A" stroke="#B2EEFA" stroke-width="2"/><text x="450" y="288">1 · Datathon</text>
        <rect x="232" y="330" width="208" height="56" rx="12" fill="#0C498A" stroke="#B2EEFA" stroke-width="2"/><text x="336" y="368">3 · Data Lab</text>
        <rect x="456" y="330" width="250" height="56" rx="12" fill="#0C498A" stroke="#B2EEFA" stroke-width="2"/><text x="581" y="368">4 · Investigación</text>
        <rect x="290" y="410" width="320" height="56" rx="12" fill="#0C498A" stroke="#B2EEFA" stroke-width="2"/><text x="450" y="448">2 · Climate Data Week</text>
      </g>
      <g font-size="24" font-weight="700" fill="#9DC384" text-anchor="middle">
        <rect x="200" y="520" width="500" height="46" rx="23" fill="rgba(157,195,132,.18)" stroke="#9DC384" stroke-width="2"/>
        <text x="450" y="551">Rieles: Programas · Finanzas</text>
      </g>
    </svg>
    <div class="side">
      <div class="glass"><h3>Lo que ya existe</h3><p>Acuerdo de colaboración Fundación CleantechHUB × Universidad Externado, firmado el 3 jul 2024 por cinco años.</p></div>
      <div class="glass"><h3>Lo que suma el Otrosí</h3><p>Amplía el alcance sin cambiar el plazo: Datathon, Climate Data Week, Data Lab e Investigación, y suma HUB REIN Colombia.</p>
        {P("Estado del Otrosí: sin acta del 1 oct; confirmar si ya está en trámite contractual interno")}</div>
      <div class="glass"><h3>Cómo se sostiene</h3><p>Dos rieles transversales: Programas (de la idea al mercado) y Finanzas (cómo se financian las acciones conjuntas).</p>
        {P("Numeración de cláusulas: usar la del texto final del Otrosí (borrador: Investigación cl. 1.5; Programas cl. 1.2/1.4; Finanzas cl. QUINTA)")}</div>
    </div>
  </div>
{FOOT}
</section>
'''

# 05 Otrosí: cinco frentes --------------------------------------------------
S["05-otrosi"] = f'''<style>
.s-05 .slide-inner{{justify-content:flex-end}}
.s-05 h2{{margin-bottom:26px}}
.s-05 .cols{{display:grid;grid-template-columns:repeat(5,1fr);gap:18px}}
.s-05 .glass{{padding:22px 20px;display:flex;flex-direction:column;background:rgba(5,26,51,.55)}}
.s-05 .num{{font-size:22px;font-weight:700;color:var(--green);letter-spacing:.06em;text-transform:uppercase}}
.s-05 h3{{font-size:32px;color:#fff;margin:6px 0 10px;line-height:1.15}}
.s-05 p{{font-size:24px;line-height:1.38;margin-bottom:8px}}
.s-05 .when{{margin-top:auto;font-size:24px;font-weight:700;color:var(--cyan);padding-top:10px;border-top:1px solid rgba(255,255,255,.18)}}
</style>
<section class="slide has-photo s-05" style="--bg: url('img/p-otrosi.jpg')">
  <div class="slide-inner">
    <span class="block-badge">2 · Alianza · Otrosí</span>
    <h2>El Otrosí: cinco frentes, un mismo flujo</h2>
    <div class="cols">
      <div class="glass"><div class="num">Frente 1</div><h3>Datathon</h3><p>Sprint de datos climáticos: estudiantes y emprendedores construyen sobre datos reales.</p><div class="when">nov 2026 · Semana Global del Emprendimiento</div>{P("Día exacto (pizarrón: 18 nov, GEN SGE 17–19) frente al calendario Academy")}</div>
      <div class="glass"><div class="num">Frente 2</div><h3>Climate Data Week</h3><p>Semana de datos climáticos en Bogotá que conecta Universidad, startups, corporativos y aliados.</p><div class="when">1T 2027 · Bogotá</div>{P("Fecha y sede por confirmar")}</div>
      <div class="glass"><div class="num">Frente 3</div><h3>Data Lab</h3><p>Laboratorio aplicado: lo que nace en la Datathon se mide en un Living lab con reglas de acceso.</p><div class="when">En vivo hoy · datalab.cleantechhub.net</div></div>
      <div class="glass"><div class="num">Frente 4</div><h3>Investigación</h3><p>Línea CEE sobre el entorno de negocios en LATAM y los modelos de negocio que habilitan los datos.</p><div class="when">Con el CEE</div>{P("Línea, responsables y entregables de investigación por definir con CEE")}</div>
      <div class="glass"><div class="num">+1</div><h3>HUB REIN Colombia</h3><p>Nodo colombiano para conectar el trabajo de la alianza con una red internacional de innovación.</p><div class="when">Alcance por definir</div>{P("Alcance y estado de HUB REIN Colombia por confirmar")}</div>
    </div>
  </div>
{FOOT}
</section>
'''

# 06 Datathon: propósito ----------------------------------------------------
S["06-datathon-proposito"] = f'''<style>
.s-06 .slide-inner{{justify-content:flex-end}}
.s-06 .purpose{{font-size:44px;line-height:1.3;font-weight:700;max-width:1700px;margin:0 0 28px}}
.s-06 .purpose em{{font-style:normal;color:var(--cyan)}}
.s-06 .row{{display:grid;grid-template-columns:1fr 1fr 1.1fr;gap:22px}}
.s-06 .glass{{padding:24px 26px;background:rgba(5,26,51,.55)}}
.s-06 .step{{font-size:22px;font-weight:700;color:var(--green);letter-spacing:.06em;text-transform:uppercase}}
.s-06 h3{{font-size:34px;color:#fff;margin:6px 0 8px}}
.s-06 p{{font-size:26px;line-height:1.38;margin-bottom:6px}}
</style>
<section class="slide has-photo s-06" style="--bg: url('img/p-equipo.jpg')">
  <div class="slide-inner">
    <span class="block-badge">3 · Datathon</span>
    <p class="kicker">Propósito</p>
    <p class="purpose">Que estudiantes y emprendedores conviertan <em>datos en flujos digitales</em> que aceleran negocios reales, y que la Universidad lidere ese aprendizaje.</p>
    <div class="row">
      <div class="glass"><div class="step">Escalón 1 · primero</div><h3>Negocios digitales</h3><p>Pasar de Excel y WhatsApp a una tabla viva, un flujo automatizado y un tablero.</p></div>
      <div class="glass"><div class="step">Escalón 2 · siguiente</div><h3>Datos e IA para startups climáticas</h3><p>Sensores, APIs y modelos. Ejemplos ilustrativos: Air4U (calidad del aire) y Biotalega.</p></div>
      <div class="glass"><div class="step">Formato</div><h3>Abierto, efímero, con datos reales</h3><p>Abierto a participantes registrados durante una ventana de 4–6 semanas. Entra una foto de datos, sale una foto, y se borra al cerrar.</p></div>
    </div>
    {P("Cupo, scoring de selección y nombre del certificado por definir con CEE")}
  </div>
{FOOT}
</section>
'''

# 07 Viaje ------------------------------------------------------------------
S["07-viaje"] = f'''<style>
.s-07 .steps{{display:grid;grid-template-columns:repeat(5,1fr);gap:18px;margin-top:18px}}
.s-07 .glass{{padding:0 0 18px;overflow:hidden;display:flex;flex-direction:column}}
.s-07 .glass img{{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;display:block;border-bottom:2px solid rgba(178,238,250,.35)}}
.s-07 .body{{padding:16px 20px 0}}
.s-07 .n{{font-size:22px;font-weight:700;color:var(--green);letter-spacing:.06em;text-transform:uppercase}}
.s-07 h3{{font-size:36px;color:#fff;margin:4px 0 8px}}
.s-07 p{{font-size:26px;line-height:1.36;margin-bottom:6px}}
.s-07 .tool{{font-size:22px;color:var(--cyan);font-weight:700}}
.s-07 .rule{{margin-top:30px;display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.s-07 .rule .glass{{padding:20px 26px;display:block}}
.s-07 .rule p{{font-size:27px;margin:0}}
</style>
<section class="slide slide-deep s-07">
  <span class="block-badge">3 · Datathon · el viaje</span>
  <h2 class="slide-title">Del informe al tablero en vivo</h2>
  <div class="slide-main">
    <div class="steps">
      <div class="glass"><img src="img/j-scene-01.jpg" alt=""><div class="body"><div class="n">Paso 1</div><h3>Informe</h3><p>Entrevista y diagnóstico con la startup: define el foco del reto.</p></div></div>
      <div class="glass"><img src="img/j-scene-02.jpg" alt=""><div class="body"><div class="n">Paso 2</div><h3>Pipelines</h3><p>De Excel o WhatsApp a una tabla viva y un flujo digital.</p><p class="tool">n8n · Baserow</p></div></div>
      <div class="glass"><img src="img/j-scene-03.jpg" alt=""><div class="body"><div class="n">Paso 3</div><h3>Dataset</h3><p>Dataset gobernado, sin datos personales, listo para construir.</p><p class="tool">Tarjeta de datos · CSV / API</p></div></div>
      <div class="glass"><img src="img/j-scene-04.jpg" alt=""><div class="body"><div class="n">Paso 4</div><h3>Datathon</h3><p>La Universidad construye; la startup es dueña del reto.</p><p class="tool">Prototipo + demo</p></div></div>
      <div class="glass"><img src="img/live-datalab.jpg" alt="" style="object-position:50% 72%"><div class="body"><div class="n">Paso 5</div><h3>Tablero</h3><p>Decisiones en pantalla con KPIs acordados, no un PDF.</p><p class="tool">Metabase</p></div></div>
    </div>
    <div class="rule">
      <div class="glass"><p><strong class="cyan">Regla:</strong> el tablero se alimenta con datos reales. Si falla un paso, no se inventa: se usa un CSV gobernado o se aplaza.</p></div>
      <div class="glass"><p><strong class="green">Ritmo propuesto:</strong> unas semanas de preparación con la startup, luego la Datathon y un puente opcional al Data Lab.</p>
        {P("Duración exacta (borrador: 3 semanas PRE + 2 días) y KPIs del tablero por acordar")}</div>
    </div>
  </div>
{FOOT}
</section>
'''

# 08 Datalab en vivo --------------------------------------------------------
S["08-datalab-vivo"] = f'''<style>
.s-08 .wrap{{display:grid;grid-template-columns:1.25fr 1fr;gap:36px;flex:1;min-height:0}}
.s-08 .envs{{display:flex;flex-direction:column;gap:12px}}
.s-08 .env{{padding:14px 20px;display:grid;grid-template-columns:52px 1fr;gap:14px;align-items:start}}
.s-08 .env .i{{width:46px;height:46px;border-radius:50%;background:var(--cyan);color:var(--deep);font-weight:700;font-size:26px;display:flex;align-items:center;justify-content:center}}
.s-08 .env h3{{font-size:28px;color:#fff;margin:0 0 2px}}
.s-08 .env p{{font-size:22px;line-height:1.32;margin:0}}
.s-08 .env .pill{{font-size:18px;margin:4px 0 0}}
</style>
<section class="slide slide-deep s-08">
  <span class="block-badge">4 · Datalab en vivo</span>
  <h2 class="slide-title">El Data Lab ya funciona: cinco entornos</h2>
  <div class="slide-main wrap">
    <div><img class="shot" src="img/live-datalab.jpg" alt="Datalab: decidimos qué construir">
      <p class="cap">datalab.cleantechhub.net · vista pública, captura del 8 oct 2026</p></div>
    <div class="envs">
      <div class="glass env"><div class="i">1</div><div><h3>Datalab · vitrina</h3><p>Estrategia: solo contenido público o consentido. Decide qué construir.</p><span class="pill g">Público</span></div></div>
      <div class="glass env"><div class="i">2</div><div><h3>Datathon</h3><p>Efímero, por evento: entra una foto de datos, sale una foto.</p><span class="pill">Abierto a participantes · 4–6 semanas</span></div></div>
      <div class="glass env"><div class="i">3</div><div><h3>Living lab</h3><p>Persistente (datos, lógica, acceso); nunca es sistema de registro.</p><span class="pill w">Cerrado · 3 actores · 90–180 días</span></div></div>
      <div class="glass env"><div class="i">4</div><div><h3>Producto cliente</h3><p>Copia de solo lectura de las salidas validadas del Living lab.</p><span class="pill w">Cerrado · 3 actores</span></div></div>
      <div class="glass env"><div class="i">5</div><div><h3>Taller General</h3><p>Selector de talleres y co-diseño.</p><span class="pill w">Cerrado · 3 actores</span></div></div>
    </div>
  </div>
{FOOT}
</section>
'''

# 09 Vitrina ----------------------------------------------------------------
S["09-vitrina"] = f'''<style>
.s-09 .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:30px;flex:1;min-height:0}}
.s-09 .col h3{{font-size:32px;margin-bottom:6px}}
.s-09 .col p.t{{font-size:25px;line-height:1.36;margin-bottom:14px;min-height:68px}}
.s-09 .col img.shot{{height:500px;object-fit:cover;object-position:top}}
.s-09 .gov{{margin-top:18px;padding:16px 24px}}
.s-09 .gov p{{font-size:24px;line-height:1.38;margin:0}}
</style>
<section class="slide slide-deep s-09">
  <span class="block-badge">4 · Datalab en vivo · vitrina</span>
  <h2 class="slide-title">Vitrina: brechas y soluciones</h2>
  <div class="slide-main" style="flex:1;display:flex;flex-direction:column;min-height:0">
    <div class="wrap">
      <div class="col"><h3><span class="accent-num">71</span> corporativos colombianos</h3>
        <p class="t">Cada uno aparece por lo que publica en su reporte de sostenibilidad, con página citada y código CIIU para cruzar sectores.</p>
        <img class="shot" src="img/live-corporativos.jpg" alt="Vitrina: corporativos y startups"></div>
      <div class="col"><h3>Match: brecha ↔ dataset limpio</h3>
        <p class="t">Ejemplo en vivo: la brecha de calidad del aire de un corporativo se cruza con los datasets de Air4U. Es una propuesta por validar.</p>
        <img class="shot" src="img/live-vitrina.jpg" alt="Match Diaco ↔ soluciones"></div>
    </div>
    <div class="glass gov"><p><strong class="cyan">Gobernanza:</strong> CTH Foundation es custodio-intermediario: muestra, no se adueña. Lo que el reporte no trae queda vacío («Pendiente de dato real»), sin suposiciones. Diseñado para alinearse con la Ley 1581 de 2012 y el Data Governance Act de la UE (no es una certificación).</p></div>
  </div>
{FOOT}
</section>
'''

# 10 Acceso controlado + Air4U ----------------------------------------------
S["10-acceso"] = f'''<style>
.s-10 .wrap{{display:grid;grid-template-columns:1.6fr 1fr;gap:32px;flex:1;min-height:0}}
.s-10 .shots{{display:flex;flex-direction:column}}
.s-10 .shots img.big{{height:auto}}
.s-10 .trio img{{height:180px;object-fit:contain;background:#fff}}
.s-10 .trio .cap{{font-size:19px}}
.s-10 .trio{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:10px}}
.s-10 .shots .cap{{font-size:20px;margin-top:4px}}
.s-10 .side .glass{{padding:22px 26px;margin-bottom:18px}}
.s-10 .side h3{{font-size:32px;margin-bottom:8px}}
.s-10 .side p,.s-10 .side li{{font-size:25px;line-height:1.38;margin-bottom:6px}}
.s-10 .side ul{{padding-left:28px}}
</style>
<section class="slide slide-deep s-10">
  <span class="block-badge">4 · Datalab en vivo · acceso</span>
  <h2 class="slide-title">Datos que se comparten con reglas</h2>
  <div class="slide-main wrap">
    <div class="shots">
      <img class="shot big" src="img/live-datathon-login.jpg" alt="Datathon · abierto a participantes registrados">
      <p class="cap">Datathon · abierto a participantes registrados · 4–6 semanas</p>
      <div class="trio">
        <div><img class="shot" src="img/card-lab.jpg" alt="Living lab"><p class="cap">Living lab · cerrado · 3 actores · 90–180 días</p></div>
        <div><img class="shot" src="img/card-client.jpg" alt="Producto cliente"><p class="cap">Producto cliente · cerrado · 3 actores</p></div>
        <div><img class="shot" src="img/card-taller.jpg" alt="Taller General"><p class="cap">Taller General · cerrado · 3 actores</p></div>
      </div>
    </div>
    <div class="side">
      <div class="glass"><h3>Un token por rol</h3><p>Solo la vitrina es pública. Cada entorno se abre con un token según el rol; en la Datathon el token vence al cerrar el evento.</p></div>
      <div class="glass"><h3>Caso en curso: Air4U</h3>
        <p>Experimento del acta del taller del 6 oct:</p>
        <ul><li>3 sensores · 12 semanas</li><li>Línea base abierta RMCAB Móvil 7ma</li><li>Éxito = delta ≥ 2 µg/m³</li></ul>
        <p class="muted">Hoy a las 14:00: avance y Laboratorio Vivo con clientes potenciales de Air4U.</p>
        {P("Obra por confirmar; datos reales de Air4U pendientes (sesión técnica 9 oct)")}</div>
    </div>
  </div>
{FOOT}
</section>
'''

# 11 Hoja de ruta -----------------------------------------------------------
S["11-ruta"] = f'''<style>
.s-11 .slide-inner{{justify-content:flex-end}}
.s-11 .tl{{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;position:relative;margin-top:10px}}
.s-11 .tl::before{{content:'';position:absolute;left:0;right:0;top:26px;height:4px;background:linear-gradient(90deg,#9DC384,#B2EEFA)}}
.s-11 .m{{position:relative;padding-top:58px}}
.s-11 .m::before{{content:'';position:absolute;top:14px;left:20px;width:28px;height:28px;border-radius:50%;background:#B2EEFA;border:4px solid #0C498A}}
.s-11 .m.done::before{{background:#9DC384}}
.s-11 .glass{{padding:18px 18px;background:rgba(5,26,51,.6);min-height:250px}}
.s-11 .d{{font-size:28px;font-weight:700;color:var(--cyan);line-height:1.15;margin-bottom:8px}}
.s-11 .done .d{{color:var(--green)}}
.s-11 p{{font-size:26px;line-height:1.35;margin-bottom:6px}}
</style>
<section class="slide has-photo s-11" style="--bg: url('img/p-ruta.jpg')">
  <div class="slide-inner">
    <span class="block-badge">Hoja de ruta</span>
    <h2>De hoy a la Climate Data Week</h2>
    <div class="tl">
      <div class="m done"><div class="glass"><div class="d">1 oct 2026</div><p>GEN Global Startup Huddle, con el CEE como anfitrión; CTH invitado como mentor corporativo.</p></div></div>
      <div class="m done"><div class="glass"><div class="d">6 oct 2026</div><p>Taller Air4U en el Datalab: experimento de calidad del aire definido.</p></div></div>
      <div class="m"><div class="glass"><div class="d">14 oct · 10:00</div><p>Esta reunión: actores, alianza, Datathon y Otrosí.</p><p class="muted">14:00: Laboratorio Vivo Air4U.</p></div></div>
      <div class="m"><div class="glass"><div class="d">nov 2026</div><p>Datathon en la Semana Global del Emprendimiento.</p>{P("Día exacto (¿18 nov?)")}</div></div>
      <div class="m"><div class="glass"><div class="d">1T 2027</div><p>Climate Data Week Bogotá.</p>{P("Fecha y sede")}</div></div>
    </div>
  </div>
{FOOT}
</section>
'''

# 12 Ask / próximos pasos ---------------------------------------------------
S["12-proximos-pasos"] = f'''<style>
.s-12 .wrap{{display:grid;grid-template-columns:1.5fr 1fr;gap:36px;flex:1;min-height:0}}
.s-12 .ask-list li{{font-size:28px;padding:14px 0;line-height:1.35}}
.s-12 .ask-list li strong{{color:var(--cyan)}}
.s-12 .who{{display:block;font-size:21px;color:var(--green);font-weight:700;margin-top:4px}}
.s-12 .glass h3{{font-size:32px;margin-bottom:10px}}
.s-12 .glass p, .s-12 .glass li{{font-size:25px;line-height:1.38;margin-bottom:6px}}
.s-12 .glass ul{{padding-left:28px}}
.s-12 .glass + .glass{{margin-top:18px}}
</style>
<section class="slide slide-deep s-12">
  <span class="block-badge">5 · Próximos pasos</span>
  <h2 class="slide-title">Lo que proponemos acordar hoy</h2>
  <div class="slide-main wrap">
    <ol class="ask-list">
      <li><span class="ask-num">1</span><div><strong>Otrosí:</strong> validar el alcance (Datathon, Climate Data Week, Data Lab, Investigación + HUB REIN Colombia) e iniciar el trámite contractual interno.<span class="who">CEE + CTH · fecha objetivo por acordar</span></div></li>
      <li><span class="ask-num">2</span><div><strong>Datathon nov 2026:</strong> confirmar fecha, sede y cupo de estudiantes y emprendedores CEE.<span class="who">CEE + CTH</span></div></li>
      <li><span class="ask-num">3</span><div><strong>Aliados:</strong> con la Coordinación de Innovación, priorizar a quién convocar desde gobierno y Estado.<span class="who">Coordinación de Innovación + CEE</span></div></li>
      <li><span class="ask-num">4</span><div><strong>Observatorio · HUB REIN Colombia:</strong> validar nombre, anclaje y línea de investigación CEE.<span class="who">CEE</span></div></li>
      <li><span class="ask-num">5</span><div><strong>Tablero:</strong> acordar los KPIs del producto final de la Datathon.<span class="who">CTH propone · CEE valida</span></div></li>
    </ol>
    <div>
      <div class="glass"><h3>CTH aporta</h3><ul><li>Método y diseño del viaje de la Datathon</li><li>Datalab en vivo: vitrina, entornos y reglas de datos</li><li>Stack abierto: n8n · Baserow · Metabase</li></ul></div>
      <div class="glass"><h3>Siguiente reunión</h3><p>Revisión del texto del Otrosí y calendario de la Datathon.</p>{P("Fecha de la siguiente reunión; seguimiento MinCiencias / OTRI tras la reunión de Marlene del 7 oct")}</div>
      <div class="glass"><h3>Aliados potenciales</h3><p>Atenea · APC Colombia · Innpulsa · Davivienda · SENA</p><p class="muted">Por convocar; ninguno confirmado aún.</p>{P("Ningún aliado ha confirmado; MinCiencias / OTRI también por explorar")}</div>
    </div>
  </div>
{FOOT}
</section>
'''

# 13 Cierre -----------------------------------------------------------------
S["13-cierre"] = f'''<style>
.s-13 .slide-inner{{justify-content:center;align-items:flex-start}}
.s-13 .big{{font-size:110px;font-weight:700;line-height:1.05;margin:24px 0 18px}}
.s-13 .big span{{color:var(--cyan)}}
.s-13 .line{{font-size:38px;line-height:1.35;max-width:1500px;margin-bottom:34px}}
.s-13 .c{{font-size:30px}}
</style>
<section class="slide has-photo s-13" style="--bg: url('img/p-cierre.jpg')">
  <div class="slide-inner">
    <div class="logo-row">
      <img class="logo-cth" src="img/logo-cth-white.svg" alt="CleantechHUB">
      <span class="logo-shield"><img src="img/logo-cee-externado.png" alt="Centro de Emprendimiento Externadista – CEE"></span>
    </div>
    <p class="big">Inspira. <span>Actúa.</span> Transforma.</p>
    <p class="line">Una alianza Universidad–CleantechHUB que convierte datos en negocios climáticos, empezando por la Datathon de noviembre.</p>
    <p class="c"><strong>Gideon Blaauw</strong> · CleantechHUB · CTH Foundation</p>
    <p class="c muted">Gracias, Marlene y Diego Alejandro.</p>
  </div>
{FOOT}
</section>
'''

for k, v in S.items():
    (OUT / f"{k}.html").write_text(v, encoding="utf-8")
print("wrote", len(S), "slides")
