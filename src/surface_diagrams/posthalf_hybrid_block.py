"""A full bounded, unselected hybrid block candidate with explicit context."""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import Factor, product
from .outside_half_lantern import _matches
from .posthalf_exterior import _cyclic
from .posthalf_outer import _certify
from .six_seven_structure import research_hurwitz_move


def preview_posthalf_hybrid_block(factors):
    """Retain a complete bounded candidate, without selecting a new source.

    The actual old23/I24 block crosses the long side UP. All seven changed
    neighbors are accounted for; matching the desired25 alone is not a
    complete named hybrid payoff.
    """
    source = tuple(factors)
    expected = ('upper.O1234', 'upper.I24', 'alternative.return.0',
                'alternative.return.1', 'alternative.return.2', 'outer.loan.1',
                'outer.loan.2', 'cyclic135.supply.2', 'reflected.exterior',
                'reflected.inner125', 'reflected.output.1', 'posthalf.exterior',
                'reflected.loan.2')
    if tuple(f.id for f in source) != expected or any(f.half or f.power != 1 for f in source):
        raise ValueError('Use the saved reached upper-cabled13-record endpoint')
    r = _PositiveReplay(source)
    r.stages[0]['title'] = 'Reached upper-cabled source before an unselected block candidate'
    previews = []

    def move(name, target, title):
        a, b = r.position(name), r.position(target)
        raw = research_hurwitz_move(r.factors, a, b)
        score = _score(raw['factors'])
        if score['max_support_word'] > 20:
            raise ValueError('Reject the FULL candidate before selecting any prefix')
        previews.append(dict(moving=name, crossed=target, raw_move=raw, score=score))
        r.drag(name, target, title=title)
        _matches(raw['factors'], r.factors)

    _cyclic(r, 'reflected.loan.2')
    move('upper.O1234', 'reflected.loan.2',
         'Commute the SAME standard outer UP once to gather the actual old23/I24 block')
    _cyclic(r, 'alternative.return.0')
    names = ('reflected.loan.2', 'upper.I24')
    crossed = []
    while r.factors[r.position(names[0]) - 1].id != 'outer.loan.1':
        neighbor = r.factors[r.position(names[0]) - 1].id
        crossed.append(neighbor)
        for name in names:
            move(name, neighbor, 'Candidate: SAME ' + name + ' UP across ' + neighbor)
    if tuple(crossed) != ('upper.O1234', 'posthalf.exterior', 'reflected.output.1',
                          'reflected.inner125', 'reflected.exterior',
                          'cyclic135.supply.2', 'outer.loan.2'):
        raise ValueError('Retain the exact seven-neighbor context')
    before, after = {f.id: f for f in source}, {f.id: f for f in r.factors}
    actors = tuple(before[n] for n in names)
    if tuple(after[n] for n in names) != actors:
        raise ValueError('Both actual block actors must stay literally fixed')
    frame = inverse_word(product(actors))
    conjugations = []
    for name in crossed:
        f = before[name]
        raw = replace(f, conjugator=reduce_word(frame + f.conjugator))
        conjugations.append(dict(source=f, raw_target=raw, actual=after[name],
                                 individual_match=_matches((after[name],), (raw,))))
    needed = Factor('target.required25', (-2, -3), 4, 2)
    required_match = _matches((after['outer.loan.2'],), (needed,))
    changed = tuple(name for name in before if before[name] != after[name])
    if set(changed) != {'outer.loan.2', 'cyclic135.supply.2',
                       'reflected.inner125', 'reflected.output.1'}:
        raise ValueError('Retain all four changed curves; no other curve may change')
    result = _certify(r)
    result.update(selected=False, complete_bounded_candidate=True,
                  applied_to_selected_research_source=False,
                  preapplication_previews=tuple(previews), actual_ordered_actors=actors,
                  crossed_neighbors=tuple(crossed), full_block_conjugation_matches=tuple(conjugations),
                  required25_match=required_match, changed_record_ids=changed,
                  named_substitutions=0,
                  scope='Full17-operation/15-adjacent-check bounded candidate only. '
                        'Both cyclic starts retain complete raw common conjugations; '
                        'every adjacent move is reconstructed before normalized presentations. '
                        'The actual25 class matches the precise target, but other neighbors '
                        'change and no useful named hybrid payoff or complete join is reached. '
                        'No candidate prefix is adopted as a new selected source. '
                        'Both unit exteriors remain literal and visible; no half, negative '
                        'factor, sphere redraw or cap. Preferred101/71 unchanged.')
    return result
