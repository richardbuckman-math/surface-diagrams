"""Reproduce the bounded one-unit target and its necessary ordered obstruction."""
from dataclasses import asdict
from pathlib import Path
import json
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.one_unit_half_lantern import audit_one_unit_half_lantern

def report():
 root=Path(__file__).resolve().parents[1]
 c=json.loads((root/'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
 source=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in c['early_alternative_transport']['stages'][22]['factors'])
 return audit_one_unit_half_lantern(source)

if __name__=='__main__':
 r=report();target=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-one-unit-half-lantern.json'
 target.write_text(json.dumps(r,default=asdict,indent=2)+'\n',encoding='utf-8')
 print('Saved',target,'bytes',target.stat().st_size,'peak',r['peak_support_word'],'endpoint',r['after_score'])
 print('Joint chart',r['target']['common_chart'],'root',r['target']['local_after'][0])
 print('The actual four-factor order is NOT a reached half-lantern. Public proof remains99.')
