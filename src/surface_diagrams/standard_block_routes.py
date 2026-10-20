"""Explicit standard-block untwisting, with every sphere-only rechart visible.

This implements the single-generator move behind Auroux's Lemmas 6--7.
It does not extract a standard block from the supplied (6,7) factorization.
"""
from dataclasses import replace

from .braid_actions import inverse_word,reduce_word
from .factorization_explorer import Factor,product
from .hyperelliptic_homology import IDENTITY,homology_action
from .mapping_classes import exact_action
from .sphere_actions import sphere_chain_certificate
from .six_seven_structure import research_hurwitz_move


def standard_block_factors(name):
    """Unit half twists for T, W0=T*T, or W1=(12345)^6."""
    t=(1,2,3,4,5,5,4,3,2,1)
    words={'T':t,'W0':t*2,'W1':(1,2,3,4,5)*6}
    if name not in words:raise ValueError('Choose standard block T, W0, or W1')
    return tuple(Factor('%s.%02d'%(name,i+1),(),letter,2,half=True)
                 for i,letter in enumerate(words[name]))


def standard_block_untwisting(name,generator):
    """Replay sigma_i^-1 * F * sigma_i -> F using adjacent Hurwitz moves.

    First expose sigma_i, sweep it to the right, rotate the remaining
    factors across it, use centrality, and undo the exposing moves.
    Centrality holds in closed genus two; it need not hold in B6.
    The one centrality rechart has an independent disk action check,
    exact five-arc sphere certificate and genus-two lift check. T itself
    lifts to the deck involution, while W0 and W1 lift to identity.
    """
    if type(generator) is not int or not 1<=generator<=5:
        raise ValueError('Choose a standard generator 1 through 5')
    standard=standard_block_factors(name);n=len(standard)
    state=tuple(replace(f,conjugator=(-generator,)) for f in standard)
    stages=[dict(kind='start',phase='start',title='Globally conjugated standard block',factors=state)]

    def move(source,target,phase,title):
        nonlocal state
        record=research_hurwitz_move(state,source,target);state=record['factors']
        stages.append(dict(record,phase=phase,title=title))

    index=next(i for i,f in enumerate(standard) if f.first==generator)
    for i in range(index,0,-1):move(i,i-1,'expose','Expose the chosen standard half twist')
    for i in range(n-1):move(i,i+1,'slide','Slide the exposed twist to the bottom, removing the conjugation')
    for i in range(n-2,-1,-1):move(i,i+1,'cycle','Move each preceding neighbor below the transported twist')

    before=(state[0],);after=(standard[index],)
    discrepancy=reduce_word(product(before)+inverse_word(product(after)))
    sphere=sphere_chain_certificate(discrepancy)
    disk_before,disk_after=exact_action(product(before)),exact_action(product(after))
    disk_equal=disk_before==disk_after
    assert sphere['certified'] and homology_action(discrepancy)==IDENTITY
    state=after+state[1:]
    stages.append(dict(kind='disk_rewrite' if disk_equal else 'sphere_rewrite',phase='centrality',
        title='Restore the support using exact disk equality' if disk_equal else
              'SPHERE MOVE: restore the support using genus-two centrality',
        factors=state,local_before=before,local_after=after,
        disk_discrepancy=discrepancy,disk_equality=disk_equal,
        disk_action_certificate=dict(before=disk_before,after=disk_after,equal=disk_equal),
        sphere_certificate=sphere,lift_homology=IDENTITY))
    for i in range(index):move(i,i+1,'restore','Undo the initial exposing moves')

    assert tuple(f.id for f in state)==tuple(f.id for f in standard)
    assert all(not reduce_word(a.word+inverse_word(b.word)) for a,b in zip(state,standard))
    if state!=standard:
        before=state;state=standard
        stages.append(dict(kind='disk_presentation',phase='finish',title='Remove freely cancelling presentation conjugators',
            factors=state,local_before=before,local_after=state,
            disk_word_certificate=dict(method='free reduction',discrepancy=reduce_word(product(before)+inverse_word(product(state))))))
    expected_lift=homology_action(product(standard))
    assert homology_action(product(stages[0]['factors']))==expected_lift
    return dict(block=name,generator=generator,conjugator=(-generator,),stages=tuple(stages),
        reference=standard,source_word=product(stages[0]['factors']),target_word=product(standard),
        product_lift_homology=expected_lift,
        sphere_move_count=sum(s['kind']=='sphere_rewrite' for s in stages),
        all_moves_exact_in_disk=disk_equal,complete_structural_derivation_found=False,
        scope='Explicit untwisting of an already isolated standard block; not the missing (6,7) block extraction',
        source_url='https://arxiv.org/pdf/math/0204285',source='Auroux, Lemmas 6-7, page 4')
