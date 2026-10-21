"""Print a reproducible obstruction and a still-open local geometric target.

No braid search, browser calculation, sphere substitution or replay edit runs
here. The source is the already checked optional five-point boundary chart.
"""
from dataclasses import asdict, replace
import json
from pathlib import Path

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_explorer import product
from surface_diagrams.homology_orbits import modular_pairing_obstruction
from surface_diagrams.hyperelliptic_homology import half_twist_class
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.six_seven_structure import SignedResearchFactor


def compact_tail_diagnostic():
    source = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-fifty-blocks/certificate.json'
    data = json.loads(source.read_text(encoding='utf-8'))['compact_boundary_chart']['factors']
    factors = tuple(SignedResearchFactor(**dict(f, conjugator=tuple(f['conjugator']))) for f in data)
    tail = factors[9:]
    if tuple(f.id for f in tail) != ('F3', 'F6', 'new.P26', 'F9', 'F11',
                                    'last.P12.square', 'last.P34.square'):
        raise ValueError('The certified compact tail changed; recheck this diagnostic')
    def pairing(i, j):
        a, b = factors[i], factors[j]
        result = modular_pairing_obstruction(
            half_twist_class(a.conjugator, a.first),
            half_twist_class(b.conjugator, b.first),
            (f.word for f in tail))
        return dict(left_id=a.id, right_id=b.id, **result)

    # A genuine B5 local target, not an asserted route transporting F6 to it.
    desired = replace(factors[13], id='target.H12', conjugator=(-2, 1))
    square = factors[14]
    pair = replace(square, power=1)
    root = replace(square, id='target.T123', conjugator=(), first=1, points=3, power=1)
    left = (desired, factors[13], square)
    actual, expected = exact_action(product(left), strands=5), exact_action(root.word, strands=5)
    transported = pair.word + desired.word + inverse_word(pair.word)
    if actual != expected or exact_action(transported, strands=5) != exact_action(factors[13].word, strands=5):
        raise ValueError('The proposed PC half-lantern target failed its exact disk check')
    return dict(source='six-seven-fifty-blocks/certificate.json:compact_boundary_chart.factors[9:]',
        source_tail=[asdict(f) for f in tail],
        f3_f9=pairing(9, 12), f6_f11=pairing(10, 13),
        local_target=dict(before=[asdict(f) for f in left], after=[asdict(root)],
            disk_action=dict(strands=5, actual=actual, expected=expected, equal=True),
            conjugating_pair=asdict(pair),
            f6_already_matches=exact_action(factors[10].word, strands=5)==exact_action(desired.word, strands=5),
            applied_to_replay=False, route_found=False),
        sphere_moves=0, shorter_derivation_found=False,
        next_step='Transport F6 into the checked T123 local target using a specific geometric move; F3/F9 require mixing outside the tail or a substitution')


if __name__ == '__main__':
    print(json.dumps(compact_tail_diagnostic(), indent=2))
