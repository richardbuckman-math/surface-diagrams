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
from surface_diagrams.hyperelliptic_homology import homology_action
from surface_diagrams.mapping_classes import ConjugatedTwist, supported_class
from surface_diagrams.sphere_actions import sphere_supported_class
from surface_diagrams.sphere_support_compact import (
    check_support_replacement, compact_sphere_support, reframe_factors)
from surface_diagrams.twist_supports import support_curve
from surface_diagrams.visuals import BraidDiagram


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
            row_key = (compact, ci)
            if row_key not in row_cache:
                sk = (c.half, supported_class(c))
                if sk not in supports:
                    # Rendering checks the shared Arc/Loop router; a proposed
                    # itinerary alone is not accepted as a support picture.
                    supports[sk] = len(assets['supports'])
                    assets['supports'].append(support_svg(compact, 6, mirror_vertical=True))
                if compact.word not in braids:
                    braids[compact.word] = len(assets['braids'])
                    assets['braids'].append(BraidDiagram(
                        6, compact.word, spacing=18, step=13,
                        crossing_style='smooth', show_generators=False)._repr_svg_())
                row_cache[row_key] = len(rows)
                rows.append(dict(id=f.id, support=supports[sk], braid=braids[compact.word],
                                 label=('H' if f.half else 'T' + str(f.points)) +
                                 ('^' + str(f.power * f.sign) if f.power * f.sign != 1 else ''),
                                 inverse=f.sign < 0, cuts=checked['cuts'],
                                 sphere_rechart=not checked['disk_equal'], certificate=ci,
                                 factor=asdict(compact)))
            displayed.append(row_cache[row_key])
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
    summary = dict(atomic_moves=len(steps), chapters=len(chapters), grouped_moves=len(groups),
                   source_sphere_moves=sum(s['sphere'] for s in steps), hard_cut_cap=40,
                   max_displayed_cuts=max(r['cuts'] for r in rows),
                   factors_above_24=sum(r['cuts'] > 24 for r in rows),
                   old_max_available_cuts=max_raw_cuts, old_unavailable_supports=unavailable_raw,
                   old_max_sphere_class_length=raw_sphere_max,
                   source_sha256=sha256(source).hexdigest(),
                   complete_structural_derivation_found=False,
                   standard_block_bridge='UNCOMPUTED')
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
    for name, data in [('assets-index.json', dict(chunk_size=chunk_size,
                                                  counts={k: len(v) for k,v in assets.items()})),
                       ('display.json', dict(summary=summary, states=displays, rows=rows,
                                             chapters=chapters, groups=groups, atomic=atomic)),
                       ('support-certificates.json', dict(summary=summary, replacements=replacements))]:
        (destination / name).write_text(json.dumps(data, separators=(',', ':')), encoding='utf-8')
    template = ROOT / 'examples/six_seven_compact.html'
    (destination / 'index.html').write_text(template.read_text(encoding='utf-8'), encoding='utf-8')
    print(json.dumps(dict(summary, support_images=len(assets['supports']), braid_images=len(assets['braids']))))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate-cache', help='Optional candidates; all used equalities are rechecked')
    build(parser.parse_args().candidate_cache)
