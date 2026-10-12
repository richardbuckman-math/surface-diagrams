"""Generate a replayable, exact first (6,7) factor-level derivation checkpoint.

This is a local consolidation inside the original product, not a derivation of
the entire spherical identity. The output is a Factorization Lab session whose
history can be inspected one Hurwitz move at a time.
"""
import json
from pathlib import Path

from surface_diagrams.factorization_explorer import initial_factors, product
from surface_diagrams.factorization_lab import LabServer, validated_session_document
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.sphere_actions import sphere_inner_certificate


OUTPUT = (Path(__file__).resolve().parents[1] / 'src' / 'surface_diagrams' /
          'lab_assets' / 'six-seven-h34-session.json')


def build_session():
    server = LabServer(0)
    original = exact_action(product(initial_factors()))

    def index(factor_id):
        return next(i for i, factor in enumerate(server.history[server.position])
                    if factor.id == factor_id)

    def apply(operation, factor_id=None, **details):
        payload = dict(op=operation, revision=server.revision, **details)
        if factor_id is not None:
            payload['index'] = index(factor_id)
        server.mutate(payload)
        assert exact_action(product(server.history[server.position])) == original

    try:
        # Reverse index order keeps each original identifier easy to locate.
        for factor_id in ('F13', 'F12', 'F10', 'F8', 'F5', 'F4', 'F1'):
            apply('split', factor_id, kind='powers')
        apply('split', 'F1.1', kind='half_lantern')
        apply('split', 'F8.1', kind='half_lantern')
        apply('split', 'F5.1', kind='lantern')

        # The first halves from F1 and F8 are both exactly H34 in B6.
        h_first, h_second = 'F1.1.HL1.1', 'F8.1.HL1.1'
        while index(h_second) > index(h_first) + 1:
            apply('move', h_second, target=index(h_second) - 1)
        apply('combine', h_first)

        # F5's third PC-lantern factor is T34. Bring it beside H34^2.
        pair_twist = 'F5.1.L1.3'
        combined = h_first + '+' + h_second
        while index(pair_twist) > index(combined) + 1:
            apply('move', pair_twist, target=index(pair_twist) - 1)
        apply('combine', combined)

        final = server.history[server.position]
        assert final[0].word == (3, 3, 3, 3)
        assert not final[0].half and final[0].points == 2 and final[0].power == 2
        assert sphere_inner_certificate(product(final))['certified']
        document = json.loads(json.dumps(server.session_document()))
        assert len(document['history']) == 35
        validated_session_document(document, '6-7')
        document['certificate'] = {
            'scope': 'First consolidation toward a (6,7) factor-level derivation; full relation remains open',
            'disk_action_preserved_at_every_step': True,
            'sphere_outer_action_trivial': True,
            'leading_factor': 'T34^2',
            'history_steps': len(document['history']),
        }
        return document
    finally:
        server.server_close()


if __name__ == '__main__':
    result = build_session()
    OUTPUT.write_text(json.dumps(result, separators=(',', ':')) + '\n', encoding='utf-8')
    print(f'Wrote {OUTPUT}: {len(result["history"])} checked states')
