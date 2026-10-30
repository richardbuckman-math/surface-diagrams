"""Straighten the last two pair curves using an actual45 loan and return."""
from dataclasses import replace
from .braid_actions import reduce_word
from .early_boundary_pure import _PositiveReplay
from .factorization_explorer import Factor
from .outside_half_lantern import _matches
from .outside_rose_return import _terms,_transport,_witness
from .posthalf_exterior import _cyclic,_outputs
from .posthalf_outer import _certify,_preview
from .projected_relations import pc_daisy_terms
from .six_seven_structure import research_hurwitz_move


def close_preferred_late45(factors, *, internal_power=-1):
    source=tuple(factors)
    expected=('alternative.return.2','alternative.P24','direct.exterior.3','direct.E2',
              'alternative.second.exterior','alternative.exterior','alternative.second.I35','alternative.returned.N')
    if tuple(f.id for f in source)!=expected or any(f.half or f.power!=1 for f in source):
        raise ValueError('Use the exact preferred first-third-exterior checkpoint')
    if internal_power not in (0,-1,-2):
        raise ValueError('Only the three specifically derived donor charts are compared')
    before={f.id:f for f in source}
    r=_PositiveReplay(source)
    r.stages[0]['title']='The preferred first third-exterior checkpoint'
    previews=[]
    def drag(name,target,title):
        p=_preview(r,name,target)
        if not p['bounded']:
            raise ValueError('Reject the complete proposed loan carry before application')
        previews.append(p)
        r.drag(name,target,title=title)
        if r.factors!=p['factors']:
            raise ValueError('The full raw bounded preview and normalized replay must join literally')
    outer=before['alternative.returned.N']
    canonical=Factor('canonical.D2345',(),2,4)
    terms=_terms(canonical.mapping_class,'canonical.D4.',pc_daisy_terms)
    chart=((-4,)*(-internal_power))+(1,)
    chart_parent=replace(outer,conjugator=chart)
    parent_matches=_matches((outer,),(chart_parent,))
    outputs=tuple(r.normalize(f) for f in _terms(chart_parent.mapping_class,'preferred45.',pc_daisy_terms))
    i=r.position(outer.id)
    r.substitute(i,1,outputs,'The retained outer lends 45 in its checked internal chart','disk_pc_daisy')
    _witness(r,(canonical,),chart,canonical_daisy=terms,actual_source_parent=outer,
             chart_parent=chart_parent,individual_parent_rechart=parent_matches)
    _outputs(r,terms,chart)
    loan=outputs[1]
    _matches((loan,),(Factor('canonical.round45',(),4,2),))
    _cyclic(r,loan.id)
    crossed=tuple(f.id for f in r.factors[1:])
    drag(loan.id,'preferred45.0','Carry the SAME round 45 DOWN through all ten actual neighbors')
    if r.factors[r.position(loan.id)]!=loan:
        raise ValueError('The actual round45 loan stays literal throughout its full carry')
    _cyclic(r,'preferred45.0')
    return_chart=loan.word+chart
    _matches(r.factors[:4],_transport(terms,return_chart))
    invariance=_matches(_transport((canonical,),return_chart),(outer,))
    r.substitute(0,4,(outer,),'Return the SAME source outer through the full changed donor daisy','disk_pc_daisy')
    _witness(r,terms,return_chart,canonical_parent=canonical,canonical_daisy=terms,
             individually_known_parent_invariance=invariance)
    _outputs(r,(canonical,),return_chart)
    returned={f.id:f for f in r.factors}
    if returned[outer.id]!=outer:
        raise ValueError('The source outer is returned LITERALLY')
    effects=tuple(dict(source=f,actual=returned[f.id],raw_target=replace(f,conjugator=reduce_word(loan.word+f.conjugator)),
                       individual_match=_matches((returned[f.id],),_transport((f,),loan.word))) for f in source)
    changed=tuple(f.id for f in source if returned[f.id]!=f)
    if set(changed)!={'alternative.P24','direct.E2'}:
        raise ValueError('Only the two specified pair curves may change at donor return')
    drag('direct.E2','direct.exterior.3','SAME short 24 UP across one commuting exterior')
    drag('alternative.second.I35','direct.exterior.3','SAME round 23 UP across three commuting exteriors')
    late=r.factors
    if {f.id for f in late}!={f.id for f in source}:
        raise ValueError('All eight source records remain individually accounted for before D5')
    d5=Factor('canonical.D5',(),1,5)
    daisy5=_terms(d5.mapping_class,'canonical.D5.',pc_daisy_terms)
    first=research_hurwitz_move(daisy5,2,1)
    second=research_hurwitz_move(first['factors'],4,3)
    chart5=(1,-3,-3,1,2,3,1,2,1,4)
    _matches(r.factors[:5],_transport(second['factors'],chart5))
    output=Factor('preferred45.exterior',(),1,5)
    r.substitute(0,5,(output,),'FIVE short actual inputs contract by the twice-modified D5 daisy','disk_pc_daisy')
    _witness(r,second['factors'],chart5,canonical_parent=d5,canonical_daisy=daisy5,
             retained_internal_interchanges=(first,second))
    _outputs(r,(d5,),chart5)
    result=_certify(r,exterior_id='direct.exterior.3')
    end={f.id:f for f in r.factors}
    exteriors=tuple(f for f in source if f.points==5)
    if any(end[f.id]!=f for f in exteriors):
        raise ValueError('All three earlier odd unit exteriors remain literal')
    result.update(preapplication_previews=tuple(previews),internal_power=internal_power,
        donor_source_parent=outer,donor_chart_parent=chart_parent,actual_round45_loan=loan,
        actual_loan_crossed_neighbors=crossed,returned_parent_literal=returned[outer.id]==outer,
        full_actual_source_conjugation_matches=effects,changed_source_ids=changed,
        retained_three_exteriors=exteriors,terminal_standard_unit_matches=_matches(r.factors,(d5,)*4),
        named_substitutions=3,useful_complete_join_reached=True,selected=False,
        scope='Eight positive DISK moves/fourteen external adjacent checks borrow an actual '
              'round45 from the retained outer and RETURN that outer literally. Only two '
              'source pair curves change, by individually checked positive45 action. This '
              'effect is realized by named substitutions, two explicit cyclic starts and '
              'a full bounded actual loan carry, not an applied global-frame move. The '
              'internal inverse generator chart creates no half-twist factors. Three old '
              'odd exteriors stay literal; four standard units remain visible. No sphere '
              'move or cap. Historical source charts and flags remain separate.')
    return result
