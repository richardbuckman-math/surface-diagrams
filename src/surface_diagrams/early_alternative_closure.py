"""Close the reached second-exterior branch by a returned rose and two daisies.

All 23 operations are positive disk moves. The four final exteriors remain
visible. Every named pattern retains each actual input match and all of its
internal Hurwitz interchanges; no whole-product boundary recognition is used.
"""
from dataclasses import replace
from .braid_actions import reduce_word, inverse_word
from .early_alternative_transport import _matches
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .mapping_classes import exact_action
from .projected_relations import pc_rose_terms, pc_daisy_terms
from .six_seven_structure import research_hurwitz_move

def close_alternative_boundary(factors):
    """Return the borrowed root, align the two outers and close their petals.

    The first five moves return the ACTUAL transported loan, not an
    untransported curve with the same enclosed points. Seven further moves
    align the outers. Three explicit petal swaps and two individually
    matched transported daisies finish the positive fourth-boundary relation.
    """
    source = tuple(factors)
    if len(source) != 16 or tuple((f.id for f in source[:3])) != ('alternative.second.exterior', 'alternative.second.I35', 'alternative.second.I24'):
        raise ValueError('Use the reached second-exterior alternative endpoint')
    # Return the transported loan by the actual rose, then close its daisy.
    r = _PositiveReplay(source)
    q = r.factors[r.position('alternative.return.2')]
    h = (2, 3, 4, -2, -1)
    z = r.normalize(Factor('alternative.returned.R145', reduce_word(q.word + h + (-3,)), 1, 3))
    r.drag('alternative.residual.I12', 'alternative.P13', after=True)
    b = r.factors[r.position('alternative.residual.I12')]
    pattern = tuple((Factor('pattern.rose.' + str(i), reduce_word(inverse_word(b.word) + t.conjugator), t.first, t.points) for i, t in enumerate(pc_rose_terms(z.mapping_class))))
    moved = research_hurwitz_move(pattern, 0, 1)
    i = r.position('alternative.second.I24')
    matches = _matches(r.factors[i:i + 3], moved['factors'])
    r.substitute(i, 3, (z,), 'A transported PC rose returns the actual borrowed root', 'disk_pc_rose')
    r.stages[-1]['named_pattern_witness'] = dict(canonical=pattern, retained_interchanges=(moved,), individual_matches=matches)
    r.drag(q.id, 'alternative.second.loan.3')
    r.drag(z.id, 'alternative.residual.O1234')
    chart = reduce_word(q.word + h + (-3,))
    pattern = pc_daisy_terms(Factor('pattern.returned.D4', chart, 1, 4).mapping_class)
    i = r.position(z.id)
    matches = _matches(r.factors[i:i + 4], pattern)
    out = r.normalize(Factor('alternative.returned.N', reduce_word(q.word + h), 1, 4))
    r.substitute(i, 4, (out,), 'Close the actual returned PC daisy', 'disk_pc_daisy')
    r.stages[-1]['named_pattern_witness'] = dict(frame=chart, individual_matches=matches, exact_disk_equality=True)
    # The TWO-factor transport B A aligns O with N; one pair is insufficient.
    a = r.factors[r.position('alternative.second.I35')]
    b = r.factors[r.position('alternative.return.2')]
    o = r.factors[r.position('alternative.residual.O1234')]
    n = r.factors[r.position('alternative.returned.N')]
    k = b.word + a.word
    _matches((replace(o, conjugator=reduce_word(k + o.conjugator)),), (n,))
    before = r.factors
    i = r.position(b.id)
    tail = before[i:]
    r.factors = r.check(tail + before[:i])
    r.record('Cyclic start at the two-petal alignment supplier', 'disk_cyclic_start', frame=inverse_word(product(before[:i])), local_before=before, local_after=r.factors, exact_conjugation=True)
    r.drag(b.id, 'alternative.second.exterior')
    r.drag(a.id, o.id)
    r.drag(b.id, o.id)
    r.drag(n.id, o.id, after=True)
    r.combine(o.id, n.id, 'closure.D4.square')
    h = inverse_word((1, 1, 2, 3, 4))
    before = r.factors
    r.factors = r.check(tuple((r.normalize(replace(x, conjugator=reduce_word(h + x.conjugator))) for x in before)))
    r.record('Common disk frame rounds the actual four-point square', 'global_conjugation', frame=h, local_before=before, local_after=r.factors)
    # Keep the three actual noncentral petal interchanges as separate moves.
    r.split('alternative.T12.square', 'closure.E1', 'closure.E2')
    r.drag('alternative.shared.I25', 'closure.E1')
    r.drag('closure.E1', 'alternative.P24')
    r.drag('alternative.P24', 'closure.E1')
    r.drag('alternative.shared.1', 'alternative.shared.2')
    before = r.factors
    i = r.position('closure.D4.square')
    tail = before[i:]
    r.factors = r.check(tail + before[:i])
    r.record('Cyclic start at the round four-point square', 'disk_cyclic_start', frame=inverse_word(product(before[:i])), local_before=before, local_after=r.factors, exact_conjugation=True)
    r.split('closure.D4.square', 'closure.U', 'closure.V')
    r.drag('closure.U', 'alternative.second.I35')
    r.drag('closure.U', 'closure.E1')
    # Derive both ordered daisy patterns by retained internal Hurwitz moves.
    canonical = tuple((Factor('pattern.daisy.' + str(i), t.conjugator, t.first, t.points) for i, t in enumerate(pc_daisy_terms(Factor('pattern.exterior', (), 1, 5).mapping_class))))
    changed = canonical
    checks = []
    for src, dst in ((1, 2), (1, 2), (4, 3)):
        m = research_hurwitz_move(changed, src, dst)
        checks.append(m)
        changed = m['factors']
    i = r.position('closure.U')
    actual = r.factors[i:i + 5]
    matches = _matches(actual, changed)
    r.substitute(i, 5, (Factor('closure.exterior.3', (), 1, 5),), 'First actual transported five-point PC daisy', 'disk_pc_daisy')
    r.stages[-1]['named_pattern_witness'] = dict(canonical=canonical, retained_interchanges=tuple(checks), individual_matches=matches)
    for twice in range(2):
        for src, dst in ((2, 1), (3, 2), (4, 3)):
            m = research_hurwitz_move(changed, src, dst)
            checks.append(m)
            changed = m['factors']
    actual = r.factors[:5]
    matches = _matches(actual, changed)
    r.substitute(0, 5, (Factor('closure.exterior.4', (), 1, 5),), 'Second actual transported five-point PC daisy', 'disk_pc_daisy')
    r.stages[-1]['named_pattern_witness'] = dict(canonical=canonical, retained_interchanges=tuple(checks), individual_matches=matches)
    for stage in r.stages:
        if stage['kind'] in ('disk_pc_rose', 'disk_pc_daisy'):
            groups = [[(f.power, enclosed_boundaries(f.mapping_class, 5)) for f in stage[key]] for key in ('local_before', 'local_after')]
            stage['framed_balance_before_minus_after'] = tuple((sum((p for p, b in groups[0] if i in b)) - sum((p for p, b in groups[1] if i in b)) for i in range(1, 6)))
    retained = [a['factors'] for s in r.stages for a in (s,) + s.get('atomic_steps', ())]
    if len(r.stages) != 24 or len(r.factors) != 4 or any((f.points != 5 or f.power != 1 or f.conjugator for f in r.factors)):
        raise ValueError('The named closure did not reach four identical visible exteriors')
    r.stages[0]['title'] = 'The reached second-exterior endpoint, with both exterior twists visible'
    return dict(stages=tuple(r.stages), factors=r.factors, graphical_steps=23, adjacent_checks=sum((s.get('adjacent_moves', 0) for s in r.stages)), actual_peak_support_word=max((_score(fs)['max_support_word'] for fs in retained)), before_score=_score(source), after_score=_score(r.factors), complete_named_boundary_derivation=True, action_only_boundary_recognitions=0, sphere_move_count=0, exterior_caps=0, explicit_exterior_twists=4, source_research_steps=59, complete_join_steps=101, scope='A complete positive named disk closure of the existing-root branch. Four exterior twists remain visible; the full route combines them and separately performs its labeled fourth-power sphere cap.')
