"""A framing-complete optional sphere-chart audit, not a shorter proof.

The public 39-operation research route and complete 106-step proof are
unchanged. In particular the nine exterior corrections below are retained;
the normalized third-boundary product alone is not lift-equivalent.
"""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import exact_action, supported_class, VerificationLimitError
from .puncture_boundary import BOUNDARY_WORD, puncture_to_boundary
from .sphere_actions import sphere_chain_certificate
from .twist_simplify import simplify_twist


def fixed_point_chart_predictions(factors, *, boundary_power=4):
    """Predict chart exponents from incidence, then require actual rewriting.

    For an internal exterior choice the old five-point boundary maps to
    three new boundaries in this chosen framed stabilizer lift. A k-point
    positive twist incident to that point contributes k-2 corrections per
    unit. This predicts a central exponent, not curve geometry or a named
    factorization; it cannot replace the actual Schreier/sphere/lift checks.
    """
    factors = tuple(factors)
    if type(boundary_power) is not int or boundary_power < 1:
        raise ValueError('Use a positive integer source boundary power')
    if not factors or any(f.half or f.power < 1 or getattr(f, 'sign', 1) != 1
                          or any(abs(x) > 4 for x in f.word) for f in factors):
        raise ValueError('Use positive full twists in the five-point disk')
    if exact_action(product(factors), 5) != exact_action(BOUNDARY_WORD * boundary_power, 5):
        raise ValueError('The source does not have the declared exact boundary action')
    incidence = tuple((f, enclosed_boundaries(f.mapping_class, 5)) for f in factors)
    candidates = []
    for point in range(1, 7):
        framed = boundary_power * (3 if point <= 5 else 1)
        correction = sum((f.points - 2) * f.power for f, inside in incidence if point in inside)
        candidates.append(dict(marked_point=point, predicted_correction_power=correction,
                               predicted_normalized_power=framed - correction,
                               predicted_framed_power=framed))
    minimum = min(c['predicted_normalized_power'] for c in candidates)
    return dict(candidates=tuple(candidates), minimal_predicted_points=tuple(
        c['marked_point'] for c in candidates if c['predicted_normalized_power'] == minimum),
        source_boundary_power=boundary_power, requires_exact_rechart=True,
        scope='Incidence prediction only. A smaller normalized exponent is not a shorter proof or a smaller framed product.')


def _present(factor):
    t = simplify_twist(factor.mapping_class, strands=5)
    result = replace(factor, conjugator=t.conjugator, first=t.first)
    if exact_action(result.word, 5) != exact_action(factor.word, 5):
        raise ValueError('A disk presentation changed its supported twist')
    return result


