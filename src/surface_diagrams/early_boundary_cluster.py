"""A positive cluster-lantern contraction in the early five-point chart.

This is a named geometric advance toward the remaining boundary relation,
not a claim that the full elementary derivation is finished or shorter.
"""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .factorization_explorer import Factor, product
from .mapping_classes import exact_action, supported_class
from .projected_relations import pc_daisy_terms
from .six_seven_structure import research_hurwitz_move
from .twist_simplify import simplify_twist
from .puncture_boundary import BOUNDARY_WORD


def positive_early_cluster(factors):
    """Expose Q14 positively and contract Q14, C8, C10 by their PC lantern.

    The round R123^2 supplies K=sigma2 sigma1. Moving K upward takes the
    first pair curve to exactly Q14. Carry Q down, then reorder the root
    pair before moving it over F6. This avoids a support-word peak of 40;
    the accepted route stays at most 20. No inverse factor or sphere move
    occurs. The endpoint contains the first four-point daisy curve.
    """
    state=tuple(factors)
    expected_ids=('prefix.P45','prefix.P12','F4','F3','F5','F6','F8.1',
                  'F10.1','F8.2','F9','F10.2','F11','F12','F13')
    if tuple(f.id for f in state)!=expected_ids or any(getattr(f,'sign',1)!=1 for f in state):
        raise ValueError('Use the positive early fourth-boundary chart in its working order')
    expected=exact_action(BOUNDARY_WORD*4,5)
    if exact_action(product(state),5)!=expected:
        raise ValueError('The source is not the independently checked fourth boundary power')
    stages=[dict(kind='start',title='The fourteen-factor early disk relation',factors=state)]

    def score(fs):
        ls=tuple(len(supported_class(f.mapping_class,5)) for f in fs)
        return dict(max_support_word=max(ls),total_support_word=sum(ls),braid_letters=len(product(fs)))

    def normalize(fs):
        out=[]
        for f in fs:
            t=simplify_twist(f.mapping_class,strands=5)
            n=replace(f,conjugator=t.conjugator,first=t.first)
            if exact_action(f.word,5)!=exact_action(n.word,5):
                raise ValueError('A disk presentation changed its supported factor')
            out.append(n)
        return tuple(out)

    def checked(fs):
        fs=normalize(tuple(fs))
        if exact_action(product(fs),5)!=expected:
            raise ValueError('The positive cluster route changed its exact disk product')
        if any(getattr(f,'sign',1)!=1 for f in fs) or score(fs)['max_support_word']>20:
            raise ValueError('The positive cluster route exceeded its positivity or support bound')
        return fs

    def adjacent(source,target):
        nonlocal state
        old=state;record=research_hurwitz_move(state,source,target)
        state=checked(record['factors'])
        return dict(record,factors=state,title=old[source].id+
            (' up past ' if source>target else ' down past ')+old[target].id)

    h=lambda name,i:Factor(name,(),i,2,half=True)
    terms=(h('early.K.2',2),h('early.K.1',1),Factor('early.R123.remaining',(),1,3),
           h('early.tail.1',1),h('early.tail.2',2),Factor('early.tail.T12',(),1,2))
    if exact_action(state[2].word,5)!=exact_action(product(terms),5):
        raise ValueError('The round square does not expose the declared K block')
    before=(state[2],);state=checked(state[:2]+terms+state[3:])
    stages.append(dict(kind='disk_split',title='Expose K = sigma2 sigma1 from the round squared twist',
        factors=state,local_before=before,local_after=terms,
        explanation='R123^2 = K R123 (sigma1 sigma2 sigma1^2), using the three-strand braid relation.'))

    atomic=[]
    for source,target in ((2,1),(1,0),(3,2),(2,1)):
        atomic.append(adjacent(source,target))
    q=Factor('prefix.P45',(-4,1,2,3),4,2)
    p=Factor('prefix.P12',(),2,2)
    if any(exact_action(a.word,5)!=exact_action(b.word,5) for a,b in zip(state[2:4],(q,p))):
        raise ValueError('The K transport did not expose the exact required Q14')
    state=checked(state[:2]+(q,p)+state[4:])
    stages.append(dict(kind='disk_hurwitz_block',title='Carry K up across the first two pair twists',
        factors=state,adjacent_moves=4,atomic_steps=tuple(atomic),
        explanation='K^-1 P34 K = Q14 and K^-1 T12 K = T23, checked in B5.'))

    atomic=[]
    for i in range(7): atomic.append(adjacent(2+i,3+i))
    stages.append(dict(kind='disk_hurwitz_block',title='Drag the required Q14 down across seven neighbors',
        factors=state,adjacent_moves=7,atomic_steps=tuple(atomic)))
    for source,target in ((12,11),(11,10),(12,11)):
        stages.append(adjacent(source,target))

    # The root order is B, B^-1 A B. Its ordered product is A B, so the
    # transported PC lantern Q A B = O1345 P35 applies without an inverse.
    outer=Factor('early.O1345',(1,),2,4)
    inner=Factor('early.P35',(-4,),3,2)
    before=state[9:12];after=(outer,inner)
    if exact_action(product(before),5)!=exact_action(product(after),5):
        raise ValueError('The reordered positive cluster lantern failed its exact disk check')
    state=checked(state[:9]+after+state[12:])
    stages.append(dict(kind='disk_cluster_lantern',
        title='PC cluster lantern: Q14 and the two roots become O1345 and P35',
        factors=state,local_before=before,local_after=after,
        explanation='The three inner clusters are {1}, {4}, and the routed pair {3,5}.'))
    daisy=pc_daisy_terms(outer.mapping_class)
    if exact_action(outer.word,5)!=exact_action(tuple(x for t in daisy for x in t.word),5):
        raise ValueError('The new four-point curve failed its next PC daisy certificate')
    return dict(stages=tuple(stages),factors=state,graphical_steps=7,
        sphere_move_count=0,all_factors_positive=True,boundary_power=4,
        disk_action_verified=True,before_score=score(factors),after_score=score(state),
        peak_support_bound=20,complete_named_derivation=False,
        next_daisy=dict(outer=outer,terms=daisy,exact_disk_equality=True,applied_to_replay=False),
        scope='Seven positive disk operations expose one four-point daisy curve; the complete named fourth-boundary derivation remains open.')
