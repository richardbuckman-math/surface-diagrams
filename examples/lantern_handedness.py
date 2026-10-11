"""A three-point puncture-capped lantern and handedness calibration.

Run ``python examples/lantern_handedness.py`` from an installed checkout. The
output is deliberately small: the boundary-to-1-to-2-to-3 chain after each
marked-point lantern factor. The display is vertically mirrored to use
Richard's requested orientation; the exact braid words are unchanged.
"""

from argparse import ArgumentParser
from html import escape
from pathlib import Path

from surface_diagrams import Arc, PlanarSurface, Style, render_svg
from surface_diagrams.based_cut_system import based_arc_from_meridian
from surface_diagrams.boundary_playground import new_project
from surface_diagrams.boundary_playground_geometry import _arc_from_class
from surface_diagrams.braid_actions import artin_action, inverse_word, reduce_word
from surface_diagrams.visuals import ColoredCurve, PlanarDiagram


ROOT = Path(__file__).resolve().parents[1]
SURFACE = PlanarSurface.row('PPP', spacing=82, height=260, margin=80)
STYLE = Style(background='#ffffff', curve_width=2.4,
              marked_point_radius=5, curve_height=0.84)


def first_arc(word):
    """The exact based image of the left-boundary-to-point-1 chain edge."""
    meridian = artin_action(3, word)[0]
    arc = based_arc_from_meridian(meridian, points=3)
    if not arc.cuts and (arc.start, arc.end) == (0, 1):
        return Arc(0, 1)
    return arc


def _puncture(image):
    """Read a positively oriented puncture from a based meridian image."""
    image = reduce_word(image)
    start, end = 0, len(image)
    while end - start > 1 and image[start] == -image[end - 1]:
        start += 1
        end -= 1
    if end - start != 1 or not 1 <= image[start] <= 3:
        raise ValueError('Expected a positive three-point puncture meridian')
    return image[start]


def chain_arcs(word):
    """Three exact images: based first edge, then two unframed adjacent edges."""
    images = artin_action(3, word)
    endpoints = tuple(_puncture(image) for image in images)
    if set(endpoints) != {1, 2, 3}:
        raise ValueError('The image must permute all three punctures')
    arcs = [based_arc_from_meridian(images[0], points=3)]
    for index in (0, 1):
        boundary = reduce_word(images[index] + images[index + 1])
        arcs.append(_arc_from_class(boundary, endpoints[index],
                                    endpoints[index + 1], 3))
    # The identity reference edges lie exactly on the horizontal chain.
    return tuple(Arc(arc.start, arc.end) if not arc.cuts and
                 abs(arc.start - arc.end) == 1 else arc for arc in arcs)


def _labeled_svg(arcs, title):
    colors = ('#c02648', '#0e7490', '#7c3aed')
    chain = tuple(ColoredCurve(f'e{index + 1}: {label}', arc, colors[index])
                  for index, (label, arc) in enumerate(zip(
                      ('boundary→1', '1→2', '2→3'), arcs)))
    diagram = PlanarDiagram(SURFACE, chain, show_legend=True)
    svg = render_svg(diagram, style=STYLE, title=title)
    # The shared surface library supplies the surface and routes all three arcs
    # together. Mirror ONLY those routed paths as a display transform; neither
    # the Arc itineraries nor the exact braid action are modified.
    drawing = diagram.drawing(STYLE)
    labels = []
    points = [item for item in drawing.ellipses if item.role == 'marked-point']
    if len(points) != 3:
        raise AssertionError('Expected exactly three marked points')
    axis_y = drawing.height / 2 - points[0].y
    svg = svg.replace('<path class="arc" ',
                      f'<path class="arc" transform="translate(0 {2 * axis_y:.3f}) scale(1 -1)" ')
    if svg.count('scale(1 -1)') != 3:
        raise AssertionError('Expected exactly three mirrored arc paths')
    for index, point in enumerate(points, start=1):
        x = drawing.width / 2 + point.x
        y = drawing.height / 2 - point.y
        labels.append(f'<rect x="{x - 9:.3f}" y="{y + 5:.3f}" width="18" '
                      'height="18" rx="3" fill="#ffffff" opacity="0.92"/>')
        labels.append(f'<text x="{x:.3f}" y="{y + 19:.3f}" '
                      'font-family="system-ui,sans-serif" font-size="13" '
                      'text-anchor="middle" fill="#111827">'
                      f'{index}</text>')
    return svg.replace('</svg>', '\n'.join(labels) + '\n</svg>')


