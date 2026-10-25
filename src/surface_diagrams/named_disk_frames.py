"""Equivariant elimination of two unnecessary disk frames in the named proof."""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .early_boundary_pure import _score
from .factorization_explorer import product
from .framed_boundary_relations import enclosed_boundaries
from .mapping_classes import exact_action
from .twist_simplify import simplify_twist


def _transport_factor(factor, frame):
    twist = simplify_twist(replace(factor.mapping_class,
        conjugator=reduce_word(frame + factor.conjugator)), strands=5)
    actual = replace(factor, conjugator=twist.conjugator, first=twist.first)
    if exact_action(actual.word, 5) != exact_action(frame + factor.word + inverse_word(frame), 5):
        raise ValueError('The transported disk presentation changed its supported class')
    return actual


def _transport_stage(source, frame):
    """Transport the actual configuration, retaining the old local proof as source.

    In particular, old canonical-chart words are NOT silently relabeled as
    new ones. The original named witness is retained under source_stage;
    its actual input matches and every neighbor check are transported below.
    """
    if 'sphere' in source['kind']:
        raise ValueError('Disk frame elimination cannot cross a sphere operation')
    stage = {k: source[k] for k in ('kind', 'title', 'adjacent_moves') if k in source}
    stage.update(source_stage=source, common_disk_transport=frame,
                 factors=tuple(_transport_factor(f, frame) for f in source['factors']))
    for key in ('local_before', 'local_after'):
        if key in source: stage[key] = tuple(_transport_factor(f, frame) for f in source[key])
    if source['kind'] in ('global_conjugation', 'disk_cyclic_start'):
        stage['frame'] = reduce_word(frame + source['frame'] + inverse_word(frame))
        stage['exact_conjugation'] = True
    if source.get('atomic_steps'):
        atoms = []
        for old in source['atomic_steps']:
            atom = dict(source_atomic_certificate=old,
                        source=old['source'], target=old['target'],
                        factors=tuple(_transport_factor(f, frame) for f in old['factors']))
            for key in ('local_before', 'local_after'):
                atom[key] = tuple(_transport_factor(f, frame) for f in old[key])
            atoms.append(atom)
        stage['atomic_steps'] = tuple(atoms)
    if source.get('named_pattern_witness'):
        original = source['named_pattern_witness']
        matches = tuple(dict(actual=_transport_factor(m['actual'], frame),
                             pattern=_transport_factor(m['pattern'], frame), exact_disk_equal=True)
                        for m in original.get('individual_matches', ()))
        if any(exact_action(m['actual'].word,5) != exact_action(m['pattern'].word,5) for m in matches):
            raise ValueError('The transported named pattern lost an individual disk match')
        stage['named_pattern_witness'] = dict(source_witness=original,
            common_transport=frame, individual_matches=matches,
            internal_checks_transport_equivariantly=True)
    stage.update(score=_score(stage['factors']), half_twists=sum(f.half for f in stage['factors']))
    if stage['score']['max_support_word'] > 20:
        raise ValueError('The transported named stage exceeds support maximum20')
    if source['kind'] in ('disk_pc_rose', 'disk_pc_daisy', 'disk_cluster_lantern', 'disk_pc_half_lantern'):
        before, after = stage['local_before'], stage['local_after']
        stage['framed_balance_before_minus_after'] = tuple(
            sum(f.power for f in before if i in enclosed_boundaries(f.mapping_class, 5)) -
            sum(f.power for f in after if i in enclosed_boundaries(f.mapping_class, 5))
            for i in range(1, 6))
    return stage


def shorten_named_disk_frames(stages):
    """Replace frames 344 then -4,-3 by4; omit the final rounding frame.

    This changes actual intermediate configurations and deletes TWO actual
    operations. It does not combine unrelated arrows or rename navigation.
    All remaining factors and named patterns are transported equivariantly.
    """
    stages = tuple(stages)
    frames = [i for i, s in enumerate(stages) if s['kind'] == 'global_conjugation']
    if len(stages) != 83 or len(frames) != 5:
        raise ValueError('Use the 82-operation existing-root disk tail')
    i, j, last = frames[0], frames[1], frames[-1]
    if tuple(stages[i]['frame']) != (3, 4, 4) or tuple(stages[j]['frame']) != (-4, -3):
        raise ValueError('The expected two consecutive frame suppliers changed')
    if tuple(stages[last]['frame']) != (-4, -3, -2, -1, -1):
        raise ValueError('The expected final rounding frame changed')
    h = tuple(stages[j]['frame']); undo = inverse_word(tuple(stages[last]['frame']))
    result = list(stages[:i])
    for k in range(i, j):
        new = _transport_stage(stages[k], h)
        if k == i:
            new.update(title='One common sigma4 frame replaces the two old frames',
                frame=reduce_word(h + tuple(stages[i]['frame'])),
                local_before=stages[i - 1]['factors'], local_after=new['factors'])
        result.append(new)
    if result[-1]['factors'] != stages[j]['factors']:
        raise ValueError('The composed-frame interval does not rejoin the unchanged route')
    result.extend(stages[j + 1:last])
    undone = _transport_stage(stages[last], undo)
    omission_matches = tuple(dict(before=a, after=b, exact_disk_equal=exact_action(a.word,5)==exact_action(b.word,5)) for a,b in zip(result[-1]['factors'],undone['factors']))
    if len(undone['factors']) != len(result[-1]['factors']) or not all(m['before'].id==m['after'].id and m['exact_disk_equal'] for m in omission_matches):
        raise ValueError('Omitting the rounding frame changed its source')
    for source in stages[last + 1:]: result.append(_transport_stage(source, undo))
    if result[-1]['factors'] != stages[-1]['factors']:
        raise ValueError('The transported daisies did not retain four standard exteriors')
    for number, stage in enumerate(result[1:], 1):
        before = product(result[number - 1]['factors']); after = product(stage['factors'])
        if stage['kind'] in ('global_conjugation', 'disk_cyclic_start'):
            g = stage['frame']; before = g + before + inverse_word(g)
        if exact_action(before, 5) != exact_action(after, 5):
            raise ValueError('A shortened ordered disk transition failed')
    retained = [a for s in result for a in (s,) + s.get('atomic_steps', ())]
    peak = max(_score(a['factors'])['max_support_word'] for a in retained)
    if peak > 20:
        raise ValueError('An intermediate neighbor check exceeded support maximum20')
    return dict(stages=tuple(result), factors=result[-1]['factors'], graphical_steps=len(result)-1,
                previous_disk_steps=82, operations_removed=2, whole_named_steps=99,
                removed_source_indices=(j, last), combined_frame=(4,),
                omitted_frame_source_presentations=omission_matches,
                first_transported_peak=17, last_transported_peak=12,
                actual_peak_support_word=peak,
                adjacent_checks=sum(s.get('adjacent_moves', 0) for s in result),
                sphere_moves=0, action_only_boundary_recognitions=0,
                scope='Two actual common-frame operations removed by exact equivariance. The actual intermediate curves and named patterns change; all old local witnesses remain explicit source certificates. Four standard exteriors stay visible.')
