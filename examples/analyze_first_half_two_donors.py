"""Audit both actual Q14 donors and a larger first-half lantern target."""
from dataclasses import asdict, replace
from pathlib import Path
import json

from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.disk_intersection import disk_intersection_certificate
from surface_diagrams.early_alternative_transport import _terms, _matches
from surface_diagrams.early_boundary_pure import _PositiveReplay, _score
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.named_disk_frames import _transport_factor
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.projected_relations import pc_half_lantern_terms, pc_rose_terms
from surface_diagrams.sphere_actions import sphere_chain_certificate
from surface_diagrams.six_seven_structure import research_hurwitz_move

ROOT=Path(__file__).resolve().parents[1]


def report():
    c=json.loads((ROOT/'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
    source=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator'])))
                 for f in c['early_alternative_transport']['stages'][11]['factors'])
    by={f.id:f for f in source};q=Factor('target.Q14',(-4,1,2,3),4,2)
    r=_PositiveReplay(source);donors=[]
    for name,prefix in (('alternative.O1234','two.outer.'),('alternative.S1','two.root.')):
        i=r.position(name);outer=r.factors[i];terms=_terms(outer.mapping_class,prefix)
        match=_matches((terms[-1],),(q,))
        r.substitute(i,1,terms,'The actual '+name+' PC daisy lends its Q14','disk_pc_daisy')
        balance=tuple(sum(f.power for f in (outer,) if j in enclosed_boundaries(f.mapping_class,5))-
                      sum(f.power for f in terms if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
        r.stages[-1]['framed_balance_before_minus_after']=balance
        donors.append(dict(source=outer,canonical_terms=terms,actual_Q14_match=match,
                           applied_to_audit=True,applied_to_public_replay=False))
    chosen=('two.outer.3','F3','two.root.2','F9')
    selected=tuple(f for f in r.factors if f.id in chosen)
    if tuple(f.id for f in selected)!=chosen:raise ValueError('The selected actual order changed')
    h=(-4,1,2,3,-2);root=Factor('target.R134',h,3,3)
    half=tuple(Factor('half.pattern.'+str(i),t.conjugator,t.first,t.points,t.power,t.half)
               for i,t in enumerate(pc_half_lantern_terms(root.mapping_class)))
    desired=(by['F3'],by['F9'],replace(q,power=2))
    half_matches=_matches(desired,half)
    if exact_action(product(desired),5)!=exact_action(root.word,5):raise ValueError('The target is not the actual disk half-lantern')
    orders=[]
    for offset in range(4):
        fs=selected[offset:]+selected[:offset];word=product(fs);witness=None
        for f in fs:
            left=exact_action(word+f.word,5);right=exact_action(f.word+word,5)
            if left!=right:
                witness=dict(factor=f,left_images=left,right_images=right,
                    first_different_meridian=next(i for i,(a,b) in enumerate(zip(left,right),1) if a!=b))
                break
        if witness is None:raise ValueError('A cyclic product is not excluded by noncentrality')
        orders.append(dict(offset=offset,factors=fs,product_word=word,witness=witness))
    before_petal_transport=r.factors
    r.drag('F3','two.root.0',title='Carry the SAME original F3 down to the unused12 petal')
    endpoint={f.id:f for f in r.factors}
    target_half_matches=_matches((endpoint['F3'],endpoint['F9']),(by['F3'],by['F9']))
    certificates=[]
    retained=[a for s in r.stages for a in (s,)+tuple(s.get('atomic_steps',()))]
    for s in retained:
        sphere=sphere_chain_certificate(product(s['factors']));lift=homology_action(product(s['factors']))
        if not sphere['certified'] or lift!=IDENTITY:raise ValueError('A retained donor state lost its sphere/lift check')
        certificates.append(dict(sphere_certificate=sphere,chosen_lift=lift))

    # A FULL joint chart, not only the shared14 pair or intersection2.
    g=h+(1,)
    canonical=(Factor('lantern.R345',(),3,3),Factor('lantern.S245',(2,),3,3),Factor('lantern.P23',(),2,2))
    after=(Factor('lantern.O2345',(),2,4),Factor('lantern.Q45',(),4,2))
    if exact_action(product(canonical),5)!=exact_action(product(after),5):raise ValueError('The canonical larger lantern failed')
    actual=tuple(_transport_factor(f,g) for f in canonical);outputs=tuple(_transport_factor(f,g) for f in after)
    root_matches=_matches((root,by['alternative.S1']),actual[:2]);inner_match=_matches((q,),(outputs[1],))
    discrepancy=reduce_word(product(actual)+inverse_word(product(outputs)))
    target_sphere=sphere_chain_certificate(discrepancy);target_lift=homology_action(discrepancy)
    if not target_sphere['certified'] or target_lift!=IDENTITY:raise ValueError('The target discrepancy failed its separate check')
    petal_comparisons=[]
    for f in source:
        if not f.half and f.points>=3:
            unit=replace(f,power=1)
            for j,p in enumerate(_terms(unit.mapping_class,'supplier.')):
                petal_comparisons.append(dict(source_unit=unit,petal_index=j,petal=p,
                    exact_match=exact_action(p.word,5)==exact_action(actual[2].word,5)))
    if any(p['exact_match'] for p in petal_comparisons):raise ValueError('A new direct supplier must be recorded as a target')
    transports=[]
    for donor in (by['alternative.prepare.345.2'],donors[0]['canonical_terms'][1]):
        for sign in (1,-1):
            frame=by['F6'].word if sign==1 else inverse_word(by['F6'].word)
            transported=_transport_factor(donor,frame)
            transports.append(dict(donor=donor,half=by['F6'],sign=sign,transported=transported,
                exact_match=exact_action(transported.word,5)==exact_action(actual[2].word,5),applied=False))
    # The desired P23 is NOW supplied by the actual transported unused12.
    supplied=endpoint['two.root.0'];supplied_match=_matches((supplied,),(actual[2],))
    round12=replace(by['alternative.T12.square'],power=1)
    _matches((donors[1]['canonical_terms'][0],),(round12,))
    # A new fully ordered six-record coupled target follows from the half
    # lantern, the one-interchange S daisy and the cabled lantern. It is not
    # applied to the actual (different) seven-instance selected order.
    canonical_half=tuple(Factor('coupled.half.'+str(i),t.conjugator,t.first,t.points,t.power,t.half)
        for i,t in enumerate(pc_half_lantern_terms(canonical[0].mapping_class)))
    s_daisy=_terms(canonical[1].mapping_class,'coupled.S.')
    s_move=research_hurwitz_move(s_daisy,1,2)
    partial=s_move['factors'][:2];canonical_q=after[1]
    _matches((s_move['factors'][2],),(canonical_q,))
    q_p_commute=research_hurwitz_move((canonical_q,canonical[2]),0,1)
    _matches(q_p_commute['factors'],(canonical[2],canonical_q))
    parent_rose=tuple(Factor('coupled.rose.'+str(i),t.conjugator,t.first,t.points)
        for i,t in enumerate(pc_rose_terms(canonical[0].mapping_class)))
    first_half=replace(parent_rose[0],half=True)
    split_parent=(first_half,replace(first_half,id='coupled.second.half'))+parent_rose[1:]
    half_move1=research_hurwitz_move(split_parent,1,2)
    half_move2=research_hurwitz_move(half_move1['factors'],1,2)
    derived_half=half_move2['factors'][:2]+(replace(half_move2['factors'][2],power=2),)
    _matches(derived_half,canonical_half)
    coupled_canonical=canonical_half+partial+(canonical[2],)
    coupled_actual=(endpoint['F3'],endpoint['F9'],replace(q,power=2),round12,endpoint['two.root.1'],supplied)
    coupled_matches=_matches(coupled_actual,tuple(_transport_factor(f,g) for f in coupled_canonical))
    coupled_discrepancy=reduce_word(product(coupled_actual)+inverse_word(outputs[0].word))
    if exact_action(product(coupled_actual),5)!=exact_action(outputs[0].word,5):raise ValueError('The coupled positive target failed')
    coupled_sphere=sphere_chain_certificate(coupled_discrepancy);coupled_lift=homology_action(coupled_discrepancy)
    if not coupled_sphere['certified'] or coupled_lift!=IDENTITY:raise ValueError('The coupled target lost its separate discrepancy check')
    seven_ids=('two.outer.3','alternative.T12.square','two.root.0','F3','two.root.1','two.root.2','F9')
    seven=tuple(replace(f,power=1) if f.id=='alternative.T12.square' else f for f in r.factors if f.id in seven_ids)
    seven_word=product(seven);seven_witness=None
    for f in seven:
        left=exact_action(seven_word+f.word,5);right=exact_action(f.word+seven_word,5)
        if left!=right:
            seven_witness=dict(factor=f,left_images=left,right_images=right,
                first_different_meridian=next(i for i,(a,b) in enumerate(zip(left,right),1) if a!=b));break
    if seven_witness is None:raise ValueError('The seven-instance order needs a new scoped assessment')
    splits=tuple(dict(factor=f,split=split_fixed_last_strand(f.word,5))
                 for f in selected+(root,)+actual+outputs+coupled_actual)
    for x in splits:
        if exact_action(x['factor'].word,5)!=exact_action(x['split'].reconstructed_word,5):raise ValueError('A full kernel reconstruction failed')
    return dict(source_alternative_stage=11,stages=r.stages,donors=donors,graphical_operations=3,
        adjacent_checks=7,before_score=_score(source),after_score=_score(r.factors),
        state_sphere_lift_certificates=certificates,
        outside_petal_transport=dict(before=before_petal_transport,actual_P23=supplied,
            target_match=supplied_match,original_target_half_matches=target_half_matches,
            round12_source_match=True,reached=True,applied_to_public_replay=False),
        coupled_half_lantern_target=dict(common_chart=g,canonical_inputs=coupled_canonical,
            actual_inputs=coupled_actual,actual_output=outputs[0],individual_matches=coupled_matches,
            half_lantern=canonical_half,half_parent_rose=parent_rose,
            half_parent_retained_moves=(half_move1,half_move2),
            half_parent_full_twist_framing_balance=tuple(sum(f.power for f in parent_rose if j in enclosed_boundaries(f.mapping_class,5))-(j in enclosed_boundaries(canonical[0].mapping_class,5)) for j in range(1,6)),
            S_daisy=s_daisy,retained_S_interchange=s_move,
            retained_inner_pair_commutation=q_p_commute,cabled_lantern_inputs=canonical,
            cabled_lantern_outputs=after,cancelled_common_inner_pair=canonical_q,
            disk_discrepancy=coupled_discrepancy,sphere_certificate=coupled_sphere,
            chosen_lift_discrepancy=coupled_lift,framed_hole_half_twist_convention_asserted=False,
            actual_seven_instances=seven,actual_order_witness=seven_witness,
            actual_prefix_square_split=False,requires_gathering=True,applied=False,
            scope='The desired six records use seven units. The actual seven unchanged instances have a noncentral product, excluding selected-only DISK Hurwitz/common frames. The spare12 unit and all other outside factors, new substitutions and sphere changes remain available.'),
        selected_only_order_obstruction=dict(selected=selected,cyclic_orders=orders,
            excluded=True,scope='Only these four expanded factors under DISK Hurwitz/common conjugation. Unused donor petals, outside transports, other substitutions and sphere changes are NOT excluded.'),
        half_lantern_target=dict(actual_inputs=desired,root=root,canonical=half,
            individual_matches=half_matches,applied=False,requires_gathering=True,
            framed_hole_half_twist_convention_asserted=False),
        next_larger_lantern=dict(common_chart=g,canonical_inputs=canonical,canonical_outputs=after,
            actual_inputs=actual,actual_outputs=outputs,root_matches=root_matches,inner_match=inner_match,
            new_outer_is_source_outer=exact_action(outputs[0].word,5)==exact_action(by['alternative.O1234'].word,5),
            original_outer_commutes_target_root=exact_action(by['alternative.O1234'].word+root.word,5)==exact_action(root.word+by['alternative.O1234'].word,5),
            root_donor_intersection=disk_intersection_certificate(root.mapping_class,by['alternative.S1'].mapping_class,strands=5),
            disk_discrepancy=discrepancy,sphere_certificate=target_sphere,chosen_lift_discrepancy=target_lift,
            framed_balance_before_minus_after=tuple(sum(f.power for f in actual if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in outputs if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6)),
            canonical_supplier_comparisons=petal_comparisons,specific_F6_transports=transports,
            applied=False,requires_half_lantern_gathering=True,requires_actual_P23=False,
            actual_P23_supplied=supplied_match,requires_restored_S1=True),
        complete_point_pushing=splits,selected_product_split=split_fixed_last_strand(product(selected),5),
        sphere_moves=0,exterior_caps=0,
        public_graphical_payloads_changed=False,complete_shorter_derivation=False)


if __name__=='__main__':
    r=report();path=ROOT/'docs/proofs/six-seven-first-half-two-donors.json'
    path.write_text(json.dumps(r,default=asdict,indent=2)+'\n',encoding='utf-8')
    print('Saved',path,'bytes',path.stat().st_size,'endpoint',r['after_score'])
    print('Two donor expansions and one positive petal transport reached; coupled target NOT applied.')
