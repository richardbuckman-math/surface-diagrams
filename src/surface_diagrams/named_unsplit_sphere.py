"""Apply the first sphere lantern directly to F1 squared and two half twists."""
from dataclasses import replace
from .braid_actions import inverse_word,reduce_word
from .factorization_explorer import Factor,product,split_factor,move_factor
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action,supported_class
from .six_seven_structure import research_hurwitz_move
from .point_pushing import split_fixed_last_strand
from .sphere_actions import sphere_chain_certificate


def unsplit_sphere_lantern(chart=()):
    """C^2 (C^-1 H C) H = T12 T56 on the six-marked sphere.

    This accepts the separating square and the two DISTINCT half twists.
    The supporting full-twist PC lantern and its framing balance are retained;
    no half-twist convention on framed holes is asserted.
    """
    g=tuple(chart);c=Factor('lantern.C',(),1,3);h=Factor('lantern.H',(),3,2,half=True)
    canonical=(replace(c,power=2),replace(h,id='lantern.C^-1(H)',conjugator=inverse_word(c.word)),h)
    full_parent=(c,replace(h,half=False),replace(c,conjugator=inverse_word(h.word)))
    disk_outputs=(Factor('lantern.I12',(),1,2),Factor('lantern.O1234',(),1,4))
    sphere_outputs=(disk_outputs[0],Factor('lantern.P56',(),5,2))
    free=reduce_word(product(canonical)+inverse_word(product(full_parent)))
    if free or exact_action(product(full_parent),6)!=exact_action(product(disk_outputs),6):
        raise ValueError('The direct lantern lost its free-word reduction or PC parent')
    def framed(fs):return tuple(replace(f,conjugator=reduce_word(g+f.conjugator)) for f in fs)
    inputs=framed(canonical);outputs=framed(sphere_outputs);parent=framed(full_parent);disk=framed(disk_outputs)
    discrepancy=reduce_word(product(inputs)+inverse_word(product(outputs)))
    sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    complement=reduce_word(disk[1].word+inverse_word(outputs[1].word))
    cs=sphere_chain_certificate(complement);cl=homology_action(complement)
    if not sphere['certified'] or lift!=IDENTITY or not cs['certified'] or cl!=IDENTITY:
        raise ValueError('The direct sphere lantern changed its chosen lift')
    balance=tuple(sum(f.power for f in parent if j in enclosed_boundaries(f.mapping_class,6))-
                  sum(f.power for f in disk if j in enclosed_boundaries(f.mapping_class,6)) for j in range(1,7))
    return dict(common_chart=g,canonical_inputs=canonical,inputs=inputs,outputs=outputs,
        full_twist_PC_parent=parent,parent_disk_outputs=disk,parent_free_word_discrepancy=free,
        parent_signed_framing_balance=balance,framed_hole_half_twist_convention_asserted=False,
        disk_discrepancy=discrepancy,sphere_certificate=sphere,chosen_lift_discrepancy=lift,
        complement_disk_discrepancy=complement,complement_sphere_certificate=cs,complement_chosen_lift=cl,
        source_centrality_assumed=False,exterior_caps=0)


