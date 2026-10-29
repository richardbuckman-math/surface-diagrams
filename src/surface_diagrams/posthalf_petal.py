"""One reached positive petal interchange shortens the post-half P13 curve."""
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import product
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action,supported_class
from .outside_half_lantern import _matches
from .point_pushing import split_fixed_last_strand
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def simplify_posthalf_P13(factors):
    """Keep W fixed, carry it UP once, and change only the actual P13 curve.

    This extends the separate post-combine research branch. It neither changes
    the preferred proof nor supplies the branch's missing complete suffix join.
    """
    source=tuple(factors)
    if len(source)!=15 or any(f.half or f.power!=1 for f in source) or source[0].points!=5 or any(f.points!=2 for f in source[10:12]) or tuple(f.id for f in source[10:12])!=('alternative.P13','posthalf.supply.0'):
        raise ValueError('Use the saved15-unit post-half exterior endpoint')
    r=_PositiveReplay(source);r.stages[0]['title']='Post-half exterior endpoint before the P13 petal interchange'
    r.drag('posthalf.supply.0','alternative.P13',title='Carry W UP one neighbor; the actual P13 support becomes shorter')
    raw=research_hurwitz_move(source,11,10);presentations=_matches(raw['factors'],r.factors)
    before={f.id:f for f in source};after={f.id:f for f in r.factors}
    if set(before)!=set(after) or any(before[k]!=after[k] for k in before if k!='alternative.P13'):
        raise ValueError('Only P13 may change; W and all other actual records stay fixed')
    old,new=before['alternative.P13'],after['alternative.P13']
    lengths=tuple(len(supported_class(f.mapping_class,5)) for f in (old,new))
    if lengths[1]>=lengths[0]:raise ValueError('This source did not give the claimed shorter P13 support')
    certificates=[]
    for i,s in enumerate(r.stages):
        for j,a in enumerate((s,)+s.get('atomic_steps',())):
            w=product(a['factors']);sphere=sphere_chain_certificate(w);lift=homology_action(w)
            if not sphere['certified'] or lift!=IDENTITY:raise ValueError('Retain separate complete sphere/lift checks')
            certificates.append(dict(stage=i,atomic=j,score=_score(a['factors']),sphere_certificate=sphere,chosen_lift=lift))
    kernels=tuple(dict(factor=f,split=split_fixed_last_strand(f.word,5)) for f in r.factors)
    for item in kernels:
        if exact_action(item['factor'].word,5)!=exact_action(item['split'].reconstructed_word,5):raise ValueError('Keep the complete nonabelian kernel AND shadow')
    return dict(stages=tuple(r.stages),factors=r.factors,graphical_operations=1,adjacent_checks=1,
        before_P13=old,after_P13=new,P13_support_lengths=lengths,fixed_W=before['posthalf.supply.0'],
        raw_adjacent_move=raw,individual_presentation_matches=presentations,state_sphere_lift_certificates=tuple(certificates),endpoint_point_pushing=kernels,
        before_score=_score(source),after_score=_score(r.factors),half_factors=0,negative_factors=0,sphere_moves=0,exterior_caps=0,
        public_replay_changed=False,useful_complete_join_reached=False,
        scope='One positive disk interchange on the reached research branch. W stays literally fixed; only P13 changes curve class. It is not a shorter or newly adopted complete derivation. The visible odd exterior stays present, and the main101-move/71-step proof remains solved and unchanged.')
