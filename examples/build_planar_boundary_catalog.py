"""Precompute unlabeled pair-once patterns for the static Pages catalog.

Run with ``python examples/build_planar_boundary_catalog.py``. The generated
JSON files are committed, so the public page never enumerates in the browser.
"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from surface_diagrams.planar_boundary_catalog import structural_types, incidence

OUT = ROOT / 'docs' / 'boundary-factorizations' / 'data'
EXPECTED = {1: 1, 2: 1, 3: 2, 4: 3, 5: 5, 6: 10, 7: 24, 8: 69, 9: 384, 10: 5250}


def build(ns=range(1, 11)):
    OUT.mkdir(parents=True, exist_ok=True)
    for n in ns:
        types = sorted(structural_types(n),
                       key=lambda blocks: (-max((len(block) for block in blocks), default=0),
                                           len(blocks), blocks))
        if len(types) != EXPECTED[n]:
            raise AssertionError(f'{n} inner boundaries: {len(types)} types, expected {EXPECTED[n]}')
        for large in types:
            incidence(n, large)
        payload = {'n': n, 'equivalence': 'row order and inner-boundary relabeling',
                   'status': 'incidence candidate, not verified factorization',
                   'types': types}
        path = OUT / f'{n}.json'
        path.write_text(json.dumps(payload, separators=(',', ':')), encoding='utf-8')
        print(f'{n}: {len(types)} types, {path.stat().st_size} bytes', flush=True)


if __name__ == '__main__':
    build(tuple(map(int, sys.argv[1:])) if len(sys.argv) > 1 else range(1, 11))
