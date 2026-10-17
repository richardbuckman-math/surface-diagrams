"""Precompute small pair-multiplicity-two candidates and known compositions."""

import json
from itertools import combinations_with_replacement
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from surface_diagrams.double_boundary_catalog import canonical_blocks, double_outer_types
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.framed_boundary_relations import (
    enclosed_boundaries, five_boundary_lifts, five_boundary_mixed_lantern,
    five_boundary_type21_lantern, five_boundary_type28_lantern, five_boundary_type31_lantern,
    five_boundary_type32_lantern, four_triple_relations,
)
from surface_diagrams.boundary_playground_geometry import support_svg

DATA = ROOT / 'docs' / 'boundary-factorizations' / 'data'
SUPPORTS = ROOT / 'docs' / 'boundary-factorizations' / 'direct-supports'


def direct_relations(n):
    """Pre-render exact curves for four-triple relations and five-hole lifts."""
    SUPPORTS.mkdir(exist_ok=True)
    direct = {}
    relations = (four_triple_relations() if n == 4 else
                 five_boundary_lifts() + (five_boundary_mixed_lantern(),
                                          five_boundary_type31_lantern(),
                                          five_boundary_type32_lantern(),
                                          five_boundary_type28_lantern(),
                                          five_boundary_type21_lantern()))
    for relation in relations:
        factors = relation['factors']
        blocks = tuple(enclosed_boundaries(factor, n) for factor in factors)
        kind = canonical_blocks(n, blocks)
        name = relation.get('name') or (f'four-triple-{len(factors)}' if n == 4 else
                                        f'five-hole-lift-{len(factors)}')
        rows = []
        for index, (factor, block) in enumerate(zip(factors, blocks), 1):
            path = SUPPORTS / f'{name}-{index}.svg'
            drawing = Factor(f'{name}-{index}', factor.conjugator, factor.first,
                             factor.points, factor.power, factor.half)
            path.write_text(support_svg(drawing, n, inner_boundaries=tuple(range(1, n + 1))),
                            encoding='utf-8')
            rows.append({'conjugator': list(factor.conjugator),
                         'first': factor.first, 'points': factor.points,
                         'support': list(block),
                         'svg': f'direct-supports/{path.name}'})
        direct[kind] = {'name': name, 'factors': rows,
                        'inner_powers': list(relation['inner_powers']),
                        **({'expanded_seed_indices': list(relation['expanded_seed_indices'])}
                           if 'expanded_seed_indices' in relation else {}),
                        **({'core_factor_count': relation['core_factor_count']}
                           if 'core_factor_count' in relation else {}),
                        **({'hurwitz_positions': list(relation['hurwitz_positions']),
                            'lantern_support': list(relation['lantern_support']),
                            'source_pattern': relation['source_pattern']}
                           if 'hurwitz_positions' in relation else {}),
                        **({'hurwitz_directions': list(relation['hurwitz_directions'])}
                           if 'hurwitz_directions' in relation else {})}
    return direct


def build():
    for n in (3, 4, 5):
        relations = json.loads((DATA / f'{n}-relations.json').read_text(encoding='utf-8'))
        pairs = {}
        for i, j in combinations_with_replacement(range(len(relations)), 2):
            rows = relations[str(i)]['ordered_factors'] + relations[str(j)]['ordered_factors']
            pairs.setdefault(canonical_blocks(n, rows), (i, j))
        direct = direct_relations(n) if n in (4, 5) else {}
        patterns = [{'blocks': [list(block) for block in kind],
                     'composition': list(pairs[kind]) if kind in pairs else None,
                     **({'direct': direct[kind]} if kind in direct else {})}
                    for kind in double_outer_types(n)]
        (DATA / f'{n}-double.json').write_text(
            json.dumps({'n': n, 'patterns': patterns}, separators=(',', ':')),
            encoding='utf-8')
        print(f'{n} inner: {len(patterns)} candidates, {len(pairs)} certified compositions, '
              f'{len(direct)} direct framed relations')


if __name__ == '__main__':
    build()
