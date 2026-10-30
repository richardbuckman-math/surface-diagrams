"""Necessary fiber-sum tests for the specified (10,10), not a decomposition.

The integral monodromy quotient is an isomorphism invariant of the fibration.
It is not silently identified with the total-space fundamental group or a
boundary-framed lift. No source factor or published derivation is changed.
"""
from dataclasses import replace
from itertools import combinations, permutations
from functools import reduce
from math import gcd, comb
from .hyperelliptic_homology import (IDENTITY, _multiply, _twist,
    half_twist_class, homology_action, homology_quotient)
from .mapping_classes import supported_class
from .small_fibration_derivations import score, action_match
from .six_seven_structure import research_hurwitz_move


def pairing(a, b):
    return a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1]


def _det(matrix):
    n=len(matrix)
    return sum((-1 if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2 else 1)
        *reduce(lambda a,b:a*b,(matrix[i][p[i]] for i in range(n)),1)
        for p in permutations(range(n)))


def _egcd(a, b):
    r0,r1,s0,s1,t0,t1=a,b,1,0,0,1
    while r1:
        q=r0//r1
        r0,r1,s0,s1,t0,t1=r1,r0-q*r1,s1,s0-q*s1,t1,t0-q*t1
    return (r0,s0,t0) if r0>=0 else (-r0,-s0,-t0)


