"""Save the actual outside-loan return and two reached cabled lanterns."""
from dataclasses import asdict
from pathlib import Path
import json
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.outside_rose_return import return_outside_rose

def report():
    root=Path(__file__).resolve().parents[1]
    source=json.loads((root/'docs/proofs/six-seven-outside-half-lantern.json').read_text(encoding='utf-8'))['preferred']['factors']
    factors=tuple(Factor(**dict(f,conjugator=tuple(f['conjugator']))) for f in source)
    return return_outside_rose(factors)

if __name__=='__main__':
    r=report();p=Path(__file__).resolve().parents[1]/'docs/proofs/six-seven-outside-rose-return.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:
        json.dump(r,f,default=asdict,indent=2);f.write('\n')
    print(r['graphical_operations'],r['adjacent_checks'],r['peak_support_word'],r['after_score'],r['curve_intersections'])
    print('Saved',p,'bytes',p.stat().st_size,'without changing the complete99 proof.')