def audit_alternative_point_four(factors):
    """Check one selected sphere rechart and its exposed local PC lantern.

    Point4 is selected by the incidence prediction, not a curve-word scan.
    Its normalized fourteen factors have boundary^3 action, with NINE
    positive boundary corrections. The corrected product is boundary^12.
    Both odd parts have -I lift; their combined sphere rechart has +I.
    This report never caps either part and is not in the public proof route.
    """
    source = tuple(factors)
    predictions = fixed_point_chart_predictions(source)
    if predictions['minimal_predicted_points'] != (4,):
        raise ValueError('Use the operation39 alternative endpoint with selected point4')
    chart = puncture_to_boundary(source, marked_point=4)
    if (chart['normalized_boundary_power'], chart['boundary_correction_power'],
            chart['framed_boundary_power']) != (3, 9, 12):
        raise ValueError('The chosen chart changed its declared framing')
    correction = Factor('alt4.boundary.corrections', (), 1, 5, power=9)
    normalized = chart['factors']
    corrected = (correction,) + normalized
    framed = tuple(c['globally_framed'] for c in chart['factor_certificates'])
    discrepancy = reduce_word(product(framed) + inverse_word(product(corrected)))
    sphere = sphere_chain_certificate(discrepancy)
    if not sphere['certified']:
        raise VerificationLimitError('The combined sphere rechart was not certified')
    lift = homology_action(discrepancy)
    writhe_discrepancy = sum(1 if x > 0 else -1 for x in discrepancy)
    if writhe_discrepancy != -160:
        raise ValueError('The sphere rechart lost its explicit disk writhe discrepancy')
    if lift != IDENTITY or exact_action(product(corrected), 5) != exact_action(BOUNDARY_WORD * 12, 5):
        raise ValueError('The retained corrections did not preserve the chosen sphere lift')

    # Adjacent input R235,S135,T12 matches the cyclic cabled PC lantern
    # R234,(sigma1 R234 sigma1^-1),T12 in a common chart fixing sigma1.
    index = next(i for i, f in enumerate(normalized) if f.id == 'alternative.F12.1')
    local = normalized[index:index + 3]
    if tuple(f.id for f in local) != ('alternative.F12.1', 'F10.2', 'alternative.next.0'):
        raise ValueError('The adjacent actual lantern configuration has changed')
    h = (-1, -1, 2, 1, 1, 2, 3, 3, 4)
    canonical = (Factor('pattern.R234', (), 2, 3), Factor('pattern.S134', (1,), 2, 3),
                 Factor('pattern.Q12', (), 1, 2))
    canonical_after = (Factor('pattern.O1234', (), 1, 4), Factor('pattern.I34', (), 3, 2))
    if exact_action(product(canonical), 5) != exact_action(product(canonical_after), 5):
        raise ValueError('The cyclic cabled PC lantern failed')
    pattern = tuple(replace(f, conjugator=reduce_word(h + f.conjugator)) for f in canonical)
    matches = tuple(dict(actual=a, pattern=b, exact_disk_equal=exact_action(a.word, 5) == exact_action(b.word, 5))
                    for a, b in zip(local, pattern))
    if not all(c['exact_disk_equal'] for c in matches):
        raise ValueError('An actual chart factor failed its individual lantern match')
    raw_after = tuple(replace(f, id=name, conjugator=reduce_word(h + f.conjugator))
                      for f, name in zip(canonical_after, ('alt4.O1235', 'alt4.I35')))
    local_after = tuple(_present(f) for f in raw_after)
    presentation_matches = tuple(dict(actual=a, pattern=b,
        exact_disk_equal=exact_action(a.word, 5) == exact_action(b.word, 5)) for a, b in zip(raw_after, local_after))
    if exact_action(product(local), 5) != exact_action(product(local_after), 5):
        raise ValueError('The actual ordered lantern did not agree in B5')
    after_normalized = normalized[:index] + local_after + normalized[index + 3:]
    after = (correction,) + after_normalized
    if exact_action(product(after), 5) != exact_action(BOUNDARY_WORD * 12, 5):
        raise ValueError('The local disk substitution changed the corrected chart product')
    balance = tuple(sum(i in enclosed_boundaries(f.mapping_class, 5) for f in local)
                    - sum(i in enclosed_boundaries(f.mapping_class, 5) for f in local_after) for i in range(1, 6))
    lengths = tuple(len(supported_class(f.mapping_class, 5)) for f in after_normalized)
    return dict(predictions=predictions, source=source, chart=chart,
        global_frame=dict(kind='global_conjugation', frame=chart['global_frame'], factors=framed),
        sphere_move=dict(kind='sphere_rechart', title='SPHERE MOVE: point4 becomes exterior; retain ALL NINE boundary corrections',
            local_before=framed, local_after=corrected, factors=corrected,
            disk_discrepancy=discrepancy, disk_equal=False, disk_writhe_discrepancy=writhe_discrepancy,
            sphere_certificate=sphere, lift_homology=lift,
            is_lift_equality=True, explicit_boundary_corrections=(correction,), not_a_cap=True),
        disk_move=dict(kind='disk_cluster_lantern', local_before=local, local_after=local_after, factors=after,
            named_pattern_witness=dict(frame=h, canonical=canonical, canonical_after=canonical_after,
                individual_matches=matches, presentation_matches=presentation_matches),
            framed_balance_before_minus_after=balance, boundary_corrections_retained=(correction,)),
        corrected_factors=corrected, factors=after, normalized_factors=after_normalized,
        normalized_boundary_power=3, boundary_correction_power=9, corrected_boundary_power=12,
        normalized_lift=homology_action(product(after_normalized)), correction_lift=homology_action(correction.word),
        sphere_move_count=1, boundary_caps=0, applied_to_public_replay=False,
        complete_named_derivation=False, replacement_for_full_proof=False,
        normalized_score=dict(max_support_word=max(lengths), total_support_word=sum(lengths),
                              braid_letters=len(product(after_normalized))),
        scope='Optional checked sphere-chart audit with all nine corrections visible in the factor records. No cap or shorter complete proof is claimed; the public106-step proof and39-operation branch are unchanged.')