def _fixed_hyperplane(vectors):
    normal=None
    for rows in combinations(vectors,3):
        candidate=tuple((-1)**j*_det(tuple(tuple(r[k] for k in range(4) if k!=j) for r in rows)) for j in range(4))
        if any(candidate):normal=candidate;break
    if normal is None:raise ValueError('The fixed-quotient test needs rank three')
    divisor=reduce(gcd,normal)
    normal=tuple(x//divisor for x in normal)
    if next(x for x in normal if x)<0:normal=tuple(-x for x in normal)
    if any(sum(x*y for x,y in zip(a,normal)) for a in vectors):
        raise ValueError('The vanishing-cycle lattice has rank four')
    columns=[tuple(int(i==j) for i in range(4)) for j in range(4)]
    row=list(normal)
    for j in range(1,4):
        a,b=row[0],row[j];d,x,y=_egcd(a,b)
        if not d:continue
        c0,cj=columns[0],columns[j]
        columns[0]=tuple(x*c0[k]+y*cj[k] for k in range(4))
        columns[j]=tuple((-b//d)*c0[k]+(a//d)*cj[k] for k in range(4))
        row[0],row[j]=d,0
    if _det(columns)!=1 or tuple(sum(x*y for x,y in zip(normal,c)) for c in columns)!=(1,0,0,0):
        raise ValueError('The saturated integral kernel needs a unimodular witness')
    v=(-normal[2],-normal[3],normal[0],normal[1])
    return dict(ordinary_annihilator=normal,primitive_common_fixed_vector=v,
        unimodular_completion_columns=tuple(columns),saturated_hyperplane_basis=tuple(columns[1:]))


def monodromy_homology_audit(factors):
    factors=tuple(factors)
    halves=tuple((i,f) for i,f in enumerate(factors) if f.half)
    separators=tuple((i,f) for i,f in enumerate(factors) if not f.half)
    if len(halves)!=10 or len(separators)!=10 or any(f.points!=2 or f.power!=1 for _,f in halves) or any(f.points!=3 or f.power!=2 for _,f in separators):
        raise ValueError('Use ten unit halves and ten squared triple twists')
    vectors=tuple(half_twist_class(f.conjugator,f.first) for _,f in halves)
    quotient=homology_quotient(vectors)
    if quotient['lattice_rank']!=3:raise ValueError('The fixed-quotient test needs rank three')
    fixed=_fixed_hyperplane(vectors);v=fixed['primitive_common_fixed_vector'];kernel=fixed['saturated_hyperplane_basis']
    matrices={f.id:homology_action(f.word) for f in factors}
    if any(matrices[f.id]!=IDENTITY for _,f in separators):raise ValueError('Every separating twist must act trivially on H1')
    full=IDENTITY
    for f in factors:
        m=matrices[f.id];full=_multiply(full,m)
        if tuple(sum(m[i][j]*v[j] for j in range(4)) for i in range(4))!=v:
            raise ValueError('Every actual monodromy generator must fix the same primitive vector')
    if full!=IDENTITY:raise ValueError('The complete chosen lift must have identity homology')
    records=[]
    for (i,f),a in zip(halves,vectors):
        pairings=tuple(pairing(a,k) for k in kernel);content=reduce(gcd,pairings)
        records.append(dict(index=i,id=f.id,vector=a,kernel_pairings=pairings,content=content,width=content*content))
    literal=[];modular=[]
    for selected in combinations(records,4):
        m=IDENTITY
        for x in selected:m=_multiply(m,matrices[x['id']])
        literal.append(dict(indices=tuple(x['index'] for x in selected),ids=tuple(x['id'] for x in selected),matrix=m,identity=m==IDENTITY))
        width=sum(x['width'] for x in selected)
        modular.append(dict(ids=tuple(x['id'] for x in selected),width=width,residue=width%12,passes=width%12==0))
    return dict(profile=(10,10),factors=factors,half_records=tuple(records),
        separating_ids=tuple(f.id for _,f in separators),all_separating_homology_identity=True,
        monodromy_coinvariants=quotient,**fixed,full_chosen_homology=full,
        literal_four_half_tests=tuple(literal),literal_passing=tuple(x for x in literal if x['identity']),
        literal_seven_subword_count=comb(10,4)*comb(10,3),modular_four_half_tests=tuple(modular),
        modular_passing=tuple(x for x in modular if x['passes']),total_quotient_width=sum(x['width'] for x in records),
        split_found=False,indecomposable_proved=False,whole_H1_or_fundamental_group_claimed=False,
        scope='The literal test is only for order-preserving subwords of this presentation. Quotient widths are necessary under arbitrary Hurwitz moves and simultaneous conjugation, but do not prove a genus-two relation or a fiber-sum decomposition.')


def necessary_two_interchange_target(audit):
    records=audit['half_records'];names=tuple(x['id'] for x in records);vectors=tuple(x['vector'] for x in records)
    for i in (4,5):
        a,b=vectors[i:i+2]
        changed=tuple(a[j]-pairing(a,b)*b[j] for j in range(4))
        vectors=vectors[:i]+(b,changed)+vectors[i+2:]
        names=names[:i]+(names[i+1],names[i])+names[i+2:]
    selected={'four_three_B.3','four_three_A.6','four_three_C.5','four_three_C.6'}
    chosen=tuple(dict(id=n,vector=a) for n,a in zip(names,vectors) if n in selected)
    m=IDENTITY
    for x in chosen:m=_multiply(m,_twist(x['vector'],1))
    if m!=IDENTITY:raise ValueError('The necessary target must retain its complete integral matrix check')
    return dict(adjacent_nonseparating_interchanges=((4,'up'),(5,'up')),selected=chosen,matrix=m,
        full_genus_two_identity_established=False,applied=False,
        scope='A homological target only. All intervening separating curves and the full nonabelian seven-factor relation still matter.')


def published_quotient_parabolics(audit):
    """Actual SL(2,Z) matrices on v-perp / Zv for the published source."""
    v=(0,-1,1,0);p=(0,1,0,0);q=(-1,0,0,1)
    if audit['primitive_common_fixed_vector']!=v:raise ValueError('This explicit basis belongs to the published chart')
    if pairing(p,q)!=1 or pairing(v,p) or pairing(v,q):raise ValueError('Use a symplectic basis of the saturated quotient')
    def coordinates(a):
        if a[0]+a[3]:raise ValueError('Vector leaves the fixed hyperplane')
        return (a[1]+a[2],-a[0])
    def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    def power(a,n):
        result=((1,0),(0,1))
        for _ in range(n):result=mul(result,a)
        return result
    records=[];full=((1,0),(0,1))
    by_id={f.id:f for f in audit['factors']}
    for r in audit['half_records']:
        f=by_id[r['id']];m=homology_action(f.word)
        cols=tuple(coordinates(tuple(sum(m[i][j]*b[j] for j in range(4)) for i in range(4))) for b in (p,q))
        actual=tuple(tuple(cols[j][i] for j in range(2)) for i in range(2));x,y=coordinates(r['vector']);d=gcd(x,y)
        if d!=r['content'] or not d:raise ValueError('Keep the saturated projected divisibility')
        u,z=x//d,y//d;one,s,t=_egcd(u,z)
        if one!=1:raise ValueError('The primitive quotient vector needs a Bezout witness')
        c=((u,-t),(z,s));ci=((s,t),(-z,u));tau=((1,-d*d),(0,1))
        if mul(mul(c,tau),ci)!=actual:raise ValueError('Retain the complete parabolic conjugation')
        full=mul(full,actual);records.append(dict(id=f.id,projected_vector=(x,y),matrix=actual,width=d*d,conjugator=c,inverse_conjugator=ci,primitive_twist_power=tau))
    S=((0,1),(-1,0));T=((1,-1),(0,1));unit=((1,0),(0,1))
    if power(S,4)!=unit or power(S,2)!=power(mul(S,T),3) or full!=unit:raise ValueError('Retain the actual SL2 presentation and full product')
    return dict(fixed_vector=v,p=p,q=q,pairing=1,records=tuple(records),full_product=full,S=S,T=T,
        relations='S^4=1 and S^2=(ST)^3; after abelianizing, s=-3t and 12t=0',
        modulus=12,necessary_four_width_sum='0 modulo12; this does not certify the genus-two word')


def rejected_geometry_previews(factors):
    from .twist_simplify import simplify_twist
    strategies={
        'carry_second_half_up_the_gap':((11,10),(15,14),(14,13),(13,12),(12,11)),
        'carry_separating_gap_up_over_first_half':((11,10),(12,11),(13,12),(14,13),(15,14)),
        'carry_separating_gap_down_over_second_half':((11,10),(14,15),(13,14),(12,13),(12,11))}
    results=[]
    for name,steps in strategies.items():
        state=tuple(factors);prefix=[];failure=None
        for source,target in steps:
            raw=research_hurwitz_move(state,source,target);s=score(raw['factors'],6)
            if raw['disk_word_certificate']['discrepancy']:raise ValueError('Raw free equality is checked first')
            if s['maximum']>20:
                failure=dict(step=(source,target),raw_move=raw,raw_score=s,
                    curves_over_bound=tuple(dict(factor=f,support=supported_class(f.mapping_class,6)) for f in raw['factors'] if len(supported_class(f.mapping_class,6))>20))
                break
            old=raw['factors'][source];t=simplify_twist(old.mapping_class,strands=6,max_states=64)
            new=replace(old,conjugator=t.conjugator,first=t.first);match=action_match(old.word,new.word,6)
            next_state=list(raw['factors']);next_state[source]=new;state=tuple(next_state)
            prefix.append(dict(raw_move=raw,individual_presentation_match=match,factors=state,score=score(state,6)))
        if failure is None:raise ValueError('This saved finite family is expected to be rejected, not silently promoted')
        results.append(dict(name=name,proposed_steps=steps,applied=False,selected_route_reached=False,
            rejected_before_application=True,prefix_preview_only=tuple(prefix),failure=failure))
    return tuple(results)


def published_nakamura_homology_comparison():
    relations=((1,1,0,0),(0,0,1,1),(1,1,0,1),(1,2,-1,0))
    q=homology_quotient(relations)
    if q!=dict(lattice_rank=4,free_rank=0,torsion=()):raise ValueError('The published relations kill all four generators')
    return dict(coordinates=('a1','a2','b1','b2'),published_homology_relators=relations,quotient=q,
        source='https://arxiv.org/html/1811.03708#S3',
        scope='These are the homology consequences explicitly used in Nakamura Section3. They are not a claimed curve-by-curve identification with the imported construction. Coinvariants distinguish the specified monodromies without asserting the total-space group of our unframed relation.')
