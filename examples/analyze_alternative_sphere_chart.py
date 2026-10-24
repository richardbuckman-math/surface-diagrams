"""Save the optional point4 chart and local lantern; public routes are unchanged."""
from dataclasses import asdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from surface_diagrams.alternative_sphere_chart import audit_alternative_point_four
from surface_diagrams.factorization_explorer import Factor


def build():
    source = ROOT / 'docs/proofs/six-seven-fifty-blocks/certificate.json'
    rows = json.loads(source.read_text(encoding='utf-8'))['early_alternative_transport']['factors']
    factors = tuple(Factor(**dict(f, conjugator=tuple(f['conjugator']))) for f in rows)
    report = audit_alternative_point_four(factors)
    output = ROOT / 'docs/proofs/six-seven-alternative-sphere-chart.json'
    output.write_text(json.dumps(report, default=asdict, separators=(',', ':')), encoding='utf-8')
    print('Saved', output, 'normalized power', report['normalized_boundary_power'],
          'PLUS corrections', report['boundary_correction_power'], 'caps', report['boundary_caps'])


if __name__ == '__main__':
    build()
