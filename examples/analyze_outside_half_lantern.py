"""Save the reached outside-petal half-lantern in both exact disk charts."""
from pathlib import Path
from dataclasses import asdict
import json
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.outside_half_lantern import reach_outside_half_lantern

def report():
 root=Path(__file__).resolve().parents[1]
 c=json.loads((root/'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
 source=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in c['early_alternative_transport']['stages'][22]['factors'])
 return dict(preferred=reach_outside_half_lantern(source),original_chart=reach_outside_half_lantern(source,round_chart=False),
             public_proof_steps=99,public_graphical_payloads_changed=False)

if __name__=='__main__':
 r=report();p=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-outside-half-lantern.json'
 with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,indent=2);f.write('\n')
 for name in ('preferred','original_chart'):
  a=r[name];print(name,a['graphical_operations'],a['adjacent_checks'],a['peak_support_word'],a['after_score'],a['curve_intersections'])
 print('Saved',p,'bytes',p.stat().st_size,'without changing the complete99-step proof or PDFs.')
