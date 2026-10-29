"""Six positive disk moves close the residual to FOUR visible unit exteriors."""
from dataclasses import replace
from .early_boundary_pure import _PositiveReplay
from .factorization_explorer import Factor
from .outside_rose_return import _terms,_transport,_witness
from .outside_half_lantern import _matches
from .projected_relations import pc_rose_terms,pc_daisy_terms
from .posthalf_cyclic_rose import cyclic_pattern
from .posthalf_exterior import _outputs,_cyclic
from .posthalf_outer import _certify,_preview
from .six_seven_structure import research_hurwitz_move


def close_posthalf_residual(factors):
    source=tuple(factors);by={f.id:f for f in source}
    if len(source)!=11 or any(f.half or f.power!=1 for f in source) or tuple(f.id for f in source[7:10])!=('outer.loan.1','outer.loan.2','third.loan.0'):
        raise ValueError('Use the selected THREE-exterior endpoint with actual adjacent tail15,25,NEW12')
    r=_PositiveReplay(source);r.stages[0]['title']='Three-exterior endpoint before the actual cyclic125 tail contraction'
    parent=Factor('residual.R125',(-4,-3),1,3);terms=_terms(parent.mapping_class,'canonical.tail.',pc_rose_terms);pattern,internal=cyclic_pattern(parent,terms,1)
    r.substitute(7,3,(parent,),'The ACTUAL older15,older25,NEW12 contract by the matched cyclic125 PCrose','disk_pc_rose')
    _witness(r,pattern,canonical_parent=parent,canonical_rose=terms,internal_cyclic_certificate=internal);_outputs(r,(parent,))
    canonical=Factor('canonical.R123',(),1,3);chart=parent.conjugator+(1,);rechart=replace(parent,conjugator=chart);parent_matches=_matches((parent,),(rechart,));loan=_terms(rechart.mapping_class,'residual.loan.',pc_rose_terms);rose=_terms(canonical.mapping_class,'canonical.rose.',pc_rose_terms)
    r.substitute(r.position(parent.id),1,loan,'The ACTUAL125 internal(+1) PCrose supplies neededNEW15 and retainsBOTH other petals','disk_pc_rose')
    _witness(r,(canonical,),chart,canonical_rose=rose,source_parent=parent,individual_parent_rechart=parent_matches);_outputs(r,rose,chart)
    preview=_preview(r,'residual.loan.2','alternative.return.2',after=True)
    if not preview['bounded']:raise ValueError('Reject NEW15 UP2 BEFORE application')
    r.drag('residual.loan.2','alternative.return.2',after=True,title='Carry the SAME NEW15 UP2 through its two actual donor leftovers')
    if r.factors!=preview['factors']:raise ValueError('The bounded15 preview must rejoin LITERALLY')
    parent4=Factor('canonical.D2345',(),2,4);daisy4=_terms(parent4.mapping_class,'canonical.D4.',pc_daisy_terms);move4=research_hurwitz_move(daisy4,1,0);pattern4,cycle4=cyclic_pattern(parent4,move4['factors'],1);g=(1,2,3);i=r.position('alternative.return.0');_matches(r.factors[i:i+4],_transport(pattern4,g));outer=Factor('residual.O1345',(1,),2,4)
    r.substitute(i,4,(outer,),'The ACTUAL134,old45,old35,NEW15 contract by the matched modified cyclic PCdaisy','disk_pc_daisy')
    _witness(r,pattern4,g,canonical_parent=parent4,canonical_daisy=daisy4,retained_internal_interchange=move4,internal_cyclic_certificate=cycle4);_outputs(r,(parent4,),g)
    _cyclic(r,'reflected.loan.2')
    d5=Factor('canonical.D5',(),1,5);daisy5=_terms(d5.mapping_class,'canonical.D5.',pc_daisy_terms);pattern5=daisy5;moves=[]
    for _ in range(2):
        move=research_hurwitz_move(pattern5,3,4);moves.append(move);pattern5=move['factors']
    pattern5,cycle5=cyclic_pattern(d5,pattern5,3);chart5=(1,-4,-3,-2,-2,1,2,3,4,1,2,3,1,2,1);_matches(r.factors[:5],_transport(pattern5,chart5));output=Factor('residual.exterior',(),1,5)
    r.substitute(0,5,(output,),'The FIVE ACTUAL residual inputs contract by the fully matched cyclic D5 daisy; retainFOURexteriors','disk_pc_daisy')
    _witness(r,pattern5,chart5,canonical_parent=d5,canonical_daisy=daisy5,retained_internal_interchanges=tuple(moves),internal_cyclic_certificate=cycle5);_outputs(r,(d5,),chart5)
    result=_certify(r)
    if len(r.factors)!=4:raise ValueError('Keep all FOUR terminal unit exteriors')
    terminal_matches=_matches(r.factors,(d5,)*4)
    for name in ('third.exterior','posthalf.exterior','reflected.exterior'):
        if next(f for f in r.factors if f.id==name)!=by[name]:raise ValueError('All THREE earlier exterior records stay LITERAL')
    result.update(named_substitutions=4,internal_adjacent_checks=3,selected=True,bounded_NEW15_preview=preview,terminal_standard_unit_matches=terminal_matches,four_visible_exteriors=r.factors,residual_named_closure_complete=True,named_disk_boundary_four_complete=True,terminal_power_combined=False,separate_fourth_power_cap_applied=False,useful_complete_join_reached=True,scope='SIX positive DISK moves/TWO external adjacent checks andFOUR individually matched named substitutions close the actual residual toFOUR visible STANDARD UNIT exteriors. All donor leftovers are consumed in explicit named patterns. The original three exterior records stay literal. Internal3crossings/rawcyclicwords/outputinvariances/fullkernels retained. No half,negativefactor,SPHEREredraw orcap;terminalcombine/fourth-power sphere redraw/cleanup remainSEPARATE. This is a complete named disk suffix join,NOT a shorter/adopted preferred derivation;preferred101/71 unchanged.')
    return result