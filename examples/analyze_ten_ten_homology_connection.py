"""Build the Sp4-only connection without replaying a geometric derivation."""
from pathlib import Path
from dataclasses import asdict,replace
from fractions import Fraction
from hashlib import sha256
import json
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.hyperelliptic_homology import homology_action
from surface_diagrams.ten_ten_homology_connection import homological_sum_connection,known_target_sphere_obstruction

ROOT=Path(__file__).resolve().parents[1]
SOURCE='docs/proofs/fibration-derivations/10-10.json'
PIN='2fd554824c44c1db0e2c570c61e91562677338796ad7f5f559f8d485e8a7c06e'
FOUR_SOURCE='docs/proofs/fibration-derivations/4-3.json'
FOUR_PIN='03f613184dfce7bf7d4f4a9d8569dff68129cc41bc3fbb96cd700459a0012a84'
OUTPUT='docs/proofs/ten-ten-homology-connection.json'

def encode(value):
    if isinstance(value,Fraction):
        if value.denominator!=1:raise ValueError('Every certificate matrix is integral')
        return value.numerator
    return asdict(value)

def report():
    raw=(ROOT/SOURCE).read_bytes()
    if sha256(raw).hexdigest()!=PIN:raise ValueError('Use the exact published twenty-factor source')
    fs=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in json.loads(raw)['factors'])
    r=homological_sum_connection(fs)
    four_raw=(ROOT/FOUR_SOURCE).read_bytes()
    if sha256(four_raw).hexdigest()!=FOUR_PIN:raise ValueError('Keep the published (4,3) source immutable')
    four=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in json.loads(four_raw)['factors'])
    embedded=tuple(replace(f,first=f.first+1,conjugator=tuple((1 if x>0 else -1)*(abs(x)+1) for x in f.conjugator)) for f in four)
    matches=tuple(homology_action(a.word)==homology_action(b.word) for a,b in zip(embedded,r['target_four_three']))
    if len(embedded)!=7 or not all(matches):raise ValueError('Match every target factor in the published (4,3) chart')
    return dict(r,known_target_sphere_obstruction=known_target_sphere_obstruction(fs),source_path=SOURCE,source_sha256=PIN,
        target_four_three_source=FOUR_SOURCE,target_four_three_sha256=FOUR_PIN,
        target_four_three_individual_homology_matches=matches,
        target_six_seven_source='factorization_explorer.initial_factors: original thirteen-factor input',
        formal_matrix_adjacent_checks=len(r['matrix_hurwitz_events']),
        answer_status='The homological monodromy connects to the original (6,7) plus a conjugate (4,3). All120 separating triples in this particular proposed curve lift fail a marked-sphere character. The general Lefschetz-fibration decomposition remains open.')

def build():
    r=report();raw=json.dumps(r,default=encode,separators=(',',':')).encode('utf-8')
    (ROOT/OUTPUT).write_bytes(raw)
    print(json.dumps(dict(bytes=len(raw),sha256=sha256(raw).hexdigest(),matrix_checks=r['formal_matrix_adjacent_checks'],geometric_moves=0)),flush=True)

if __name__=='__main__':build()
