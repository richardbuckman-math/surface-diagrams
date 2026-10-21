"""Precalculate a compact, explicitly recharted view of the saved research route.

The source route and prescribed global frames are versioned beside the page.
This groups an existing route; it does not supply the missing standard-block
extraction or claim fewer mathematical elementary moves. No browser algebra
runtime is required to open the pictures.
"""
import argparse
from dataclasses import asdict, replace
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from build_six_seven_derivation_pdf import PHASES, factor, reverse_route
from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.braid_stack import braid_fragment_svg, connected_braid_svg
from surface_diagrams.factorization_simplify import six_seven_simplification
from surface_diagrams.factorization_explorer import export_factors,Factor
from surface_diagrams.factorization_geometry import number_support_points
from surface_diagrams.hyperelliptic_homology import homology_action
from surface_diagrams.mapping_classes import ConjugatedTwist, supported_class
from surface_diagrams.sphere_actions import sphere_supported_class
from surface_diagrams.sphere_support_compact import (
    check_support_replacement, compact_sphere_support, reframe_factors)
from surface_diagrams.twist_supports import support_curve


def support_key(twist):
    return (twist.points, twist.power, twist.half,
            sphere_supported_class(twist), homology_action(twist.word))


def route_groups(steps):
    """Group consecutive disk Hurwitz runs; keep every sphere arrow separate."""
    result = []
    for i, step in enumerate(steps):
        kind = step['original']['kind']
        if (result and kind == 'disk_hurwitz' and
                result[-1]['kind'] == kind and result[-1]['phase'] == step['phase']):
            result[-1]['end'] = i + 1
        else:
            result.append(dict(start=i, end=i + 1, kind=kind, phase=step['phase']))
    return result


