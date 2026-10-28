"""Compare closed half-twist neighborhoods on already reached disk routes."""
from dataclasses import asdict,replace
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.disk_intersection import disk_intersection_certificate
from surface_diagrams.factorization_explorer import product
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.braid_actions import inverse_word

ROOT=Path(__file__).resolve().parents[1]

def neighborhood_statistics(factors,certificates,*,max_letters=400000):
    fs=tuple(factors);halves=tuple(f for f in fs if f.half)
    if any(f.power!=1 for f in halves):raise ValueError('This audit follows unit half-twist records')
    pairs=[]
    for a,b in combinations(fs,2):
        if not (a.half or b.half):continue
        left=replace(a.mapping_class,half=False,power=1);right=replace(b.mapping_class,half=False,power=1)
        key=(left,right)
        if key not in certificates:
            certificates[key]=dict(index=len(certificates),left=left,right=right,
                certificate=disk_intersection_certificate(left,right,strands=5,max_letters=max_letters))
        item=certificates[key];n=item['certificate']['intersection_number']
        pairs.append(dict(ids=(a.id,b.id),both_halves=a.half and b.half,certificate_index=item['index'],intersection=n))
    return dict(half_neighborhood_lengths={f.id:len(supported_class(f.mapping_class,5)) for f in halves},
        pair_maximum=max((p['intersection'] for p in pairs),default=0),pair_sum=sum(p['intersection'] for p in pairs),
        half_pair_maximum=max((p['intersection'] for p in pairs if p['both_halves']),default=0),
        factor_records=len(fs),pairs=tuple(pairs))

def build_report():
    folder=ROOT/'docs/proofs/six-seven-fifty-blocks';source_path=folder/'certificate.json'
    outside_path=ROOT/'docs/proofs/six-seven-outside-half-lantern.json'
    c=json.loads(source_path.read_text(encoding='utf-8'));outside=json.loads(outside_path.read_text(encoding='utf-8'))
    raw=c['early_alternative_transport']['stages'];current=c['named_full_route']['stages'];cyclic=c['named_cyclic_start_shortening']['replacement_interval']
    late=raw[20:23]+cyclic[1:-1]
    if current[31]['factors']!=late[0]['factors'] or current[39]['factors']!=late[-1]['factors']:
        raise ValueError('The late-daisy comparison must have literal complete input/output joins')
    clarity_path=folder/'clarity-certificate.json';clarity=json.loads(clarity_path.read_text(encoding='utf-8'))
    clear_joins=[next(s for s in clarity['stages'] if s.get('source_index')==i) for i in (34,42)]
    if any(s['ledger'] is not None for s in clear_joins) or any(a['factors']!=b['factors'] for a,b in zip(clear_joins,(late[0],late[-1]))):
        raise ValueError('The complete preferred clarity joins changed')
    routes=dict(current_early=current[31:40],late_daisy=late,
        historical_square=raw[20:30],outside_clear=raw[20:23]+outside['preferred']['stages'][1:],
        outside_original_chart=raw[20:23]+outside['original_chart']['stages'][1:])
    certificates={};half_words={};results={};expected=exact_action((1,2,3,4)*20,5)
    for name,stages in routes.items():
        metrics=[]
        for i,stage in enumerate(stages):
            for j,state in enumerate([stage]+stage.get('atomic_steps',[])):
                fs=tuple(factor_from_data(f) for f in state['factors'])
                if exact_action(product(fs),5)!=expected:raise ValueError('An audited state lost its faithful disk action')
                if any(f.power<1 or getattr(f,'sign',1)!=1 for f in fs):raise ValueError('Keep positive factors')
                metrics.append(dict(stage=i,atomic=j,title=state.get('title',stage['title']+' / adjacent '+str(j)),**neighborhood_statistics(fs,certificates)))
                for f in fs:
                    if not f.half or f in half_words:continue
                    neighbor=replace(f,half=False)
                    if exact_action(neighbor.word,5)!=exact_action(f.word+f.word,5):raise ValueError('The full neighborhood is not the actual half squared')
                    split=split_fixed_last_strand(neighbor.word,5)
                    if exact_action(split.reconstructed_word,5)!=exact_action(neighbor.word,5):raise ValueError('Retain the full nonabelian kernel and shadow')
                    half_words[f]=dict(actual_half=f,actual_half_word=f.word,closed_neighborhood=neighbor,
                        neighborhood_is_half_squared=True,closed_neighborhood_split=split)
        for a,b in zip(stages,stages[1:]):
            before=product(tuple(factor_from_data(f) for f in a['factors']));after=product(tuple(factor_from_data(f) for f in b['factors']))
            if b['kind'] in ('disk_cyclic_start','global_conjugation'):
                frame=tuple(b['frame']);before=frame+before+inverse_word(frame)
            if exact_action(before,5)!=exact_action(after,5):raise ValueError('An ordered transition failed')
        results[name]=dict(moves=len(stages)-1,retained_states=len(metrics),states=metrics,
            summary=dict(half_support_peak=max(n for m in metrics for n in m['half_neighborhood_lengths'].values()),
                half_pair_peak=max(m['half_pair_maximum'] for m in metrics),pair_peak=max(m['pair_maximum'] for m in metrics),
                pair_sum_peak=max(m['pair_sum'] for m in metrics),factor_record_peak=max(m['factor_records'] for m in metrics),
                factor_record_peak_while_halves=max(m['factor_records'] for m in metrics if m['half_neighborhood_lengths'])))
    return dict(source_sha256=sha256(source_path.read_bytes()).hexdigest(),source_clarity_sha256=sha256(clarity_path.read_bytes()).hexdigest(),preferred_clarity_source_interval=(34,42),outside_source_sha256=sha256(outside_path.read_bytes()).hexdigest(),
        routes=results,closed_pair_certificates=tuple(certificates.values()),half_neighborhood_certificates=tuple(half_words.values()),
        late_daisy_complete_input=current[31]['factors'],late_daisy_complete_output=current[39]['factors'],
        late_daisy_stages=late,literal_complete_joins=True,source_witness_refs=('early_alternative_transport.stages[20:23]','named_cyclic_start_shortening.replacement_interval[1:-1]'),
        current_preferred_unchanged=True,applied_to_public_replay=False,
        scope='Exact minimal intersections of CLOSED neighborhood curves. Every unordered factor-record pair incident to a remaining half is counted once, regardless of twist power. These are not arc intersection counts, a joint minimum drawing, or a complete-proof operation lower bound. The late variant delays a three-petal expansion; its aggregate reduction partly reflects fewer factor records. Half support and worst-pair peaks do not improve. All compared routes are already reached; no new transport or substitution is claimed.')

if __name__=='__main__':
    report=build_report();path=ROOT/'docs/proofs/six-seven-half-neighborhood-geometry.json'
    path.write_text(json.dumps(report,default=asdict,separators=(',',':')),encoding='utf-8')
    for name,r in report['routes'].items():print(name,r['moves'],r['retained_states'],r['summary'])
    print('Saved',path.name,path.stat().st_size,'bytes; preferred derivation unchanged')