def build_demo(output):
    """Write independent SVGs and a local HTML index; return arc records."""
    output = Path(output)
    project = new_project(3)
    split = project.split(0, 'lantern')
    positive = project.word
    lantern = split.word
    if artin_action(3, positive) != artin_action(3, lantern):
        raise AssertionError('The encoded marked-disk lantern equality failed')
    if artin_action(3, positive) == artin_action(3, inverse_word(positive)):
        raise AssertionError('Positive and inverse twists were not distinguished')

    cases = (
        ('lantern-f0', (), 'F0 · starting chain'),
        ('lantern-f1', split.factors[0].word, 'F1 · after T₁₂'),
        ('lantern-f2', split.factors[0].word + split.factors[1].word,
         'F2 · after T₁₂ T₁₃'),
        ('lantern-f3', lantern, 'F3 · after T₁₂ T₁₃ T₂₃'),
        ('lantern-direct', positive, 'Direct T₁₂₃ comparison'),
    )
    output.mkdir(parents=True, exist_ok=True)
    cards = []
    sequences = {}
    for slug, word, title in cases:
        arcs = chain_arcs(word)
        sequences[slug] = arcs
        svg = _labeled_svg(arcs, title)
        (output / f'{slug}.svg').write_text(svg, encoding='utf-8')
        word_text = ' '.join(f'σ{abs(letter)}{"⁻¹" if letter < 0 else ""}'
                             for letter in word) or 'empty word'
        descriptions = ''.join(
            f'<li><strong>e{index}</strong> {arc.start}→{arc.end}; '
            f'cuts <code>{escape(str(arc.cuts))}</code>; '
            f'{"straight" if arc.is_straight(3) else "first side " + ("above" if arc.initial_up else "below")} '
            '(before the display mirror)</li>'
            for index, arc in enumerate(arcs, 1))
        cards.append(f'<article><h2>{escape(title)}</h2>{svg}'
                     f'<p>Braid word: <code>{escape(word_text)}</code></p>'
                     f'<ul>{descriptions}</ul>'
                     '</article>')
    pairwise = ' · '.join(' '.join(f'σ{abs(letter)}{"⁻¹" if letter < 0 else ""}'
                                   for letter in factor.word)
                          for factor in split.factors)
    html = f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PC lantern relation: three-point cut-system check</title>
<style>
body {{font:16px/1.5 system-ui,sans-serif; max-width:1100px; margin:auto; padding:24px; color:#172033}}
h1 {{line-height:1.18}} .cards {{display:grid; grid-template-columns:repeat(auto-fit,minmax(310px,1fr)); gap:16px}}
article {{border:1px solid #cbd5e1; border-radius:12px; padding:16px; background:#fff}}
article svg {{display:block; width:100%; height:auto; margin:14px auto}}
h2 {{font-size:1.12rem}} code {{overflow-wrap:anywhere}} .note {{background:#eff6ff; padding:12px 16px; border-radius:9px}}
</style>
<main><h1>PC lantern relation</h1>
<p><strong>PC = puncture-capped.</strong> This is our short name for the
three-marked-point version of the lantern relation.</p>
<p>The colored cut system is the chain <strong>e1: boundary→1,
e2: 1→2, e3: 2→3</strong>. Each panel applies one more factor. The direct
T₁₂₃ panel provides a side-by-side target for the end of the lantern sequence.</p>
<p>This is the lantern relation after capping the three inner boundary circles
with once-marked disks. The three twists around those small circles disappear;
the outer boundary twist and three pairwise twists remain.</p>
<p><strong>Exact marked-disk equality:</strong> T₁₂₃ = T₁₂ T₁₃ T₂₃.
In the current braid encoding, <code>{escape(pairwise)}</code> has the same full Artin
action as <code>σ1 σ2 σ1 σ2 σ1 σ2</code>. This is the marked-point
version; it does not encode framed inner-boundary twists.</p>
<p class="note"><strong>Richard's display orientation:</strong> the arc pictures are
vertically mirrored from the earlier review, following Richard's requested
positive-twist picture. This changes only SVG coordinates. The exact positive
braid words, Artin actions, and Arc itineraries are unchanged. The display flip
is a convention check, not by itself a proof of the geometric sign.</p>
<div class="cards">{''.join(cards)}</div></main></html>'''
    (output / 'index.html').write_text(html, encoding='utf-8')
    return sequences


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '.preview' / 'lantern-handedness')
    args = parser.parse_args()
    build_demo(args.output)
    print(args.output / 'index.html')
