"""Build a local graphical checkpoint, explicitly not a completed derivation."""
import json
from dataclasses import asdict, is_dataclass
from html import escape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.six_seven_structure import (
    root_transport_consolidation, six_half_stabilizer_audit, sphere_root_half_transport,
)


def build():
    destination = ROOT / '.preview' / 'six-seven-root-transport'
    destination.mkdir(parents=True, exist_ok=True)
    route = root_transport_consolidation()
    report = dict(route=route, root_transport=sphere_root_half_transport(),
                  stabilizer_audit=six_half_stabilizer_audit())
    (destination / 'certificate.json').write_text(json.dumps(
        report, default=lambda value: asdict(value) if is_dataclass(value) else value,
        separators=(',', ':')), encoding='utf-8')
    pictures, failures = {}, []
    cards = []
    for index, stage in enumerate(route['stages']):
        rows = []
        for factor in stage['factors']:
            key = factor.mapping_class
            if key not in pictures:
                filename = f'support-{len(pictures)}.svg'
                try:
                    drawing = support_svg(factor, 6, mirror_vertical=True)
                    (destination / filename).write_text(drawing, encoding='utf-8')
                    pictures[key] = filename
                except ValueError as error:
                    pictures[key] = None
                    failures.append(dict(factor=factor.id, reason=str(error)))
            picture = pictures[key]
            image = (f'<a href="{picture}" target="_blank"><img src="{picture}" '
                     f'loading="lazy" alt="Support of {escape(factor.id)}"></a>'
                     if picture else '<span>Support picture unavailable</span>')
            label = ('H' if factor.half else f'T({factor.points})')
            if factor.power != 1:
                label += f'^{factor.power}'
            rows.append(f'<div class="factor" title="{escape(str(factor.conjugator))}">'
                        f'<b>{escape(factor.id)}</b>{image}<span>{label}</span></div>')
        scope = ('Sphere + closed genus two; disk action changes'
                 if stage['kind'] == 'sphere_rewrite' else
                 'Exact disk move' if index else 'Supplied starting product')
        kind = 'sphere' if stage['kind'] == 'sphere_rewrite' else 'disk'
        cards.append(f'<section id="stage-{index}" class="stage {kind}"><h2>{index}. '
                     f'{escape(stage["title"])}</h2><p>{scope}</p>' + ''.join(rows) + '</section>')
    links = ' · '.join(f'<a href="#stage-{index}">{index}</a>' for index in range(len(cards)))
    page = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>(6,7) root transport — incomplete research checkpoint</title>
<style>body{font:15px/1.45 system-ui;margin:24px;color:#20334b;background:#f1f5f8}
header{max-width:1000px}.notice{background:#fff0d0;padding:14px;border-left:4px solid #b97720}
.board{display:flex;gap:18px;overflow-x:auto;padding:12px 0 24px;align-items:stretch}
.stage{flex:0 0 340px;padding:12px;background:white;border:1px solid #b7ccd3;border-radius:10px}
.stage:target{outline:3px solid #327f9d}.stage.sphere{border:3px solid #7654ac}
h2{font-size:17px;min-height:50px}.factor{display:grid;grid-template-columns:110px 1fr 45px;
align-items:center;border-top:1px solid #e1e7eb;min-height:70px;font-size:11px;gap:5px}
.factor b{overflow-wrap:anywhere}.factor img{height:65px;max-width:100%}a{color:#175b7a}
</style><body><header><h1>(6,7): transporting and pairing two original half twists</h1>
<p class="notice"><strong>The complete structural derivation remains open.</strong>
This checkpoint splits two separating factors into roots, pairs original F3 and F9,
and ends with fourteen mixed factors. It does not reduce the complete product to a named identity.</p>
<p>Read each vertical column from top to bottom, then scroll right. Purple marks the one
sphere-only recharting step: its exact nontrivial disk discrepancy and +I genus-two
homology certificate are saved. Every other move preserves the full disk braid.</p>
<p>Points are numbered 1–6 from left to right. Pictures show individual supports in a disk chart, with the approved vertical display
convention. They are not a joint cut-complex certificate. Click a curve to enlarge it.</p>
<p><a href="certificate.json">Exact route and certificates</a></p><nav>STAGE_LINKS</nav>
</header><div class="board">CARDS</div></body></html>'''
    (destination / 'index.html').write_text(
        page.replace('STAGE_LINKS', links).replace('CARDS', ''.join(cards)), encoding='utf-8')
    (destination / 'picture-limitations.json').write_text(json.dumps(failures), encoding='utf-8')
    print(f'{len(cards)} checked states; {len(pictures)} distinct supports; {len(failures)} picture limitations')
    print(destination / 'index.html')


if __name__ == '__main__':
    build()