def shorten_unsplit_first_lantern(stages):
    """Fourteen early operations replace seventeen, with a literal old14 join."""
    stages=tuple(stages)
    if len(stages)!=18 or stages[14]['kind']!='sphere_rewrite' or stages[17]['kind']!='sphere_rewrite':
        raise ValueError('Use the retained first17 operations of the complete source')
    source=stages[0]['factors'];r=list(stages[:3]);state=stages[2]['factors'];expected=exact_action(product(source),6)
    def position(name):return next(i for i,f in enumerate(state) if f.id==name)
    def record(title,kind,**kw):
        if exact_action(product(state),6)!=expected:raise ValueError('A pre-lantern disk transport changed its product')
        r.append(dict(title=title,kind=kind,factors=state,**kw))
    for name in ('F8','F10'):
        i=position(name);before=(state[i],);state=split_factor(state,i,'powers')
        record('Split '+name+' into ordinary roots','disk_split',local_before=before,local_after=state[i:i+2])
    def adjacent(name,target):
        nonlocal state
        i,j=position(name),position(target)
        if abs(i-j)!=1:raise ValueError('The direct early move is not adjacent')
        raw=research_hurwitz_move(state,i,j);state=move_factor(state,i,j)
        matches=tuple(exact_action(a.word,6)==exact_action(b.word,6) for a,b in zip(raw['factors'],state))
        if not all(matches):raise ValueError('An early disk normalization lost its raw factor match')
        return dict(raw,factors=state,raw_factors=raw['factors'],individual_presentation_matches=matches)
    for name,target in (('F8.1','F7'),('F10.1','F9'),('F10.1','F8.2'),('F10.1','F7')):
        a=adjacent(name,target);record(name+' up past '+target,'disk_hurwitz',source=a['source'],target=a['target'],atomic_steps=(a,))
    d=stages[11]['local_after'][0];i=position('F7');old=state[i]
    if exact_action(old.word,6)!=exact_action(d.word,6):raise ValueError('The transported actual F7 no longer matches its checked arc')
    state=state[:i]+(d,)+state[i+1:]
    record('Use the exact disk presentation of the transported F7 arc','disk_rewrite',local_before=(old,),local_after=(d,))
    atom=[]
    while position(d.id)>2:
        i=position(d.id);atom.append(adjacent(d.id,state[i-1].id))
    if len(atom)!=6:raise ValueError('The unsplit source changed the six-neighbor gather')
    record('Carry F7 up through SIX factors; keep the original F1 square intact','disk_hurwitz_block',adjacent_moves=6,atomic_steps=tuple(atom))
    before=state[:3];after=stages[14]['local_after'];g=after[0].conjugator;pattern=unsplit_sphere_lantern(g)
    matches=tuple(dict(actual=a,pattern=b,exact_disk_equal=exact_action(a.word,6)==exact_action(b.word,6)) for a,b in zip(before,pattern['inputs']))
    outputs=tuple(dict(actual=a,pattern=b,exact_disk_equal=exact_action(a.word,6)==exact_action(b.word,6)) for a,b in zip(after,pattern['outputs']))
    if len(before)!=3 or not all(x['exact_disk_equal'] for x in matches+outputs):raise ValueError('The actual direct lantern input/output match failed')
    discrepancy=reduce_word(product(before)+inverse_word(product(after)))
    sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('The actual direct lantern changed its lifted sphere action')
    splits=tuple(dict(factor=f,split=split_fixed_last_strand(f.word,6)) for f in before+tuple(after))
    for row in splits:
        if exact_action(row['factor'].word,6)!=exact_action(row['split'].reconstructed_word,6):raise ValueError('The direct lantern lost a full nonabelian reconstruction')
    state=tuple(after)+state[3:]
    if state!=stages[14]['factors']:raise ValueError('The direct lantern failed its LITERAL old14 join')
    r.append(dict(title='SPHERE LANTERN: keep F1 squared; absorb the two distinct actual half twists',kind='sphere_rewrite',factors=state,
        local_before=before,local_after=after,disk_discrepancy=discrepancy,sphere_certificate=sphere,lift_homology=lift,
        named_pattern_witness=dict(unsplit_sphere_lantern=pattern,individual_matches=matches,output_matches=outputs,
            complete_actual_point_pushing=splits,old_prefix_disk_product_equal=exact_action(product(before),6)==exact_action(product(stages[13]['factors'][:3]),6))))
    result=tuple(r)+stages[15:];retained=[a for s in r for a in (s,)+tuple(s.get('atomic_steps',()))]
    certificates=[]
    for s in retained:
        sp=sphere_chain_certificate(product(s['factors']));li=homology_action(product(s['factors']))
        if not sp['certified'] or li!=IDENTITY:raise ValueError('A retained early state lost its sphere/lift certificate')
        certificates.append(dict(sphere_certificate=sp,chosen_lift=li))
    def peak(ss):return max(len(supported_class(f.mapping_class,6)) for s in ss for f in s['factors'])
    for s in result[3:11]:
        f=next(f for f in s['factors'] if f.id=='F1')
        if f!=source[0]:raise ValueError('The original separating square was changed or split')
    return dict(stages=result,factors=result[-1]['factors'],graphical_steps=14,previous_graphical_steps=17,
        previous_whole_named_steps=82,whole_named_steps=79,operations_removed=3,literal_rejoin=True,
        old_join_stage=14,new_join_stage=11,original_F1_square_unsplit=True,actual_target_halves_distinct=exact_action(before[1].word,6)!=exact_action(before[2].word,6),
        old_prefix_adjacent_checks=14,new_prefix_adjacent_checks=12,changed_prefix_peak_support_word=peak(retained),
        previous_prefix_peak_support_word=peak(stages[:15]),state_sphere_lift_certificates=tuple(certificates),
        sphere_moves_added=0,exterior_caps_added=0,framed_hole_half_twist_convention_asserted=False,
        scope='Keep the original separating square intact. The transported F7 remains distinct from F2; a direct actual sphere lantern consumes both. No F1 split, C1 preconditioning, or matched-half combine occurs. The complete factor tuple rejoins old14 literally after11 operations.')
