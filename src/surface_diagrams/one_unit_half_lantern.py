"""A bounded one-unit transport, exact half-lantern target and ordered obstruction.

This is an audit, not a new public graphical route or a shorter complete proof.
The local target has an individual joint PC chart. The actual four factors
occur in another cyclic order and are not gathered into that target.
"""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import exact_action
from .point_pushing import split_fixed_last_strand
from .projected_relations import pc_daisy_terms, pc_half_lantern_terms, pc_rose_terms
from .sphere_actions import sphere_chain_certificate
from .six_seven_structure import research_hurwitz_move


def audit_one_unit_half_lantern(factors):
    """Test the specified original alternative state22, without a route search."""
    source = tuple(factors)
    r = _PositiveReplay(source)
    if len(source) != 17 or source[0].id != 'alternative.O1234':
        raise ValueError('Use the preserved original alternative state22')
    square = source[r.position('alternative.T12.square')]
    q = replace(square, power=1)
    if q != Factor(q.id, (), 1, 2):
        raise ValueError('The one-unit probe requires the actual round T12 square')
    a, original_b = (source[r.position(name)] for name in ('F6', 'F11'))
    if exact_action(q.word * 2 + a.word + inverse_word(q.word * 2), 5) != exact_action(original_b.word, 5):
        raise ValueError('The original whole-square transport target changed')
    r.stages[0]['title'] = 'Original alternative state22, before the square transport'
    r.split(square.id, 'one.unit.Q1', 'one.unit.Q2')
    r.drag('one.unit.Q1', 'alternative.O1234', title='Carry only one actual T12 unit to the top')
    before = r.factors; moved = before[0]
    r.factors = r.check(before[1:] + before[:1])
    r.record('Cyclic start after one actual T12 unit', 'disk_cyclic_start',
             frame=inverse_word(moved.word), local_before=before, local_after=r.factors,
             exact_conjugation=True)
    r.drag('one.unit.Q1', 'F11', title='Carry only one unit up the short side to F11')
    a, b = (r.factors[r.position(name)] for name in ('F6', 'F11'))
    if exact_action(q.word + a.word + inverse_word(q.word), 5) != exact_action(b.word, 5):
        raise ValueError('The one-unit half target failed')

    # The first half's right sigma1 stabilizer gives the EXACT joint chart;
    # its shortest saved conjugator alone matches only that first half.
    chart = reduce_word(a.conjugator + (a.first,))
    root = r.normalize(Factor('one.unit.target.R124', chart, 1, 3))
    canonical = tuple(Factor('pattern.half.' + str(i), t.conjugator,
                            t.first, t.points, t.power, t.half)
                      for i, t in enumerate(pc_half_lantern_terms(Factor('pattern.root', chart, 1, 3).mapping_class)))
    desired = (a, b, replace(q, power=2))
    matches = tuple(dict(actual=x, pattern=y, exact_disk_equal=exact_action(x.word, 5) == exact_action(y.word, 5))
                    for x, y in zip(desired, canonical))
    if not all(m['exact_disk_equal'] for m in matches) or exact_action(product(desired), 5) != exact_action(root.word, 5):
        raise ValueError('The proposed half-lantern did not match all actual classes')
    local_lift = homology_action(product(desired) + inverse_word(root.word))
    if local_lift != IDENTITY: raise ValueError('The local disk target changed its chosen lift')
    rose = tuple(Factor('pattern.rose.' + str(i), t.conjugator, t.first, t.points, t.power, t.half)
                 for i, t in enumerate(pc_rose_terms(Factor('pattern.root', chart, 1, 3).mapping_class)))
    first_half = replace(rose[0], half=True)
    split_rose = (first_half, replace(first_half, id='pattern.rose.second_half')) + rose[1:]
    first_move = research_hurwitz_move(split_rose, 1, 2)
    second_move = research_hurwitz_move(first_move['factors'], 1, 2)
    derived = second_move['factors'][:2] + (replace(second_move['factors'][2], power=2),)
    if any(exact_action(x.word, 5) != exact_action(y.word, 5) for x, y in zip(derived, canonical)):
        raise ValueError('The retained rose derivation did not give the half-lantern pattern')
    parent_balance = tuple(sum(f.power for f in rose if i in enclosed_boundaries(f.mapping_class, 5)) -
                           sum(f.power for f in (root,) if i in enclosed_boundaries(f.mapping_class, 5)) for i in range(1, 6))
    framing_source = dict(rose_terms=rose, split_rose=split_rose,
        retained_hurwitz_checks=(first_move, second_move), derived_terms=derived,
        parent_pc_rose_balance_before_minus_after=parent_balance,
        half_twist_boundary_lift_asserted=False,
        scope='The signed full-twist PC rose balance is retained. The target is a marked-disk relation; no framed-hole half-twist convention or holed-surface substitution is asserted.')


    # Source positions are Q2,A,Q1,B, not A,B,Q1,Q2. Noncentrality of
    # their product in their own generated subgroup is Hurwitz invariant.
    selected_ids = ('one.unit.Q2', 'F6', 'one.unit.Q1', 'F11')
    selected = tuple(f for f in r.factors if f.id in selected_ids)
    if tuple(f.id for f in selected) != selected_ids:
        raise ValueError('The four actual factors no longer have the audited order')
    orders = []
    for offset in range(4):
        order = selected[offset:] + selected[:offset]; word = product(order)
        witness = None
        for factor in order:
            left, right = exact_action(word + factor.word, 5), exact_action(factor.word + word, 5)
            if left != right:
                meridian = next(i for i, (u, v) in enumerate(zip(left, right), 1) if u != v)
                witness = dict(factor=factor, left_images=left, right_images=right,
                               first_different_meridian=meridian, noncommuting=True)
                break
        if witness is None: raise ValueError('This cyclic product was not excluded by noncentrality')
        orders.append(dict(offset=offset, factors=order, product_word=word, witness=witness))

    # A real source outer can lend this exact root in an internal chart.
    # This is only an available donor; no expansion or gathering is applied.
    outer = source[0]
    donor_chart = root.conjugator
    donor_outer = Factor('one.unit.donor.outer', donor_chart, 1, 4)
    donor_terms = tuple(Factor('one.unit.donor.' + str(i), t.conjugator, t.first, t.points, t.power, t.half)
                        for i, t in enumerate(pc_daisy_terms(donor_outer.mapping_class)))
    if (exact_action(outer.word, 5) != exact_action(donor_outer.word, 5) or
            exact_action(donor_terms[0].word, 5) != exact_action(root.word, 5)):
        raise ValueError('The actual four-point outer does not lend the proposed root')
    donor_matches = tuple(dict(petal=p, existing_unit_matches=tuple(f.id for f in r.factors if not f.half and exact_action(replace(f,power=1).word,5)==exact_action(p.word,5))) for p in donor_terms[1:])
    splits = tuple(dict(factor=f, split=split_fixed_last_strand(f.word, 5)) for f in desired + (root,))
    for entry in splits:
        if exact_action(entry['factor'].word, 5) != exact_action(entry['split'].reconstructed_word, 5):
            raise ValueError('A target point-pushing reconstruction changed the disk braid')
    actual_split = split_fixed_last_strand(product(selected), 5)
    retained = [s for stage in r.stages for s in (stage,) + stage.get('atomic_steps', ())]
    certificates = []
    for state in retained:
        sphere = sphere_chain_certificate(product(state['factors']))
        lift = homology_action(product(state['factors']))
        if not sphere['certified'] or lift != IDENTITY:
            raise ValueError('A retained disk state lost its sphere or chosen-lift certificate')
        certificates.append(dict(factors=state['factors'], sphere_certificate=sphere, chosen_lift=lift))
    return dict(stages=tuple(r.stages), factors=r.factors, graphical_operations=4,
        adjacent_checks=sum(s.get('adjacent_moves', 0) for s in r.stages),
        before_score=_score(source), after_score=_score(r.factors),
        peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        state_sphere_lift_certificates=tuple(certificates), sphere_move_count=0,
        target=dict(local_before=desired, local_after=(root,), common_chart=chart,
            canonical=canonical, individual_matches=matches, chosen_lift_discrepancy=local_lift,
            framing_source=framing_source, point_pushing_splits=splits,
            applied=False, requires_gathering=True, exact_disk_relation=True),
        ordered_obstruction=dict(actual_selected_factors=selected, cyclic_orders=tuple(orders),
            actual_product_split=actual_split, product_is_noncentral_in_generated_subgroup=True,
            selected_only_disk_hurwitz_and_common_frame_excluded=True,
            scope='Excludes selected-four-factor-only DISK Hurwitz/common-conjugation routes to a PC half-lantern. Outside interactions and sphere changes are NOT excluded. Nor are other substitutions, splitting or combining.'),
        donor=dict(actual_outer=outer, chart=donor_chart, canonical_outer=donor_outer,
                   terms=donor_terms, first_root_exact_match=True, existing_petal_matches=donor_matches, applied=False),
        public_replay_changed=False, complete_proof_steps=99, complete_under_twenty_derivation=False,
        scope='Separate four-operation positive disk audit. The local half-lantern target is individually exact but is NOT gathered or applied. The complete99-step proof, every graphical payload and both PDFs remain unchanged.')
