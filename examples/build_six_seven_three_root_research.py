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
    three_root_half_lantern_compression,
    three_root_petal_exchange,
    three_root_cross_petal_lantern,
    three_root_cross_cluster_lantern,
    three_root_tail_cluster_lantern,
    three_root_tail_fixedness_audit,
    three_root_alternate_half_lantern,
    three_root_last_separator_decomposition,
)


def build():
    destination = ROOT / '.preview' / 'six-seven-three-root-transport'
    destination.mkdir(parents=True, exist_ok=True)
    route = three_root_transport_consolidation()
    transport = three_root_half_transport()
    prefix_lantern = three_root_prefix_lantern()
    reduction = three_root_lantern_reduction()
    residual = three_root_residual_lantern()
    compression = three_root_half_lantern_compression()
    exchange = three_root_petal_exchange()
    cross_petal = three_root_cross_petal_lantern()
    cross_cluster = three_root_cross_cluster_lantern()
    tail_cluster = three_root_tail_cluster_lantern()
    fixedness = three_root_tail_fixedness_audit(tail_cluster)
    alternate = three_root_alternate_half_lantern()
    last_separators = three_root_last_separator_decomposition()
    report = dict(route=route, transport=transport, prefix_lantern=prefix_lantern,
                  reduction=reduction, residual=residual, compression=compression,
                  petal_exchange=exchange,
                  cross_petal_lantern=cross_petal,
                  cross_cluster_lantern=cross_cluster,
                  tail_cluster_lantern=tail_cluster,
                  tail_fixedness_audit=fixedness,
                  alternate_half_lantern=alternate,
                  last_separator_decomposition=last_separators,
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

    compression_cards = []
    for index, stage in enumerate(compression['stages']):
        compression_cards.append(f'<section class="stage"><h2>{index}. {escape(stage["title"])}</h2>'
                                 '<p>Exact disk move within this branch</p>'
                                 + factor_rows(stage['factors']) + '</section>')
    compression_attempts = ''.join(
        f'<li>{escape(attempt["target_id"])}: exact transported sphere support differs</li>'
        for attempt in compression['direct_cancellation_attempts'])
    compression_target = image_for(compression['positive_equation_target'])

    exchange_cards = []
    for index, stage in enumerate(exchange['stages']):
        sphere = stage['kind'] == 'sphere_rewrite'
        kind = ' sphere' if sphere else ''
        scope = ('Sphere + closed genus two; disk action changes' if sphere else
                 'Exact disk move' if index else 'The shorter signed branch above')
        exchange_cards.append(f'<section class="stage{kind}"><h2>{index}. {escape(stage["title"])}</h2>'
                              f'<p>{scope}</p>' + factor_rows(stage['factors']) + '</section>')

    def prepared_relation_cards(relation, left_title, right_title):
        return ''.join(f'<section class="stage sphere"><h2>{title}</h2>'
                       '<p>Checked local sphere/genus-two relation; not applied to the endpoint</p>'
                       + factor_rows(relation[side]) + '</section>'
                       for side, title in (('left', left_title), ('right', right_title)))

    next_lantern = prepared_relation_cards(exchange['prepared_cluster_lantern'],
        'The transported roots A, B, and Q23', 'The two boundary pair twists P15 and R46')
    next_two = prepared_relation_cards(exchange['prepared_two_lantern_consequence'],
        'The endpoint’s five petals and C13 square', 'A pair, a squared pair, and two distinct inverse pairs')

    cross_cards = []
    for index, stage in enumerate(cross_petal['stages']):
        sphere = stage['kind'] == 'sphere_rewrite'
        kind = ' sphere' if sphere else ''
        scope = ('Exact sphere action and +I lift; disk discrepancy retained' if sphere else
                 'Exact disk word cancellation; no expanded meridian action needed' if index else
                 'The positive petal-exchange endpoint above')
        cross_cards.append(f'<section class="stage{kind}"><h2>{index}. {escape(stage["title"])}</h2>'
                           f'<p>{scope}</p>' + factor_rows(stage['factors']) + '</section>')

    cluster_cards = []
    for index, stage in enumerate(cross_cluster['stages']):
        sphere = stage['kind'] == 'sphere_rewrite'
        kind = ' sphere' if sphere else ''
        scope = ('Sphere and closed genus two; disk discrepancy retained' if sphere else
                 'Exact disk move' if index else 'The cross-stage PC lantern endpoint')
        cluster_cards.append(f'<section class="stage{kind}"><h2>{index}. {escape(stage["title"])}</h2>'
                             f'<p>{scope}</p>' + factor_rows(stage['factors']) + '</section>')

    tail_cards = []
    for index, stage in enumerate(tail_cluster['stages']):
        sphere = stage['kind'] == 'sphere_rewrite'
        kind = ' sphere' if sphere else ''
        scope = ('Sphere and closed genus two; disk discrepancy retained' if sphere else
                 'Exact disk move' if index else 'The positive mixed C4-cluster endpoint')
        tail_cards.append(f'<section class="stage{kind}"><h2>{index}. {escape(stage["title"])}</h2>'
                          f'<p>{scope}</p>' + factor_rows(stage['factors']) + '</section>')

    fixedness_pictures = ''.join(
        f'<figure><figcaption>{label}</figcaption>{image_for(factor)}</figure>'
        for label, factor in (('The remaining C12 support', fixedness['samples'][0]['c12']),
                              ('The inverse Q45 support', fixedness['samples'][0]['inverse'])))
    fixedness_rows = ''.join(
        f'<tr><td>{row["double_moves"]}</td><td>{len(row["certificate"]["chart_class"])}</td>'
        '<td>C12 changes this curve</td></tr>' for row in fixedness['samples'])

    alternate_cards = []
    for index, stage in enumerate(alternate['stages']):
        scope = ('The earlier positive fourteen-record C4-cluster checkpoint'
                 if not index else 'Exact disk move within this branch')
        alternate_cards.append(
            f'<section class="stage"><h2>{index}. {escape(stage["title"])}</h2>'
            f'<p>{scope}</p>' + factor_rows(stage['factors']) + '</section>')

    last_cards = []
    for index, stage in enumerate(last_separators['stages']):
        sphere = stage['kind'] == 'sphere_rewrite'
        kind = ' sphere' if sphere else ''
        scope = ('Sphere and closed genus two; disk discrepancy retained' if sphere else
                 'Exact disk move' if index else 'The positive (26,2) endpoint above')
        last_cards.append(f'<section class="stage{kind}"><h2>{index}. {escape(stage["title"])}</h2>'
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
table{border-collapse:collapse;background:white}th,td{padding:10px 14px;text-align:left;border:1px solid #cbd5df}
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
<div class="board">RESIDUAL_CARDS</div>
<h2>An optional shorter branch: reverse the duplicated PC half lanterns</h2>
<p>Bring the earlier P15 unit down beside the five-term C13 suffix. Together,
those six factors equal C13² P15⁻¹ exactly in the disk. This compresses the
display to fourteen records and four squared triple twists, but retains an
inverse pair twist. The red row is essential.</p>
<p class="notice"><strong>This is not a positive (12,4) factorization.</strong>
There are fourteen positive nonseparating units, two negative nonseparating
units, and four positive separating twists upstairs. The five direct
cancellation transports below fail on exact sphere support classes. Other
Hurwitz routes or substitutions remain possible.</p>
<p>Equivalently, the thirteen positive records above the red row multiply to
this positive P15 twist on the sphere and in closed genus two:</p>
<div class="local"><figure><figcaption>The positive target P15</figcaption>COMPRESSION_TARGET</figure></div>
<p>This is not a factorization confined to a disk bounded by P15: F3 moves
that boundary's exact sphere class and hence crosses it.</p>
<ul>COMPRESSION_ATTEMPTS</ul><div class="board">COMPRESSION_CARDS</div>
<h2>Continue by moving C5, then using its complementary PC rose</h2>
<p>The inverse need not be discarded. Slide C5 down unchanged until it is
just before C13; there it preserves P15’s exact sphere class. Draw the whole
C5 square along the complementary {1,3,5} triple, then expand each unit by
a cyclically ordered PC rose ending in the P15 petal. That last petal is
equal to the inverse pair’s positive unit in the disk. Move it past C13
and cancel.</p>
<p class="notice">This returns to a positive (24,3) factorization, now with
seventeen records and four half-twist records. C5 has been expanded and the
C13 separating twist restored. Changing a single C5 root’s hemisphere has
lift −I; changing the whole square is the checked +I step shown in purple.
The complete structural (6,7) derivation remains open.</p>
<div class="board">EXCHANGE_CARDS</div>
<h2>A new local lantern to use next</h2>
<p>Write A for the complementary C5 root and B for the C13 root. In A’s
three-point chart, B is A applied to the standard T124 curve; plain T124
would give the wrong curve. The checked sphere relation is ABQ23=P15R46.</p>
<div class="board">NEXT_LANTERN</div>
<p>Two ordered uses of that lantern give the next local relation below.
The second inverse pair is B⁻¹Q23⁻¹B. Its curve differs from Q23, so the
two inverse factors cannot be combined into Q23⁻². This consequence is
checked on all five exact sphere arcs and has lift +I; its disk discrepancy
has exponent sum 20. It is prepared, not yet applied to the full endpoint.</p>
<div class="board">NEXT_TWO</div>
<h2>A cross-stage inverse PC lantern</h2>
<p>Three pair twists from different parts of the product can be gathered:
the prefix P45, the residual P34, and the first C5 P35 petal. Bring P34 up
by moving each intervening neighbor down across it. Then bring P35 up
unchanged. Simply dragging P34 upward would leave the wrong curve.</p>
<p>Their three exact sphere support classes match a common-chart PC rose
around {3,4,5}; the complete replacement also fixes all five sphere arcs
and has genus-two lift +I. The local Hurwitz steps have freely cancelling
before/after braid words, avoiding the based-action expansion limit.</p>
<p class="notice">This branch has fifteen positive records but one ordinary
three-point twist. It is a mixed mapping-class factorization, not a new
positive Lefschetz factorization or a complete (6,7) derivation. The
ordinary root still needs to be accounted for. Pictures show individual
supports, not cumulative joint cut-complex certificates.</p>
<div class="board">CROSS_CARDS</div>
<h2>A transported {35},4,6 cluster lantern cancels another inverse</h2>
<p>Move F3 down across C4 first. In the checked common chart, the new root
is A=T123 and the transported C4 root is B=T124. Split C4's square and
apply the exact disk lantern AB=O P35 Q46⁻¹. Bring the nearby positive
Q46 upward unchanged and cancel it against the inverse in the disk.</p>
<p>The four-point O3456 curve can then be drawn along its complementary
P12 on the sphere, with lift +I and disk exponent discrepancy ten.
Bring the later P35 petal up and combine it with the first P35 in the disk.</p>
<p class="notice">Fourteen positive records remain, with two squared
triple twists and one ordinary triple twist. This is still a mixed
factorization, not a positive LF type or the full (6,7) derivation.
Individual support drawings do not certify cumulative cut complexes.</p>
<div class="board">CLUSTER_CARDS</div>
<h2>A C13 cluster branch with an unresolved inverse</h2>
<p>The first short common-chart tests at C12 fail. Bring C13 up unchanged
instead: its complementary root fits the {36},5,4 cluster lantern.
Rechart the whole square before splitting. Recharting just one ordinary
root would change the genus-two lift by the deck involution.</p>
<p>The exact disk lantern introduces Q45 inverse. Its outer curve matches
the prefix P12 on the sphere; after the sphere rechart, the two P12 twists
combine exactly in the disk. Eight direct transported inverse cancellations
fail on exact sphere classes.</p>
<p class="notice">This is a signed research branch with fifteen records.
The red inverse Q45 is essential: omitting it changes the genus-two action.
It is not a positive LF relation or a complete (6,7) derivation. The
earlier positive checkpoint remains available above.</p>
<div class="board">TAIL_CARDS</div>
<h2>Checking the C12 obstruction without expanding its large image curve</h2>
<div class="local">FIXEDNESS_PICTURES</div>
<p>Two adjacent Hurwitz moves between the inverse and its neighboring C13
root change their supports. At each of the four positions below, C12
still changes the inverse’s curve class. It therefore cannot be used as
a petal of a PC rose for C12 in that position.</p>
<table><thead><tr><th>Two-move repetitions</th><th>Word length in C12’s chart</th>
<th>Exact result</th></tr></thead><tbody>FIXEDNESS_ROWS</tbody></table>
<p>The new check moves the curve into C12’s standard chart and checks its
free-product normal form. At repetition two, direct image expansion hits
the existing word bound; the chart has only 4,846 letters and gives an
exact obstruction. The full certificate is in the linked JSON.</p>
<p class="notice">These are failed local configurations, not new derivation
steps. The full (6,7) structural derivation remains open. Individual support
pictures are not cumulative joint cut-complex certificates.</p>
<h2>Return to the positive C4 checkpoint: an alternative PC half lantern</h2>
<p>This is a separate branch from the earlier fourteen-record positive C4-cluster
checkpoint, not a continuation of the signed C13 branch. Gather the three
remaining {1,3,5} petals beside the squared P35 term. Their ordered disk product
compresses to C5² P15⁻¹. The red inverse is retained explicitly.</p>
<p>Expand C5² with the rotated PC half lantern whose squared pair term is P15².
Its final pair cancels one inverse unit exactly in the disk. Expand the last
ordinary C4 root by a PC rose. This gives four new {1,3} half twists and removes
all remaining ordinary roots and inverse factors.</p>
<p class="notice">The endpoint is a positive genus-two (26,2) intermediate:
eight half-twist records, nine full pair-twist units, and two squared triple
twists. Every new move is exact in the disk relative to this branch's checkpoint.
That checkpoint already used sphere relations, so these are not disk-equivalent
snapshots of the original product. The complete structural (6,7) derivation
remains open; a final standard boundary identity has not been identified.</p>
<p>The common-chart certificates check the faithful disk action of each local
relation without expanding its long surrounding conjugator. The endpoint also
has an exact five-arc sphere-action certificate and a separate +I genus-two
homology check. These drawings show individual supports, not cumulative joint
cut-complex certificates.</p>
<div class="board" id="alternate-half-lantern">ALTERNATE_CARDS</div>
<h2>The last two separators: a short chart and one remaining inverse</h2>
<p>Both roots preserve the round {1,2} and {3,4} curves. On the sphere the
first root A is the second root B transported by the inverse half twist
on {5,6}. Rechart the whole A square before applying the ordered consequence
of two lanterns: A² B² = P12² P34² Q56⁻¹ (B⁻¹ Q56⁻¹ B).</p>
<p>The second inverse must cross the first inverse, then P34², P12², and
F11. It then matches residual.P26 on the sphere. The purple curve replacement
retains its disk discrepancy; the subsequent cancellation is exact in B6.</p>
<p class="notice"><strong>This is not a positive (30,0) factorization.</strong>
All triple twists are gone, but one inverse Q56 remains. There are 32 positive
and two negative nonseparating units upstairs. The seventeen positive records
therefore multiply to the positive round P56 on the sphere and in closed genus
two. Omitting the red inverse would change the action. A final standard boundary
identity and the complete structural (6,7) derivation remain open.</p>
<p>The nine states below retain exact local disk moves, sphere-action and lift
checks, and all sphere-only discrepancies. These are individual support pictures,
not cumulative joint cut-complex certificates or equivalent disk-only workspaces.</p>
<div class="board" id="last-separators">LAST_CARDS</div></body></html>'''
    (destination / 'index.html').write_text(
        page.replace('LOCAL_ARCS', local).replace('FACTOR_CARDS', ''.join(cards))
            .replace('PREFIX_CARDS', ''.join(prefix_cards))
            .replace('REDUCTION_CARDS', ''.join(reduction_cards))
            .replace('RESIDUAL_CARDS', ''.join(residual_cards))
            .replace('COMPRESSION_CARDS', ''.join(compression_cards))
            .replace('COMPRESSION_TARGET', compression_target)
            .replace('COMPRESSION_ATTEMPTS', compression_attempts)
            .replace('EXCHANGE_CARDS', ''.join(exchange_cards))
            .replace('CROSS_CARDS', ''.join(cross_cards))
            .replace('CLUSTER_CARDS', ''.join(cluster_cards))
            .replace('TAIL_CARDS', ''.join(tail_cards))
            .replace('FIXEDNESS_PICTURES', fixedness_pictures).replace('FIXEDNESS_ROWS', fixedness_rows)
            .replace('ALTERNATE_CARDS', ''.join(alternate_cards))
            .replace('LAST_CARDS', ''.join(last_cards))
            .replace('NEXT_LANTERN', next_lantern).replace('NEXT_TWO', next_two), encoding='utf-8')
    (destination / 'picture-limitations.json').write_text(json.dumps(limitations), encoding='utf-8')
    print(f'{len(cards)} exact disk + {len(prefix_cards)} prefix + {len(reduction_cards)} reduction '
          f'+ {len(residual_cards)} residual + {len(compression_cards)} compression '
          f'+ {len(exchange_cards)} exchange + {len(cross_cards)} cross-petal '
          f'+ {len(cluster_cards)} cross-cluster + {len(tail_cards)} tail-cluster '
          f'+ {len(alternate_cards)} alternate-half-lantern '
          f'+ {len(last_cards)} last-separator states; '
          f'{len(pictures)} supports; {len(limitations)} picture limitations')
    print(destination / 'index.html')


if __name__ == '__main__':
    build()
