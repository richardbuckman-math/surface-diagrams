"""Build a disk-exact consolidation walkthrough for the supplied twenty factors.

This demonstrates the lab operations. It preserves the transcribed product;
it does not repair its failed sphere closure or prove the intended relation.
"""
import json
from pathlib import Path

from surface_diagrams.factorization_explorer import product
from surface_diagrams.factorization_lab import LabServer, validated_session_document
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.ten_ten import TEN_TEN_FACTORS


OUTPUT = (Path(__file__).resolve().parents[1] / 'src' / 'surface_diagrams' /
          'lab_assets' / 'ten-ten-t45-session.json')


def build_session():
    server = LabServer(seed_slug='10-10')
    original = exact_action(product(TEN_TEN_FACTORS))

    def index(identity):
        return next(i for i, f in enumerate(server.history[server.position]) if f.id == identity)

    def apply(operation, identity=None, **details):
        payload = dict(op=operation, revision=server.revision, **details)
        if identity is not None:
            payload['index'] = index(identity)
        server.mutate(payload)
        if exact_action(product(server.history[server.position])) != original:
            raise ValueError('Walkthrough changed the complete disk action')

    def bring_beside(moving, fixed):
        while index(moving) > index(fixed) + 1:
            apply('move', moving, target=index(moving) - 1)

    try:
        for identity in ('F18', 'F7'):
            apply('split', identity, kind='powers')
        for identity in ('F18.1', 'F7.1'):
            apply('split', identity, kind='half_lantern')
        apply('split', 'F7.2', kind='lantern')

        first, second = 'F7.1.HL1.1', 'F18.1.HL1.1'
        for identity in (first, second):
            if server.history[-1][index(identity)].word != (4,):
                raise ValueError('Expected the standard H45 half twist')
        bring_beside(second, first)
        apply('combine', first)

        combined = first + '+' + second
        pair = 'F7.2.L1.1'
        if exact_action(server.history[-1][index(pair)].word) != exact_action((4, 4)):
            raise ValueError('Expected the standard T45 lantern petal')
        bring_beside(pair, combined)
        apply('combine', combined)
        consolidated = combined + '+' + pair
        while index(consolidated) > 0:
            apply('move', consolidated, target=index(consolidated) - 1)

        final = server.history[-1]
        if final[0].word != (4, 4, 4, 4):
            raise ValueError('Walkthrough did not expose T45 squared')
        document = json.loads(json.dumps(server.session_document()))
        # The immutable source is reconstructed by the selected seed. Avoid
        # repeating its full text in every history state sent to the local API.
        for state in document['history']:
            state.pop('source_transcription', None)
            state.pop('seed_validation', None)
        history, _, _, _, limited = validated_session_document(document, '10-10')
        if limited or history[0] != TEN_TEN_FACTORS:
            raise ValueError('Walkthrough failed its session checks')
        document['certificate'] = dict(
            scope='Local consolidation inside the supplied transcription; sphere closure remains unproved',
            disk_action_preserved_at_every_step=True,
            leading_factor='T45^2',
            history_steps=len(document['history']),
            sphere_outer_action_trivial=False,
        )
        return document
    finally:
        server.server_close()


if __name__ == '__main__':
    result = build_session()
    OUTPUT.write_text(json.dumps(result, separators=(',', ':')) + '\n', encoding='utf-8')
    print(f'Wrote {OUTPUT.name}: {len(result["history"])} checked states')
