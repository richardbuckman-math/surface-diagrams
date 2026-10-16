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
    five_boundary_type31_lantern_states, framed_outer_certificate,
)

BASE = ROOT / 'docs' / 'boundary-factorizations'
DATA = BASE / 'data'
SUPPORTS = BASE / 'direct-supports'


def build_story(states, positions, lantern_start, source_pattern,
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
    moving_id = labels[positions[0]]
    moves = []
    for index in positions:
        moves.append(f'{moving_id} down past {labels[index + 1]}')
        labels[index:index + 2] = labels[index + 1], labels[index]
        ids.append(tuple(labels))
    labels[lantern_start:lantern_start + 3] = ['L235']
    ids.append(tuple(labels))
    assert len(ids) == len(states) == 5

    stage_names = (f'{len(states[0])}-factor source', 'First Hurwitz move',
                   'Second Hurwitz move', 'Third Hurwitz move',
                   'Inverse framed lantern')
    highlights = ((positions[0],), (positions[0], positions[0] + 1),
                  (positions[1], positions[1] + 1),
                  tuple(sorted({positions[2], positions[2] + 1,
                                *range(lantern_start, lantern_start + 3)})),
                  (lantern_start,))
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

    result = {'n': 5, 'outer_power': 2, 'source_pattern': source_pattern,
              'target_pattern': target_pattern, 'moving_factor': moving_id,
              'stages': stages,
              'moves': moves + ['T{2,3} · T{3,5} · T{2,5} → T{2,3,5}']}
    (DATA / f'{slug}-lantern-states.json').write_text(
        json.dumps(result, separators=(',', ':')), encoding='utf-8')
    print(f'Type {target_pattern}: saved five certified states and', len(picture_by_factor),
          'distinct pictured factors')


def build():
    patterns = json.loads((DATA / '5-double.json').read_text(encoding='utf-8'))['patterns']
    build_story(five_boundary_mixed_lantern_states(), (3, 4, 5), 6,
                30, 26, 'mixed', patterns)
    build_story(five_boundary_type31_lantern_states(), (5, 6, 7), 8,
                34, 31, 'type31', patterns)


if __name__ == '__main__':
    build()
