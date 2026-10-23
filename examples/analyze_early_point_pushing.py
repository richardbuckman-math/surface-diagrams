"""Keep the exact point-pushing kernel of the early B5 chart, not only its B4 shadow."""
from dataclasses import asdict
import json
from pathlib import Path
import time

from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.point_pushing import split_fixed_last_strand, common_shadow_obstruction


def early_point_pushing_report():
    folder = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-fifty-blocks'
    rows = json.loads((folder / 'certificate.json').read_text(encoding='utf-8'))['early_boundary']['chart']['factors']
    factors = tuple(Factor(**dict(f, conjugator=tuple(f['conjugator']))) for f in rows)
    splits = tuple(split_fixed_last_strand(f.word, 5) for f in factors)
    records = []
    for f, split in zip(factors, splits):
        checked = exact_action(f.word, 5) == exact_action(split.reconstructed_word, 5)
        if not checked:
            raise ValueError('A point-pushing reconstruction changed the source disk braid')
        records.append(dict(id=f.id, half=f.half, split=asdict(split),
                            kernel_exponents=tuple(sum(1 if a > 0 else -1 for a in split.kernel_loop if abs(a) == i)
                                                   for i in range(1, 5)), exact_disk_reconstruction=checked))
    halves = tuple(s for f, s in zip(factors, splits) if f.half)
    obstruction = common_shadow_obstruction(halves)
    obstruction['source_ids'] = tuple(f.id for f in factors if f.half)
    obstruction['other_pair'] = common_shadow_obstruction((halves[1], halves[3]))
    total = split_fixed_last_strand(product(factors), 5)
    expected_shadow = Factor('four-point boundary', (), 1, 4, power=4).word
    if total.kernel_loop != (1, 2, 3, 4) * 4 or exact_action(total.shadow_word, 4) != exact_action(expected_shadow, 4):
        raise ValueError('The separated product did not retain both boundary components')
    return dict(scope='Exact DISK stabilizer decomposition retaining both the B4 shadow and the F4 point-pushing kernel. This is a calculation diagnostic, not a new positive graphical proof, sphere move, or framed-puncture chart.',
                source='certificate.json / early_boundary / chart / factors', factors=records,
                half_common_frame_obstruction=obstruction, product_split=asdict(total),
                kernel_is_four_boundary_loops=True, shadow_is_four_four_point_boundaries=True,
                graphical_proof_changed=False, graphical_step_count=106,
                complete_under_twenty_derivation=False,
                next_step='Use the exact kernel as a transport invariant while seeking a shorter named route in the four-strand shadow; one simultaneous common frame cannot put all four original halves inside the four-point subdisk.')


if __name__ == '__main__':
    start = time.perf_counter()
    report = early_point_pushing_report()
    target = Path(__file__).resolve().parents[1] / 'docs/proofs/six-seven-point-pushing.json'
    target.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Saved full point-pushing kernel and exact common-frame obstruction in', round(time.perf_counter() - start, 3), 'seconds')
    print('The published graphical proof has 106 steps; this diagnostic performs no sphere or framed conversion.')
