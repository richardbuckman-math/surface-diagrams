"""Build a genuine (4,3) class target; do not replay or replace the source."""
from dataclasses import asdict
from pathlib import Path
from hashlib import sha256
import json
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.ten_ten_short_target import short_four_three_target

ROOT=Path(__file__).resolve().parents[1]
SOURCE='docs/proofs/fibration-derivations/10-10.json'
PIN='2fd554824c44c1db0e2c570c61e91562677338796ad7f5f559f8d485e8a7c06e'
OUTPUT='docs/proofs/ten-ten-short-four-three-target.json'

def factors(data):return tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in data)

def report():
    raw=(ROOT/SOURCE).read_bytes()
    if sha256(raw).hexdigest()!=PIN:raise ValueError('Use the exact published (10,10) source')
    source=json.loads(raw)
    return dict(short_four_three_target(factors(source['factors']),factors(source['source_exact_blocks'][2])),
        source_path=SOURCE,source_sha256=PIN,reference_source_ref='source_exact_blocks.2',
        source_six_literal_ref='factors: B.1,B.2,B.3,B.4,C.5,C.6',
        status='The seven-factor (4,3) relation and its known-C recognition are complete; supplying/gathering Hstar in the twenty-factor fibration is open.')

def build():
    r=report();raw=json.dumps(r,default=asdict,separators=(',',':')).encode('utf-8')
    (ROOT/OUTPUT).write_bytes(raw)
    print(json.dumps(dict(bytes=len(raw),sha256=sha256(raw).hexdigest(),six_literal=len(r['six_literal_source_records']),
        target_support=len(r['target_supports'][4]),internal_reference_checks=4,source_twenty_moves=0)),flush=True)

if __name__=='__main__':build()
