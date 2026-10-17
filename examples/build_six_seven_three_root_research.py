"""Draw a disk-exact, incomplete F2/F7 consolidation with lab snapshots."""
import json
from dataclasses import asdict
from html import escape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.factorization_explorer import export_factors
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.six_seven_structure import (
    three_root_half_transport, three_root_transport_consolidation,
    f2_f7_cluster_lantern, three_root_prefix_lantern,
    three_root_lantern_reduction, three_root_residual_lantern,
)


def build():
    destination = ROOT / '.preview' / 'six-seven-three-root-transport'
    destination.mkdir(parents=True, exist_ok=True)
    route = three_root_transport_consolidation()
    transport = three_root_half_transport()
    prefix_lantern = three_root_prefix_lantern()
    reduction = three_root_lantern_reduction()
    residual = three_root_residual_lantern()
    report = dict(route=route, transport=transport, prefix_lantern=prefix_lantern,
                  reduction=reduction, residual=residual,
                  prepared_cluster_lantern=f2_f7_cluster_lantern())
    (destination / 'certificate.json').write_text(json.dumps(
        report, default=asdict, separators=(',', ':')), encoding='utf-8')
    pictures, limitations = {}, []

    def image_for(factor):
        # Equal disk supports should have identical pictures even when their
        # powers or conjugator presentations differ. Keep arc/loop styling
        # separate; this does not identify merely sphere-equivalent curves.
        key = (factor.half, supported_class(factor.mapping_class))
        if key not in pictures:
            filename = f'support-{len(pictures)}.svg'
            try:
                drawing = support_svg(factor, 6, mirror_vertical=True)
                (destination / filename).write_text(drawing, encoding='utf-8')
                pictures[key] = filename
            except ValueError as error:
                pictures[key] = None
                limitations.append(dict(id=factor.id, reason=str(error)))
        filename = pictures[key]
        return (f'<a href="{filename}" target="_blank"><img src="{filename}" '
                f'loading="lazy" alt="Support of {escape(factor.id)}"></a>'
                if filename else '<span>Support picture unavailable</span>')

    def factor_rows(factors):
        rows = []
        for factor in factors:
            sign = getattr(factor, 'sign', 1)
            label = 'H' if factor.half else f'T({factor.points})'
            exponent = sign * factor.power
            if exponent != 1:
                label += f'^{exponent}'
            inverse = ' inverse' if sign < 0 else ''
            rows.append(f'<div class="factor{inverse}"><b>{escape(factor.id)}</b>'
                        f'{image_for(factor)}<span>{label}</span></div>')
        return ''.join(rows)

    cards = []
    for index, stage in enumerate(route['stages']):
        filename = f'lab-stage-{index}.json'
        (destination / filename).write_text(json.dumps(export_factors(stage['factors']),
                                            separators=(',', ':')), encoding='utf-8')
        cards.append(f'<section class="stage"><h2>{index}. {escape(stage["title"])}</h2>'
                     f'<p>Exact in the disk · <a href="{filename}" download>Save for the (6,7) lab</a></p>'
                     + factor_rows(stage['factors']) + '</section>')

    prefix_cards = []
    for index, stage in enumerate(prefix_lantern['stages']):
        kind = ' sphere' if index else ''
        scope = ('Sphere + closed genus two; disk action changes' if index else
                 'The exact disk endpoint above')
        prefix_cards.append(f'<section class="stage{kind}"><h2>{escape(stage["title"])}</h2>'
                            f'<p>{scope}</p>' + factor_rows(stage['factors']) + '</section>')

    reduction_cards = []
    for index, stage in enumerate(reduction['stages']):
        sphere = stage['kind'] == 'sphere_rewrite'
        kind = ' sphere' if sphere else ''
        scope = ('Sphere + closed genus two; disk action changes' if sphere else
                 'Exact disk move' if index else 'After the prefix sphere lantern')
        reduction_cards.append(f'<section class="stage{kind}"><h2>{index}. {escape(stage["title"])}</h2>'
                               f'<p>{scope}</p>' + factor_rows(stage['factors']) + '</section>')

    residual_cards = []
    for index, stage in enumerate(residual['stages']):
        sphere = stage['kind'] == 'sphere_rewrite'
        kind = ' sphere' if sphere else ''
        scope = ('Sphere + closed genus two; disk action changes' if sphere else
                 'Exact disk move' if index else 'The positive mixed endpoint above')
        residual_cards.append(f'<section class="stage{kind}"><h2>{index}. {escape(stage["title"])}</h2>'
                              f'<p>{scope}</p>' + factor_rows(stage['factors']) + '</section>')

    local = ''.join(f'<figure><figcaption>{label}</figcaption>{image_for(factor)}</figure>'
                    for label, factor in (('Original F2', transport['source']),
                                          ('After applying C1', transport['intermediate']),
                                          ('After applying C8 C10: original F7', transport['target'])))
    page = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>(6,7): disk-exact F2/F7 transport — partial derivation</title>
