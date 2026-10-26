"""Reach the original-half PC half-lantern by an actual outside rose donor.

This branch is not a replacement for the complete99-step proof. It uses
an actual new petal and local preconditioning, rather than trying to gather
the obstructed unchanged four-factor subsequence from the one-unit audit.
"""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .disk_intersection import disk_curve_intersection
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import exact_action
from .point_pushing import split_fixed_last_strand
from .projected_relations import pc_half_lantern_terms, pc_rose_terms
from .sphere_actions import sphere_chain_certificate


def _cyclic_start(replay, name, title):
    before = replay.factors
    i = replay.position(name)
    replay.factors = replay.check(before[i:] + before[:i])
    replay.record(title, 'disk_cyclic_start', frame=inverse_word(product(before[:i])),
                  local_before=before, local_after=replay.factors, exact_conjugation=True)


def _matches(actual, pattern):
    if len(actual) != len(pattern): raise ValueError('Named-pattern term counts differ')
    result = tuple(dict(actual=a, pattern=b, exact_disk_equal=exact_action(a.word, 5)==exact_action(b.word, 5))
                   for a, b in zip(actual, pattern))
    if not all(m['exact_disk_equal'] for m in result):
        raise ValueError('An actual input failed its joint PC chart')
    return result


def reach_outside_half_lantern(factors, *, round_chart=True):
    """Ten disk operations, or eleven with the clearer common chart.

    The existing R123 rose lends a Q12 unit. It combines with Q2, while
    the old Q1 is now an UNSELECTED factor and preconditions the gathering
    interval. Both ORIGINAL halves are absorbed in the reached half-lantern.
    No extra half, negative factor or sphere move is introduced.
    """
    if type(round_chart) is not bool: raise ValueError('Choose a boolean chart option')
    source = tuple(factors)
    if len(source) != 17 or source[0].id != 'alternative.O1234':
        raise ValueError('Use preserved original alternative state22')
    r = _PositiveReplay(source)
    r.stages[0]['title'] = 'Original alternative state22 before the outside-petal route'
    if r.factors[r.position('alternative.R2')] != Factor('alternative.R2', (), 1, 3):
        raise ValueError('The donor must be the actual round R123')
    if r.factors[r.position('alternative.T12.square')] != Factor('alternative.T12.square', (), 1, 2, 2):
        raise ValueError('The round square supplier changed')
    r.split('alternative.T12.square', 'one.unit.Q1', 'one.unit.Q2')
    _cyclic_start(r, 'one.unit.Q2', 'Cyclic start at the second unit avoids an extra commuting move')
    r.drag('one.unit.Q1', 'F11', title='Carry one unit up the short side to F11')

    i = r.position('alternative.R2'); donor = r.factors[i]
    terms = tuple(Factor('outside.rose.'+str(j), t.conjugator, t.first, t.points, t.power, t.half)
                  for j, t in enumerate(pc_rose_terms(donor.mapping_class)))
    donor_match = _matches((terms[0],), (r.factors[r.position('one.unit.Q2')],))
    r.substitute(i, 1, terms, 'Actual R123 PC rose supplies the OUTSIDE T12 unit', 'disk_pc_rose')
    r.stages[-1]['named_pattern_witness'] = dict(actual_outer=donor, canonical_terms=terms,
        supplied_unit_match=donor_match, exact_disk_equality=True)
    _cyclic_start(r, 'outside.rose.1', 'Cyclic start after the two actual T12 units')
    r.combine('one.unit.Q2', 'outside.rose.0', 'outside.Q.square')
    r.drag('outside.Q.square', 'alternative.F12.2',
           title='Bring the new actual square up past the outer and last C12 root, stopping after F11')
    frame = (3, 4, 4) if round_chart else ()
    if frame:
        before = r.factors
        r.factors = r.check(tuple(r.normalize(replace(f, conjugator=reduce_word(frame+f.conjugator))) for f in before))
        r.record('Common disk chart makes the half-lantern outer round', 'global_conjugation',
                 frame=frame, local_before=before, local_after=r.factors, exact_conjugation=True)
    # Q1 is deliberately NOT a donor in the new local target. Moving it up
    # conjugates only the intervening context, and makes the A-down gather
    # stay bounded. Direct A-down, square-up and AB-down attempts exceeded20.
    r.drag('one.unit.Q1', 'F6', after=True,
           title='The unselected Q1 unit preconditions the actual gathering interval')
    r.drag('F6', 'alternative.F12.1',
           title='Carry original F6 down to F11 and the outside-donor square')
    i = r.position('F6'); actual = r.factors[i:i+3]
    chart = reduce_word(frame+(-4,-4,-3,-1,2,1))
    pattern = tuple(Factor('pattern.half.'+str(j), t.conjugator, t.first, t.points, t.power, t.half)
                    for j, t in enumerate(pc_half_lantern_terms(Factor('pattern.root', chart, 1, 3).mapping_class)))
    matches = _matches(actual, pattern)
    root = r.normalize(Factor('outside.half.root', reduce_word(frame+(-4,-4,-3)), 1, 3))
    discrepancy = reduce_word(product(actual)+inverse_word(root.word))
    local_sphere = sphere_chain_certificate(discrepancy)
    local_lift = homology_action(discrepancy)
    if not local_sphere['certified'] or local_lift != IDENTITY:
        raise ValueError('The reached disk half-lantern failed its sphere/lift check')
    r.substitute(i, 3, (root,), 'Apply the ACTUAL ordered original-half PC half-lantern', 'disk_pc_half_lantern')
    parent_rose = tuple(Factor('pattern.parent.'+str(j), t.conjugator, t.first, t.points, t.power, t.half)
                        for j, t in enumerate(pc_rose_terms(root.mapping_class)))
    r.stages[-1]['named_pattern_witness'] = dict(common_chart=chart, canonical=pattern,
        individual_matches=matches, original_half_ids=('F6','F11'),
        supplied_square_ancestry=('one.unit.Q2','outside.rose.0'), unselected_preconditioner='one.unit.Q1',
        disk_discrepancy=discrepancy, sphere_certificate=local_sphere, chosen_lift_discrepancy=local_lift,
        parent_pc_rose=parent_rose,
        parent_framing_balance=tuple(sum(f.power for f in parent_rose if j in enclosed_boundaries(f.mapping_class,5))-
                                    sum(f.power for f in (root,) if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6)),
        half_twist_framed_boundary_lift_asserted=False,
        generic_derivation_reference='six-seven-one-unit-half-lantern.json / target / framing_source',
        applied=True, requires_gathering=False)
    # Only the full-twist rose is being given a framed-hole balance here.
    # No convention for framed-hole half twists is silently assumed.
    for s in r.stages:
        if s['kind']=='disk_pc_rose':
            s['framed_balance_before_minus_after'] = tuple(
                sum(f.power for f in s['local_before'] if j in enclosed_boundaries(f.mapping_class,5))-
                sum(f.power for f in s['local_after'] if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
    retained = [s for stage in r.stages for s in (stage,)+stage.get('atomic_steps',())]
    certificates = []
    for s in retained:
        sphere = sphere_chain_certificate(product(s['factors'])); lift = homology_action(product(s['factors']))
        if not sphere['certified'] or lift != IDENTITY:
            raise ValueError('A retained state lost its marked-sphere or chosen-lift certificate')
        certificates.append(dict(factors=s['factors'], sphere_certificate=sphere, chosen_lift=lift))
    if any(f.half for f in r.factors): raise ValueError('The original halves were not all absorbed')
    values = [disk_curve_intersection(a.mapping_class,b.mapping_class,strands=5)
              for i,a in enumerate(r.factors) for b in r.factors[i+1:]]
    q12 = Factor('outside.target.Q12', (), 1, 2)
    internal_root = replace(root, conjugator=reduce_word(inverse_word(q12.word)+root.conjugator))
    if exact_action(internal_root.word,5) != exact_action(root.word,5):
        raise ValueError('The proposed internal rose chart changes its outer')
    return_rose = tuple(Factor('outside.target.return.'+str(j),t.conjugator,t.first,t.points,t.power,t.half)
                        for j,t in enumerate(pc_rose_terms(internal_root.mapping_class)))
    middle_match = _matches((r.factors[r.position('one.unit.Q1')],),(return_rose[1],))
    _matches((replace(actual[0],half=False),),(return_rose[2],))
    restored_donor = r.normalize(Factor('outside.target.restored.R2',frame,1,3))
    restored_rose = tuple(Factor('outside.target.restore.'+str(j),t.conjugator,t.first,t.points,t.power,t.half)
                          for j,t in enumerate(pc_rose_terms(restored_donor.mapping_class)))
    restore_matches = _matches((q12,r.factors[r.position('outside.rose.1')],r.factors[r.position('outside.rose.2')]),restored_rose)
    next_return = dict(actual_new_root=root, internal_rose=return_rose,
        actual_Q1_middle_match=middle_match, unit_donor_match=_matches((q12,),(return_rose[0],)),
        restored_donor=restored_donor, restore_rose=restored_rose,
        restore_individual_matches=restore_matches,
        applied=False, requires_transport=True,
        scope='Two exact rose targets only. Returning the Q12 petal would need a concrete transport preserving the other matches; no return, duplicate-pair combine or complete join is claimed.')
    kernels = tuple(dict(factor=f, split=split_fixed_last_strand(f.word,5)) for f in r.factors)
    for k in kernels:
        if exact_action(k['factor'].word,5)!=exact_action(k['split'].reconstructed_word,5):
            raise ValueError('An endpoint point-pushing kernel reconstruction failed')
    return dict(stages=tuple(r.stages), factors=r.factors, graphical_operations=len(r.stages)-1,
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in r.stages), round_chart=round_chart,
        peak_support_word=max(_score(s['factors'])['max_support_word'] for s in retained),
        before_score=_score(source), after_score=_score(r.factors),
        curve_intersections=dict(maximum=max(values),total=sum(values),pairs=len(values)),
        state_sphere_lift_certificates=tuple(certificates), endpoint_point_pushing=kernels,
        next_rose_return=next_return,
        source_alternative_step=22, source_working_prefix=17,
        working_prefix_operations=39+len(r.stages)-1,
        half_twists_introduced=0, half_twists_remaining=0, sphere_moves=0, exterior_caps=0,
        actual_half_lantern_applied=True, source_old_four_factor_obstruction_bypassed_by_outside_donor=True,
        public_replay_changed=False, complete_proof_steps=99, complete_shorter_derivation=False,
        scope='Reached positive outside-petal half-lantern, using BOTH original halves and no auxiliary halves. This is a different all-full-twist branch, not a shorter complete99-step proof. No graphical route or PDF changes are asserted.')
