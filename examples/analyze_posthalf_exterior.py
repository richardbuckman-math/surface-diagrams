"""Certify the reached post-combine rose loans and exterior; no replay edits."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import matrix,equality
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.disk_intersection import disk_intersection_certificate
from surface_diagrams.posthalf_exterior import expose_posthalf_exterior
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-fixed-half-meeting.json';m=json.loads(path.read_text(encoding='utf-8'))
    source=tuple(factor_from_data(f) for f in m['stages'][3]['factors']);r=expose_posthalf_exterior(source)
    archive=ROOT/'docs/proofs/six-seven-fifty-blocks/certificate.json';c=json.loads(archive.read_text(encoding='utf-8'))
    k,old=next((i,s) for i,s in enumerate(c['named_full_route']['stages']) if i>14 and any(f['points']==5 and f['power']==1 for f in s['factors']))
    original=tuple(factor_from_data(f) for f in old['factors'])
    new_matrix,old_matrix=matrix(r['factors']),matrix(original)
    intermediate=r['repeated_rose_endpoint'];by={f.id:f for f in intermediate};q=Factor('target.round45',(),4,2)
    probes=[]
    for name in ('posthalf.output.0','posthalf.output.1'):
        f=by[name]
        for sign in (1,-1):
            g=f.word if sign==1 else inverse_word(f.word);candidate=replace(by['alternative.return.1'],conjugator=reduce_word(g+by['alternative.return.1'].conjugator))
            probes.append(dict(conjugator=f,sign=sign,candidate=candidate,target=q,exact_match=equality(candidate.word,q.word),support_length=len(supported_class(candidate.mapping_class,5)),applied=False))
    commuting=tuple(dict(factor=by[name],target=q,commutation=equality(by[name].word+q.word,q.word+by[name].word)) for name in ('posthalf.loan.1','posthalf.loan.2'))
    if not all(a['commutation']['equal'] for a in commuting):raise ValueError('The scoped commuting-subgroup diagnostic changed')
    supplier_diagnostics=tuple(dict(actual=by[name],target=q,closed_intersection=disk_intersection_certificate(by[name].mapping_class,q.mapping_class,strands=5)) for name in ('F8.2','alternative.F12.1','F10.2'))
    final={f.id:f for f in r['factors']}
    target=(final['posthalf.inner125'],final['posthalf.return.R123'],final['alternative.return.2'])
    return dict(route=r,source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='stages.3',preferred_source_index_at_checkpoint=43,
        source_closed_matrix=matrix(source),endpoint_closed_matrix=new_matrix,
        reference_first_exterior=dict(archive_file='six-seven-fifty-blocks/certificate.json',archive_sha256=sha256(archive.read_bytes()).hexdigest(),source_ref='named_full_route.stages.'+str(k),factors=original,closed_matrix=old_matrix,score=old['score'],preferred_source_index_at_checkpoint=50),
        new_first_exterior_source_operations_at_checkpoint=57,seven_more_source_operations_than_reference=True,
        limited_unapplied_45_probes=tuple(probes),supplier_closed_diagnostics=supplier_diagnostics,
        commuting_loan_petal_diagnostic=dict(generators=commuting,existing_return45_not_target=equality(by['alternative.return.1'].word,q.word),scope='Both loan petals commute with round45. No word in those two alone can conjugate a different existing curve to round45. This does not exclude other outside interactions or transports.'),
        next_cabled_candidate=dict(actual_inputs=target,applied=False,requires_full_joint_chart=True,requires_bounded_gather=True,scope='Exact actual records only; NO cabled-lantern match or gather is claimed for the new inner125,returned123 and existing35 pair.'),
        public_replay_changed=False,complete_preferred_moves=101,complete_preferred_steps=71,
        scope='The new14-move extension reaches a visible exterior with all actual inputs individually certified. It has NO complete join to the preferred suffix. Its15-record endpoint has CLOSED sum862/max36 versus the archived16-record first exterior1536/74; different inventories,more source operations,support maximum18 versus17 and braid258 versus220 prevent any claim that all complexity measures improve. This comparison is not an arc intersection count or one jointly minimal drawing. Preferred proof,payloads,PDFs and earlier audits remain unchanged.')

if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-exterior.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Reached',r['route']['graphical_operations'],'operations/',r['route']['adjacent_checks'],'external checks;peak',r['route']['peak_support_word'])
    print('Closed reference/new',r['reference_first_exterior']['closed_matrix']['total'],r['endpoint_closed_matrix']['total'],'saved',p.stat().st_size,'bytes')
