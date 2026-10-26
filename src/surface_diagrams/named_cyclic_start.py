"""Delete a standalone commutation by a different actual cyclic square route."""
from dataclasses import replace
from .braid_actions import inverse_word, reduce_word
from .early_boundary_pure import _PositiveReplay, _score
from .factorization_explorer import product
from .mapping_classes import exact_action


def shorten_named_cyclic_start(stages):
    """Replace nine operations by eight, rejoining the same actual Q15 state.

    Start after BOTH the square and its commuting four-point outer. The
    single short-side square drag now includes that commuting neighbor.
    Leave the outer at the bottom until the later Q15 cyclic start. That
    start rejoins the original route, with individual disk presentations
    checked. No source centrality is needed for either conjugation.
    """
    stages = tuple(stages)
    if len(stages) != 81 or stages[23]['title'] != 'Commute the recovered round square to the top':
        raise ValueError('Use the preserved 80-operation named disk tail')
    source = stages[22]['factors']
    if tuple(f.id for f in source[:3]) != ('alternative.O1234','alternative.T12.square','alternative.R2'):
        raise ValueError('The commuting square/outer source changed')
    o,q = source[:2]
    if exact_action(o.word+q.word,5) != exact_action(q.word+o.word,5):
        raise ValueError('The square does not commute with this actual outer')
    r = _PositiveReplay(source)
    before = r.factors; cut = r.position('alternative.R2')
    r.factors = r.check(before[cut:]+before[:cut])
    r.record('Cyclic start after BOTH the square and its commuting outer', 'disk_cyclic_start',
             frame=inverse_word(product(before[:cut])),local_before=before,local_after=r.factors,
             exact_conjugation=True,bypassed_standalone_commutation=stages[23])
    r.drag(q.id,'F11',title='One short-side square drag includes its commuting outer')
    before = r.factors; frame = (4,)
    r.factors = r.check(tuple(r.normalize(replace(f,conjugator=reduce_word(frame+f.conjugator))) for f in before))
    r.record('The same composed sigma4 common frame','global_conjugation',frame=frame,
             local_before=before,local_after=r.factors,exact_conjugation=True)
    r.drag('alternative.F12.1','F10.2',title='Reorder C12 before the matching-half gather')
    r.drag('F11','F6',after=True,title='Gather the final matching original halves')
    r.combine('F6','F11','alternative.P24')
    old_daisy = stages[30]; i = r.position('alternative.F12.2')
    if old_daisy['kind'] != 'disk_pc_daisy':
        raise ValueError('The actual C12 daisy rejoin supplier changed')
    donor = r.factors[i]
    before_match = exact_action(donor.word,5)==exact_action(product(old_daisy['local_before']),5)
    if not before_match:raise ValueError('The cut change altered the actual daisy donor')
    r.substitute(i,1,old_daisy['local_after'],old_daisy['title'],old_daisy['kind'])
    r.stages[-1]['source_stage'] = old_daisy
    r.stages[-1]['actual_donor_match'] = dict(actual=donor,pattern=old_daisy['local_before'][0],exact_disk_equal=True)
    if 'named_pattern_witness' in old_daisy:
        r.stages[-1]['named_pattern_witness'] = old_daisy['named_pattern_witness']
    # The retained source local proof supplies this transported PC daisy;
    # do not silently substitute the normalized donor's different chart.
    if 'framed_balance_before_minus_after' in old_daisy:
        r.stages[-1]['framed_balance_before_minus_after'] = old_daisy['framed_balance_before_minus_after']
    before = r.factors; cut = r.position('alternative.next.2')
    rotated = r.check(before[cut:]+before[:cut])
    rejoin = tuple(stages[31]['factors'])
    matches = tuple(dict(actual=a,pattern=b,exact_disk_equal=a.id==b.id and exact_action(a.word,5)==exact_action(b.word,5))
                    for a,b in zip(rotated,rejoin))
    if len(rotated)!=len(rejoin) or not all(m['exact_disk_equal'] for m in matches):
        raise ValueError('The actual Q15 cyclic start failed to rejoin the old route')
    r.factors = r.check(rejoin)
    r.record('Cyclic start at Q15 REJOINS the unchanged route','disk_cyclic_start',
             frame=inverse_word(product(before[:cut])),local_before=before,local_after=r.factors,
             exact_conjugation=True,cyclic_before_disk_presentations=rotated,
             rejoin_individual_presentations=matches)
    result = stages[:23]+tuple(r.stages[1:])+stages[32:]
    for number,stage in enumerate(result[1:],1):
        before=product(result[number-1]['factors']);after=product(stage['factors'])
        if stage['kind'] in ('disk_cyclic_start','global_conjugation'):
            g=stage['frame'];before=g+before+inverse_word(g)
        if exact_action(before,5)!=exact_action(after,5):
            raise ValueError('A shortened ordered disk transition failed')
    retained=[a for s in result for a in (s,)+s.get('atomic_steps',())]
    peak=max(_score(a['factors'])['max_support_word'] for a in retained)
    interval=[a for s in r.stages for a in (s,)+s.get('atomic_steps',())]
    return dict(stages=result,factors=result[-1]['factors'],graphical_steps=len(result)-1,
        previous_disk_steps=80,previous_whole_named_steps=99,whole_named_steps=98,operations_removed=1,
        source_interval=(22,31),replacement_interval=tuple(r.stages),
        rejoin_individual_presentations=matches,extension_peak_support_word=max(_score(a['factors'])['max_support_word'] for a in interval),
        actual_peak_support_word=peak,adjacent_checks=sum(s.get('adjacent_moves',0) for s in result),
        sphere_moves=0,action_only_boundary_recognitions=0,
        scope='One actual standalone commutation bypassed by a different cyclic cut and square drag. The outer stays at the bottom until Q15 rejoins the unchanged route. Adjacent checks are retained; this is not navigation regrouping.')
