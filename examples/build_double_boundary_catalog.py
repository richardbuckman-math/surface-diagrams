"""Precompute small pair-multiplicity-two candidates and known compositions."""

import json
from itertools import combinations_with_replacement
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from surface_diagrams.double_boundary_catalog import canonical_blocks, double_outer_types

DATA = ROOT / 'docs' / 'boundary-factorizations' / 'data'


def build():
    for n in (3, 4):
        relations = json.loads((DATA / f'{n}-relations.json').read_text(encoding='utf-8'))
        pairs = {}
        for i, j in combinations_with_replacement(range(len(relations)), 2):
            rows = relations[str(i)]['ordered_factors'] + relations[str(j)]['ordered_factors']
            pairs.setdefault(canonical_blocks(n, rows), (i, j))
        patterns = [{'blocks': [list(block) for block in kind],
                     'composition': list(pairs[kind]) if kind in pairs else None}
                    for kind in double_outer_types(n)]
        (DATA / f'{n}-double.json').write_text(
            json.dumps({'n': n, 'patterns': patterns}, separators=(',', ':')),
            encoding='utf-8')
        print(f'{n} inner: {len(patterns)} candidates, {len(pairs)} certified compositions')


if __name__ == '__main__':
    build()
