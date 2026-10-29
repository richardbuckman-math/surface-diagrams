"""The newly round345 supplier reaches an actual cyclic135 PC rose."""
from .braid_actions import inverse_word,reduce_word
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import Factor,product
from .outside_half_lantern import _matches
from .outside_rose_return import _terms,_transport,_witness
from .posthalf_exterior import _outputs
from .posthalf_outer import _certify
from .projected_relations import pc_rose_terms
from .six_seven_structure import research_hurwitz_move


def cyclic_pattern(parent,terms,offset):
    terms=tuple(terms);after=terms[offset:]+terms[:offset];frame=inverse_word(product(terms[:offset]));raw=reduce_word(frame+product(terms)+inverse_word(frame)+inverse_word(product(after)))
    if raw:raise ValueError('The FULL internal cyclic common conjugation must be free-word exact FIRST')
    invariance=_matches(_transport((parent,),frame),(parent,))
    return after,dict(before=terms,after=after,offset=offset,frame=frame,raw_cyclic_discrepancy=raw,independently_known_output_invariance=invariance)


def contract_posthalf_cyclic_rose(factors):
    source=tuple(factors)
    if len(source)!=14 or any(f.half or f.power!=1 for f in source) or tuple(f.id for f in source[8:12])!=('F8.2','alternative.S1','posthalf.supply.0','alternative.P13'):
        raise ValueError('Use the chosen posthalf-block endpoint,with ROUND F8')
    parent=Factor('canonical.R345',(),3,3);_matches((source[8],),(parent,));canonical=_terms(parent.mapping_class,'canonical.rose.',pc_rose_terms)
    r=_PositiveReplay(source);r.stages[0]['title']='Simpler block endpoint before the actual35 loan'
    supply=tuple(Factor('cyclic135.supply.'+str(i),f.conjugator,f.first,f.points) for i,f in enumerate(canonical));cyclic,internal=cyclic_pattern(parent,supply,2)
    r.substitute(8,1,cyclic,'Cyclic PC rose of the ACTUAL round345 lends35 and retains34/45','disk_pc_rose');_witness(r,(parent,),canonical_rose=canonical,internal_cyclic_certificate=internal);_outputs(r,cyclic)
    i,j=r.position('cyclic135.supply.1'),r.position('alternative.S1');raw=research_hurwitz_move(r.factors,i,j)
    if abs(i-j)!=1 or _score(raw['factors'])['max_support_word']>20:raise ValueError('Check the actual35 crossing BEFORE application')
    r.drag('cyclic135.supply.1','alternative.S1',title='Carry the SAME35 DOWN across its commuting235 neighbor')
    if r.factors[r.position('alternative.S1')]!=source[9]:raise ValueError('The commuting neighbor must remain LITERAL')
    pattern,root_cyclic=cyclic_pattern(parent,canonical,1);chart=(-1,-1,-3,-2,1,2,3);i=r.position('cyclic135.supply.1');_matches(r.factors[i:i+3],_transport(pattern,chart))
    raw_root=Factor('cyclic135.R135',chart,3,3);output=r.normalize(raw_root);_matches((output,),(raw_root,))
    r.substitute(i,3,(output,),'The ACTUAL35,W15,P13 contract by the individually matched cyclic PC rose','disk_pc_rose');_witness(r,pattern,chart,canonical_parent=parent,canonical_rose=canonical,internal_cyclic_certificate=root_cyclic,source_chart_output=raw_root);_outputs(r,(parent,),chart)
    result=_certify(r);result.update(named_substitutions=2,half_factors=0,negative_factors=0,sphere_moves=0,exterior_caps=0,remaining_345_donor_petals=tuple(f for f in r.factors if f.id in ('cyclic135.supply.0','cyclic135.supply.2')),consumed_matching15_id='posthalf.supply.0',retained_other15_id='outer.loan.1',round345_loan_returned=False,selected=True,scope='Three reached positive disk operations/one adjacent check exchange round345,W15,P13 for actualR135 and TWO retained round34/45 petals. Every actual named input/output is matched in one chart. The two15 copies are not conflated; W is consumed,other125-loan15 remains. No sphere move,cap,half or useful complete suffix join. Preferred101/71 remains solved and unchanged.')
    return result
