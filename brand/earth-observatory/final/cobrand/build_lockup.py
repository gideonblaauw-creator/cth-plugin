import re,base64,cairosvg
from PIL import Image
ext=open('/workspace/earth-observatory-logos/externado/logo-uec-negativo-oficial.svg').read()
inner=re.search(r'</style>(.*)</svg>',ext,re.S).group(1)
cth=base64.b64encode(open('../src/cleantechhub.png','rb').read()).decode()
# white CTH for reverse
im=Image.open('../src/cleantechhub.png').convert('RGBA'); a=im.split()[3]
w=Image.new('RGBA',im.size,(255,255,255,0)); w.putalpha(a); w.save('/tmp/cth-white.png')
cthw=base64.b64encode(open('/tmp/cth-white.png','rb').read()).decode()
V={'green':('#669348','#9DC384','#222222'),'blue':('#0C498A','#69B5FA','#222222'),'reverse':('#FFFFFF','#B2EEFA','#FFFFFF')}
def mark(c1,c2):
    return f'''<circle cx="48" cy="48" r="14" fill="{c1}"/><ellipse cx="48" cy="48" rx="42" ry="18" fill="none" stroke="{c2}" stroke-width="2.5" transform="rotate(-25 48 48)"/><ellipse cx="48" cy="48" rx="38" ry="16" fill="none" stroke="{c1}" stroke-width="2" transform="rotate(35 48 48)"/><circle cx="86" cy="38" r="5" fill="{c2}"/><circle cx="14" cy="58" r="5" fill="{c2}"/><circle cx="58" cy="82" r="4" fill="{c1}"/>'''
for k,(c1,c2,ec) in V.items():
    W,H=1400,200
    eg=inner.replace('class="st0"',f'fill="{ec}"')
    sep=c2 if k!='reverse' else '#B2EEFA'
    svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Universidad Externado de Colombia · CleantechHUB · Observatorio de la Tierra">
<g transform="translate(20,52) scale(1.12)">{eg}</g>
<rect x="368" y="40" width="2" height="120" fill="{sep}"/>
<image xlink:href="data:image/png;base64,{cthw if k=='reverse' else cth}" x="398" y="58" width="320" height="85" preserveAspectRatio="xMidYMid meet"/>
<rect x="746" y="40" width="2" height="120" fill="{sep}"/>
<g transform="translate(772,38) scale(1.3)">{mark(c1,c2)}</g>
<text x="912" y="112" font-family="Titillium Web" font-weight="700" font-size="40" fill="{c1}">Observatorio de la Tierra</text>
</svg>'''
    open(f'eo-cobrand-{k}.svg','w').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f'eo-cobrand-{k}-transparent.png',output_width=2800)
    if k!='reverse':
        cairosvg.svg2png(bytestring=svg.encode(),write_to=f'eo-cobrand-{k}-white.png',output_width=2800,background_color='white')
    else:
        cairosvg.svg2png(bytestring=svg.encode(),write_to=f'eo-cobrand-{k}-on-blue.png',output_width=2800,background_color='#0C498A')
