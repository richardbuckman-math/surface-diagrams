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
    root_pair_lantern, root_transport_consolidation, root_cluster_lantern_route,
    six_half_stabilizer_audit,
    sphere_root_half_transport,
)


def build():
    destination = ROOT / '.preview' / 'six-seven-root-transport'
    destination.mkdir(parents=True, exist_ok=True)
    route = root_transport_consolidation()
    signed_route = root_cluster_lantern_route()
    lantern = root_pair_lantern()
    report = dict(route=route, root_transport=sphere_root_half_transport(),
                  cluster_lantern=lantern, signed_lantern_route=signed_route,
                  stabilizer_audit=six_half_stabilizer_audit())
    (destination / 'certificate.json').write_text(json.dumps(
        report, default=lambda value: asdict(value) if is_dataclass(value) else value,
        separators=(',', ':')), encoding='utf-8')
    pictures, failures = {}, []
    def image_for(factor):
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
        filename = pictures[key]
        return (f'<a href="{filename}" target="_blank"><img src="{filename}" '
                f'loading="lazy" alt="Support of {escape(factor.id)}"></a>'
                if filename else '<span>Support picture unavailable</span>')

    def cards_for(result, prefix):
        cards = []
        for index, stage in enumerate(result['stages']):
            rows = []
            for factor in stage['factors']:
                image = image_for(factor)
                sign = getattr(factor, 'sign', 1)
                exponent = sign * factor.power
                label = ('H' if factor.half else f'T({factor.points})')
                if exponent != 1:
                    label += f'^{exponent}'
                inverse = ' inverse' if sign < 0 else ''
                rows.append(f'<div class="factor{inverse}" title="{escape(str(factor.conjugator))}">'
                            f'<b>{escape(factor.id)}</b>{image}<span>{label}</span></div>')
            scope = ('<strong>SPHERE MOVE</strong> · Sphere + closed genus two; disk action changes'
                     if stage['kind'] == 'sphere_rewrite' else
                     'Exact disk move' if index else 'Starting product for this route')
            kind = 'sphere' if stage['kind'] == 'sphere_rewrite' else 'disk'
            cards.append(f'<section id="{prefix}-{index}" class="stage {kind}"><h2>{index}. '
                         f'{escape(stage["title"])}</h2><p>{scope}</p>' + ''.join(rows) + '</section>')
        return cards

    cards = cards_for(route, 'stage')
    signed_cards = cards_for(signed_route, 'lantern')
    links = ' · '.join(f'<a href="#stage-{index}">{index}</a>' for index in range(len(cards)))
    local = []
    for side in ('left', 'right'):
        rows = ''.join(f'<div class="factor"><b>{escape(factor.id)}</b>'
                       f'{image_for(factor)}<span>T({factor.points})</span></div>'
                       for factor in lantern[side])
        local.append(f'<section class="stage"><h2>{"Left" if side == "left" else "Right"} product</h2>'
                     + rows + '</section>')
    relation = '<div class="local">' + '<strong>=</strong>'.join(local) + '</div>'
    relation += (f'<div class="local"><section class="stage"><h2>Original F3</h2>'
                 f'{image_for(lantern["source"])}</section><strong>R →</strong>'
                 f'<section class="stage"><h2>Original F9</h2>{image_for(lantern["target"])}</section></div>')
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
.factor.inverse{background:#fff0f2;color:#8c2040;border-left:3px solid #a82b4a}
.local{display:flex;align-items:center;gap:16px;overflow-x:auto;margin:14px 0}.local img{max-width:100%}
</style><body><header><h1>(6,7): transporting and pairing two original half twists</h1>
<p class="notice"><strong>The complete structural derivation remains open.</strong>
This checkpoint splits two separating factors into roots, pairs original F3 and F9,
and ends with fourteen mixed factors. It does not reduce the complete product to a named identity.</p>
<h2>A local PC lantern explains the transport</h2>
<p>Its inner clusters are {2,5}, {3,4}, and the capped point {6}. The products below
are exactly equal in the disk: C10 C13 Q2345 = O23456 P25 P34. If point 6 is restored
as a framed boundary, include its boundary twist on the right.</p>
<p>Consequently R = P25 P34 Q2345⁻¹ carries original F3 to original F9 by exact disk
conjugation. O23456 is trivial on the marked sphere but lifts to the hyperelliptic
involution (homology −I); it cannot simply be discarded in a genus-two equality.</p>
LOCAL_RELATION
<h2>Seventeen-state root-consolidation route</h2>
<p>Read each vertical column from top to bottom, then scroll right. Purple marks the one
sphere-only recharting step: its exact nontrivial disk discrepancy and +I genus-two
homology certificate are saved. Every other move preserves the full disk braid.</p>
<p>Points are numbered 1–6 from left to right. Pictures show individual supports in a disk chart, with the approved vertical display
convention. They are not a joint cut-complex certificate. Click a curve to enlarge it.</p>
<p><a href="certificate.json">Exact route and certificates</a></p><nav>STAGE_LINKS</nav>
</header><div class="board">CARDS</div>
<h2 id="signed-route">Continue: apply both transported cluster lanterns</h2>
<p class="notice">This is still an incomplete derivation. These eight additional states
replace both ordinary-root pairs by their own transported lanterns. Red rows are
inverse twists. This signed research route cannot be imported into the positive-only lab.</p>
<p>Both peripheral five-point twists are removed in one sphere step: each alone
lifts to −I, whereas the paired removal lifts to +I. The final two sphere steps
draw the inverse four-point twists along the equivalent complementary pair curves.</p>
<p>The apparent triangle of pairs {1,4}, {4,6}, {1,6} does not yet give another
PC lantern: the exact routed curves have algebraic intersections 1, 3, 3 upstairs,
rather than 1, 1, 1. Their endpoint sets are not enough.</p>
<div class="board">SIGNED_CARDS</div></body></html>'''
    (destination / 'index.html').write_text(
        page.replace('LOCAL_RELATION', relation).replace('STAGE_LINKS', links)
            .replace('SIGNED_CARDS', ''.join(signed_cards)).replace('CARDS', ''.join(cards)), encoding='utf-8')
    (destination / 'picture-limitations.json').write_text(json.dumps(failures), encoding='utf-8')
    print(f'{len(cards)} + {len(signed_cards)} checked states; {len(pictures)} distinct supports; {len(failures)} picture limitations')
    print(destination / 'index.html')


if __name__ == '__main__':
    build()
