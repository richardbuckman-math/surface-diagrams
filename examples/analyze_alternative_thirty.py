"""Save the separate two-sphere-move audit; no public proof or drawing changes."""
from dataclasses import asdict
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from surface_diagrams.alternative_thirty_audit import audit_alternative_thirty
from surface_diagrams.factorization_explorer import Factor


def build():
    c = json.loads((ROOT / 'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
    fs = tuple(Factor(**dict(x, conjugator=tuple(x['conjugator']))) for x in c['early_alternative_exterior']['factors'])
    report = audit_alternative_thirty(fs)
    output = ROOT / 'docs/proofs/six-seven-alternative-thirty.json'
    output.write_text(json.dumps(report, default=asdict, separators=(',', ':')), encoding='utf-8')
    print('Saved optional audit:', report['sphere_move_count'], 'explicit sphere moves,', len(report['factors']), 'halves; no W1 route claimed')


if __name__ == '__main__': build()