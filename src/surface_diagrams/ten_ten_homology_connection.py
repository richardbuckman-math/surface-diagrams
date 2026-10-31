"""An explicit Sp4(Z) connection, not a Lefschetz-fibration equivalence.

Separator matrices are I here; their Torelli actions are not discarded in any
claimed geometric route, because no geometric route is asserted or applied.
"""
from fractions import Fraction
from itertools import product as cartesian
from dataclasses import replace
from .factorization_explorer import initial_factors
from .small_fibration_derivations import source_factors
from .hyperelliptic_homology import (IDENTITY, homology_action, half_twist_class,
    _twist, _multiply, homology_quotient)
from .ten_ten_summand_audit import pairing


def homological_sum_connection(factors):
    """Check this source-specific connection after taking integral homology.

    The caller pins the actual twenty-factor source. The returned 134 formal
    matrix Hurwitz operations are not bounded curve moves or a seven-factor
    sphere relation. Independent integral symplectic maps identify the two
    resulting matrix blocks with the original (4,3) and (6,7) monodromies.
    """
    fs=tuple(factors)
    if len(fs)!=20 or sum(f.half for f in fs)!=10:
        raise ValueError('Use the specified twenty-factor (10,10) source')
    if any(not ((f.half and f.points==2 and f.power==1) or
                (not f.half and f.points==3 and f.power==2)) for f in fs):
        raise ValueError('Use unit halves and squared separating triple twists')
    if any(homology_action(f.word)!=IDENTITY for f in fs if not f.half):
        raise ValueError('Separating factors must act trivially on homology')
    def integral(x):
        assert not isinstance(x,Fraction) or x.denominator==1
        return int(x)
    def mv(m,v):return tuple(integral(sum(m[i][j]*v[j] for j in range(4))) for i in range(4))
    def inverse(m):
        a=[list(map(Fraction,row))+list(map(Fraction,IDENTITY[i])) for i,row in enumerate(m)]
        for j in range(4):
            k=next(i for i in range(j,4) if a[i][j]);a[k],a[j]=a[j],a[k]
            divisor=a[j][j];a[j]=[x/divisor for x in a[j]]
            for i in range(4):
                if i!=j:
                    q=a[i][j];a[i]=[x-q*y for x,y in zip(a[i],a[j])]
        return tuple(tuple(row[4:]) for row in a)
    def columns(vs):return tuple(tuple(vs[j][i] for j in range(4)) for i in range(4))
    def total(records):
        m=IDENTITY
        for r in records:m=_multiply(m, r['matrix'])
        return m
    def record(f):
        v=half_twist_class(f.conjugator,f.first) if f.half else None
        return dict(id=f.id,vector=v,matrix=homology_action(f.word),half=f.half)
    start=tuple(record(f) for f in fs)
    states=[start];events=[]
    def move(source,target,reason):
        assert abs(source-target)==1
        old=states[-1];a,b=old[min(source,target):max(source,target)+1]
        if source<target:
            c=dict(b,matrix=_multiply(_multiply(a['matrix'],b['matrix']),inverse(a['matrix'])))
            c['vector']=None if b['vector'] is None else mv(a['matrix'],b['vector'])
            local=(c,a)
        else:
            c=dict(a,matrix=_multiply(_multiply(inverse(b['matrix']),a['matrix']),b['matrix']))
            c['vector']=None if a['vector'] is None else mv(inverse(b['matrix']),a['vector'])
            local=(b,c)
        c['matrix']=tuple(tuple(integral(x) for x in row) for row in c['matrix'])
        for r in local:
            assert r['matrix']==(_twist(r['vector'],1) if r['half'] else IDENTITY)
        k=min(source,target);following=old[:k]+local+old[k+2:]
        assert total(old)==total(following)==IDENTITY
        events.append(dict(kind='adjacent_matrix_hurwitz',source=source,target=target,reason=reason,local_before=(a,b),local_after=local,
            all_twenty_matrices_retained=True,geometric_move_applied=False))
        states.append(following)

    def cyclic(start,size,cut,reason):
        before=states[-1][start:start+size]
        assert total(before)==IDENTITY
        for _ in range(cut):
            for j in range(start,start+size-1):
                move(j+1,j,reason)
        following=states[-1][start:start+size]
        expected=before[cut:]+before[:cut]
        assert [(r['id'],r['matrix']) for r in following]==[(r['id'],r['matrix']) for r in expected]

    def arrange_identity_slots(start,size,template,reason):
        before=states[-1][start:start+size]
        halves=iter(r['id'] for r in before if r['half'])
        seps=iter(r['id'] for r in before if not r['half'])
        desired=tuple(next(halves) if f.half else next(seps) for f in template)
        for j,name in enumerate(desired,start):
            i=next(i for i,r in enumerate(states[-1]) if r['id']==name)
            while i>j:
                assert any(r['matrix']==IDENTITY for r in states[-1][i-1:i+1])
                move(i,i-1,reason)
                i-=1
        assert [r['id'] for r in states[-1][start:start+size]]==list(desired)

    # These are the already known necessary matrix target, not a new geometric
    # test of its rejected/unapplied gap lifts.
    for source,target in ((11,10),(15,14),(14,13),(13,12),(12,11)):
        move(source,target,'Load the known two-half necessary target in the matrix quotient only')
    chosen={'four_three_B.1','four_three_B.2','four_three_B.3','four_three_B.4',
        'four_three_A.6','four_three_C.5','four_three_C.6'}
    selected_order=tuple(r['id'] for r in states[-1] if r['id'] in chosen)
    for j,name in enumerate(selected_order):
        i=next(i for i,r in enumerate(states[-1]) if r['id']==name)
        while i>j:
            move(i,i-1,'Formal matrix gather of the selected seven slots; no curve gather')
            i-=1
    gathered=states[-1];S,R=gathered[:7],gathered[7:]
    assert total(S)==total(R)==IDENTITY
    gathered_halves=tuple(r['vector'] for r in R if r['half'])
    expected=((1,1,1,-1),(1,7,3,-1),(3,24,10,-3),(1,10,4,-1),(0,3,1,0),(-2,1,-1,2))
    assert gathered_halves==expected

    # One internal matrix interchange simplifies each block. Full curve
    # interchanges at these slots have not been bounded or applied.
    move(5,6,'Selected four-half matrix normalization')
    assert [r['id'] for r in states[-1][:7] if r['half']]==['four_three_B.3','four_three_A.6','four_three_C.6','four_three_C.5']
    # Rotate the identity matrix block to its A.6 slot, then move its three
    # identity separator matrices to the standard A positions. These are only
    # equalities/permutations of matrix factorizations.
    target4=tuple(replace(f,first=f.first+1,conjugator=tuple((1 if x>0 else -1)*(abs(x)+1) for x in f.conjugator)) for f in source_factors('four_three_A'))
    cyclic(0,7,4,'Selected identity matrix block cyclic start, fully expanded as matrix Hurwitz moves')
    arrange_identity_slots(0,7,target4,'Reposition only separator identity matrices in the selected block')
    left=states[-1][:7]

    right=states[-1][7:]
    right_half_ids=[r['id'] for r in right if r['half']]
    # Move the first B.5 half down over B.6 in the residual block.
    a_id,b_id=right_half_ids[1:3]
    ia=next(i for i,r in enumerate(states[-1]) if r['id']==a_id)
    ib=next(i for i,r in enumerate(states[-1]) if r['id']==b_id)
    assert ib==ia+1
    move(ia,ib,'Residual six-half matrix normalization: B.5 down over B.6')
    right=states[-1][7:]
    # In the half-only matrix quotient, carry the width16 half up twice.
    # Any intervening separator matrices equal I and are moved explicitly.
    name='new.half-lantern.2'
    i=next(i for i,r in enumerate(states[-1]) if r['id']==name)
    outside=tuple(r['id'] for r in states[-1][7:i] if r['half'])[-2:]
    target_name=outside[0]
    j=next(i for i,r in enumerate(states[-1]) if r['id']==target_name)
    while i>j:
        move(i,i-1,'Residual matrix normalization: carry width16 half up across two halves and all separator identities')
        i-=1
    right=states[-1][7:]
    cut=next(i for i,r in enumerate(right) if r['half'])+1
    cyclic(7,13,cut,'Residual identity matrix block cyclic start, fully expanded as matrix Hurwitz moves')
    target6=initial_factors()
    arrange_identity_slots(7,13,target6,'Reposition only separator identity matrices in the residual block')
    right=states[-1][7:]
    assert total(right)==IDENTITY

    # Pair bases read directly from the resulting vectors. Vector signs never
    # affect the represented transvection.
    u=(1,-2,0,-1);v=(0,2,1,0)
    new4=(tuple(-u[i]+2*v[i] for i in range(4)),tuple(u[i]-v[i] for i in range(4)))
    new6=((1,4,2,-1),(0,3,1,0))
    old4=tuple(half_twist_class(f.conjugator,f.first) for f in target4 if f.half)[:2]
    old6=tuple(half_twist_class(f.conjugator,f.first) for f in target6 if f.half)[:2]

    def symplectic_pair_map(source,target,source_complement,target_complement):
        assert pairing(*source)==pairing(*target)==pairing(*source_complement)==pairing(*target_complement)
        assert all(pairing(a,b)==0 for a in source for b in source_complement)
        assert all(pairing(a,b)==0 for a in target for b in target_complement)
        inv_source=inverse(columns(source+source_complement))
        choices=[]
        for a,b,c,e in cartesian(range(-4,5),repeat=4):
            if a*e-b*c!=1:continue
            x,y=target_complement
            complement=(tuple(a*x[i]+c*y[i] for i in range(4)),tuple(b*x[i]+e*y[i] for i in range(4)))
            m=_multiply(columns(target+complement),inv_source)
            if any(x.denominator!=1 for row in m for x in row):continue
            m=tuple(tuple(int(x) for x in row) for row in m)
            unit=tuple(tuple(int(i==j) for i in range(4)) for j in range(4))
            assert all(pairing(mv(m,p),mv(m,q))==pairing(p,q) for p in unit for q in unit)
            assert tuple(mv(m,z) for z in source)==target
            choices.append((sum(abs(x) for row in m for x in row),m,((a,b),(c,e))))
        assert choices
        _,m,completion=min(choices)
        return dict(matrix=m,inverse=inverse(m),source_pair=source,target_pair=target,
            source_complement=source_complement,target_complement=target_complement,complement_SL2=completion)

    map4=symplectic_pair_map(new4,old4,((0,-1,1,0),(2,2,0,1)),((0,-1,1,0),(2,0,0,1)))
    map6=symplectic_pair_map(new6,old6,((0,-1,1,0),(-3,-2,0,-1)),((0,3,1,0),(-1,2,0,1)))
    for state,target,m in ((left,target4,map4['matrix']),(right,target6,map6['matrix'])):
        assert len(state)==len(target)
        for r,f in zip(state,target):
            actual=_multiply(_multiply(m,r['matrix']),inverse(m))
            assert actual==homology_action(f.word),(r['id'],f.id,actual)
    gluing=_multiply(map6['matrix'],map4['inverse'])
    assert all(isinstance(x,int) or x.denominator==1 for row in gluing for x in row)
    gluing=tuple(tuple(integral(x) for x in row) for row in gluing)
    after_global=tuple(dict(r,matrix=_multiply(_multiply(map6['matrix'],r['matrix']),map6['inverse']),
        vector=None if r['vector'] is None else mv(map6['matrix'],r['vector'])) for r in states[-1])
    target_matrices=tuple(_multiply(_multiply(gluing,homology_action(f.word)),inverse(gluing)) for f in target4)+tuple(homology_action(f.word) for f in target6)
    assert tuple(r['matrix'] for r in after_global)==target_matrices
    assert total(after_global)==IDENTITY
    out=dict(input_factors=fs,matrix_states=states,matrix_hurwitz_events=events,
        matrix_gathered_state=gathered,selected_seven=S,residual_thirteen=R,
        selected_lattice=homology_quotient(tuple(r['vector'] for r in S if r['half'])),
        residual_lattice=homology_quotient(tuple(r['vector'] for r in R if r['half'])),
        selected_normalized_matrices=left,residual_normalized_matrices=right,
        selected_to_original_four_three=map4,residual_to_original_six_seven=map6,
        relative_homology_gluing_matrix=gluing,target_four_three=target4,target_six_seven=target6,
        final_global_matrix=map6['matrix'],after_global_conjugation=after_global,target_twenty_matrices=target_matrices,
        applied_geometric_moves=0,full_seven_factor_sphere_identity_proved=False,
        full_residual_sphere_identity_proved=False,fibration_equivalence_proved=False,
        scope='Explicit connection only after applying the Sp4(Z) homology representation. All twenty matrices are retained throughout the formal gathers. The three separator identities convey no Torelli information. The seed is the saved homology target whose geometric lifts were rejected/unapplied. No curve gather, bounded geometric route, genus-two seven-factor identity, new actual (6,7), or fibration isomorphism is asserted.')
    return out


