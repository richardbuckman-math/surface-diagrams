"""Merge the positive T45 frame into the preceding exterior-lantern chart."""
from dataclasses import replace
from .braid_actions import inverse_word,reduce_word
from .early_boundary_pure import _score
from .early_alternative_transport import _matches
from .factorization_explorer import Factor,product
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action
from .named_disk_frames import _transport_factor,_transport_stage
from .point_pushing import split_fixed_last_strand
from .projected_relations import pc_daisy_terms
from .sphere_actions import sphere_chain_certificate


def _raw_transport(factors,frame):
    return tuple(replace(f,conjugator=reduce_word(frame+f.conjugator)) for f in factors)


def merge_positive_T45_frame(stages):
    """One actual frame disappears; eight actual configurations change.

    The preceding lantern, its loan and every adjacent check are transported
    by the positive T45. Source charts/certificates stay explicitly SOURCE;
    the later fourteen-operation closure itself is not redefined.
    """
    stages=tuple(stages);first,last=50,58
    if len(stages)!=72 or tuple(stages[first].get('frame',()))!=(2,3,4,-2,-1) or tuple(stages[last].get('frame',()))!=(4,4):
        raise ValueError('Use the preserved71-operation upward-daisy disk tail')
    frame=tuple(stages[last]['frame']);composed=reduce_word(frame+stages[first]['frame'])
    if frame!=Factor('actual.T45',(),4,2).word:raise ValueError('The final frame must be the actual positive T45')
    changed=[]
    for index in range(first,last):
        source=stages[index];stage=_transport_stage(source,frame)
        raw=_raw_transport(source['factors'],frame)
        stage['transported_presentations']=_matches(stage['factors'],raw)
        if index==first:
            stage.update(title='ONE positive T45 lantern chart replaces the two former frames',
                frame=composed,local_before=stages[first-1]['factors'],local_after=stage['factors'])
        elif source['kind']=='disk_cyclic_start':
            raw_before=_raw_transport(source['local_before'],frame)
            raw_after=_raw_transport(source['local_after'],frame)
            if reduce_word(stage['frame']+product(raw_before)+inverse_word(stage['frame']))!=reduce_word(product(raw_after)):
                raise ValueError('A transported raw cyclic start failed before presentation changes')
            stage['raw_cyclic_certificate']=dict(frame=stage['frame'],local_before=raw_before,local_after=raw_after,
                exact_free_word_conjugation=True,individual_after_presentations=_matches(stage['factors'],raw_after))
        for atom,old in zip(stage.get('atomic_steps',()),source.get('atomic_steps',())):
            before=_raw_transport(old['local_before'],frame);after=_raw_transport(old['local_after'],frame)
            if reduce_word(product(before))!=reduce_word(product(after)):
                raise ValueError('A transported adjacent check lost its raw free-word equality')
            atom.update(raw_local_before=before,raw_local_after=after,exact_raw_free_word_equality=True,
                transported_presentations=_matches(atom['factors'],_raw_transport(old['factors'],frame)))
        if source['kind']=='disk_pc_daisy':
            canonical_outer=Factor('pattern.D4',(),1,4)
            terms=tuple(Factor('pattern.daisy.'+str(i),t.conjugator,t.first,t.points)
                for i,t in enumerate(pc_daisy_terms(canonical_outer.mapping_class)))
            chart=reduce_word(frame+stages[first]['frame']+(-3,))
            pattern=tuple(_transport_factor(f,chart) for f in terms)
            outer=_transport_factor(canonical_outer,chart)
            stage['named_pattern_witness']=dict(source_stage=source,canonical_outer=canonical_outer,
                canonical_terms=terms,common_chart=chart,
                outer_match=_matches(stage['local_before'],(outer,)),
                individual_matches=_matches(stage['local_after'],pattern),every_actual_input_matched=True)
        elif source['kind']=='disk_cluster_lantern':
            old=source['named_pattern_witness'];chart=reduce_word(frame+old['frame'])
            normalized=tuple(_transport_factor(f,inverse_word(chart)) for f in stage['local_before'])
            canonical=old['canonical'];splits=tuple(split_fixed_last_strand(f.word,5) for f in normalized)
            canonical_splits=tuple(split_fixed_last_strand(f.word,5) for f in canonical)
            for actual,split,expected in zip(normalized,splits,canonical_splits):
                if exact_action(split.reconstructed_word,5)!=exact_action(actual.word,5) or split.kernel_loop!=expected.kernel_loop or exact_action(split.shadow_word,4)!=exact_action(expected.shadow_word,4):
                    raise ValueError('The actual lantern lost its full normalized kernel/shadow')
            stage['named_pattern_witness'].update(common_chart=chart,normalized_actual=normalized,
                normalized_actual_splits=splits,canonical_splits=canonical_splits,
                canonical_matches=_matches(normalized,canonical),
                output_presentation_matches=_matches(stage['local_after'],tuple(_transport_factor(f,frame) for f in old['raw_after'])),
                every_actual_input_matched=True)
        if source['kind'] in ('disk_pc_daisy','disk_cluster_lantern'):
            discrepancy=reduce_word(product(stage['local_before'])+inverse_word(product(stage['local_after'])))
            sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
            if not sphere['certified'] or lift!=IDENTITY:raise ValueError('A transformed named relation lost its separate sphere/lift check')
            stage['named_pattern_witness'].update(disk_discrepancy=discrepancy,
                sphere_certificate=sphere,chosen_lift_discrepancy=lift)
        changed.append(stage)
    if changed[-1]['factors']!=stages[last]['factors']:
        raise ValueError('The positive-frame merge failed its literal later join')
    retained=[a for s in changed for a in (s,)+s.get('atomic_steps',())];certificates=[]
    for s in retained:
        sphere=sphere_chain_certificate(product(s['factors']));lift=homology_action(product(s['factors']))
        if not sphere['certified'] or lift!=IDENTITY:raise ValueError('A retained positive-frame state lost its sphere/lift check')
        certificates.append(dict(sphere_certificate=sphere,chosen_lift=lift))
    result=stages[:first]+tuple(changed)+stages[last+1:]
    for i,s in enumerate(result[1:],1):
        before=product(result[i-1]['factors']);after=product(s['factors'])
        if s['kind'] in ('global_conjugation','disk_cyclic_start'):
            g=s['frame'];before=g+before+inverse_word(g)
        if exact_action(before,5)!=exact_action(after,5):raise ValueError('The shortened disk tail lost an ordered transition')
    all_retained=[a for s in result for a in (s,)+s.get('atomic_steps',())]
    return dict(stages=result,factors=result[-1]['factors'],graphical_steps=len(result)-1,
        previous_whole_named_steps=90,whole_named_steps=89,operations_removed=1,
        source_interval=(first,last),removed_source_index=last,composed_frame=composed,
        changed_states=len(changed),changed_retained_states=len(retained),literal_rejoin=True,
        changed_peak_support_word=max(_score(a['factors'])['max_support_word'] for a in retained),
        actual_peak_support_word=max(_score(a['factors'])['max_support_word'] for a in all_retained),
        adjacent_checks=sum(s.get('adjacent_moves',0) for s in result),
        previous_adjacent_checks=sum(s.get('adjacent_moves',0) for s in stages),
        changed_state_sphere_lift_certificates=tuple(certificates),sphere_moves=0,
        exterior_caps=0,action_only_boundary_recognitions=0,
        scope='One actual positive T45 frame is merged into the preceding exterior-lantern frame. Eight actual configurations and all named inputs change equivariantly, then rejoin literally; all adjacent and sphere/lift checks remain.')
