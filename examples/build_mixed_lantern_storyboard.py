"""Save the checked five-hole Hurwitz/lantern states and routed curves."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.double_boundary_catalog import canonical_blocks
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.framed_boundary_relations import (
    enclosed_boundaries, five_boundary_mixed_lantern_states,
    five_boundary_type28_lantern_states, five_boundary_type31_lantern_states,
    five_boundary_type32_lantern_states,
    framed_outer_certificate,
)

BASE = ROOT / 'docs' / 'boundary-factorizations'
DATA = BASE / 'data'
SUPPORTS = BASE / 'direct-supports'


def build_story(states, steps, lantern_start, source_pattern,
                target_pattern, slug, patterns):

    def published(state):
        kind = canonical_blocks(5, [enclosed_boundaries(factor, 5) for factor in state])
        return next(row['direct'] for row in patterns
                    if tuple(map(tuple, row['blocks'])) == kind)

    source, target = published(states[0]), published(states[-1])
    picture_by_factor = {}
    for state, direct in ((states[0], source), (states[-1], target)):
        for factor, saved in zip(state, direct['factors']):
            assert (list(factor.conjugator), factor.first, factor.points) == (
                saved['conjugator'], saved['first'], saved['points'])
            picture_by_factor.setdefault(factor, saved['svg'])

    labels = [f'F{index}' for index in range(1, len(states[0]) + 1)]
    ids = [tuple(labels)]
    moves, moving_ids = [], []
    for index, direction in steps:
        moving_id = labels[index if direction > 0 else index + 1]
        crossed_id = labels[index + 1 if direction > 0 else index]
        moving_ids.append(moving_id)
        moves.append(f'{moving_id} {"down" if direction > 0 else "up"} past {crossed_id}')
        labels[index:index + 2] = labels[index + 1], labels[index]
        ids.append(tuple(labels))
    lantern_support = enclosed_boundaries(states[-1][lantern_start], 5)
    labels[lantern_start:lantern_start + 3] = ['L' + ''.join(map(str, lantern_support))]
    ids.append(tuple(labels))
    assert len(ids) == len(states) == len(steps) + 2

    stage_names = (f'{len(states[0])}-factor source (type {source_pattern})',
                   *(f'Hurwitz move {index + 1}' for index in range(len(steps))),
                   'Inverse framed lantern')
    positions = tuple(index for index, _ in steps)
    highlights = [(positions[0], positions[0] + 1)]
    highlights.extend((index, index + 1) for index in positions)
    highlights[-1] = tuple(sorted({*highlights[-1],
                                   *range(lantern_start, lantern_start + 3)}))
    highlights.append((lantern_start,))
    stages = []
    for stage_number, (state, names) in enumerate(zip(states, ids)):
        powers = framed_outer_certificate(5, state, 2)
        rows = []
        for factor, label in zip(state, names):
            if factor not in picture_by_factor:
                path = SUPPORTS / f'{slug}-hurwitz-crossed-{len(picture_by_factor)}.svg'
                drawing = Factor(label, factor.conjugator, factor.first,
                                 factor.points, factor.power, factor.half)
                with path.open('w', encoding='utf-8', newline='\n') as out:
                    out.write(support_svg(drawing, 5, inner_boundaries=(1, 2, 3, 4, 5)))
                picture_by_factor[factor] = f'direct-supports/{path.name}'
            rows.append({'id': label, 'svg': picture_by_factor[factor],
                         'support': list(enclosed_boundaries(factor, 5)),
                         'conjugator': list(factor.conjugator),
                         'first': factor.first, 'points': factor.points})
        stages.append({'title': stage_names[stage_number],
                       'inner_powers': list(powers), 'rows': rows,
                       'highlight_rows': list(highlights[stage_number])})

    local_supports = [enclosed_boundaries(factor, 5) for factor in
                      states[-2][lantern_start:lantern_start + 3]]
    def twist_label(support):
        return 'T{' + ','.join(map(str, support)) + '}'
    move_description = (f'{moving_ids[0]} stays fixed as it moves down; each crossed factor is conjugated.'
                        if len(set(moving_ids)) == 1 else
                        'Move ' + '; then '.join(moves) + '. Each crossed factor is conjugated.')
    result = {'n': 5, 'outer_power': 2, 'source_pattern': source_pattern,
              'target_pattern': target_pattern, 'moving_factor': moving_ids[0],
              'move_description': move_description,
              'lantern_support': list(lantern_support),
              'lantern_pair_supports': [list(support) for support in local_supports],
              'stages': stages,
              'moves': moves + [' · '.join(map(twist_label, local_supports)) +
                                ' → ' + twist_label(lantern_support)]}
    (DATA / f'{slug}-lantern-states.json').write_text(
        json.dumps(result, separators=(',', ':')), encoding='utf-8')
    print(f'Type {target_pattern}: saved {len(states)} certified states and', len(picture_by_factor),
          'distinct pictured factors')


def build():
    patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
    build_story(five_boundary_mixed_lantern_states(), ((3, 1), (4, 1), (5, 1)), 6,
                30, 26, 'mixed', patterns)
    build_story(five_boundary_type31_lantern_states(), ((5, 1), (6, 1), (7, 1)), 8,
                34, 31, 'type31', patterns)
    build_story(five_boundary_type32_lantern_states(), ((4, -1), (5, 1), (6, 1)), 7,
                34, 32, 'type32', patterns)
    build_story(five_boundary_type28_lantern_states(), ((5, -1), (6, -1), (8, -1), (7, 1)), 8,
                32, 28, 'type28', patterns)


if __name__ == '__main__':
    build()
