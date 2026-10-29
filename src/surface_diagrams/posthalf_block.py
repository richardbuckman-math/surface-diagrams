"""Bounded ordered-loan transport simplifies four actual post-half curves."""
from .braid_actions import inverse_word,reduce_word
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import Factor,product
from .outside_half_lantern import _matches
from .posthalf_exterior import _cyclic
from .posthalf_outer import _certify
from .six_seven_structure import research_hurwitz_move


def transport_posthalf_loan_block(factors,*,preparation='inverse'):
    """Keep the two actual125 loan petals ordered; carry them up six neighbors.

    Optional prep/undo edits cost TWO actual positive interchanges. The inverse
    preparation has a lower CLOSED trajectory peak than the direct transport.
    Every adjacent interchange is listed separately; none is called parallel.
    """
    source=tuple(factors)
    if preparation not in ('direct','forward','inverse'):raise ValueError('Choose a measured donor preparation')
    if len(source)!=14 or any(f.half or f.power!=1 for f in source) or tuple(f.id for f in source[:5])!=('outer.O1245','posthalf.exterior','outer.loan.1','outer.loan.2','posthalf.return.R123'):
        raise ValueError('Use the saved selected14-record posthalf-outer endpoint')
    r=_PositiveReplay(source);r.stages[0]['title']='Post-half outer endpoint before the ordered125-loan transport'
    previews=[]
    def move(name,target,title):
        a,b=r.position(name),r.position(target)
        if abs(a-b)!=1:raise ValueError('Every listed move is ONE adjacent interchange')
        raw=research_hurwitz_move(r.factors,a,b);score=_score(raw['factors'])
        if score['max_support_word']>20:raise ValueError('Reject this candidate BEFORE application')
        previews.append(dict(moving=name,crossed=target,raw_score=score,raw_move=raw))
        r.drag(name,target,title=title)
        _matches(raw['factors'],r.factors)
    a,b='outer.loan.1','outer.loan.2';block=source[2:4]
    if preparation=='forward':move(a,b,'Preparation: first loan petal DOWN once')
    elif preparation=='inverse':move(b,a,'Preparation: second loan petal UP once')
    _cyclic(r,'posthalf.return.R123')
    names=(a,b) if preparation=='direct' else (b,a);crossed=[]
    while r.factors[r.position(names[0])-1].id!='alternative.return.2':
        neighbor=r.factors[r.position(names[0])-1].id;crossed.append(neighbor)
        for name in names:move(name,neighbor,'Carry '+name+' UP across '+neighbor)
    if tuple(crossed)!=('posthalf.exterior','outer.O1245','alternative.P13','posthalf.supply.0','alternative.S1','F8.2'):
        raise ValueError('Retain the exact six-neighbor ordered block')
    if preparation=='forward':move(a,b,'Restore original loan order: first petal UP once')
    elif preparation=='inverse':move(b,a,'Restore original loan order: second petal DOWN once')
    now={f.id:f for f in r.factors};original={f.id:f for f in source}
    if tuple(now[n] for n in (a,b))!=block:raise ValueError('Both actual loan records must be restored LITERALLY')
    raw_frame=inverse_word(product(block));conjugated=tuple(dict(source=original[n],raw_target=Factor(original[n].id,reduce_word(raw_frame+original[n].conjugator),original[n].first,original[n].points),actual=now[n]) for n in crossed)
    for c in conjugated:c['individual_full_block_conjugation_match']=_matches((c['actual'],),(c['raw_target'],))
    changed=tuple(n for n in original if original[n]!=now[n])
    if set(changed)!={'alternative.P13','posthalf.supply.0','alternative.S1','F8.2'}:raise ValueError('Only these four actual curves change')
    round_match=_matches((now['F8.2'],),(Factor('round345',(),3,3),))
    result=_certify(r);result.update(preparation=preparation,preapplication_previews=tuple(previews),crossed_neighbors=tuple(crossed),actual_loan_block=block,loan_records_restored_literally=True,full_block_conjugation_matches=conjugated,changed_record_ids=changed,round345_match=round_match,matching15_copies=_matches((now['posthalf.supply.0'],),(now[a],)),selected=preparation=='inverse',sphere_moves=0,exterior_caps=0,scope='A reached research route with each positive adjacent interchange listed. Donor reordering/undo adds two moves to improve the measured CLOSED trajectory. The four changed supports shorten; ten actual records,including both loan records,are retained literally. Two matching15 copies remain separate. No half,sphere move,cap,named substitution or useful complete suffix join is introduced; preferred101/71 remains solved and unchanged.')
    return result
