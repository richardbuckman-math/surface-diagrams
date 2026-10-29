"""A fixed spare crossing simplifies the actual post-half F10 root."""
from .early_boundary_pure import _PositiveReplay,_score
from .factorization_explorer import product
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action
from .outside_half_lantern import _matches
from .point_pushing import split_fixed_last_strand
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate


def _certify(r):
    states=[];adjacent=[]
    for i,s in enumerate(r.stages):
        for j,a in enumerate((s,)+s.get('atomic_steps',())):
            word=product(a['factors']);sphere=sphere_chain_certificate(word);lift=homology_action(word)
            if not sphere['certified'] or lift!=IDENTITY:raise ValueError('Keep separate complete sphere and chosen-lift checks')
            states.append(dict(stage=i,atomic=j,score=_score(a['factors']),sphere_certificate=sphere,chosen_lift=lift))
        if i:
            before=r.stages[i-1]['factors']
            for a in s['atomic_steps']:
                raw=research_hurwitz_move(before,a['source'],a['target'])
                adjacent.append(dict(raw_move=raw,individual_presentations=_matches(raw['factors'],a['factors'])))
                before=a['factors']
    splits=tuple(dict(factor=f,split=split_fixed_last_strand(f.word,5)) for f in r.factors)
    for item in splits:
        if exact_action(item['factor'].word,5)!=exact_action(item['split'].reconstructed_word,5):raise ValueError('Keep every complete nonabelian kernel AND shadow')
    return dict(stages=tuple(r.stages),factors=r.factors,graphical_operations=len(r.stages)-1,adjacent_checks=len(adjacent),actual_adjacent_certificates=tuple(adjacent),state_sphere_lift_certificates=tuple(states),endpoint_point_pushing=splits,before_score=_score(r.stages[0]['factors']),after_score=_score(r.factors),disk_action_verified=True,boundary_power=4,all_factors_positive=True,sphere_moves=0,exterior_caps=0,half_factors=0,negative_factors=0,public_replay_changed=False,useful_complete_join_reached=False)


def gather_posthalf_spare(factors):
    """Reach both bounded crossings, but select only the simpler first endpoint.

    The same15 spare stays literally fixed. First F10 changes; the second
    crossing changes the14 petal and gives back most of the CLOSED reduction.
    Neither endpoint changes the preferred complete derivation.
    """
    source=tuple(factors)
    if len(source)!=15 or any(f.half or f.power!=1 for f in source) or source[0].points!=5 or tuple(f.id for f in source[-4:])!=('alternative.P13','posthalf.supply.1','F10.2','posthalf.output.1'):
        raise ValueError('Use the selected saved15-unit post-half P13 endpoint')
    r=_PositiveReplay(source);r.stages[0]['title']='Selected shorter P13 endpoint, before the spare moves'
    # Check the actual FIRST candidate before applying any part of the gather.
    first=research_hurwitz_move(source,14,13)
    if _score(first['factors'])['max_support_word']>20:raise ValueError('Reject the first crossing before application')
    r.drag('posthalf.output.1','F10.2',title='Carry the SAME15 spare UP once; only F10 becomes simpler')
    selected=_certify(r);before={f.id:f for f in source};after={f.id:f for f in r.factors}
    if any(before[k]!=after[k] for k in before if k!='F10.2'):raise ValueError('Only actual F10 may change in the selected move')
    # The second crossing is independently bounded, reached, and kept as an
    # UNSELECTED complete-gather comparison, never as a failed partial route.
    second=research_hurwitz_move(r.factors,13,12)
    if _score(second['factors'])['max_support_word']>20:raise ValueError('Reject the second crossing before application')
    full=_PositiveReplay(source);full.stages[0]['title']=r.stages[0]['title']
    full.drag('posthalf.output.1','alternative.P13',after=True,title='Full two-neighbor spare-UP gather, retained only as a comparison')
    if full.stages[1]['atomic_steps'][0]['factors']!=selected['factors']:raise ValueError('The selected endpoint must literally be the first complete atomic state')
    alternative=_certify(full)
    if next(f for f in full.factors if f.id=='posthalf.output.1')!=before['posthalf.output.1']:raise ValueError('The spare must stay literally fixed through both crossings')
    selected['selected']=True;alternative['selected']=False
    return dict(selected=selected,complete_gather_alternative=alternative,scope='Both positive disk routes are reached at bound20. The selected one-crossing endpoint improves actual F10 without changing P13 or any other curve. The full gather changes the14 petal and is not preferred. No new named contraction,half,sphere move,cap or useful complete suffix join is claimed; main101moves/71steps remains solved and unchanged.')
