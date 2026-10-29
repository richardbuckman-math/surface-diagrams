"""Small exact residual order audit; no source factorization is changed."""
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_posthalf_cyclic_rose import commutators
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.factorization_explorer import Factor,product
from surface_diagrams.framed_boundary_relations import enclosed_boundaries
from surface_diagrams.hyperelliptic_homology import IDENTITY,homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.outside_half_lantern import _matches
from surface_diagrams.outside_rose_return import _terms
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.posthalf_cyclic_rose import cyclic_pattern
from surface_diagrams.projected_relations import pc_rose_terms
from surface_diagrams.sphere_actions import sphere_chain_certificate
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-third-exterior.json';old=json.loads(path.read_text(encoding='utf-8'));source=tuple(factor_from_data(f) for f in old['route']['factors']);by={f.id:f for f in source};selected=tuple(by[n] for n in ('alternative.return.0','alternative.return.1','alternative.return.2','outer.loan.1'));witnesses=commutators(selected)
    if any(x['left']==x['right'] for x in witnesses):raise ValueError('Retain all FOUR exact nonzero necessary commutators')
    parent=Factor('target.R125',(-4,-3),1,3);rose=_terms(parent.mapping_class,'target.rose.',pc_rose_terms);cyclic,internal=cyclic_pattern(parent,rose,1);actual=tuple(by[n] for n in ('outer.loan.1','outer.loan.2','third.loan.0'))
    if source[7:10]!=actual:raise ValueError('Keep the actual adjacent tail interval')
    matches=_matches(actual,cyclic);discrepancy=reduce_word(product(actual)+inverse_word(parent.word));sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('Retain the unapplied named rose separate disk/sphere/+I checks')
    splits=tuple(dict(actual=f,split=split_fixed_last_strand(f.word,5)) for f in selected+actual+(parent,))
    for x in splits:
        if exact_action(x['actual'].word,5)!=exact_action(x['split'].reconstructed_word,5):raise ValueError('Keep full source/target NONABELIAN kernels AND shadows')
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',source_factors=source,failed_adjacent_four_point_daisy=dict(actual_order=selected,exact_integral_commutators=witnesses,applied=False,scope='Only this unchanged UNIT selected-only DISK Hurwitz/common-frame orbit is excluded from a central-product PC daisy. Outside interactions,new curves,substitutions,splitting and sphere changes remain unexcluded. Nonzero integral witnesses prove inequality;zero would be inconclusive.'),exact_adjacent_tail_rose_target=dict(source_interval=(7,10),actual_inputs=actual,parent=parent,canonical_source_chart=(-4,-3),source_rose=rose,cyclic_inputs=cyclic,internal_cyclic_certificate=internal,individual_matches=matches,disk_discrepancy=discrepancy,sphere_certificate=sphere,chosen_lift=lift,signed_pc_balance=tuple(sum(f.power for f in actual if j in enclosed_boundaries(f.mapping_class,5))-(1 if j in enclosed_boundaries(parent.mapping_class,5) else 0) for j in range(1,6)),applied=False,scope='The ACTUAL adjacent older15,older25,NEW12 match a cyclic PC rose toR125. No contraction,transport,gather or completejoin is applied. The three input units have explicit distinct ancestries;no original consumed12 is silently restored.'),full_source_and_target_point_pushing=splits,actual_source_moves=0,sphere_moves=0,exterior_caps=0,preferred_moves=101,preferred_steps=71,public_replay_changed=False,scope='TARGET/obstruction audit ONLY. Actual source stays2d73third-exterior endpoint;complete preferred101/71 stays SOLVED/UNCHANGED. AllTHREEoddexteriors/donorleftovers remain. No new route,phase,geometric improvement,fourthexterior or named residual closure claimed.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-residual-targets.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Audit only',p.stat().st_size)