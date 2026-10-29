"""PC lantern for two two-point clusters and one marked point; no replay edit."""
from .braid_actions import inverse_word,reduce_word
from .factorization_explorer import Factor,product
from .framed_boundary_relations import enclosed_boundaries
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action
from .outside_half_lantern import _matches
from .outside_rose_return import _terms,_transport
from .point_pushing import split_fixed_last_strand
from .projected_relations import pc_daisy_terms
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def two_pair_cabled_lantern(*,chart=()):
    """A1234 R345 R125 = D5 I34 I12, with every named expansion retained.

    This is a reusable local identity, not an applied source factorization.
    The two root prefixes are moved cyclically to the end by explicit common
    conjugations; two actual commuting crossings then expose the D5 daisy.
    """
    chart=tuple(chart)
    if any(type(x) is not int or not 1<=abs(x)<=4 for x in chart):raise ValueError('Use only signed B5 chart generators1..4')
    a=Factor('canonical.A1234',(),1,4);b=Factor('canonical.R345',(),3,3);c=Factor('canonical.R125',(-4,-3),1,3)
    d=Factor('canonical.D5',(),1,5);i34=Factor('canonical.I34',(),3,2);i12=Factor('canonical.I12',(),1,2)
    d5=_terms(d.mapping_class,'D5.',pc_daisy_terms);db=_terms(b.mapping_class,'R345.',pc_daisy_terms);dc=_terms(c.mapping_class,'R125.',pc_daisy_terms)
    shared_matches=(_matches(d5[:1],(a,)),_matches(db[:1],(i34,)),_matches(dc[:1],(i12,)),_matches(d5[1:3],db[1:]),_matches(d5[3:],dc[1:]))
    cyclic=[]
    for parent,terms in ((b,db),(c,dc)):
        after=terms[1:]+terms[:1];frame=inverse_word(terms[0].word);raw=reduce_word(frame+product(terms)+inverse_word(frame)+inverse_word(product(after)))
        if raw:raise ValueError('The full INTERNAL cyclic equality must be free-word exact FIRST')
        invariant=_matches(_transport((parent,),frame),(parent,))
        if exact_action(parent.word,5)!=exact_action(product(terms),5):raise ValueError('The independently known root needs its named PC daisy')
        cyclic.append(dict(parent=parent,before=terms,after=after,frame=frame,raw_cyclic_discrepancy=raw,independently_known_output_invariance=invariant))
    expanded=(a,)+cyclic[0]['after']+cyclic[1]['after'];moves=[];state=expanded
    for source,target in ((3,4),(4,5)):
        move=research_hurwitz_move(state,source,target)
        expected=list(state);expected[source],expected[target]=expected[target],expected[source]
        matches=_matches(move['factors'],tuple(expected));moves.append(dict(raw_move=move,individual_commutation_matches=matches));state=move['factors']
    final_matches=_matches(state,d5+(i34,i12));canonical_inputs=(a,b,c);canonical_outputs=(d,i34,i12)
    inputs=_transport(canonical_inputs,chart);outputs=_transport(canonical_outputs,chart)
    if exact_action(product(inputs),5)!=exact_action(product(outputs),5):raise ValueError('The fully named cabled identity failed in B5')
    discrepancy=reduce_word(product(inputs)+inverse_word(product(outputs)));sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('Retain separate local sphere and chosen+I discrepancies')
    splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in inputs+outputs)
    for x in splits:
        if exact_action(x['actual'].word,5)!=exact_action(x['split'].reconstructed_word,5):raise ValueError('No kernel or B4 shadow may be forgotten')
    return dict(common_chart=chart,cluster_sizes=(2,2,1),canonical_inputs=canonical_inputs,canonical_outputs=canonical_outputs,inputs=inputs,outputs=outputs,canonical_D5_daisy=d5,canonical_root_daisies=(db,dc),shared_petal_matches=shared_matches,internal_cyclic_certificates=tuple(cyclic),expanded_before_commutations=expanded,retained_internal_adjacent_moves=tuple(moves),expanded_after_commutations=state,final_individual_daisy_matches=final_matches,internal_adjacent_checks=2,disk_discrepancy=discrepancy,sphere_certificate=sphere,chosen_lift_discrepancy=lift,signed_pc_balance=tuple(sum(f.power for f in inputs if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in outputs if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6)),complete_point_pushing=splits,applied_to_replay=False,sphere_moves=0,exterior_caps=0,scope='Local reusable two-pair cabled PC lantern,fully derived from named daisies and explicit internal cyclic conjugations. Marked points are not framed holes. It supplies no actual third source factor,gather,substitution or complete proof join.')