<style>body{font:15px/1.45 system-ui;margin:24px;background:#f1f5f8;color:#20334b}
header{max-width:1100px}.notice{background:#fff0d0;border-left:4px solid #b97720;padding:14px}
.board,.local{display:flex;gap:18px;overflow-x:auto;align-items:stretch;padding:12px 0 24px}
.stage{flex:0 0 340px;padding:12px;background:white;border:1px solid #b7ccd3;border-radius:10px}
.stage.sphere{border:3px solid #7654ac}
.board .stage+.stage{position:relative;margin-left:14px}
.board .stage+.stage:before{content:'→';position:absolute;left:-30px;top:22px;font-size:24px;color:#596f87}
h2{font-size:17px;min-height:50px}.factor{display:grid;grid-template-columns:110px 1fr 45px;
align-items:center;border-top:1px solid #e1e7eb;min-height:70px;font-size:11px;gap:5px}
.factor b{overflow-wrap:anywhere}.factor img{height:65px;max-width:100%}a{color:#175b7a}
.factor.inverse{background:#fff0f2;color:#8c2040;border-left:3px solid #a82b4a}
figure{flex:0 0 300px;margin:0;background:white;padding:12px;border-radius:10px}
figure img{width:300px;max-width:100%}figcaption{font-weight:bold;margin-bottom:12px}
</style><body><header><h1>(6,7): pairing original F2 and F7 in the disk</h1>
<p class="notice"><strong>The full structural derivation is still open.</strong>
This route starts by pairing a second pair of the original half twists. Named
lantern moves then remove all ordinary three-point roots and temporary negative
factors, reaching a positive (24,3) intermediate. Identifying a final standard
boundary relation, and hence a complete structural derivation, remains open.</p>
<p>The exact disk identity is (C8 C10 C1) F2 (C8 C10 C1)⁻¹ = F7, where Cj is one
ordinary root of original Fj. The first eighteen states use only exact disk moves.</p>
<div class="local">LOCAL_ARCS</div>
<p>C1 starts before F2 in the supplied product. Move one C1 root down across F2 first;
then extract C8 and C10 from the later factors. Their inverse action turns F7 into
the same simple arc. The remaining Hurwitz moves bring the two equal halves together.</p>
<p>Read each column downward, then scroll right. Each saved JSON snapshot can be
opened with <strong>Open JSON</strong> in the existing (6,7) lab to inspect its braids
and cut complexes. These static pictures show individual supports only.</p>
<p>Points are numbered 1–6 from left to right. The approved vertical display convention is used.</p>
<p><a href="certificate.json">Exact route and scope certificates</a> ·
<a href="https://richardbuckman-math.github.io/surface-diagrams/lab/index.html">(6,7) lab</a></p>
</header><div class="board">FACTOR_CARDS</div>
<h2>A subsequent named sphere lantern</h2>
<p>The first three records now multiply to (C1 D)², where D is the simple arc shown
above. This is a common-chart image of the sphere genus-two lantern, so it can be
replaced by the two positive pair twists below. Purple marks the sphere-only step;
its exact nontrivial disk discrepancy and +I lift certificate are saved.</p>
<p class="notice">Four ordinary three-point roots remain later in the product.
This is still an incomplete mixed factorization, not a positive (8,6) Lefschetz
factorization. The final sphere state cannot be opened as an equivalent disk-only lab workspace.</p>
<div class="board">PREFIX_CARDS</div>
<h2>Continue through a cluster lantern and a PC half lantern</h2>
<p>A cluster lantern introduces one inverse pair twist (red). The peripheral omission
and complementary-root rechart are one paired sphere step; each separately has lift −I.
The remaining C13 square has a specific PC half-lantern pair term that matches the
negative pair exactly in the disk. Drag that squared pair up and cancel one unit.</p>
<p class="notice">The endpoint is positive again, but two odd three-point-root records
remain. This is further checked progress, not the complete (6,7) derivation or a new
Lefschetz factorization. These sphere research states are not disk-only lab workspaces.</p>
<p>The final sphere action is checked on all five exact adjacent-point arc classes,
with endpoints fixed, plus the separate +I genus-two lift check. This avoids a large
disk point-push word; it does not assert a joint drawing certificate for these pictures.</p>
<div class="board">REDUCTION_CARDS</div>
<h2>The last root pair: transport the lantern before cancelling</h2>
<p>Write A=C10 and B=C12. The saved endpoint has BAB⁻¹ and B³ in a common
chart S. Bring one B unit up past F11: the adjacent pair is BA, not AB.
Conjugate the checked relation ABP=R1R2 by B to obtain
BA=(BR1B⁻¹)(BR2B⁻¹)(BPB⁻¹)⁻¹, using the actual common chart SB.</p>
<p>The remaining two B units combine into a square. Move each intervening
neighbor down across the inverse pair, so that the inverse curve is transported
upward. It matches the prefix pair on the sphere. The purple rechart retains
its nontrivial disk discrepancy; the final cancellation itself is disk-exact.</p>
<p class="notice">The endpoint is a positive genus-two (24,3) factorization:
24 nonseparating and 3 separating Dehn twists when powers are expanded in the
double cover. All odd three-point roots and both temporary inverse factors
are gone. This count and the exact identity checks do not identify it with a
known boundary relation. The full requested structural derivation is still open.</p>
<div class="board">RESIDUAL_CARDS</div></body></html>'''
    (destination / 'index.html').write_text(
        page.replace('LOCAL_ARCS', local).replace('FACTOR_CARDS', ''.join(cards))
            .replace('PREFIX_CARDS', ''.join(prefix_cards))
            .replace('REDUCTION_CARDS', ''.join(reduction_cards))
            .replace('RESIDUAL_CARDS', ''.join(residual_cards)), encoding='utf-8')
    (destination / 'picture-limitations.json').write_text(json.dumps(limitations), encoding='utf-8')
    print(f'{len(cards)} exact disk + {len(prefix_cards)} prefix + {len(reduction_cards)} reduction '
          f'+ {len(residual_cards)} residual states; '
          f'{len(pictures)} supports; {len(limitations)} picture limitations')
    print(destination / 'index.html')


if __name__ == '__main__':
    build()
