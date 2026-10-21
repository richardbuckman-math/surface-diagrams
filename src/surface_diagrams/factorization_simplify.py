"""Small exact Hurwitz/global-conjugation improvements of supported factors.

The score measures presentation lengths and horizontal-cut visits, not minimal
pairwise geometric intersection. A local minimum is not an optimality claim.
This uses disk equalities only; no sphere substitutions are hidden in it.
"""
from dataclasses import replace
from functools import lru_cache

from .braid_actions import reduce_word
from .cyclic_factorizations import rotate_factors
from .factorization_explorer import initial_factors
from .mapping_classes import supported_class
from .six_seven_structure import research_hurwitz_move
from .sphere_support_compact import reframe_factors
from .twist_simplify import simplify_twist
from .twist_supports import support_curve


@lru_cache(maxsize=8192)
def _shorten(factor):
    twist = simplify_twist(factor.mapping_class)
    return replace(factor, conjugator=twist.conjugator, first=twist.first)


def complexity(factors, *, max_cuts=24):
    depths = tuple(len(f.conjugator) for f in factors)
    cuts = tuple(len(support_curve(f.mapping_class).cuts) for f in factors)
    if not depths or max(cuts) > max_cuts:
        raise ValueError('Factorization exceeds its support cut cap or is empty')
    return (sum(depths), max(depths), sum(cuts), max(cuts))


def _normalize(factors):
    after = tuple(map(_shorten, factors))
    certificates = []
    for before, new in zip(factors, after):
        if before != new:
            if ((before.id,before.points,before.power,before.half) !=
                    (new.id,new.points,new.power,new.half) or
                    supported_class(before.mapping_class) != supported_class(new.mapping_class)):
                raise ValueError('Disk support normalization failed')
            certificates.append(dict(before=before, after=new,
                                     disk_support_class=supported_class(new.mapping_class)))
    return after, certificates


def apply_simplification(factors, kind, args):
    """One recorded move, followed by checked disk support normalizations."""
    if kind == 'disk_hurwitz':
        if len(args) != 2:
            raise ValueError('A Hurwitz move needs two adjacent positions')
        certificate = research_hurwitz_move(factors, *args)
    elif kind == 'global_conjugation':
        certificate = reframe_factors(factors, args)
    elif kind == 'cyclic_hurwitz':
        if len(args) != 3:
            raise ValueError('A cyclic Hurwitz move needs a rotation and two adjacent positions')
        rotation = rotate_factors(factors,args[0])
        hurwitz = research_hurwitz_move(rotation['factors'],*args[1:])
        certificate = dict(kind=kind,rotation=rotation,hurwitz=hurwitz,
                           factors=hurwitz['factors'],frame=rotation['frame'])
    else:
        raise ValueError('Only disk Hurwitz moves and explicit global conjugation, including cyclic starts, are allowed')
    after, normalizations = _normalize(certificate['factors'])
    return dict(kind=kind, args=tuple(args), factors=after, certificate=certificate,
                disk_normalizations=normalizations)


def replay_simplification(factors, moves, *, max_cuts=24):
    """Reconstruct an exact, strictly improving route from its move list."""
    original = tuple(factors)
    state, normalizations = _normalize(original)
    frame = ()
    stages = [dict(kind='start', title='Original (6,7)', factors=original,
                   score=complexity(original,max_cuts=max_cuts), frame=())]
    if state != original:
        stages.append(dict(kind='disk_support',title='Shorten disk support conjugators',
                           factors=state,score=complexity(state,max_cuts=max_cuts),frame=frame,
                           disk_normalizations=normalizations))
    for kind,args in moves:
        before = state
        record = apply_simplification(state,kind,tuple(args))
        state = record['factors']
        score = complexity(state,max_cuts=max_cuts)
        if score >= complexity(before,max_cuts=max_cuts):
            raise ValueError('Simplification move does not improve the declared score')
        if kind == 'global_conjugation':
            frame = reduce_word(tuple(args)+frame)
            title = 'Global conjugation by ' + ' '.join(map(str,args))
        elif kind == 'cyclic_hurwitz':
            frame = reduce_word(record['certificate']['frame']+frame)
            title = 'Change circular starting point, then an adjacent Hurwitz move'
        else:
            title = 'Move ' + before[args[0]].id + (' down' if args[0]<args[1] else ' up')
        stages.append(dict(record,title=title,score=score,frame=frame))
    return dict(stages=tuple(stages),frame=frame,max_cuts=max_cuts,
                method='bounded disk Hurwitz/global conjugation with cyclic starts',
                sphere_moves=0,globally_optimal=False)


def six_seven_simplification():
    """Replay the checked improvements, including the October 21 short frame."""
    return replay_simplification(initial_factors(),(
        ('disk_hurwitz',(2,3)), ('global_conjugation',(-3,)),
        ('global_conjugation',(5,)), ('disk_hurwitz',(6,7)),
        ('disk_hurwitz',(7,8)), ('global_conjugation',(2,3,2))))


def greedy_simplify(factors, *, max_steps=14, max_cuts=24, include_cyclic=True):
    """Bounded adjacent-move/single-generator descent, with a replayable plan.

    A temporary increase in the largest conjugator is permitted when the
    total decreases; the hard geometric drawing cap remains in force.
    """
    if type(max_steps) is not int or max_steps < 0:
        raise ValueError('max_steps must be a nonnegative integer')
    original = tuple(factors)
    state,_ = _normalize(original)
    plan = []
    for _ in range(max_steps):
        current = complexity(state,max_cuts=max_cuts)
        moves = [('disk_hurwitz',(a,b)) for i in range(len(state)-1)
                 for a,b in ((i,i+1),(i+1,i))]
        moves += [('global_conjugation',(g,)) for g in (*range(1,6),*range(-5,0))]
        if include_cyclic and len(state)>1:
            # Every ordinary adjacency is already present. Changing the start
            # once exposes the sole missing last/first adjacency; considering
            # all n rotations would repeat the same circular neighborhood.
            last=len(state)-1
            moves += [('cyclic_hurwitz',(1,a,b)) for a,b in
                      ((last-1,last),(last,last-1))]
        options = []
        for kind,args in moves:
            try:
                record = apply_simplification(state,kind,args)
                score = complexity(record['factors'],max_cuts=max_cuts)
            except ValueError:
                continue
            if score < current:
                options.append((score,kind,args,record['factors']))
        if not options:
            break
        _,kind,args,state = min(options,key=lambda option: option[:3])
        plan.append((kind,args))
    return replay_simplification(original,plan,max_cuts=max_cuts)
