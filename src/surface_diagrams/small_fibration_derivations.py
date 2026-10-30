"""Source-pinned graphical derivations for the (6,2), (4,3), and (10,10).

Construction/embedding, equal-product disk moves, same-curve sphere redraws,
and cancellation of an explicit common compensation are separate step kinds.
The imported drawing edits never replace the exact algebraic starting source.
"""
from dataclasses import replace
from functools import lru_cache
from ._fibration_source_records import SOURCE_RECORDS
from .factorization_explorer import Factor,product
from .braid_actions import inverse_word,reduce_word
from .mapping_classes import exact_action,supported_class
from .hyperelliptic_homology import homology_action,IDENTITY
from .sphere_actions import sphere_inner_certificate,sphere_supported_class
from .point_pushing import split_fixed_last_strand
from .projected_relations import pc_half_lantern_terms,pc_daisy_terms
from .six_seven_structure import research_hurwitz_move
from .twist_simplify import simplify_twist
from .framed_boundary_relations import enclosed_boundaries


def source_factors(name):
    records=SOURCE_RECORDS[name]['factors'];n=SOURCE_RECORDS[name]['points'];out=[]
    for x in records:
        if x['sign']!=1:raise ValueError('A negative source factor belongs in explicit framing data')
        f=Factor(**dict(x['factor'],conjugator=tuple(x['factor']['conjugator'])))
        if f.word!=tuple(x['source_word']):raise ValueError('Keep every imported raw source word')
        out.append(f)
    return tuple(out)


def source_panel(index):
    p=SOURCE_RECORDS['four_three_panels'][index];out=[]
    for x in p['factors']:
        if 'factor' not in x or x['sign']!=1:raise ValueError('This source panel contains drawing-only or framing data')
        out.append(Factor(**dict(x['factor'],conjugator=tuple(x['factor']['conjugator']))))
    return tuple(out)


def action_match(a,b,n):
    x,y=exact_action(tuple(a),n),exact_action(tuple(b),n)
    if x!=y:raise ValueError('The complete faithful disk actions do not match')
    return dict(left_word=tuple(a),right_word=tuple(b),left_images=x,right_images=y,exact_disk_equal=True)


def individual_matches(a,b,n):
    if len(a)!=len(b):raise ValueError('Individual matching needs every ordered input/output')
    return tuple(dict(actual=x,reference=y,**action_match(x.word,y.word,n)) for x,y in zip(a,b))


def transport(fs,g):
    return tuple(replace(f,conjugator=reduce_word(tuple(g)+f.conjugator)) for f in fs)



def cable_pure_word(word,strands,duplicate):
    """Parallel-copy one labeled strand, retaining the full positive/negative braid.

    Block crossings follow the labeled strand through every generator. No
    deletion or quotient is used. The final pure braid restores all labels.
    """
    word=tuple(word)
    if type(strands) is not int or strands<2 or type(duplicate) is not int or not 1<=duplicate<=strands or any(type(x) is not int or not 1<=abs(x)<strands for x in word):raise ValueError('Choose a valid labeled strand and signed source braid generators')
    labels=list(range(1,strands+1));out=[];crossings=[]
    def block_cross(a,b,start):
        return tuple(start+j+k for j in range(b) for k in range(a-1,-1,-1))
    for x in word:
        i=abs(x)-1;weights=[2 if z==duplicate else 1 for z in labels]
        a,b=weights[i:i+2];start=sum(weights[:i])+1
        local=block_cross(a,b,start) if x>0 else inverse_word(block_cross(b,a,start))
        crossings.append(dict(source_generator=x,labels_before=tuple(labels),parallel_block_word=local))
        out.extend(local);labels[i],labels[i+1]=labels[i+1],labels[i]
    if labels!=list(range(1,strands+1)):
        raise ValueError('This source cabling lemma uses a PURE braid; all source labels must return')
    return dict(word=reduce_word(out),strands_before=strands,strands_after=strands+1,
                duplicated_label=duplicate,crossings=tuple(crossings),final_labels=tuple(labels),
                framing='parallel copy with zero internal twist; all induced pair corrections are retained explicitly')


