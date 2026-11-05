"""Reproduce source-pinned necessary fiber-sum tests; no existing proof changes."""
from pathlib import Path
from dataclasses import asdict
from hashlib import sha256
import json
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.ten_ten_summand_audit import (monodromy_homology_audit,
    necessary_two_interchange_target,rejected_geometry_previews,published_nakamura_homology_comparison,published_quotient_parabolics)
ROOT=Path(__file__).resolve().parents[1]
SOURCE='docs/proofs/fibration-derivations/10-10.json'
PIN='2fd554824c44c1db0e2c570c61e91562677338796ad7f5f559f8d485e8a7c06e'

def report():
    raw=(ROOT/SOURCE).read_bytes()
    if sha256(raw).hexdigest()!=PIN:raise ValueError('Use the exact published twenty-factor source')
    source=json.loads(raw)
    factors=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in source['factors'])
    r=monodromy_homology_audit(factors)
    return dict(r,source_path=SOURCE,source_sha256=PIN,
        necessary_target=necessary_two_interchange_target(r),quotient_parabolics=published_quotient_parabolics(r),rejected_previews=rejected_geometry_previews(factors),
        published_comparison=published_nakamura_homology_comparison(),
        applied_moves=0,preferred_proof_changed=False,
        question='Is this specific (10,10) fibration isomorphic to F_(6,7) #_phi A_(4,3), for some summands and gluing phi?',
        answer_status='Open here: no complete reverse equivalence and no indecomposability theorem have been proved.')

def build():
    r=report();p=ROOT/'docs/proofs/ten-ten-fiber-sum-audit.json'
    p.write_bytes(json.dumps(r,default=asdict,separators=(',',':')).encode('utf-8'))
    print(json.dumps(dict(bytes=p.stat().st_size,sha256=sha256(p.read_bytes()).hexdigest(),
        literal_tests=len(r['literal_four_half_tests']),literal_passing=len(r['literal_passing']),
        modular_passing=len(r['modular_passing']),coinvariants=r['monodromy_coinvariants'],
        preview_rejections=[x['failure']['raw_score']['maximum'] for x in r['rejected_previews']],applied_moves=0)),flush=True)
if __name__=='__main__':build()
