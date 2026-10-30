"""Consolidate three actual pairs so one bounded root carry shortens35."""
from .early_boundary_pure import _PositiveReplay
from .factorization_explorer import Factor,product
from .outside_half_lantern import _matches
from .outside_rose_return import _terms,_transport,_witness
from .posthalf_exterior import _cyclic,_outputs
from .posthalf_outer import _certify,_preview
from .projected_relations import pc_daisy_terms,pc_rose_terms
from .six_seven_structure import research_hurwitz_move


def close_hybrid_root_carry(factors):
    source=tuple(factors)
    expected=('upper.I24','hybrid.exterior','hybrid.inner134','hybrid.second.0',
              'cyclic135.supply.2','reflected.exterior','hybrid.first.1',
              'hybrid.first.2','reflected.output.1','posthalf.exterior','reflected.loan.2')
    if tuple(f.id for f in source)!=expected or any(f.half or f.power!=1 for f in source):
        raise ValueError('Use the reached eleven-record hybrid third-exterior source')
    before={f.id:f for f in source}
    r=_PositiveReplay(source)
    r.stages[0]['title']='The reached hybrid third-exterior source'
    previews=[]
    def drag(name,target,title):
        p=_preview(r,name,target)
        if not p['bounded']:
            raise ValueError('Reject the complete proposed crossing before application')
        previews.append(p)
        r.drag(name,target,title=title)
        if r.factors!=p['factors']:
            raise ValueError('Bounded raw preview and normalized replay must join literally')
    _cyclic(r,'hybrid.inner134')
    drag('hybrid.second.0','reflected.exterior','SAME round12 DOWN2 across only commuting45/exterior')
    canonical=Factor('canonical.R123',(),1,3)
    rose=_terms(canonical.mapping_class,'canonical.rose.',pc_rose_terms)
    actors=tuple(before[n] for n in ('hybrid.second.0','hybrid.first.1','hybrid.first.2'))
    g=(-4,-3)
    i=r.position('hybrid.second.0')
    _matches(r.factors[i:i+3],_transport(rose,g))
    parent=Factor('short15.R125',g,1,3)
    r.substitute(i,3,(parent,),'THREE actual units contract by the matched125 PC rose','disk_pc_rose')
    _witness(r,rose,g,canonical_parent=canonical,canonical_rose=rose)
    _outputs(r,(canonical,),g)
    drag(parent.id,'reflected.output.1','SAME actual125 DOWN once straightens35 to the exact required class')
    carried_parent=r.factors[r.position(parent.id)]
    if carried_parent!=parent:
        raise ValueError('The actual125 root stays literal during its single carry')
    i=r.position(parent.id)
    r.substitute(i,1,actors,'Re-expand the SAME125 and restore all three source records literally','disk_pc_rose')
    _witness(r,(canonical,),g,canonical_rose=rose)
    _outputs(r,rose,g)
    restored=tuple(r.factors[r.position(f.id)] for f in actors)
    if restored!=actors:
        raise ValueError('All three specified source records are literally restored by the named expansion')
    drag('hybrid.second.0','hybrid.first.1','SAME round12 DOWN once creates the short15 petal')
    drag('reflected.exterior','hybrid.first.1','SAME odd exterior DOWN2 through commuting inputs')
    d4=Factor('canonical.D2345',(),2,4)
    daisy4=_terms(d4.mapping_class,'canonical.D4.',pc_daisy_terms)
    g=(1,)
    _matches(r.factors[:4],_transport(daisy4,g))
    outer=Factor('short15.O1345',g,2,4)
    r.substitute(0,4,(outer,),'FOUR actual inputs contract by the matched PC D4 daisy','disk_pc_daisy')
    _witness(r,daisy4,g,canonical_parent=d4,canonical_daisy=daisy4)
    _outputs(r,(d4,),g)
    late=r.factors
    shared=tuple(f.id for f in source if f.id in {x.id for x in late})
    if len(shared)!=7 or any(next(f for f in late if f.id==n)!=before[n] for n in shared):
        raise ValueError('All SEVEN shared source/late records remain literal')
    drag('posthalf.exterior','upper.I24','SAME odd exterior DOWN2 through commuting23/24')
    drag('reflected.exterior','upper.I24','SAME other exterior DOWN4 through commuting petals')
    d5=Factor('canonical.D5',(),1,5)
    daisy5=_terms(d5.mapping_class,'canonical.D5.',pc_daisy_terms)
    internal=research_hurwitz_move(daisy5,2,1)
    g=(1,-3,-3,1,2,3,1,2,1,4)
    _matches(r.factors[:5],_transport(internal['factors'],g))
    output=Factor('short15.exterior',(),1,5)
    r.substitute(0,5,(output,),'FIVE actual inputs contract by the matched modified PC D5 daisy','disk_pc_daisy')
    _witness(r,internal['factors'],g,canonical_parent=d5,canonical_daisy=daisy5,
             retained_internal_interchange=internal)
    _outputs(r,(d5,),g)
    result=_certify(r)
    end={f.id:f for f in r.factors}
    exteriors=tuple(f for f in source if f.points==5)
    if any(end[f.id]!=f for f in exteriors):
        raise ValueError('All three earlier odd exteriors stay literal')
    result.update(preapplication_previews=tuple(previews),actual_consolidated_inputs=actors,
        actual_carried_root=parent,root_stayed_literal_during_carry=carried_parent==parent,
        actual_restored_outputs=restored,restored_three_records_literal=restored==actors,
        shared_source_late_ids=shared,retained_three_exteriors=exteriors,
        terminal_standard_unit_matches=_matches(r.factors,(d5,)*4),named_substitutions=4,
        useful_complete_join_reached=True,selected=False,
        scope='Eleven positive DISK operations/twelve external adjacent checks close the same '
              'third-exterior source to four visible standard units. Consolidation and expansion '
              'are TWO actual named PC rose substitutions around a single actual root carry. '
              'All three output source records are restored literally before further moves; '
              'this is not raw free-word cancellation of three source factors. All four later '
              'daisy inputs and all five final inputs are individually matched in full charts. '
              'No half,negative factor,sphere move,cap,global frame or preferred adoption.')
    return result