def _cabled_daisy_proof(R,Q):
    source=source_panel(0);D4=Factor('canonical.D4',(),1,4)
    terms=tuple(Factor('canonical.daisy.'+str(i),x.conjugator,x.first,x.points,x.power,x.half)
                for i,x in enumerate(pc_daisy_terms(D4.mapping_class)))
    current=terms;moves=[]
    for a,b in ((1,2),(2,3),(1,2)):
        q=research_hurwitz_move(current,a,b);moves.append(q);current=q['factors']
    matches=individual_matches(current,source,4)
    cabled=[cable_pure_word(f.word,4,4) for f in source]
    outer=cable_pure_word(D4.word,4,4)
    individual=[]
    for i,(c,f) in enumerate(zip(cabled,R)):
        individual.append(action_match(c['word']+(() if i==0 else Q.word),f.word,5))
    targets=(Factor('D5',(),1,5),replace(Q,power=2))
    balance=tuple(sum(f.power for f in R if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in targets if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
    if balance!=(1,1,1,0,0):raise ValueError('Retain all actual full-boundary PC corrections')
    return dict(canonical_four_point_parent=D4,canonical_four_point_daisy=terms,
        retained_three_internal_hurwitz=tuple(moves),all_four_source_petal_matches=matches,
        four_point_relation=action_match(product(source),D4.word,4),cabled_actual_sources=tuple(cabled),
        individually_known_pair_corrections=tuple(individual),cabled_outer=outer,
        outer_correction=action_match(outer['word']+Q.word,Factor('D5',(),1,5).word,5),
        retained_positive_pair_compensation=replace(Q,power=2),
        formal_full_boundary_pc_balance=balance,
        boundary_balance_scope='Formal full-boundary diagnostic: positive inner corrections on the first three objects cap to marked points. No framed-hole powers are assigned to individual half twists.',
        complete_cabled_relation=action_match(product(R),Factor('D5',(),1,5).word+replace(Q,power=2).word,5))


def _cabled_half_lantern_proof(right):
    parent=Factor('canonical.T345',(),3,3)
    terms=tuple(Factor('canonical.HL.'+str(i),x.conjugator,x.first,x.points,x.power,x.half)
                for i,x in enumerate(pc_half_lantern_terms(parent.mapping_class)))
    cycled=terms[1:]+terms[:1];prefix=terms[0].word
    raw=reduce_word(inverse_word(prefix)+product(terms)+prefix+inverse_word(product(cycled)))
    if raw:raise ValueError('The internal PC half-lantern cyclic word must be checked raw first')
    # The two half terms avoid the doubled fifth endpoint but wind around it.
    # Their whole three-factor packet is pure; cable each non-pure half by
    # treating its actual fixed fifth strand, retaining the other permutation.
    def fixed_cable(word):
        # The half exchanges3/4; the fifth labeled endpoint returns. Its full
        # path through the square-based conjugator is retained below.
        labels=list(range(1,6));out=[];steps=[]
        for x in word:
            i=abs(x)-1;weights=[2 if z==5 else 1 for z in labels];a,b=weights[i:i+2];start=sum(weights[:i])+1
            positive=lambda a,b:tuple(start+j+k for j in range(b) for k in range(a-1,-1,-1))
            local=positive(a,b) if x>0 else inverse_word(positive(b,a))
            steps.append(dict(source_generator=x,labels_before=tuple(labels),parallel_block_word=local));out.extend(local)
            labels[i],labels[i+1]=labels[i+1],labels[i]
        if labels[-1]!=5:raise ValueError('The cabled fifth strand must stay fixed as a labeled endpoint')
        return dict(word=reduce_word(out),crossings=tuple(steps),final_labels=tuple(labels))
    cab=tuple(fixed_cable(f.word) for f in cycled)
    T=Factor('canonical.T456.square',(),4,3,power=2);Q=Factor('canonical.Q56',(),5,2)
    h=Factor('canonical.H34',(),3,2,half=True)
    winding=replace(h,id='canonical.winding.H34',conjugator=Factor('T456',(),4,3).word)
    extracted=(winding,T,h)
    matches=(action_match(cab[0]['word'],winding.word,6),
             action_match(cab[1]['word']+replace(Q,power=2).word,T.word,6),
             action_match(cab[2]['word'],h.word,6))
    move=research_hurwitz_move(extracted,1,0)
    ordered=individual_matches(move['factors'],right,6)
    outer=cable_pure_word(parent.word,5,5)
    return dict(canonical_pc_parent=parent,canonical_pc_half_lantern=terms,
        pc_relation=action_match(parent.word,product(terms),5),raw_cyclic_discrepancy=raw,
        independently_known_parent_invariance=action_match(product(cycled),parent.word,5),
        cabled_outputs=cab,individual_cabling_matches=matches,cabled_parent=outer,
        outer_pair_correction=action_match(outer['word']+Q.word,Factor('O3456',(),3,4).word,6),
        explicit_internal_hurwitz=move,every_source_output_match=ordered,
        full_disk_relation=action_match(Factor('O3456',(),3,4).word+Q.word,product(right),6),
        framing_scope='The same zero-internal-twist parallel copy is used throughout; its Q56 correction is explicit. No framed-half-hole convention or ordinary puncture deletion is assumed.')


def _fixes_last(word,n):
    order=list(range(1,n+1))
    for x in word:order[abs(x)-1],order[abs(x)]=order[abs(x)],order[abs(x)-1]
    return order[-1]==n


def full_kernel(word,n):
    word=tuple(word)
    if not _fixes_last(word,n):
        return dict(source_word=word,strands=n,applicable=False,reason='The last strand moves; no fixed-last split or deletion is used',full_faithful_images=exact_action(word,n))
    split=split_fixed_last_strand(word,n)
    return dict(source_word=word,strands=n,applicable=True,split=split,
                reconstructed=action_match(word,split.reconstructed_word,n))


def score(fs,n):
    lengths=tuple(len(supported_class(f.mapping_class,n)) for f in fs)
    return dict(rows=len(fs),maximum=max(lengths,default=0),total=sum(lengths),braid_letters=len(product(fs)))


class _Replay:
    def __init__(self,fs,n,title,target=None):
        self.fs=tuple(fs);self.n=n;self.target=tuple(self.fs if target is None else target)
        action_match(product(self.fs),product(self.target),n)
        self.stages=[dict(kind='start',title=title,factors=self.fs,points=n,target=self.target,score=score(self.fs,n))]
    def record(self,title,kind,**extra):
        action_match(product(self.fs),product(self.target),self.n)
        self.stages.append(dict(title=title,kind=kind,factors=self.fs,points=self.n,target=self.target,
            score=score(self.fs,self.n),**extra))
    def sub(self,i,count,terms,title,kind='disk_named_substitution',**proof):
        before=self.fs[i:i+count];terms=tuple(terms)
        match=action_match(product(before),product(terms),self.n)
        discrepancy=reduce_word(product(before)+inverse_word(product(terms)))
        local_sphere=sphere_inner_certificate(discrepancy);local_lift=homology_action(discrepancy)
        if not local_sphere['certified'] or local_lift!=IDENTITY:raise ValueError('Keep separate local disk, marked-sphere and chosen+I checks')
        self.fs=self.fs[:i]+terms+self.fs[i+count:]
        self.record(title,kind,local_before=before,local_after=terms,disk_certificate=match,
            local_kernels=(full_kernel(product(before),self.n),full_kernel(product(terms),self.n)),
            every_actual_factor_kernel=tuple(full_kernel(f.word,self.n) for f in before+terms),
            full_local_disk_discrepancy=discrepancy,local_sphere_certificate=local_sphere,local_chosen_lift=local_lift,**proof)
    def moves(self,steps,title):
        start=self.fs;preview=self.fs;atomic=[]
        for a,b in steps:
            raw=research_hurwitz_move(preview,a,b)
            raw_score=score(raw['factors'],self.n)
            if raw_score['maximum']>20:raise ValueError('Reject the whole proposed carry before application at support bound20')
            if raw['disk_word_certificate']['discrepancy']:raise ValueError('Raw equality must be checked first')
            fs=list(raw['factors']);changed=a
            old=fs[changed];twist=simplify_twist(old.mapping_class,strands=self.n,max_states=64)
            new=replace(old,conjugator=twist.conjugator,first=twist.first)
            match=action_match(old.word,new.word,self.n);fs[changed]=new
            candidate=tuple(fs);s=score(candidate,self.n)
            if s['maximum']>20:raise ValueError('The normalized presentation must retain support bound20')
            atomic.append(dict(raw_move=raw,individual_presentation=match,factors=candidate,score=s,
                raw_support_score=raw_score,preapplication_support_bound=20,bounded_before_application=True))
            preview=candidate
        self.fs=preview
        self.record(title,'disk_hurwitz_block',local_before=start,local_after=self.fs,
            adjacent_checks=len(atomic),atomic_steps=tuple(atomic),full_preapplication_preview=True)
    def combine(self,i,name):
        a,b=self.fs[i:i+2]
        if a.half!=b.half or a.points!=b.points:raise ValueError('Combine equal supported types only')
        unit=individual_matches((replace(a,power=1),),(replace(b,power=1),),self.n)
        if a.half:
            if a.power!=1 or b.power!=1:raise ValueError('Combine only two unit halves')
            term=replace(a,id=name,half=False,power=1)
        else:term=replace(a,id=name,power=a.power+b.power)
        self.sub(i,2,(term,),'Combine the two matched '+name,'disk_combine',individual_unit_matches=unit)
    def cyclic(self,k,title):
        before=self.fs;p=product(before[:k]);after=before[k:]+before[:k]
        raw=reduce_word(inverse_word(p)+product(before)+p+inverse_word(product(after)))
        if raw:raise ValueError('Retain raw free cyclic equality before individual normalization')
        equality=action_match(product(before),product(after),self.n)
        self.fs=after;self.record(title,'disk_cyclic_start',inverse_prefix_common_word=inverse_word(p),
            raw_common_discrepancy=raw,known_output_invariance=equality)


def _finish(r,profile,**extra):
    points=r.n
    ambient=tuple(replace(f,first=f.first) for f in r.fs)
    w=product(ambient);sphere=sphere_inner_certificate(w);lift=homology_action(w)
    if not sphere['certified'] or lift!=IDENTITY:raise ValueError('A complete genus-two derivation needs separate sphere identity and chosen+I')
    n=sum(f.power if f.half else 2*f.power if f.points in (2,4) else 0 for f in ambient)
    s=sum(f.power//2 if not f.half and f.points==3 and f.power%2==0 else 0 for f in ambient)
    if any(not f.half and f.points==3 and f.power%2 for f in ambient) or (n,s)!=profile:
        raise ValueError('Count actual unit half twists and squared triples, not just rows')
    checks=sum(x.get('adjacent_checks',0) for x in r.stages)
    states=[q for st in r.stages for q in (st,)+tuple(st.get('atomic_steps',()))]
    return dict(stages=tuple(r.stages),factors=r.fs,points=points,profile=profile,
        adjacent_checks=checks,operations=len(r.stages)-1,
        listed_operations=sum(x.get('move_count',1) for x in r.stages[1:]),
        local_peak=dict(maximum=max(q['score']['maximum'] for q in states),total=max(q['score']['total'] for q in states),rows=max(q['score']['rows'] for q in states)),
        terminal_sphere_certificate=sphere,terminal_chosen_lift=lift,
        terminal_full_kernel=full_kernel(w,6),complete=True,**extra)


@lru_cache(maxsize=1)
def six_two_derivation():
    A=Factor('A123',(),1,3);B=Factor('B456',(),4,3);D=Factor('D6',(),1,6)
    source=source_factors('six_two');H=tuple(replace(f,id='H'+str(i+1)) for i,f in enumerate(source[2:5]))
    rotation=(5,4,3,2,1);C=A.word+B.word;hw=product(H)
    rotation_match=action_match(rotation*3,C+hw,6)
    swaps=individual_matches(transport((A,B),hw),(B,A),6)
    r=_Replay((D,),6,'The six-point boundary twist')
    packet=(A,B)+H+(replace(A,id='A123.2'),replace(B,id='B456.2'))+tuple(replace(f,id=f.id+'.2') for f in H)
    r.sub(0,1,packet,'Use two half-turn packets: r^3 = A B H14 H25 H36',
          rotation_word=rotation,actual_rotation_match=rotation_match,actual_block_exchange_matches=swaps,
          canonical_full_twist=action_match(rotation*6,D.word,6))
    r.moves(((4,5),(3,4),(2,3),(5,6),(4,5),(3,4)),
            'Carry the SAME three-half block down across both triple roots')
    r.moves(((3,2),(2,1)),'Commute the returned A root upward across the two disjoint B roots')
    r.combine(0,'A123.square');r.combine(1,'B456.square')
    matches=individual_matches(r.fs,source,6)
    return _finish(r,(6,2),source_individual_matches=matches,source_sequence='six_two',
        formula='D6 = (ABH)^2 = A^2 B^2 H^2; H=H14 H25 H36',
        scope='A named positive block-rotation derivation. Ordinary triple roots are intermediate calculation factors; the eight final factors have type(6,2). The disk boundary relation and its separate sphere/+I closure are both retained.')


@lru_cache(maxsize=1)
def four_three_derivation():
    panels=SOURCE_RECORDS['four_three_panels'];combined=panels[6]['factors']
    f=lambda x:Factor(**dict(x['factor'],conjugator=tuple(x['factor']['conjugator'])))
    A=Factor('T123',(),1,3);B=Factor('T345',(),3,3);Q=Factor('Q45',(),4,2)
    R=(A,replace(f(combined[1]),id='T145'),replace(f(combined[2]),id='T245'),B)
    D=Factor('D5.square',(),1,5,power=2);Q4=replace(Q,id='positive.compensation',power=4)
    beta=(1,2,1);variant=transport(R,beta);variant=variant[1:]+variant[:1]
    variant=tuple(replace(x,id=x.id+'.variation') for x in variant)
    packet=R+variant
    r=_Replay((Q4,D),5,'Keep the explicit positive compensation Q45^4 on the left')
    root_target=Factor('D5',(),1,5).word+replace(Q,power=2).word
    cabled=action_match(product(R),root_target,5)
    root_invariance=action_match(product(transport(R,beta)),root_target,5)
    old_prefix=product(transport(R,beta)[:1]);raw_cycle=reduce_word(inverse_word(old_prefix)+product(transport(R,beta))+old_prefix+inverse_word(product(variant)))
    if raw_cycle:raise ValueError('Keep the full raw cyclic word of the second cabled daisy')
    r.sub(0,2,packet,'Two cabled PC daisies give D5 squared with the SAME Q45^4 compensation',
        canonical_cabled_daisy=R,cabled_relation=cabled,full_named_cabled_daisy_proof=_cabled_daisy_proof(R,Q),variant_chart=beta,
        independently_known_variant_invariance=root_invariance,raw_variant_cyclic_discrepancy=raw_cycle,
        construction_note='Cable the last object of the four-point PC daisy to the explicit45 pair. This is a construction lemma with its complete braid certificate, not deletion of a strand or an unchecked framed-hole convention.')
    r.cyclic(7,'Choose the cyclic start at the second T123 root')
    r.combine(0,'T123.square');r.combine(3,'T345.square')
    converted=source_panel(8)
    # Expand the later root first so each correction crosses ONLY ordinary roots.
    for index,expected,label in ((5,converted[6:8],'145'),(5,converted[4:6],'245')):
        parent=r.fs[index]
        chart=parent.conjugator+(-(parent.first+1),)
        stabilized=replace(parent,conjugator=chart)
        stabilizer=individual_matches((parent,),(stabilized,),5)
        canonical=pc_half_lantern_terms(stabilized.mapping_class)
        halves=tuple(Factor('half.'+label+'.'+str(j+1),x.conjugator,x.first,x.points,x.power,x.half) for j,x in enumerate(canonical[:2]))
        individual_matches(halves,expected,5)
        correction=replace(Q,id='correction.'+label,power=2)
        individual_matches((correction,),(Factor('canonical.correction',canonical[2].conjugator,canonical[2].first,canonical[2].points,canonical[2].power),),5)
        commutator=action_match(correction.word+product(halves),product(halves)+correction.word,5)
        r.sub(index,1,(correction,)+halves,'PC half lantern on the actual '+label+' root; expose its positive correction',
            named_relation='PC half lantern with correction first',canonical_input=stabilized,
            canonical_ordered_outputs=canonical,individual_parent_stabilizer=stabilizer,
            individual_output_matches=individual_matches(halves,expected,5),full_correction_packet_commutation=commutator)
        pos=next(i for i,x in enumerate(r.fs) if x.id==correction.id)
        # Every crossed ordinary support commutes with Q45; halves remain below.
        original=r.fs
        for x in original[:pos]:action_match(x.word+correction.word,correction.word+x.word,5)
        r.moves(tuple((i,i-1) for i in range(pos,0,-1)),'Move ONLY the new positive correction to the explicit LEFT ledger')
    r.combine(0,'positive.compensation')
    individual_matches((r.fs[0],),(Q4,),5)
    main=r.fs[1:];matches=individual_matches(main,converted,5)
    cancelled_before=r.fs;old_target=r.target
    r.fs=main;r.target=(D,)
    cancellation=action_match(product(main),D.word,5)
    r.record('Cancel the SAME recorded Q45^4 prefix from BOTH sides of the relation',
        'cancel_common_compensation',common_prefix=(Q4,),before_factors=cancelled_before,
        before_target=old_target,after_target=r.target,individual_main_matches=matches,
        resulting_relation=cancellation,
        scope='Explicit algebraic common-prefix cancellation in the proof, not deletion of a twist from a fixed-product fibration, a sphere move, or a peripheral cap.')
    r.moves(((6,5),),'Move half7 up to6')
    r.moves(((4,5),),'Move half5 down to6')
    r.moves(((4,3),(3,2)),'Move half5 up to3, with both adjacent crossings retained')
    r.moves(((3,2),),'Move root4 up to3; the two ordinary triple roots now match')
    r.combine(1,'third.separating.square')
    reference=source_factors('four_three_A');join=individual_matches(r.fs,reference,5)
    return _finish(r,(4,3),source_individual_matches=join,source_sequence='four_three_A',
        positive_compensation=Q4,unmixed_ledger_cancellation=True,
        source_four_point_daisy=SOURCE_RECORDS['four_three_panels'][:4],
        scope='Positive cabled-daisy construction with explicit equal compensation on BOTH sides, two separate PC half lanterns and five later adjacent Hurwitz checks. No negative twist factors, sphere substitutions or silent deletion. The final seven actual factors individually match source A.')


@lru_cache(maxsize=1)
def ten_ten_derivation():
    A=source_factors('four_three_A');B=source_factors('four_three_B');C=source_factors('four_three_C')
    D5=Factor('D5',(),1,5,power=2)
    blocks=(B,A,C)
    block_checks=tuple(action_match(product(x),D5.word,5) for x in blocks)
    r=_Replay(B+A+C,5,'Assemble three EXACT (4,3) blocks: B, A, C',target=(replace(D5,power=6),))
    rotate=lambda b,k:b[k:]+b[:k]
    parts=(rotate(B,6),rotate(A,3),rotate(C,2));after=sum(parts,())
    raw_cycles=[]
    for before,k,following in zip(blocks,(6,3,2),parts):
        p=product(before[:k]);raw=reduce_word(inverse_word(p)+product(before)+p+inverse_word(product(following)))
        if raw:raise ValueError('All three parallel starts need their complete raw common word')
        raw_cycles.append(dict(inverse_prefix=inverse_word(p),raw_discrepancy=raw,
            independent_boundary_invariance=action_match(product(before),product(following),5)))
    before=r.fs;r.fs=after
    independence=[]
    def one_rotation(state,block,k):
        start=block*7;chunk=state[start:start+7]
        return state[:start]+chunk[k:]+chunk[:k]+state[start+7:]
    shifts=(6,3,2)
    for a,b in ((0,1),(0,2),(1,2)):
        left=one_rotation(one_rotation(before,a,shifts[a]),b,shifts[b]);right_order=one_rotation(one_rotation(before,b,shifts[b]),a,shifts[a])
        if left!=right_order:raise ValueError('Parallel blocks require literal two-order equality')
        independence.append(dict(blocks=(a,b),same_input=before,left_then_right=left,right_then_left=right_order,literal_two_order_equality=True))
    r.record('Rotate the three disjoint central blocks from the SAME input','disk_parallel_cyclic',
        input_factors=before,block_ranges=((0,7),(7,14),(14,21)),raw_common_cycles=tuple(raw_cycles),
        independent_blocks=True,block_boundary_checks=block_checks,move_count=3,
        independence_witnesses=tuple(independence),
        parallel_cards=tuple(dict(before=before,after=one_rotation(before,i,shifts[i]),block=i) for i in range(3)))
    r.cyclic(18,'Rotate the FULL central21-factor product right by three')
    r.moves(((0,1),(1,2),(11,10),(10,9)),'Perform the first two source pulls')
    r.moves(((3,2),(8,9)),'Perform the next two source pulls')
    round45=Factor('round45',(),4,2,half=True)
    individual_matches((r.fs[8],),(round45,),5)
    r.moves(tuple((i,i+1) for i in range(8,15)),'Carry the actual ninth half twist down to16')
    r.moves(tuple((i,i+1) for i in range(3,14)),'Carry the actual fourth half twist down to15')
    r.combine(14,'merged.pair.one');r.combine(15,'merged.pair.two')
    old=r.fs;old_target=r.target
    r.fs=tuple(replace(f,first=f.first+1,conjugator=tuple((1 if x>0 else -1)*(abs(x)+1) for x in f.conjugator)) for f in old)
    r.target=tuple(replace(f,first=f.first+1,conjugator=tuple((1 if x>0 else -1)*(abs(x)+1) for x in f.conjugator)) for f in old_target);r.n=6
    r.record('Embed the five-point construction; add the sixth point on the LEFT','construction_embedding',
        source_points=5,target_points=6,offset=1,before_factors=old,before_target=old_target,
        scope='Embedding is a construction/context change, not an equality between B5 and B6 or a claim that the embedded D5 power is central in B6.')
    conversion=tuple(SOURCE_RECORDS['ten_ten_conversion_word']);chart=inverse_word(conversion)
    left=source_factors('half_lantern_standard_left');right=source_factors('half_lantern_standard_right')
    actual=r.fs[14:16]
    inputs=individual_matches(transport(actual,chart),left,6)
    # Redraw ONLY the same T12 sphere curve as its complementary four-point outer.
    redraw_standard=(left[0],Factor('complement.O3456',(),3,4))
    redraw_actual=transport(redraw_standard,conversion)
    after_curve=replace(redraw_actual[1],id=actual[1].id)
    before_curve=actual[1]
    discrepancy=reduce_word(before_curve.word+inverse_word(after_curve.word))
    sphere=sphere_inner_certificate(discrepancy);lift=homology_action(discrepancy)
    if not sphere['certified'] or lift!=IDENTITY or sphere_supported_class(before_curve.mapping_class)!=sphere_supported_class(after_curve.mapping_class):
        raise ValueError('The sphere step must retain the SAME curve, factor identity and power, with separate+I')
    entire_before=r.fs
    r.fs=r.fs[:15]+(after_curve,)+r.fs[16:]
    full_discrepancy=reduce_word(product(entire_before)+inverse_word(product(r.fs)))
    full_sphere=sphere_inner_certificate(full_discrepancy)
    if not full_sphere['certified'] or homology_action(full_discrepancy)!=IDENTITY:raise ValueError('Retain the full actual context of the sphere redraw')
    # A sphere redraw changes the disk product; retain its actual new target.
    r.target=r.fs
    r.record('SPHERE REDRAW ONLY: the same actual pair curve from its complementary side','sphere_redraw',
        local_before=(before_curve,),local_after=(after_curve,),local_disk_discrepancy=discrepancy,
        full_disk_discrepancy=full_discrepancy,full_context_sphere_certificate=full_sphere,
        sphere_certificate=sphere,chosen_lift_discrepancy=lift,individual_actual_input_matches=inputs,
        canonical_before=left,canonical_after=redraw_standard,common_chart=conversion,
        factor_identity_retained=before_curve.id==after_curve.id,power_retained=before_curve.power==after_curve.power)
    replacement=tuple(replace(f,id='new.half-lantern.'+str(i+1)) for i,f in enumerate(transport(right,conversion)))
    r.sub(14,2,replacement,'Apply the EXACT DISK half lantern after the separate redraw',
        named_relation='cabled disk half lantern',canonical_input=redraw_standard,canonical_output=right,
        common_chart=conversion,individual_actual_input_matches=individual_matches(r.fs[14:16],transport(redraw_standard,conversion),6),
        individual_actual_output_matches=individual_matches(replacement,transport(right,conversion),6),
        canonical_disk_relation=action_match(product(redraw_standard),product(right),6),
        full_named_cabled_half_lantern_proof=_cabled_half_lantern_proof(right))
    reviewed=source_factors('ten_ten_reviewed_final');bad_word=product(reviewed)
    bad_lift=homology_action(bad_word)
    original_start=r.stages[0]['factors'];edited_start=source_factors('ten_ten_reviewed_start')
    source_comparisons=[]
    for i,(original,edited) in enumerate(zip(original_start,edited_start),1):
        a,b=exact_action(original.word,5),exact_action(edited.word,5)
        source_comparisons.append(dict(position=i,original=original,edited=edited,equal=a==b,original_images=a,edited_images=b,first_differing_meridian=next((j for j,(x,y) in enumerate(zip(a,b),1) if x!=y),None)))
    if tuple(x['position'] for x in source_comparisons if not x['equal'])!=(6,13,19,20):raise ValueError('Keep the exact four source-edit discrepancies')
    if bad_lift==IDENTITY:raise ValueError('Preserve the reviewed-source failure independently')
    return _finish(r,(10,10),dependencies=('four_three_A',),source_exact_blocks=blocks,
        source_block_certificates=block_checks,source_conversion_word=conversion,
        excluded_reviewed_drawing_data=dict(factors=reviewed,homology=bad_lift,
            source_start=edited_start,individual_original_vs_edited_comparisons=tuple(source_comparisons),adopted=False,
            scope='Four later half-arc drawing edits are distinct from the exact original algebraic A/B/C source; their final homology is not+I. They are archived, never silently adopted or overwritten.'),
        unrelated_dictation_seed_unchanged=True,
        scope='The ORIGINAL exact A/B/C source with the recorded source transports yields a genuine20-factor (10,10) relation. The four incompatible later drawing edits and the separate October17 transcription remain historical. Assembly/embedding, every raw Hurwitz move, sphere redraw and disk substitution have distinct certificates.')


def all_derivations():
    return {'6-2':six_two_derivation(),'4-3':four_three_derivation(),'10-10':ten_ten_derivation()}
