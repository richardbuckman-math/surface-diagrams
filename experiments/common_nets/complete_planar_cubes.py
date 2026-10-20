"""Complete a partial planar cube catalog with a checked second spine net."""
import argparse
import json
from pathlib import Path
from . import cubes


def common_spine_net(surfaces, units, targets):
    """Find one family member for every requested target; verify all foldings."""
    if not targets:
        return None
    choices = None
    for i in targets:
        patterns = set(cubes.foot_patterns(surfaces[i], units, extension=True))
        patterns.update((p, -1) for p in cubes.foot_patterns(surfaces[i], units))
        choices = patterns if choices is None else choices & patterns
        if not choices:
            return None
    pattern = min(choices)
    net = cubes.make_net(units, *pattern)
    mappings = [cubes.fold_net(net, surface) for surface in surfaces]
    covered = [i for i, mapping in enumerate(mappings) if mapping is not None]
    for i in covered:
        cubes.verify_net(net, surfaces[i], mappings[i])
    assert set(targets) <= set(covered)
    net.update(mappings=mappings, coverage=covered, extended_column=pattern[1])
    return net


def run(source, destination):
    from reportlab.graphics import renderSVG
    from .figures import net_drawing, shape_drawing
    row = json.loads(source.read_text())['7']
    first = row['extended_family_best']
    planar = {i for i, shape in enumerate(row['shapes']) if cubes.is_planar(shape)}
    missing = sorted(planar - set(first['coverage']))
    net = common_spine_net(row['surfaces'], 7, missing)
    if net is None:
        raise ValueError('No supplement found in the checked spine family')
    union = set(first['coverage']) | set(net['coverage'])
    assert planar <= union
    destination.mkdir(parents=True, exist_ok=True)
    certificate = dict(net=net, missing_indices=missing, planar_total=len(planar),
                       first_coverage=len(first['coverage']), union_coverage=len(union),
                       scope='Planar seven-cube face-adjacency trees only; folded end states, not folding motions.')
    (destination / 'certificate.json').write_text(json.dumps(certificate))
    renderSVG.drawToFile(net_drawing(net, 1100, 240, 'square'), str(destination / 'net.svg'))
    cards = []
    for i in missing:
        filename = 'shape-%03d.svg' % (i + 1)
        renderSVG.drawToFile(shape_drawing(row['surfaces'][i], net['mappings'][i], 300, 220), str(destination / filename))
        cards.append('<figure><img src="%s"><figcaption>Catalog shape %d</figcaption></figure>' % (filename, i + 1))
    html = '''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Seven-cube supplement</title><style>body{font:18px/1.5 system-ui;max-width:1150px;margin:24px auto;padding:18px;color:#17304b;background:#f7fafc}img{max-width:100%}.shapes{display:flex;flex-wrap:wrap}figure{margin:10px;flex:1;min-width:220px;text-align:center}a{color:#155e96}</style>
<h1>A second net completes the planar seven-cube collection</h1>
<p>The earlier net covers 79 of 83 planar trees. This 30-square net covers 28, including the four missing shapes shown below. Together they cover all 83. This does not solve the general three-dimensional cube problem.</p>
<p>Blue dashed lines are hinges. Solid black edges and red internal edges are cuts. Colors match the target faces. Turning the paper over is allowed. Exact face/hinge checks certify the folded end states, not collision-free folding paths.</p>
<a href="net.svg" download><img src="net.svg" alt="Thirty-square supplemental net"></a>
<div class="shapes">''' + ''.join(cards) + '</div><p><a href="net.svg" download>Download SVG net</a> | <a href="certificate.json" download>Exact folding certificate</a></p>'
    (destination / 'index.html').write_text(html, encoding='utf-8')
    print(json.dumps({k: v for k, v in certificate.items() if k != 'net'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('.preview/common-nets/cubes.json'))
    parser.add_argument('--destination', type=Path, default=Path('.preview/common-nets/seven-cube-supplement'))
    args = parser.parse_args()
    run(args.source, args.destination)
