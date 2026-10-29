"""The positive125 action and short-side cyclic daisy reach a third exterior."""
from dataclasses import replace
from .braid_actions import inverse_word,reduce_word
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import Factor,product
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action
from .outside_half_lantern import _matches
from .outside_rose_return import _terms,_witness
from .posthalf_cyclic_rose import cyclic_pattern
from .posthalf_exterior import _cyclic,_outputs
from .posthalf_outer import _certify,_preview
from .projected_relations import pc_rose_terms,pc_daisy_terms
from .puncture_boundary import BOUNDARY_WORD
from .six_seven_structure import research_hurwitz_move


def expose_posthalf_third_exterior(factors):
    source=tuple(factors);by={f.id:f for f in source}
    if len(source)!=13 or any(f.half or f.power!=1 for f in source) or tuple(f.id for f in source[:2])!=('upper.O1234','upper.I24'):
        raise ValueError('Use the selected upper-cabled TWO-exterior endpoint')
    r=_PositiveReplay(source);r.stages[0]['title']='Actual upper-cabled endpoint before the positive125 action'
    parent=Factor('canonical.R123',(),1,3);d5=Factor('canonical.D5',(),1,5);canonical_daisy=_terms(d5.mapping_class,'canonical.D5.',pc_daisy_terms)
    i,j=r.position('reflected.inner125'),r.position('reflected.output.1');raw=research_hurwitz_move(r.factors,i,j)
    if abs(i-j)!=1 or _score(raw['factors'])['max_support_word']>20:raise ValueError('Reject the125 DOWN35 crossing BEFORE application')
    r.drag('reflected.inner125','reflected.output.1',title='The SAME125 DOWN once changes35 to the EXACT canonical daisy petal')
    _matches((r.factors[r.position('reflected.output.1')],),canonical_daisy[2:3])
    donor=r.factors[r.position('reflected.inner125')];chart=donor.conjugator+(1,);rechart=replace(donor,conjugator=chart);root_match=_matches((donor,),(rechart,));loan=_terms(rechart.mapping_class,'third.loan.',pc_rose_terms);canonical_rose=_terms(parent.mapping_class,'canonical.rose.',pc_rose_terms)
    _matches(loan[:1],(Factor('round12',(),1,2),));_matches(loan[1:],canonical_daisy[3:])
    r.substitute(r.position(donor.id),1,loan,'Internal(+1) PCrose of the ACTUAL125 supplies exact25/15 and retains12','disk_pc_rose')
    _witness(r,(parent,),chart,canonical_rose=canonical_rose,actual_parent_rechart_match=root_match,source_parent=donor);_outputs(r,canonical_rose,chart)
    preview=_preview(r,'third.loan.0','cyclic135.supply.2')
    if not preview['bounded']:raise ValueError('Reject12 UP3 BEFORE application')
    r.drag('third.loan.0','cyclic135.supply.2',title='Carry SAME12 UP3 through ONLY commuting35,exterior,45')
    r.drag('cyclic135.supply.2','reflected.exterior',title='Carry SAME45 DOWN once across only the commuting exterior')
    # The long gather would cross the outside-winding134 at support23.
    # Its bounded prefix is only a hypothetical preview, never a replay route.
    rejected_long=_preview(r,'upper.O1234','reflected.exterior')
    if rejected_long['bounded']:raise ValueError('The saved rejected long-side candidate changed')
    _cyclic(r,'cyclic135.supply.2')
    short=_preview(r,'upper.O1234','posthalf.exterior')
    if not short['bounded']:raise ValueError('Reject the short-side O gather BEFORE application')
    r.drag('upper.O1234','posthalf.exterior',title='The SAME round outer UP2 through ONLY commuting23 and the other exterior')
    if r.factors!=short['factors']:raise ValueError('The short-side replay must match its complete bounded preview')
    for name in ('reflected.loan.2','reflected.exterior','posthalf.exterior'):
        if r.factors[r.position(name)]!=by[name]:raise ValueError('All short-side neighbors stay LITERAL')
    pattern,internal=cyclic_pattern(d5,canonical_daisy,1);_matches(r.factors[:5],pattern)
    output=Factor('third.exterior',(),1,5)
    r.substitute(0,5,(output,),'The ACTUAL45,35,25,15,outer contract by the matched CYCLIC D5 daisy','disk_pc_daisy')
    _witness(r,pattern,canonical_parent=d5,canonical_daisy=canonical_daisy,internal_cyclic_certificate=internal);_outputs(r,(d5,))
    result=_certify(r);exteriors=tuple(f for f in r.factors if f.id in ('reflected.exterior','posthalf.exterior','third.exterior'));residual=tuple(f for f in r.factors if f.id not in ('reflected.exterior','posthalf.exterior','third.exterior'));minus=tuple(tuple(-x for x in row) for row in IDENTITY)
    if len(exteriors)!=3 or any(homology_action(f.word)!=minus for f in exteriors) or homology_action(product(residual))!=minus or exact_action(product(residual),5)!=exact_action(BOUNDARY_WORD,5):raise ValueError('Retain THREE odd exteriors and the separate residual boundary-one/-I diagnostic')
    result.update(named_substitutions=2,selected=True,three_visible_exteriors=exteriors,every_exterior_chosen_lift=minus,residual_factors=residual,residual_boundary_power_diagnostic=1,residual_chosen_lift=minus,residual_named_closure_complete=False,bounded_12_preview=preview,bounded_short_side_preview=short,unapplied_rejected_long_gather=rejected_long,remaining_125_donor_petal=next(f for f in r.factors if f.id=='third.loan.0'),consumed_source_ids=('upper.O1234','cyclic135.supply.2','reflected.inner125','reflected.output.1'),scope='SEVEN positive DISK moves/SEVEN external checks reach THIRD VISIBLE standard UNIT exterior. The125 donor supplies25/15 and remainsONE12petal. BOTH older125loans,old23 andBOTH earlier exteriors stay literal. Long-side gather is UNAPPLIED/rejected23;short sidecommutes. No half,negativefactor,sphere redraw,cap or useful complete suffix join. Residual boundary-one/-I is DIAGNOSTIC,not a named closure. Preferred101/71 stays SOLVED/UNCHANGED.')
    return result