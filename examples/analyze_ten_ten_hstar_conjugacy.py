"""Build the source-pinned B.7-to-Hstar conjugacy; do not replay old proofs."""
from pathlib import Path
from hashlib import sha256
from dataclasses import asdict
import json
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.ten_ten_hstar_conjugacy import source_hstar_conjugacy

ROOT=Path(__file__).resolve().parents[1]
SOURCE='docs/proofs/fibration-derivations/10-10.json'
PIN='2fd554824c44c1db0e2c570c61e91562677338796ad7f5f559f8d485e8a7c06e'
TARGET='docs/proofs/ten-ten-short-four-three-target.json'
TARGET_PIN='bc349407881635661a5435a5c59f00377e8bf56484855b9830ec8dc10b827a4b'
OUTPUT='docs/proofs/ten-ten-hstar-source-conjugacy.json'
def factors(records):return tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in records)

def report():
    a=(ROOT/SOURCE).read_bytes();b=(ROOT/TARGET).read_bytes()
    if sha256(a).hexdigest()!=PIN or sha256(b).hexdigest()!=TARGET_PIN:raise ValueError('Preserve both immutable source pins')
    s=json.loads(a);t=json.loads(b)
    return dict(source_hstar_conjugacy(factors(s['factors']),factors(t['reference_C_factors']),factors(t['target_factors'])),
        source_path=SOURCE,source_sha256=PIN,target_report_path=TARGET,target_report_sha256=TARGET_PIN,
        status='Exact source B.7 G-conjugacy to Hstar is complete; an actual bounded positive Hurwitz supply/gather and the reverse LF decomposition remain open.')

def build():
    r=report();data=json.dumps(r,default=asdict,separators=(',',':')).encode('utf-8');(ROOT/OUTPUT).write_bytes(data)
    print(json.dumps(dict(bytes=len(data),sha256=sha256(data).hexdigest(),source_ancestry=r['source_half'].id,
        group_word_letters=len(r['source_group_conjugator']),group_occurrences=r['group_factor_occurrences'],endpoint_support=18,source_moves=0)),flush=True)

if __name__=='__main__':build()
