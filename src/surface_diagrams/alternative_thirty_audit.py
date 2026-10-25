"""Explicit optional sphere ending and a disk-only Hurwitz obstruction.

This audit is separate from every public graphical route. It certifies two
labeled sphere moves, not a Hurwitz derivation to the standard thirty word.
"""
from collections import Counter
from dataclasses import replace
from itertools import product as choices_product
from math import prod

from .braid_actions import inverse_word, reduce_word, free_homotopy_key
from .early_boundary_pure import _PositiveReplay
from .factorization_explorer import Factor, product
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import VerificationLimitError, exact_action
from .point_pushing import split_fixed_last_strand, point_push_braid
from .sphere_actions import sphere_chain_certificate
from .sphere_support_compact import half_endpoints


def pure_linking_certificate(word, strands=6, *, max_letters=100000):
    """Track labeled crossings, then divide by two only for a PURE disk braid."""
    if type(strands) is not int or strands < 2 or type(max_letters) is not int or max_letters < 1:
        raise ValueError('Use positive integer bounds and at least two strands')
    labels = list(range(1, strands + 1))
    counts = [[0] * strands for _ in labels]
    trace = []
    for position, crossing in enumerate(word):
        if position >= max_letters:
            raise VerificationLimitError('Linking calculation exhausted its word bound')
        if type(crossing) is not int or not 1 <= abs(crossing) < strands:
            raise ValueError('Crossing index exceeds the disk braid')
        i = abs(crossing) - 1
        a, b = labels[i] - 1, labels[i + 1] - 1
        sign = 1 if crossing > 0 else -1
        counts[a][b] += sign
        counts[b][a] += sign
        trace.append((crossing, labels[i], labels[i + 1]))
        labels[i], labels[i + 1] = labels[i + 1], labels[i]
    if labels != list(range(1, strands + 1)):
        raise ValueError('Pair linking numbers require a pure disk braid')
    if any(value % 2 for row in counts for value in row):
        raise ValueError('Pure braid crossing parity failed')
    matrix = tuple(tuple(value // 2 for value in row) for row in counts)
    spectrum = tuple(sorted(Counter(matrix[i][j] for i in range(strands) for j in range(i + 1, strands)).items()))
    return dict(strands=strands, final_permutation=tuple(labels), crossing_trace=tuple(trace),
                signed_crossings=tuple(map(tuple, counts)), linking_matrix=matrix,
                off_diagonal_spectrum=spectrum, pure=True)


def _sphere_move(before, after, title, local_before, local_after):
    discrepancy = reduce_word(product(before) + inverse_word(product(after)))
    local_discrepancy = reduce_word(product(local_before) + inverse_word(product(local_after)))
    sphere = sphere_chain_certificate(discrepancy)
    local_sphere = sphere_chain_certificate(local_discrepancy)
    if not sphere['certified'] or not local_sphere['certified']:
        raise VerificationLimitError('The proposed sphere move was not certified')
    lift = homology_action(discrepancy)
    local_lift = homology_action(local_discrepancy)
    if lift != IDENTITY or local_lift != IDENTITY:
        raise ValueError('The proposed sphere move changes the chosen genus-two lift')
    return dict(kind='sphere_rewrite', title=title, factors=after,
                local_before=local_before, local_after=local_after,
                disk_discrepancy=discrepancy, local_disk_discrepancy=local_discrepancy,
                disk_writhe_discrepancy=sum(1 if x > 0 else -1 for x in discrepancy),
                disk_equal=False, sphere_certificate=sphere, local_sphere_certificate=local_sphere,
                lift_homology=lift, local_lift_homology=local_lift,
                scope='Marked six-point sphere mapping class and separately checked chosen lift; no spherical-braid identity asserted.')


def _point_star_probe(pairs):
    """Only the eight unchanged cyclic subsequences, not a Hurwitz search."""
    frame = (5, 4, 3, 2)  # point2 becomes strand6; retain every kernel
    choices = {i: [] for i in (1, 3, 4, 5, 6)}
    for index, f in enumerate(pairs):
        edge = half_endpoints(f.mapping_class)
        if 2 not in edge:
            continue
        other = next(i for i in edge if i != 2)
        unit = replace(f, power=1)
        split = split_fixed_last_strand(frame + unit.word + inverse_word(frame), 6)
        if exact_action(split.shadow_word, 5) != exact_action((), 5):
            raise ValueError('A point-star petal lost its pure point-pushing shadow')
        choices[other].append(dict(index=index, id=f.id, split=split))
    count = prod(map(len, choices.values()))
    if count > 16:
        raise VerificationLimitError('The fixed point-star audit exceeds sixteen candidates')
    if count == 0:
        raise ValueError('A required endpoint of the fixed point-star audit is missing')
    boundary = (1, 2, 3, 4, 5)
    candidates = []
    for selected in choices_product(*(choices[i] for i in sorted(choices))):
        ordered = tuple(sorted(selected, key=lambda item: item['index']))
        loop = reduce_word(x for item in reversed(ordered) for x in item['split'].kernel_loop)
        candidates.append(dict(indices=tuple(item['index'] for item in ordered),
            ids=tuple(item['id'] for item in ordered), kernel_loop=loop,
            matches_peripheral_point_push=free_homotopy_key(loop) == free_homotopy_key(boundary)))
    star = point_push_braid(boundary, 6)
    sphere = sphere_chain_certificate(star)
    if not sphere['certified']:
        raise VerificationLimitError('The canonical peripheral point-star was not certified')
    lift = homology_action(star)
    negative = tuple(tuple(-x for x in row) for row in IDENTITY)
    if lift != negative:
        raise ValueError('The peripheral point-star has an unexpected chosen lift')
    star6 = tuple(Factor('target.star6.' + str(i), tuple(range(-5, -i)), i, 2) for i in range(5, 0, -1))
    star2 = tuple(replace(f, id=f.id.replace('star6', 'star2'), conjugator=reduce_word(inverse_word(frame) + f.conjugator)) for f in star6)
    if reduce_word(product(star6)) != star:
        raise ValueError('The peripheral target lost its ordered positive petals')
    swap = _sphere_move(star2, star6,
        'TARGET ONLY: coupled SPHERE peripheral-star substitution; both sides have -I lift', star2, star6)
    swap.update(kind='sphere_relation_target', applied=False, requires_transport=True,
                source_lift_homology=homology_action(product(star2)), target_lift_homology=lift,
                source_linking=pure_linking_certificate(product(star2)),
                target_linking=pure_linking_certificate(product(star6)))
    return dict(global_frame=frame, tracked_pairs=tuple(item for values in choices.values() for item in values),
        candidates=tuple(candidates), tested_candidates=count,
        matched_candidates=sum(item['matches_peripheral_point_push'] for item in candidates),
        canonical_peripheral_loop=boundary, canonical_peripheral_word=star,
        canonical_sphere_certificate=sphere, canonical_lift_homology=lift,
        next_peripheral_star_substitution=swap,
        applied=False, unchanged_subsequences_only=True,
        scope='A finite test of the eight current cyclic point2-star subsequences. No gathering or orbit exclusion is claimed; complete nonabelian kernels are retained.')


def audit_alternative_thirty(factors):
    """Keep the paired cap, complementary curve change and half splits separate."""
    source = tuple(factors)
    r = _PositiveReplay(source)
    exteriors = tuple(f for f in source if f.points == 5)
    four = tuple(f for f in source if f.points == 4)
    if len(source) != 16 or len(exteriors) != 2 or len(four) != 1 or any(f.power != 1 for f in exteriors) or four[0].first != 1:
        raise ValueError('Use the saved second-exterior endpoint')
    r.drag(exteriors[1].id, exteriors[0].id, after=True,
           title='Commute the second visible exterior up across three pair factors')
    r.combine(exteriors[0].id, exteriors[1].id, 'sphere.thirty.double-exterior')
    stages = list(r.stages)
    before = r.factors
    cap = before[0]
    if cap != Factor(cap.id, (), 1, 5, 2):
        raise ValueError('The paired cap is not the standard second boundary power')
    after = before[1:]
    stages.append(_sphere_move(before, after,
        'SPHERE MOVE: cap BOTH exterior twists together; the square has +I lift', (cap,), ()))
    cap_stage = len(stages) - 1
    old = next(f for f in after if f.points == 4)
    new = replace(old, id='sphere.thirty.complement26', first=5, points=2)
    pairs = tuple(new if f.id == old.id else f for f in after)
    stages.append(_sphere_move(after, pairs,
        'SPHERE MOVE: replace the four-point curve by its complementary two-point curve', (old,), (new,)))
    complement_stage = len(stages) - 1
    if (stages[cap_stage]['disk_writhe_discrepancy'], stages[complement_stage]['disk_writhe_discrepancy']) != (40, 10):
        raise ValueError('The two separate sphere discrepancies changed')
    halves, splits = [], []
    for f in pairs:
        if f.half or f.points != 2:
            raise ValueError('The optional ending must contain only full pair twists')
        terms = tuple(replace(f, id=f.id + '.half.' + str(j + 1), power=1, half=True) for j in range(2 * f.power))
        discrepancy = reduce_word(f.word + inverse_word(product(terms)))
        if discrepancy:
            raise ValueError('A pair expansion failed free-word disk equality')
        splits.append(dict(local_before=(f,), local_after=terms, disk_discrepancy=discrepancy))
        halves.extend(terms)
    halves = tuple(halves)
    if len(halves) != 30 or reduce_word(product(halves)) != reduce_word(product(pairs)):
        raise ValueError('The thirty-half expansion lost an ordered factor')
    stages.append(dict(kind='disk_expand_pairs', title='Expand each pair into its two positive halves; retain all fourteen local checks',
                       factors=halves, local_before=pairs, local_after=halves, factor_splits=tuple(splits), disk_discrepancy=()))
    endpoint_edges = tuple(half_endpoints(f.mapping_class) for f in halves)
    reached = {1}
    while True:
        enlarged = reached | {v for a, b in endpoint_edges if a in reached or b in reached for v in (a, b)}
        if enlarged == reached: break
        reached = enlarged
    if reached != set(range(1, 7)):
        raise ValueError('The saved optional thirty no longer has connected endpoint graph')
    action = sphere_chain_certificate(product(halves))
    if not action['certified']:
        raise VerificationLimitError('The optional ending sphere action is not certified')
    if homology_action(product(halves)) != IDENTITY:
        raise ValueError('The optional ending has the wrong chosen lift')
    actual = pure_linking_certificate(product(halves))
    standard_word = (1, 2, 3, 4, 5) * 6
    standard = pure_linking_certificate(standard_word)
    if actual['off_diagonal_spectrum'] == standard['off_diagonal_spectrum']:
        raise ValueError('The saved disk-only obstruction no longer applies')
    return dict(source=source, stages=tuple(stages), pairs=pairs, factors=halves,
        audit_transitions=len(stages) - 1, sphere_move_count=2, cap_stage=cap_stage,
        complement_stage=complement_stage, capped_exterior_power=2, retained_pair_expansions=len(splits),
        endpoint_edges=endpoint_edges, endpoint_component_sizes=(6,), sphere_certificate=action,
        point_star_probe=_point_star_probe(pairs),
        lift_homology=IDENTITY, disk_linking=actual, standard_full_twist_word=standard_word,
        standard_disk_linking=standard,
        disk_only_hurwitz_and_global_conjugation_excluded=True,
        sphere_hurwitz_equivalence_unknown=True, complete_named_derivation=False,
        applied_to_public_replay=False, replacement_for_full_proof=False,
        scope='Optional checked sphere ending with thirty positive halves. Connected endpoints and equal length do not identify W1. Disk-only Hurwitz/global conjugation cannot reach the standard six-strand full twist; sphere-specific steps remain open.')