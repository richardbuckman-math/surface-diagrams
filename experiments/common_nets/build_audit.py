"""Make a compact illustrated, offline verification packet; no PDF changes."""
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import shutil
import zipfile


def build():
    from reportlab.graphics import renderSVG
    from .figures import net_drawing, shape_drawing
    from .engine import fold_net
    root = Path(__file__).resolve().parents[2]
    inputs = root / '.preview/common-nets'
    source = inputs / 'tetrahedra.json'
    audit = json.loads((inputs / 'independent-audit.json').read_text())
    data = json.loads(source.read_text())
    assert audit['input_sha256'] == sha256(source.read_bytes()).hexdigest()
    assert audit['5']['matches_mabry_reference'] and audit['6']['global_upper_bound'] == 19
    assert audit['4']['common_count_discrepancy_resolved']
    output = inputs / 'audit'
    output.mkdir(exist_ok=True)
    assets = []

    def svg(drawing, filename):
        renderSVG.drawToFile(drawing, str(output / filename))
        assets.append(filename)
        return filename

    five = data['levels']['5']
    five_net = five['net']
    svg(net_drawing(five_net, 650, 330), 'five-net.svg')
    svg(net_drawing(data['levels']['6']['best_single_net'], 650, 330), 'six-net.svg')
    targets = []
    for i, surface in enumerate(five['surfaces']):
        name = svg(shape_drawing(surface, five_net['mappings'][i], 220, 180), 'five-target-%d.svg' % (i + 1))
        targets.append('<figure><img src="%s" alt="Five-unit target %d"><figcaption>Shape %d</figcaption></figure>' % (name, i + 1, i + 1))
    four = []
    for i, net in enumerate(audit['4']['common_nets']):
        # Recheck each common positive with the original independent face /
        # hinge verifier, and include all mappings for reproducible comparison.
        net['mappings'] = [fold_net(net, s) for s in data['levels']['4']['surfaces']]
        assert all(m is not None for m in net['mappings'])
        name = svg(net_drawing(net, 240, 170), 'four-candidate-%02d.svg' % (i + 1))
        four.append('<figure><img loading="lazy" src="%s" alt="Four-unit common net %d"><figcaption>Common net %d</figcaption></figure>' % (name, i + 1, i + 1))
    (output / 'audit-data.json').write_text(json.dumps(audit, separators=(',', ':')))
    shutil.copyfile(source, output / 'tetrahedra.json')
    shutil.copyfile(Path(__file__).parent / 'reference/mabry-four-comparison.json', output / 'catalog-comparison.json')
    note = root / 'docs/proofs/common-net-novelty.md'
    shutil.copyfile(note, output / 'research-note.md')
    body = '''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tetrahedron common-net audit</title><style>body{font:18px/1.55 system-ui;max-width:1120px;margin:24px auto;padding:18px;color:#17304b;background:#f7fafc}h1{line-height:1.2}.notice{padding:18px;background:#fff1d8;border-radius:10px}.net{width:100%;max-height:330px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}figure{margin:0;background:white;padding:10px;text-align:center;border-radius:7px}figure img{width:100%;height:180px;object-fit:contain}a{color:#155e96}details{margin:28px 0}table{border-collapse:collapse}td,th{padding:8px 16px;border:1px solid #ccd5dd}section{margin:40px 0}</style>
<h1>Tetrahedron common nets: what is known and what was rechecked</h1>
<div class="notice"><b>Five-unit construction: rediscovery.</b> It matches Rick Mabry's earlier net exactly. <b>Six-unit optimum: 19/23 in our fixed-cut model.</b> A second geometric implementation agrees. Publication priority is unconfirmed; no external review has been obtained.</div>
<p>One unit is a regular tetrahedron, joined along whole faces. Mirrors count once. Paper cuts are fixed, either side may face out, and panels hinge only along whole triangle edges. Results certify folded end states, not collision-free folding motions.</p>
<section><h2>Five units: the already known cobra net</h2><p>The complete check of 6,000 source trees finds exactly one common fixed-hinge net up to plane symmetry. Its paper pattern and hinges match <a href="https://lsusmath.rickmabry.org/rmabry/dodec/delta/common8V.html">Mabry's twelve-face page</a>. His other examples allow cuts to change between targets; those belong to a different model. No new construction is claimed here.</p>
<a href="five-net.svg" download><img class="net" src="five-net.svg" alt="Known five-unit net"></a><div class="grid">'''+''.join(targets)+'''</div></section>
<section><h2>Six units: independent geometry agrees with the 19 bound</h2><a href="six-net.svg" download><img class="net" src="six-net.svg" alt="Nineteen-target six-unit net"></a>
<p>The second implementation derives folding transitions from shared 3D vertex coordinates. It shares the input catalog and tree enumerator with the earlier program, so it is not an outside review. It exhausts four source inventories, totaling 104,201 trees, and confirms the positive 19-target witness.</p>
<table><tr><th>Source, zero-based</th><th>Trees</th><th>Planar unfoldings</th><th>Upper bound</th></tr>'''
    for row in audit['6']['source_results']:
        body += '<tr><td>{source}</td><td>{trees:,}</td><td>{planar:,}</td><td>{coverage_upper_bound}</td></tr>'.format(**row)
    body += '''</table><p>A net for 20 of 23 targets would have to cover one of these four sources, since only 19 targets lie outside them. Every net in each complete source catalog covers at most 19. This proves the global upper bound within this model.</p></section>
<section><h2>Four units: complete agreement with the published catalog</h2><p>The individual inventories agree: 203, 280, and 452. <a href="https://lsusmath.rickmabry.org/rmabry/dodec/delta/commonNets-fiveDeltahedra-catalog1.pdf">Mabry's complete catalog</a> also agrees with our intersection: 37 shared outlines, with 47 fixed-cut variants. The 16 pictured on his main page are a narrower selection: nets exclusive to the three cluster types, with one variant each.</p><p>The full breakdown is 16 exclusive outlines, 19 outlines that also fold into other deltahedra, and two outlines with six cut variants each. Thus 16+19+2=37 outlines and 16+19+12=47 fixed-cut nets. The two multi-variant outlines are IDs 005 and 405. The sixteen picture labels exactly match the exclusive filter. This resolves the comparison without a new four-unit claim.</p><p><a href="catalog-comparison.json" download>Download the checked catalog summary and source hash</a></p><details><summary>Inspect all 47 common nets, rechecked by both folding implementations</summary><div class="grid">'''+''.join(four)+'''</div></details></section>
<section><h2>Verification files</h2><p><a href="research-note.md">Detailed research note and references</a> | <a href="audit-data.json" download>Audit data and fold maps</a> | <a href="tetrahedra.json" download>Exact input catalog</a></p><p>Blue dashed lines are hinges; black boundaries and red internal lines are cuts. Download either large net by clicking it. The input SHA-256 is <code>'''+escape(audit['input_sha256'])+'''</code>.</p></section>'''
    body = body.replace('</style>', 'code{overflow-wrap:anywhere}table{display:block;max-width:100%;overflow-x:auto}</style>', 1)
    (output / 'index.html').write_text(body, encoding='utf-8')
    readme = ('Unzip and open index.html. Recheck the computation, using standard-library Python:\n'
              'python -m experiments.common_nets.audit --source tetrahedra.json --destination rechecked.json\n'
              'This takes roughly two minutes on the development machine. Source code is included.\n'
              'Known five-unit construction: Rick Mabry, common8V.html. Six-unit priority unconfirmed.\n')
    (output / 'README.txt').write_text(readme)
    archive = root / 'output/common-net-audit.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for name in assets + ['index.html', 'README.txt', 'research-note.md', 'audit-data.json', 'tetrahedra.json', 'catalog-comparison.json']:
            z.write(output / name, name)
        for name in ['__init__.py', 'audit.py', 'engine.py', 'verify_six.py', 'catalog_compare.py', 'reference/mabry-four-comparison.json']:
            z.write(Path(__file__).parent / name, 'experiments/common_nets/' + name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    print(json.dumps(dict(archive=str(archive), svg_count=len(assets))))


if __name__ == '__main__':
    build()
