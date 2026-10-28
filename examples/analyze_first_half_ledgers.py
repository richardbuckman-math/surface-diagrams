"""Classify possible short full-twist endforms of the isolated first-half block."""
from dataclasses import asdict,replace
from itertools import permutations
from pathlib import Path
import hashlib,json
from surface_diagrams.alternative_thirty_audit import pure_linking_certificate
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.linking_ledgers import positive_linking_ledgers
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.point_pushing import split_fixed_last_strand

ROOT=Path(__file__).resolve().parents[1]


def report():
    source=json.loads((ROOT/'docs/proofs/six-seven-first-half-two-donors.json').read_text(encoding='utf-8'))
    factors=tuple(Factor(**dict(x,conjugator=tuple(x['conjugator']))) for x in source['stages'][-1]['factors'])
    by={f.id:f for f in factors};ids=('two.outer.3','alternative.T12.square','two.root.0','F3','two.root.1','two.root.2','F9')
    selected=tuple(f for f in factors if f.id in ids);word=product(selected)
    linking=pure_linking_certificate(word,5);ledgers=positive_linking_ledgers(linking['linking_matrix'])
    expected={(((1,2),1),((2,4),1),((3,4),2),((1,2,3),1)),
              (((1,2),2),((1,3),1),((3,4),1),((2,3,4),1))}
    if set(ledgers['ledgers'])!=expected or ledgers['minimum_distinct_supports']!=4:
        raise ValueError('The isolated block needs a new exact ledger assessment')
    # A concrete unchanged-class attempt at the first allowed incidence ledger.
    candidate=(replace(by['alternative.R2'],power=1),replace(by['alternative.T12.square'],power=1),
               by['two.root.1'],replace(by['two.outer.1'],power=2))
    target=exact_action(word,5);orders=[]
    for order in permutations(range(4)):
        actual=tuple(candidate[i] for i in order);action=exact_action(product(actual),5)
        different=next((i for i,(a,b) in enumerate(zip(target,action),1) if a!=b),None)
        if different is None:raise ValueError('A new actual four-record equality must be pursued')
        orders.append(dict(order=order,exact_match=False,first_different_meridian=different,
            source_image=target[different-1],candidate_image=action[different-1]))
    splits=tuple(dict(factor=f,split=split_fixed_last_strand(f.word,5)) for f in selected+candidate)
    total=split_fixed_last_strand(word,5)
    for row in splits:
        if exact_action(row['factor'].word,5)!=exact_action(row['split'].reconstructed_word,5):
            raise ValueError('An individual nonabelian reconstruction failed')
    if exact_action(word,5)!=exact_action(total.reconstructed_word,5):raise ValueError('The block reconstruction failed')
    return dict(source_audit='98312ba: first-half-two-donors, retained endpoint',
        source_canonical_sha256=hashlib.sha256(json.dumps(source,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        selected_factors=selected,full_labeled_linking=linking,positive_ledger_certificate=ledgers,
        three_record_full_twist_endform_excluded=True,
        doubled_edges=((1,2),(3,4)),doubled_edges_disjoint=True,
        unchanged_four_record_probe=dict(candidates=candidate,orders=orders,all24_orders_fail=True,applied=False),
        individual_point_pushing=splits,complete_product_point_pushing=total,
        sphere_moves=0,exterior_caps=0,public_proof_or_payload_changed=False,complete_named_steps=82,
        reached_new_transport=False,complete_shorter_derivation=False,
        scope='The isolated product cannot become three or fewer positive full-twist records by disk product-preserving moves/common conjugation, even through half/power splitting. The two four-support ledgers are only necessary targets. The24 failures concern ONLY the listed unchanged curve classes. Outside interactions, other positive endforms, half-factor endforms and sphere changes are not excluded.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-first-half-ledgers.json'
    p.write_text(json.dumps(r,default=asdict,indent=2)+'\n',encoding='utf-8')
    print('Saved',p,'minimum distinct supports',r['positive_ledger_certificate']['minimum_distinct_supports'])
    print('Two incidence ledgers only; all24 fixed-class orderings fail. Public proof unchanged at82.')
