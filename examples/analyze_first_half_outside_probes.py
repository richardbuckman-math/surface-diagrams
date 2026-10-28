"""Reproduce scoped frame and outside-donor failures; change no public replay."""
from dataclasses import asdict, replace
from pathlib import Path
import json

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.disk_intersection import disk_intersection_certificate
from surface_diagrams.early_alternative_transport import _terms
from surface_diagrams.early_boundary_pure import _PositiveReplay, _score
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.named_disk_frames import _transport_factor
from surface_diagrams.point_pushing import split_fixed_last_strand
from surface_diagrams.projected_relations import pc_rose_terms
from surface_diagrams.sphere_actions import sphere_chain_certificate

ROOT = Path(__file__).resolve().parents[1]
FRAME = (4, 4, 2, 3, 4, -2, -1)
Q14 = Factor('target.Q14', (-4, 1, 2, 3), 4, 2)


def factors(stage):
    return tuple(Factor(**dict(f, conjugator=tuple(f['conjugator'])))
                 for f in stage['factors'])


def equal(left, right):
    return exact_action(left.word, 5) == exact_action(right.word, 5)


def donor_audit(root):
    """Disjointness is necessary for ANY internal daisy/rose petal chart."""
    daisy = _terms(root.mapping_class, 'probe.daisy.')
    rose = tuple(Factor('probe.rose.'+str(i), t.conjugator, t.first, t.points)
                 for i, t in enumerate(pc_rose_terms(root.mapping_class)))
    return dict(root=root, target=Q14,
        commutes=exact_action(root.word+Q14.word, 5) == exact_action(Q14.word+root.word, 5),
        intersection_certificate=disk_intersection_certificate(
            root.mapping_class, Q14.mapping_class, strands=5),
        daisy=daisy, rose=rose,
        canonical_petal_matches=dict(daisy=tuple(equal(f,Q14) for f in daisy),
                                    rose=tuple(equal(f,Q14) for f in rose)))


class Probe(_PositiveReplay):
    def check(self, fs):
        try:
            return super().check(fs)
        except ValueError:
            self.rejected = dict(factors=tuple(fs), score=_score(fs),
                                 not_a_reached_state=True)
            raise


def report():
    # Only preserved raw research chapters are sources: no dependency on the
    # changing preferred full route or on Git history in a shallow CI checkout.
    c = json.loads((ROOT/'docs/proofs/six-seven-fifty-blocks/certificate.json').read_text(encoding='utf-8'))
    raw = c['early_alternative_transport']['stages']
    rows = []
    for i in range(46,52):
        stage = raw[i]
        scores = tuple(_score(tuple(_transport_factor(f, FRAME) for f in factors(s)))
                       for s in (stage,)+tuple(stage.get('atomic_steps',())))
        rows.append(dict(raw_stage=i, title=stage['title'], scores=scores,
                         peak=max(s['max_support_word'] for s in scores)))
    left = tuple(_transport_factor(f,FRAME) for f in factors(raw[51]))
    right = tuple(_transport_factor(f,(4,4)) for f in factors(
        c['early_alternative_exterior']['stages'][1]))
    if tuple(f.id for f in left) != tuple(f.id for f in right):
        raise ValueError('The preserved frame-join ancestry changed')
    joins = tuple(dict(id=a.id,left=a,right=b,exact_disk_equal=equal(a,b))
                  for a,b in zip(left,right))
    frame = dict(frame=FRAME, states=rows, literal_join=left==right,
                 individual_join_matches=joins, applied=False,
                 reason='The fixed composed chart exceeds the support bound20')

    source = factors(raw[11]); by = {f.id:f for f in source}
    normal = tuple(_transport_factor(by[name],inverse_word(by['alternative.O1234'].conjugator))
                   for name in ('F3','F9','alternative.S1'))
    source_splits = tuple(dict(factor=f,split=split_fixed_last_strand(f.word,5)) for f in normal)

    r = Probe(source)
    r.drag('F3','F6',title='F3 DOWN across the actual235 root and F6')
    r.drag('F6','alternative.prepare.F5.2',title='Changed F6 UP across the transported235 root')
    end = {f.id:f for f in r.factors}
    checks = []
    for stage in r.stages:
        for state in (stage,)+tuple(stage.get('atomic_steps',())):
            word = product(state['factors']); sphere = sphere_chain_certificate(word)
            lift = homology_action(word)
            if not sphere['certified'] or lift != IDENTITY:
                raise ValueError('A retained disk state failed its separate sphere/lift check')
            checks.append(dict(sphere_certificate=sphere,chosen_lift=lift))
    reached = dict(stages=r.stages,graphical_operations=2,adjacent_checks=3,
        state_sphere_lift_certificates=checks,after_score=_score(r.factors),
        original_half_matches=tuple(dict(id=name,exact_disk_equal=equal(end[name],by[name]))
                                    for name in ('F3','F9')),
        donor=donor_audit(end['alternative.prepare.F5.2']),
        applied_to_public_replay=False)

    up = Probe(source)
    up.drag('F3','alternative.prepare.F5.1',title='F3 UP across35 and the upper235 root')
    try:
        up.drag('F6','alternative.prepare.F5.1',title='F6 UP through three pure neighbors')
    except ValueError as error:
        if str(error) != 'The purification route exceeded its support-word bound of 20':
            raise
        rejected = dict(reason=str(error),completed_operations=len(up.stages)-1,
            completed_stages=up.stages,rejected_configuration=up.rejected,
            donor=donor_audit(next(f for f in up.rejected['factors']
                                 if f.id=='alternative.prepare.F5.1')))
    else:
        raise ValueError('The pinned rejected gather unexpectedly completed')

    hypothetical = []
    for name in ('F8.2','F12'):
        unit = replace(by[name],power=1)
        root = _transport_factor(unit,by['F6'].word)
        hypothetical.append(dict(source_unit=unit,positive_half_transport=by['F6'],
            donor=donor_audit(root),applied=False,requires_transport=True))
    return dict(scope='Scoped DISK research audit; no shortening or orbit exclusion',
        source_alternative_stage=11,frame_merge=frame,source_outer_chart_splits=source_splits,
        reached_outside_route=reached,rejected_opposite_route=rejected,
        hypothetical_unit_transports=hypothetical,public_graphical_payloads_changed=False,
        complete_shorter_derivation=False,sphere_moves=0,half_lantern_applied=False)


if __name__=='__main__':
    result = report()
    path = ROOT/'docs/proofs/six-seven-first-half-outside-probes.json'
    path.write_text(json.dumps(result,default=asdict,indent=2)+'\n',encoding='utf-8')
    print('Saved',path,'bytes',path.stat().st_size)
    print('Fixed-frame peaks',[s['peak'] for s in result['frame_merge']['states']])
    print('The complete89 proof, graphical payloads and PDFs are unchanged.')