def build(candidate_cache=None):
    destination = ROOT / 'docs/proofs/six-seven-compact'
    source = (destination / 'source-route.json').read_bytes()
    report = json.loads(source)
    prescribed = json.loads((destination / 'frames.json').read_text())
    if prescribed['source_sha256'] != sha256(source).hexdigest():
        raise ValueError('Prescribed frames belong to a different source route')
    steps = reverse_route(report)
    states = [steps[0]['before']] + [s['after'] for s in steps]
    if len(prescribed['frames']) != len(states):
        raise ValueError('A prescribed global frame is required for every state')
    pool = {}
    # Cached candidates are hints only. Recheck each used replacement against
    # its actual framed source, never reuse a different source's discrepancy.
    cache_path = Path(candidate_cache) if candidate_cache else destination / 'support-certificates.json'
    if cache_path.exists():
        data = json.loads(cache_path.read_text(encoding='utf-8'))
        for record in data.get('results', data.get('replacements', [])):
            if record.get('candidate'):
                t = ConjugatedTwist(**record.get('original', record.get('source')))
                c = ConjugatedTwist(**record['candidate'])
                if len(support_curve(c).cuts) <= 40:
                    k = support_key(t)
                    old = pool.get(k)
                    if old is None or len(c.conjugator) < len(old.conjugator):
                        pool[k] = c
    replacement_cache, replacements = {}, []
    assets = dict(supports=[], braids=[])
    supports, braids, row_cache, rows, displays = {}, {}, {}, [], []
    max_raw_cuts = 0
    unavailable_raw = 0
    raw_sphere_max = 0
    raw_supports = set()

    def register_factor(compact, ci):
        checked = replacements[ci]
        c = compact.mapping_class
        row_key = (compact, ci)
        if row_key not in row_cache:
            sk = (c.half, supported_class(c))
            if sk not in supports:
                supports[sk] = len(assets['supports'])
                assets['supports'].append(support_svg(compact, 6, mirror_vertical=False))
            if compact.word not in braids:
                braids[compact.word] = len(assets['braids'])
                assets['braids'].append(braid_fragment_svg(compact.word)['svg'])
            row_cache[row_key] = len(rows)
            rows.append(dict(id=compact.id, support=supports[sk], braid=braids[compact.word],
                label=('H' if compact.half else 'T' + str(compact.points)) +
                    ('^' + str(compact.power * getattr(compact,'sign',1)) if compact.power * getattr(compact,'sign',1) != 1 else ''),
                inverse=getattr(compact,'sign',1) < 0, cuts=checked['cuts'],
                sphere_rechart=not checked['disk_equal'], certificate=ci,
                factor=asdict(compact), word=compact.word,
                height=braid_fragment_svg(compact.word)['height']))
        return row_cache[row_key]

    for state_index, (records, frame) in enumerate(zip(states, prescribed['frames'])):
        original = tuple(map(factor, records))
        framed = reframe_factors(original, frame)
        displayed = []
        for f in framed['factors']:
            t = f.mapping_class
            if (t not in replacement_cache or (state_index == len(states) - 1 and
                    ConjugatedTwist(**replacements[replacement_cache[t]]['candidate']).word != t.word)):
                if state_index == len(states) - 1:
                    candidate = t  # Finish at Richard's literal original 13.
                else:
                    candidate = pool.get(support_key(t))
                    if candidate is None:
                        result = compact_sphere_support(t, max_cuts=24)
                        if result['candidate'] is None:
                            result = compact_sphere_support(t, max_cuts=40)
                        if result['candidate'] is None:
                            raise ValueError('No certified chart support under the hard 40-cut cap: ' + f.id)
                        candidate = ConjugatedTwist(**result['candidate'])
                        pool[support_key(t)] = candidate
                checked = check_support_replacement(t, candidate, max_cuts=40)
                replacement_cache[t] = len(replacements)
                replacements.append(dict(source=asdict(t), **checked))
            ci = replacement_cache[t]
            checked = replacements[ci]
            c = ConjugatedTwist(**checked['candidate'])
            compact = replace(f, conjugator=c.conjugator, first=c.first)
            displayed.append(register_factor(compact, ci))
        for f in original:
            if f.mapping_class in raw_supports:
                continue
            raw_supports.add(f.mapping_class)
            raw_sphere_max = max(raw_sphere_max, len(sphere_supported_class(f.mapping_class)))
            try:
                max_raw_cuts = max(max_raw_cuts, len(support_curve(f.mapping_class).cuts))
            except ValueError:
                unavailable_raw += 1
        displays.append(dict(index=state_index, factors=displayed, frame=frame,
                             global_word_certificate=framed['word_certificate'],
                             max_cuts=max((rows[i]['cuts'] for i in displayed), default=0)))
        if state_index % 25 == 0:
            print('Precalculated state', state_index, '/', len(states) - 1, flush=True)
    atomic = [dict(start=i, end=i + 1, phase=s['phase'],
                   title='Undo: ' + s['original']['title'], kind=s['original']['kind'],
                   sphere=s['sphere'], reverse_disk_discrepancy=s['reverse_disk_discrepancy'])
              for i, s in enumerate(steps)]
    chapters = []
    for i, step in enumerate(steps):
        if not chapters or chapters[-1]['phase'] != step['phase']:
            chapters.append(dict(start=i, end=i + 1, phase=step['phase']))
        else:
            chapters[-1]['end'] = i + 1
    titles = {key: (title, explanation) for key, title, explanation in PHASES}
    for c in chapters:
        c['title'], c['explanation'] = titles[c['phase']]
        c['sphere_steps'] = [i + 1 for i in range(c['start'], c['end']) if steps[i]['sphere']]
    groups = route_groups(steps)
    for g in groups:
        g['title'] = ('Reverse ' + str(g['end'] - g['start']) + ' adjacent Hurwitz moves'
                      if g['kind'] == 'disk_hurwitz' else atomic[g['start']]['title'])
        g['sphere_steps'] = [i + 1 for i in range(g['start'], g['end']) if steps[i]['sphere']]
    forward_atomic = [dict(start=i, end=i+1, phase=s['phase'],
                           title=s['original']['title'], kind=s['original']['kind'],
                           sphere=s['sphere'], reverse_disk_discrepancy=s['original'].get('disk_discrepancy', []))
                      for i,s in enumerate(reversed(steps))]
    phase_names = dict(route='Simplify the original thirteen factors',
        prefix_lantern='Apply the prefix sphere lantern', reduction='Reduce the first cluster',
        residual='Apply the residual lantern', compression='Use the two PC half lanterns',
        petal_exchange='Exchange complementary petals', cross_petal_lantern='Use the transported PC lantern',
        cross_cluster_lantern='Use the common-chart cluster lantern',
        alternate_half_lantern='Use the alternate half lantern',
        last_separator_decomposition='Decompose the final separating twists',
        positive_sphere_expansion='Replace the inverse pair by positive sphere factors')
    forward = dict(atomic=forward_atomic)
    for name, blocks in [('chapters',chapters),('groups',groups)]:
        forward[name] = []
        for block in reversed(blocks):
            a,b = len(steps)-block['end'],len(steps)-block['start']
            forward[name].append(dict(start=a,end=b,phase=block['phase'],
                title=phase_names[block['phase']] if name=='chapters' else
                    (str(b-a)+' adjacent Hurwitz moves' if block['kind']=='disk_hurwitz' else forward_atomic[a]['title']),
                sphere_steps=[i+1 for i in range(a,b) if forward_atomic[i]['sphere']]))
    simple_report = six_seven_simplification()
    simple_states, simple_moves, identity_supports = [], [], {}
    for i,stage in enumerate(simple_report['stages']):
        ids=[]
        for f in stage['factors']:
            t=f.mapping_class
            if t not in identity_supports:
                identity_supports[t]=len(replacements)
                replacements.append(dict(source=asdict(t),**check_support_replacement(t,t,max_cuts=40)))
            ids.append(register_factor(f,identity_supports[t]))
        simple_states.append(dict(index=i,factors=ids,frame=stage['frame'],
                                  max_cuts=max(rows[k]['cuts'] for k in ids),score=stage['score']))
        if i:
            simple_moves.append(dict(start=i-1,end=i,title=stage['title'],kind=stage['kind'],
                                     phase='simplification',sphere=False,sphere_steps=[],
                                     reverse_disk_discrepancy=[]))
    simplification=dict(states=simple_states,chapters=simple_moves,groups=simple_moves,
                        atomic=simple_moves,summary=dict(initial=simple_states[0]['score'],
                        final=simple_states[-1]['score'],sphere_moves=0,
                        hurwitz_moves=sum(s['kind']=='disk_hurwitz' for s in simple_report['stages']),
                        global_conjugations=sum(s['kind']=='global_conjugation' for s in simple_report['stages'])))
    (destination/'simplification-certificate.json').write_text(
        json.dumps(simple_report,default=asdict,separators=(',',':')),encoding='utf-8')
    session=export_factors(simple_report['stages'][-1]['factors'])
    session['global_conjugator']=simple_report['frame']
    (destination/'simplified-six-seven.json').write_text(json.dumps(session,separators=(',',':')),encoding='utf-8')
    summary = dict(atomic_moves=len(steps), chapters=len(chapters), grouped_moves=len(groups),
                   source_sphere_moves=sum(s['sphere'] for s in steps), hard_cut_cap=40,
                   max_displayed_cuts=max(r['cuts'] for r in rows),
                   factors_above_24=sum(r['cuts'] > 24 for r in rows),
                   old_max_available_cuts=max_raw_cuts, old_unavailable_supports=unavailable_raw,
                   old_max_sphere_class_length=raw_sphere_max,
                   source_sha256=sha256(source).hexdigest(),
                   complete_structural_derivation_found=False,
                   standard_block_bridge='UNCOMPUTED',support_mirror_vertical=False,
                   braids_continuous=True)
    # Keep the default thirteen-factor route's pictures in the first chunks.
    # Otherwise its last-state supports are scattered through the older replay.
    prioritized=[i for s in simple_states for i in s['factors']]
    for kind,field in [('supports','support'),('braids','braid')]:
        order=list(dict.fromkeys(rows[i][field] for i in prioritized))
        used=set(order)
        order.extend(i for i in range(len(assets[kind])) if i not in used)
        remap={old:new for new,old in enumerate(order)}
        assets[kind]=[assets[kind][i] for i in order]
        for row in rows:
            row[field]=remap[row[field]]
    asset_dir = destination / 'assets'
    asset_dir.mkdir(exist_ok=True)
    chunk_size = 32
    for kind, images in assets.items():
        for start in range(0, len(images), chunk_size):
            (asset_dir / (kind + '-' + str(start // chunk_size) + '.json')).write_text(
                json.dumps(images[start:start + chunk_size], separators=(',', ':')), encoding='utf-8')
    obsolete = destination / 'assets.json'
    if obsolete.exists():
        obsolete.unlink()  # This builder's superseded single generated asset bundle.
    template = ROOT / 'examples/six_seven_compact.html'
    viewer=(ROOT/'examples/six_seven_compact.js').read_text(encoding='utf-8')
    connected=(ROOT/'src/surface_diagrams/lab_assets/connected-braid.js').read_text(encoding='utf-8')
    version=sha256(json.dumps(dict(assets=assets,rows=rows,states=displays,simple=simplification),
                             separators=(',',':')).encode()+viewer.encode()+connected.encode()+
                   template.read_bytes()).hexdigest()[:16]
    for name, data in [('assets-index.json', dict(chunk_size=chunk_size,version=version,
                                                  counts={k: len(v) for k,v in assets.items()})),
                       ('display.json', dict(summary=summary, states=displays, rows=rows,
                                             chapters=chapters, groups=groups, atomic=atomic,
                                             forward=forward,simplification=simplification)),
                       ('support-certificates.json', dict(summary=summary, replacements=replacements))]:
        (destination / name).write_text(json.dumps(data, separators=(',', ':')), encoding='utf-8')
    html=template.read_text(encoding='utf-8').replace('<html lang="en">',
            '<html lang="en" data-replay-version="'+version+'">',1)
    for asset in ('connected-braid.js','viewer.js'):
        html=html.replace('src="'+asset+'"','src="'+asset+'?v='+version+'"')
    for asset in ('calibration.html','simplified-six-seven.json','simplification-certificate.json',
                  'source-route.json','support-certificates.json','frames.json'):
        html=html.replace('href="'+asset+'"','href="'+asset+'?v='+version+'"')
    (destination / 'index.html').write_text(html, encoding='utf-8')
    (destination / 'connected-braid.js').write_text(connected, encoding='utf-8')
    (destination / 'viewer.js').write_text(viewer, encoding='utf-8')
    half=Factor('Below 5',(4,),5,2,half=True)
    full=Factor('Neighborhood boundary',(4,),5,2)
    panels=[]
    for f,label in [(half,'Half twist: σ₄ σ₅ σ₄⁻¹'),(full,'Its square: σ₄ σ₅² σ₄⁻¹')]:
        panels.append('<section><h2>'+label+'</h2><div class="pair">'+
            number_support_points(support_svg(f,6,mirror_vertical=False))+connected_braid_svg((f.word,))+'</div></section>')
    (destination/'calibration.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Arc–braid cylinder calibration</title>'
        '<style>body{max-width:1000px;margin:30px auto;padding:15px;font:17px/1.6 system-ui;color:#18344a}.pair{display:flex;gap:30px;align-items:center}.pair svg:first-child{width:70%;height:240px}.pair svg:last-child{width:86px;height:130px}section{border-top:1px solid #abc;margin-top:25px}</style>'
        '<h1>Arc–braid cylinder calibration</h1><p>Points are numbered 1–6 from left to right. Read the braid top to bottom. '
        'The arc joins 4 to 6 below 5. Its neighborhood boundary supports the square of the half twist. '
        'Positive crossings and all algebraic words retain their signs; no display reflection is applied to these supports.</p>'+
        ''.join(panels)+'<p><a href="index.html">Back to the forward (6,7) route</a></p></html>',encoding='utf-8')
    print(json.dumps(dict(summary, support_images=len(assets['supports']), braid_images=len(assets['braids']))))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate-cache', help='Optional candidates; all used equalities are rechecked')
    build(parser.parse_args().candidate_cache)
