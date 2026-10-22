"""Report exact closed-curve intersections at the new pure checkpoints."""
from dataclasses import replace
import json
from pathlib import Path

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.disk_intersection import disk_intersection_certificate
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.mapping_classes import supported_class
from surface_diagrams.six_seven_structure import research_hurwitz_move
from surface_diagrams.twist_simplify import simplify_twist


def pure_intersection_report():
    folder=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-fifty-blocks'
    saved=json.loads((folder/'certificate.json').read_text(encoding='utf-8'))
    result={};factors_by_key={}
    checkpoints={key:saved[key]['factors'] for key in ('early_purification','pure_cluster_contractions')}
    checkpoints['before_square_unwind']=saved['pure_cluster_contractions']['stages'][11]['factors']
    for key,records in checkpoints.items():
        factors=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in records)
        matrix=[[0]*len(factors) for _ in factors]
        for i,a in enumerate(factors):
            for j in range(i+1,len(factors)):
                value=disk_intersection_certificate(a.mapping_class,factors[j].mapping_class,strands=5)['intersection_number']
                matrix[i][j]=matrix[j][i]=value
        result[key]=dict(ids=tuple(f.id for f in factors),matrix=matrix,
            maximum=max(max(row) for row in matrix),total=sum(map(sum,matrix))//2,
            pairs=len(factors)*(len(factors)-1)//2)
        factors_by_key[key]=factors
    current=factors_by_key['pure_cluster_contractions'];current_ids={f.id:f for f in current}
    result['current_outer_candidate']={name:disk_intersection_certificate(current_ids['pure.O1234'].mapping_class,current_ids[name].mapping_class,strands=5) for name in ('early.F13.1','early.F12.1')}
    result['next_exterior_lantern']=saved['pure_cluster_contractions']['next_exterior_lantern']
    fs=factors_by_key['before_square_unwind'];by_id={f.id:f for f in fs}
    o,b,c=(by_id[name] for name in ('pure.O1234','early.F13.1','early.F12.1'))
    moved=replace(b,conjugator=inverse_word(c.word)+b.conjugator)
    source,target=(next(i for i,f in enumerate(fs) if f.id==name) for name in ('early.F12.1','early.F13.1'))
    peak=max(len(supported_class(f.mapping_class,5)) for f in fs)
    while source>target:
        raw=research_hurwitz_move(fs,source,source-1);changed=raw['factors'][source]
        twist=simplify_twist(changed.mapping_class,strands=5)
        fs=raw['factors'][:source]+(replace(changed,conjugator=twist.conjugator,first=twist.first),)+raw['factors'][source+1:]
        peak=max(peak,max(len(supported_class(f.mapping_class,5)) for f in fs));source-=1
    result['outer_candidate']=dict(
        o_b=disk_intersection_certificate(o.mapping_class,b.mapping_class,strands=5),
        o_c=disk_intersection_certificate(o.mapping_class,c.mapping_class,strands=5),
        b_c=disk_intersection_certificate(b.mapping_class,c.mapping_class,strands=5),
        inverse_c_transport=disk_intersection_certificate(o.mapping_class,moved.mapping_class,strands=5),
        actual_transport_support_peak=peak,applied_to_replay=False,
        warning='Pairwise counts alone do not certify a triple or an ordered lantern relation.')
    return result


if __name__=='__main__':
    print(json.dumps(pure_intersection_report(),separators=(',',':')))
