"""Find exact real-line certificates for saved planar incidence patterns.

Usage: python examples/find_planar_boundary_relations.py 3 4 5 6 7
Only newly found certificates are saved. An unfound pattern stays open.
"""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from surface_diagrams.line_arrangement_relations import find_real_line_arrangement

DATA = ROOT / 'docs' / 'boundary-factorizations' / 'data'


def text_number(number):
    return str(number)


def build(ns):
    for n in ns:
        types = json.loads((DATA / f'{n}.json').read_text(encoding='utf-8'))['types']
        path = DATA / f'{n}-relations.json'
        saved = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        found = 0
        for index, large in enumerate(types):
            if str(index) in saved:
                continue
            result = find_real_line_arrangement(n, tuple(tuple(b) for b in large),
                                                slope_tries=24, offset_tries=24)
            if result is None:
                continue
            saved[str(index)] = {
                'method': 'Hironaka real-line arrangement, Theorem 1.2',
                'slopes': list(map(text_number, result['slopes'])),
                'intercepts': list(map(text_number, result['intercepts'])),
                'ordered_factors': [list(block) for _, _, block in result['intersections']],
                'x_values': [text_number(x) for x, _, _ in result['intersections']],
            }
            found += 1
        path.write_text(json.dumps(saved, separators=(',', ':'), sort_keys=True), encoding='utf-8')
        print(f'{n} inner boundaries: {len(saved)} / {len(types)} arrangements, {found} new', flush=True)


if __name__ == '__main__':
    build(tuple(map(int, sys.argv[1:])) if len(sys.argv) > 1 else range(3, 8))
