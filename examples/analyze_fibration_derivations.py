"""Generate the complete self-contained certificates for three small fibrations."""
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path
import json
from surface_diagrams.small_fibration_derivations import all_derivations
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/proofs/fibration-derivations'

def reports():
    archive=ROOT/'docs/proofs/fibration-sources/planar-mcg-2026-10-30'
    pins=json.loads((archive/'provenance.json').read_bytes())
    for x in pins['files']:
        if sha256((archive/x['archive_relative_path']).read_bytes()).hexdigest()!=x['sha256']:
            raise ValueError('An imported source archive changed')
    source=ROOT/'src/surface_diagrams/_fibration_source_records.py'
    for slug,r in all_derivations().items():
        yield slug,dict(r,source_provenance=pins,native_source_records_sha256=sha256(source.read_bytes()).hexdigest(),
            imported_factor_records_sha256=sha256((archive/'factor-records.json').read_bytes()).hexdigest(),
            native_implementation='src/surface_diagrams/small_fibration_derivations.py',
            mathematical_count_scope='Operations are the displayed macro steps; external adjacent checks are counted separately. Complete internal named-rule checks remain in their own witnesses. Assembly/context changes and equal-product moves have distinct kinds.',
            picture_scope='Individual actual supports and chart-word lengths; not a simultaneous joint cut system, an arc-intersection count, a jointly minimal drawing or a whole-proof tangle bound.')

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    for slug,r in reports():
        p=OUT/(slug+'.json');p.write_text(json.dumps(r,default=asdict,separators=(',',':')),encoding='utf-8')
        print(json.dumps(dict(slug=slug,bytes=p.stat().st_size,sha256=sha256(p.read_bytes()).hexdigest(),
            steps=r['operations'],listed=r['listed_operations'],external_checks=r['adjacent_checks'],profile=r['profile'],peak=r['local_peak'])),flush=True)
if __name__=='__main__':build()
