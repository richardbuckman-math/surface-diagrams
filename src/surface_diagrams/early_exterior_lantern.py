"""A positive, disk-exact extraction of one actual exterior boundary twist.

This is a six-operation research branch from the latest pure endpoint.  The
single exterior twist stays visible; no sphere or genus-two cap is performed.
The remaining named derivation of the boundary product is still open.
"""
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor
from .mapping_classes import exact_action
from .braid_actions import inverse_word


def extract_positive_exterior(factors):
    """Reach and apply an exterior PC lantern with support bound twenty.

    A positive UNIT of the existing square, rather than the full square,
    transports B to the actual lantern needed by the current O and C.  A
    central cyclic start permits gathering around the short side without
    the support spike of the direct linear gathers.
    """
    factors = tuple(factors)
    r = _PositiveReplay(factors)
    r.stages[0]['title'] = 'The twenty-factor pure endpoint before exterior extraction'
    r.split('early.T12.square', 'exterior.split.1', 'exterior.split.2')
    r.drag('exterior.split.2', 'early.F13.1',
           title='One positive square unit crosses F8 and transports B to the exact exterior-lantern curve')
    matched_b = Factor('exterior.target.B235', (-3, -1, -1, 2), 3, 3)
    if exact_action(r.factors[r.position('early.F13.1')].word, 5) != exact_action(matched_b.word, 5):
        raise ValueError('The square unit did not expose the required exterior-lantern B curve')

    shift = r.position('early.F13.1')
    before_cycle = r.factors
    r.factors = r.check(r.factors[shift:] + r.factors[:shift])
    r.record('Choose a cyclic start at the matched B in the central disk product',
             'disk_cyclic_start', cyclic_shift=shift, local_before=before_cycle,
             local_after=r.factors, exact_disk_equality=True, not_a_sphere_move=True)
    r.drag('early.F13.1', 'early.P13.pair',
           title='Carry matched B across the square unit and P13, stopping before C')
    target = r.factors[r.position('early.F12.1') + 1].id
    r.drag('pure.O1234', target,
           title='Bring the round four-point curve up around the short cyclic side, immediately after C')
    index = r.position('early.F13.1')
    if tuple(f.id for f in r.factors[index:index + 3]) != (
            'early.F13.1', 'early.F12.1', 'pure.O1234'):
        raise ValueError('The actual exterior-lantern triple was not gathered in order')

    exterior = Factor('exterior.boundary', (), 1, 5)
    inner14 = Factor('exterior.inner14', (-1, -1, -1, -3), 2, 2)
    inner23 = Factor('exterior.inner23', (-3, -1, -1, -3), 2, 2)
    r.substitute(index, 3, (exterior, inner14, inner23),
                 'Extract an actual exterior twist by the positive PC cluster lantern',
                 'disk_cluster_lantern')
    retained = tuple(s['factors'] for s in r.stages) + tuple(
        a['factors'] for s in r.stages for a in s.get('atomic_steps', ()))
    peak = max(_score(state)['max_support_word'] for state in retained)
    if peak > 20 or any(f.half or f.power < 1 for state in retained for f in state):
        raise ValueError('The exterior extraction lost positivity or exceeded its support bound')
    return dict(stages=tuple(r.stages), factors=r.factors,
                graphical_steps=len(r.stages) - 1,
                adjacent_checks=sum(s.get('adjacent_moves', 0) for s in r.stages),
                sphere_move_count=0, all_factors_positive=True, half_twists_remaining=0,
                before_score=_score(factors), after_score=_score(r.factors),
                peak_support_bound=20, actual_peak_support_word=peak,
                boundary_power=4, explicit_exterior_twists=1,
                exterior_twist_retained=True, exterior_not_capped=True,
                matched_middle=matched_b, disk_action_verified=True,
                complete_named_derivation=False, applied_to_public_replay=False,
                scope='Six positive B5 operations extract one visible exterior twist; no sphere cap is performed and the remaining named boundary closure is open.')


def contract_exterior_petals(factors):
    """Gather the untouched T34 petals and contract their actual PC lantern.

    The exterior extraction transports the other side of the cyclic product,
    leaving this local configuration available. The result has six triple
    curves and twelve pair curves beside the visible exterior twist.
    """
    r = _PositiveReplay(tuple(factors))
    exterior = Factor('exterior.boundary', (), 1, 5)
    if tuple(f for f in r.factors if f.points == 5) != (exterior,):
        raise ValueError('Use the positive endpoint with one visible exterior twist')
    r.stages[0]['title'] = 'One exterior twist has been extracted and stays visible'
    r.drag('early.P35', 'early.daisy.1',
           title='Carry the actual T34 petal through two roots to its matching petals')
    r.substitute(r.position('early.P35'), 3,
                 (Factor('residual.T345', (1, 2, 3, -4), 2, 3),),
                 'Contract the three actual pair petals by the PC lantern',
                 'disk_cluster_lantern')
    by_id = {f.id: f for f in r.factors}
    transport = by_id['exterior.split.1'].word + inverse_word(by_id['pure.next.1'].word)
    source, target = by_id['residual.T345'], by_id['F8.2']
    if exact_action(transport + source.word + inverse_word(transport), 5) != exact_action(target.word, 5):
        raise ValueError('The saved two-factor root-alignment target failed its disk check')
    required = Factor('residual.required15', (1, 2, 3), 4, 2)
    outer = Factor('residual.target1345', (1,), 2, 4)
    inner = Factor('residual.target34', (), 3, 2)
    cluster_before = (by_id['early.daisy.1'], source, required)
    cluster_after = (outer, inner)
    # This is the transported PC lantern of the clusters (34,1,5).
    # The existing U is not this petal; an actual R-transport is still needed.
    from .factorization_explorer import product
    supplier = by_id['pure.next.1'].word
    actual_petal = by_id['exterior.split.1']
    if (exact_action(product(cluster_before), 5) != exact_action(product(cluster_after), 5)
            or exact_action(supplier + actual_petal.word + inverse_word(supplier), 5)
            != exact_action(required.word, 5)):
        raise ValueError('The next positive cluster-lantern target failed its ordered check')
    return dict(stages=tuple(r.stages), factors=r.factors,
                graphical_steps=2, adjacent_checks=2, sphere_move_count=0,
                before_score=_score(tuple(factors)), after_score=_score(r.factors),
                boundary_power=4, all_factors_positive=True, disk_action_verified=True,
                exterior_twist_retained=True, exterior_not_capped=True,
                next_cluster_lantern=dict(local_before=cluster_before, local_after=cluster_after,
                    actual_petal=actual_petal, supplier=by_id['pure.next.1'],
                    exact_disk_equality=True, requires_transport=True, applied_to_replay=False),
                next_root_alignment=dict(source=source, target=target,
                    conjugating_word=transport, positive_factor=by_id['exterior.split.1'],
                    inverse_factor=by_id['pure.next.1'], exact_disk_equality=True,
                    applied_to_replay=False, requires_transport=True),
                complete_named_derivation=False,
                scope='A positive PC lantern leaves six triple curves and twelve pair curves beside the visible exterior twist; their named third-boundary closure is open.')
