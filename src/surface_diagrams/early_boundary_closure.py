"""A named positive disk derivation of the residual fourth-boundary product.

All cyclic starts and common frames are explicit conjugations.  The terminal
four exterior twists are central, so undoing those conjugations proves the
source equality without assuming its boundary action.  No sphere cap occurs.
"""
from dataclasses import replace

from .braid_actions import inverse_word
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .mapping_classes import exact_action
from .projected_relations import pc_rose_terms, pc_daisy_terms

def _cyclic_last_first(r, title):
    before = r.factors
    moved = before[-1]
    r.factors = r.check(before[-1:] + before[:-1])
    r.record(title, 'disk_cyclic_start', moved_factor=moved, frame=moved.word,
             exact_conjugation=True, local_before=before, local_after=r.factors)


def close_round_boundary(factors):
    """Reach FOUR visible exteriors by named PC relations and fixed drags.

    Collect the inside-four-point factors around the short cyclic side, close
    their six-pair rose by a lantern, a Hurwitz move and a PC daisy, recognize
    TWO already matched PC daisies without the old 21 petal interchanges.
    This completes the named boundary closure, not the under-twenty-step goal.
    """
    factors = tuple(factors)
    r = _PositiveReplay(factors)
    if len(factors) != 15 or sum(f.points == 5 for f in factors) != 2:
        raise ValueError('Use the reached round-four-point reconstruction endpoint')
    r.stages[0]['title'] = 'Two visible exteriors and the positive residual to be closed geometrically'
    r.factors = r.check(tuple(r.normalize(replace(f, conjugator=(1, 1) + f.conjugator))
                              for f in r.factors))
    r.record('Explicit common T12 frame removes the shared winding of the leading curves',
             'global_conjugation', frame=(1, 1), exact_conjugation=True)
    root = r.factors[r.position('F10.2')]
    terms = tuple(r.normalize(Factor('close.rose245.' + str(i), t.conjugator, t.first, t.points))
                  for i, t in enumerate(pc_rose_terms(root.mapping_class)))
    r.substitute(r.position('F10.2'), 1, terms,
                 'PC rose of the actual 245 curve separates its inside-four petal', 'disk_pc_rose')
    for name, previous in (('exterior.inner23', 'exterior.inner14'),
                           ('close.rose245.0', 'exterior.inner23'),
                           ('pure.next.1', 'close.rose245.0')):
        r.drag(name, previous, after=True,
               title='Collect ' + name + ' with the preceding inside-four-point curves')
    r.drag('round.T34', 'round.rose345.2',
           title='Carry round T34 down the short side across the two end petals and the exterior')
    _cyclic_last_first(r, 'Choose the cyclic start at round T34; its full common frame is retained')
    r.drag('round.O1234', 'round.rose345.2',
           title='Carry round T1234 down the short side instead of through the five long petals')
    _cyclic_last_first(r, 'Choose the cyclic start at round T1234; all inside-four factors are now consecutive')
    collection_end = len(r.stages) - 1

    # A small reusable four-point rose derivation, rather than an action-only recognition.
    r.substitute(1, 3, (Factor('close.R134', (-1,), 2, 3),),
                 'PC lantern contracts the actual 34, 13, 14 petals to the 134 root', 'disk_cluster_lantern')
    r.drag('close.rose245.0', 'exterior.inner23',
           title='One inverse Hurwitz swap makes the remaining 23 petal round')
    r.substitute(1, 4, (Factor('close.O1234', (), 1, 4),),
                 'The four actual factors contract by the PC daisy in common frame sigma2 sigma3',
                 'disk_pc_daisy')
    inside_end = len(r.stages) - 1

    # The middle FOUR petals already form a PC daisy in a common B4
    # frame. Carrying the spare T1234 through the two leading petals both
    # supplies its prefix and removes their boundary winding. No search or
    # petal interchange is performed by this replay.
    witnesses = []
    checks = []

    def contract_daisy(index, frame, name, title):
        before = r.factors[index:index + 5]
        generic = pc_daisy_terms(Factor('daisy.outer', frame, 1, 5).mapping_class)
        local_checks = tuple(dict(actual=f, canonical=t,
            exact_disk_equal=exact_action(f.word, 5) == exact_action(t.word, 5))
            for f, t in zip(before, generic))
        if len(before) != 5 or not all(c['exact_disk_equal'] for c in local_checks):
            raise ValueError('The actual factors do not match the transported PC daisy individually')
        witnesses.append(dict(frame=frame, actual=before, generic=generic,
                              individual_checks=local_checks, exact_disk_equal=True))
        checks.extend(local_checks[1:])
        r.substitute(index, 5, (Factor(name, (), 1, 5),), title, 'disk_pc_daisy')
        r.stages[-1]['daisy_frame'] = frame
        r.stages[-1]['individual_daisy_checks'] = local_checks

    r.drag('close.O1234', 'close.rose245.1',
           title='Carry T1234 through only the TWO leading petals; their boundary winding disappears')
    contract_daisy(r.position('close.O1234'), (-3, 1, 1, 1, -3, -2, -1),
                   'close.outer3', 'PC daisy: the FOUR middle petals already match in one disk chart')
    petal_end = len(r.stages) - 1
    for name in ('exterior.boundary', 'close.outer3', 'second.exterior'):
        r.drag(name, r.factors[0].id,
               title='Commute the visible exterior ' + name + ' out of the remaining daisy')
    contract_daisy(3, (3, 3, 3, 2, 3, 1, 2, -3), 'close.outer4',
                   'PC daisy: the FOUR remaining actual petals give the fourth exterior')
    if len(r.factors) != 4 or any(f.points != 5 or f.conjugator for f in r.factors):
        raise ValueError('The named closure did not reach four visibly round exterior twists')
    retained = tuple(s['factors'] for s in r.stages) + tuple(
        a['factors'] for s in r.stages for a in s.get('atomic_steps', ()))
    peak = max(_score(state)['max_support_word'] for state in retained)
    if peak > 14 or any(f.half or f.power != 1 for state in retained for f in state):
        raise ValueError('The named closure lost positivity or its support bound')
    # Preserve framing balances even though this chapter displays marked points.
    for stage in r.stages:
        if stage['kind'] in ('disk_pc_rose', 'disk_pc_daisy', 'disk_cluster_lantern'):
            supports = [[enclosed_boundaries(f.mapping_class, 5) for f in stage[key]]
                        for key in ('local_before', 'local_after')]
            stage['framed_balance_before_minus_after'] = tuple(
                sum(i in b for b in supports[0]) - sum(i in b for b in supports[1]) for i in range(1, 6))
    bounds = (('earlycollect', 0, collection_end), ('earlyrose', collection_end, inside_end),
              ('earlypetals', inside_end, petal_end), ('earlyclosed', petal_end, len(r.stages) - 1))
    phases = {name: (dict(r.stages[start], kind='start'),) + tuple(r.stages[start + 1:end + 1])
              for name, start, end in bounds}
    return dict(stages=tuple(r.stages), phases=phases, factors=r.factors,
                graphical_steps=len(r.stages) - 1,
                adjacent_checks=sum(s.get('adjacent_moves', 0) for s in r.stages),
                phase_operations={name: len(stages) - 1 for name, stages in phases.items()},
                petal_crossing_route=(), canonical_petal_checks=tuple(checks),
                daisy_witnesses=tuple(witnesses), bypassed_noncentral_petal_interchanges=21,
                previous_graphical_steps=33, graphical_steps_saved=15, boundary_closure_under_twenty=True,
                sphere_move_count=0, all_factors_positive=True, half_twists_remaining=0,
                before_score=_score(factors), after_score=_score(r.factors),
                actual_peak_support_word=peak, peak_support_bound=14,
                boundary_power=4, explicit_exterior_twists=4, exterior_twists_retained=True,
                exterior_not_capped=True, complete_named_boundary_derivation=True,
                complete_under_twenty_derivation=False, applied_to_public_replay=False,
                global_and_cyclic_frames_explicit=True,
                scope='A named positive disk route reaches four visible exterior twists. All common/cyclic conjugations are explicit; the terminal central product closes the source equality without an action-only final recognition. No sphere cap is performed.')
