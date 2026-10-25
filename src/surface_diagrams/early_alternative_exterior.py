"""A reached second exterior lantern on the alternative positive disk route."""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .early_alternative_transport import _matches, _terms
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries
from .mapping_classes import exact_action
from .point_pushing import split_fixed_last_strand


def expose_second_alternative_exterior(factors):
    """Lend a round124 root, transport it, then apply its actual lantern.

    The common lantern chart is constructed from a retained NONABELIAN
    point-pushing loop. It is not inferred from the three intersection
    counts. All eight moves are positive disk operations; no cap occurs.
    """
    source = tuple(factors)
    r = _PositiveReplay(source)
    if source[0] != Factor('alternative.inside.D4', (), 1, 4) or len(source) != 13:
        raise ValueError('Use the saved operation51 alternative endpoint')
    x = source[r.position('alternative.shared.O2345')]
    y = source[r.position('alternative.F12.1')]
    q = source[r.position('alternative.return.2')]
    # Standardize X and the common35 petal to D4 and D12. The exact
    # last-strand split then identifies the missing block winding.
    source_chart = reduce_word(x.conjugator + (-3, 1, 2))
    canonical_y = Factor('pattern.Y125', (-4, -3), 1, 3)
    normalized_y = replace(y, conjugator=reduce_word(inverse_word(source_chart) + y.conjugator))
    actual_split = split_fixed_last_strand(normalized_y.word, 5)
    canonical_split = split_fixed_last_strand(canonical_y.word, 5)
    d12, d34, d4 = Factor('pattern.D12', (), 1, 2), Factor('pattern.D34', (), 3, 2), Factor('pattern.D4', (), 1, 4)
    block_frame = reduce_word(d12.word + d34.word + inverse_word(d4.word))
    transported_y = replace(canonical_y, conjugator=reduce_word(block_frame + canonical_y.conjugator))
    transported_split = split_fixed_last_strand(transported_y.word, 5)
    if actual_split.kernel_loop != (-4, -3, 1, 2, 3, 4) or canonical_split.kernel_loop != (1, 2):
        raise ValueError('The local nonabelian winding no longer matches the saved chart')
    if actual_split.kernel_loop != transported_split.kernel_loop or exact_action(actual_split.shadow_word, 4) != exact_action(transported_split.shadow_word, 4):
        raise ValueError('The block frame did not reconstruct the full disk braid')
    _matches((normalized_y,), (transported_y,))
    for curve in (d12, d34, d4):
        _matches((replace(curve, conjugator=block_frame),), (curve,))
    frame0 = reduce_word(source_chart + block_frame)
    # X Z Y = exterior D12 D34; the other third curve Z'=Y^-1 Z Y
    # gives X Y Z'. The actual round124 donor becomes exactly this Z'.
    canonical = (d4, canonical_y, Factor('pattern.Zprime', inverse_word(canonical_y.word), 3, 3))
    canonical_after = (Factor('pattern.exterior', (), 1, 5), d12, d34)
    if exact_action(product(canonical), 5) != exact_action(product(canonical_after), 5):
        raise ValueError('The canonical cabled exterior lantern failed')
    source_target = replace(canonical[2], conjugator=reduce_word(frame0 + canonical[2].conjugator))
    donor = Factor('pattern.round124', (-3,), 1, 3)
    donor_target_match = _matches((replace(donor, conjugator=reduce_word(q.word + donor.conjugator)),), (source_target,))
    _matches((x, y), tuple(replace(a, conjugator=reduce_word(frame0 + a.conjugator)) for a in canonical[:2]))

    # This five-letter common chart keeps all retained states within16;
    # the unframed short-side gather reaches38.
    h = (2, 3, 4, -2, -1)
    before = r.factors
    r.factors = r.check(tuple(r.normalize(replace(a, conjugator=reduce_word(h + a.conjugator))) for a in before))
    r.record('Common disk frame keeps the second exterior lantern readable', 'global_conjugation',
             frame=h, local_before=before, local_after=r.factors, exact_conjugation=True)
    terms = tuple(r.normalize(a) for a in _terms(Factor('pattern.loan.D4', h + (-3,), 1, 4).mapping_class, 'alternative.second.loan.'))
    r.substitute(0, 1, terms, 'The four-point PC daisy lends its actual three-point root', 'disk_pc_daisy')
    before = r.factors
    r.factors = r.check(before[-1:] + before[:-1])
    r.record('Cyclic start at the actual pair that transports the borrowed root', 'disk_cyclic_start',
             frame=before[-1].word, local_before=before, local_after=r.factors, exact_conjugation=True)
    r.drag(q.id, terms[0].id, title='The actual pair carries the borrowed root to the exact missing class')
    r.drag(y.id, 'alternative.P13', title='Bring the three-point curve up across one neighboring pair')
    before = r.factors
    index = r.position(x.id)
    tail = before[index:]
    r.factors = r.check(tail + before[:index])
    r.record('Cyclic start at the matched four-point curve', 'disk_cyclic_start',
             frame=product(tail), local_before=before, local_after=r.factors, exact_conjugation=True)
    r.drag(terms[0].id, y.id, after=True, title='Gather the borrowed root up the four-neighbor short side')
    frame = reduce_word(h + frame0)
    pattern = tuple(replace(a, conjugator=reduce_word(frame + a.conjugator)) for a in canonical)
    index = r.position(x.id)
    matches = _matches(r.factors[index:index + 3], pattern)
    raw_after = (Factor('alternative.second.exterior', (), 1, 5),
                 Factor('alternative.second.I35', frame, 1, 2), Factor('alternative.second.I24', frame, 3, 2))
    after = tuple(r.normalize(a) for a in raw_after)
    r.substitute(index, 3, after, 'Cabled PC lantern reaches a SECOND visible exterior twist', 'disk_cluster_lantern')
    r.stages[-1]['named_pattern_witness'] = dict(frame=frame, canonical=canonical, canonical_after=canonical_after,
        individual_matches=matches, raw_after=raw_after, presentation_matches=_matches(raw_after, after),
        source_chart=source_chart, block_frame=block_frame, block_frame_decomposition=(d12.word, d34.word, inverse_word(d4.word)),
        normalized_y_split=actual_split, canonical_y_split=canonical_split, transported_y_split=transported_split,
        donor_target_match=donor_target_match, exact_disk_equality=True)
    for stage in r.stages:
        if stage['kind'] in ('disk_pc_daisy', 'disk_cluster_lantern'):
            sets = [[(a.power, enclosed_boundaries(a.mapping_class, 5)) for a in stage[key]] for key in ('local_before', 'local_after')]
            stage['framed_balance_before_minus_after'] = tuple(sum(p for p, b in sets[0] if i in b) - sum(p for p, b in sets[1] if i in b) for i in range(1, 6))
    retained = [z['factors'] for s in r.stages for z in (s,) + s.get('atomic_steps', ())]
    return dict(stages=tuple(r.stages), factors=r.factors, graphical_steps=len(r.stages) - 1,
                adjacent_checks=sum(s.get('adjacent_moves', 0) for s in r.stages),
                actual_peak_support_word=max(_score(fs)['max_support_word'] for fs in retained),
                before_score=_score(source), after_score=_score(r.factors), sphere_move_count=0,
                explicit_exterior_twists=2, exterior_caps=0, all_factors_positive=True,
                source_step=51, combined_research_steps=59, remaining_boundary_power=2,
                replacement_for_full_proof=False, applied_to_public_replay=False,
                scope='Reached second exterior lantern in eight positive disk operations. Both exterior twists remain visible; this is not a shorter complete proof or an overall intersection reduction.')