def known_target_sphere_obstruction(factors):
    """Resolve the old 120 separating triples with a different quotient.

    This algebraically reconstructs the saved, unselected, unbounded target
    without simplifying or applying its crossings. It does not rerun the old
    expanding sphere-curve checks or increase their bounds. Every selected
    seven-factor word has a nonzero marked-sphere linking character.
    """
    from itertools import combinations
    from .factorization_explorer import product
    from .six_seven_structure import research_hurwitz_move
    from .sphere_linking import sphere_linking_character

    state=tuple(factors);reconstruction=[]
    if len(state)!=20:raise ValueError('Use the specified twenty-factor source')
    for source,target in ((11,10),(15,14),(14,13),(13,12),(12,11)):
        q=research_hurwitz_move(state,source,target)
        assert not q['disk_word_certificate']['discrepancy']
        reconstruction.append(q);state=q['factors']
    half_ids={'four_three_B.3','four_three_A.6','four_three_C.5','four_three_C.6'}
    sep_positions=tuple(i for i,f in enumerate(state) if not f.half)
    tests=[]
    for selected in combinations(sep_positions,3):
        fs=tuple(f for i,f in enumerate(state) if f.id in half_ids or i in selected)
        assert len(fs)==7 and sum(f.half for f in fs)==4
        word=product(fs)
        assert homology_action(word)==IDENTITY
        certificate=sphere_linking_character(word)
        assert certificate['nonidentity_sphere_proved']
        tests.append(dict(ids=tuple(f.id for f in fs),factors=fs,
            full_sp4_product=IDENTITY,sphere_character=certificate))
    assert len(tests)==120
    return dict(algebraic_reconstruction_of_known_unapplied_target=tuple(reconstruction),
        hypothetical_endpoint=state,all_twenty_source_records_retained=True,
        separating_triple_tests=tuple(tests),test_count=120,nonidentity_sphere_count=120,
        unknown_count=0,applied_geometric_moves=0,bounded_geometric_route=False,
        selected_half_ids=tuple(sorted(half_ids)),
        scope='Only the saved unselected five-crossing class target, with every choice of three of its ten separating records. All120 have nonzero marked-sphere characters despite Sp4 identity. The previous bounded geometric rejection remains; its raw/normalized data and old UNKNOWN flags are historical. This does not exclude other changed half classes, changed separating curves or general Hurwitz/global decompositions.')
