"""Exact source-monodromy conjugacy for Hstar; no Hurwitz supply/gather."""
from dataclasses import replace
from .factorization_explorer import Factor,product
from .braid_actions import reduce_word,inverse_word
from .mapping_classes import exact_action,supported_class
from .hyperelliptic_homology import homology_action,IDENTITY
from .small_fibration_derivations import action_match,full_kernel
from .sphere_linking import sphere_linking_character
from .sphere_actions import sphere_chain_certificate


def source_hstar_conjugacy(source,reference_C,target):
    """Conjugate literal source B.7 to the exact standalone target Hstar.

    R=M a M^-1 P^-1 uses only actual source factors. Its nine group-factor
    occurrences are not nine geometric moves, and negative letters are
    confined to a conjugator. No source factorization is changed.
    """
    source=tuple(source);reference_C=tuple(reference_C);target=tuple(target)
    if len(source)!=20 or len(reference_C)!=7 or len(target)!=7:
        raise ValueError('Use the pinned twenty-factor input and two seven-factor references')
    by={f.id:f for f in source};a=by['four_three_B.7'];c=reference_C[6];h=target[4]
    if not (a.half and c.half and h.half and a.power==c.power==h.power==1):
        raise ValueError('All conjugated factors must be positive unit halves')
    names=('four_three_B.1','four_three_B.2','four_three_B.3','four_three_B.4')
    P=product(tuple(by[x] for x in names));M=product((by['four_three_C.5'],by['four_three_C.6']))
    if target[:4]!=tuple(by[x] for x in names) or target[5:]!=(by['four_three_C.5'],by['four_three_C.6']):
        raise ValueError('The six target/source records must remain literal')
    plan=(('four_three_C.5',1),('four_three_C.6',1),('four_three_B.7',1),
          ('four_three_C.6',-1),('four_three_C.5',-1),('four_three_B.4',-1),
          ('four_three_B.3',-1),('four_three_B.2',-1),('four_three_B.1',-1))
    R=reduce_word(tuple(x for name,sign in plan for x in (by[name].word if sign>0 else inverse_word(by[name].word))))
    if R!=reduce_word(M+a.word+inverse_word(M)+inverse_word(P)):
        raise ValueError('Preserve the exact ordered source group word')
    short_R=reduce_word(M+a.word+c.word)
    candidate=replace(a,id='hypothetical.B7.to.Hstar',conjugator=reduce_word(R+a.conjugator))
    discrepancy=reduce_word(candidate.word+inverse_word(h.word))
    if homology_action(discrepancy)!=IDENTITY:raise ValueError('Pass full Sp4 before full action expansion')
    character=sphere_linking_character(discrepancy)
    if character['nonidentity_sphere_proved']:raise ValueError('Pass every sphere character first')
    D=Factor('embedded.D5.squared',(),2,5,power=2)
    items=(
        ('actual B.7 and reference C.7 braid relation',a.word+c.word+a.word,c.word+a.word+c.word),
        ('actual P M and reference C.7 product',P+M+c.word,D.word),
        ('explicit boundary commutation with B.7 only',D.word+a.word,a.word+D.word),
        ('actual source conjugator equals short R times inverse boundary',R,short_R+inverse_word(D.word)),
        ('two-half braid conjugation',(a.word+c.word)+a.word+inverse_word(a.word+c.word),c.word),
        ('reference inner block gives exact Hstar',M+c.word+inverse_word(M),h.word),
        ('actual source group conjugation gives exact Hstar',candidate.word,h.word))
    proofs=tuple(dict(title=title,**action_match(left,right,6)) for title,left,right in items)
    support=supported_class(candidate.mapping_class,6);target_support=supported_class(h.mapping_class,6)
    if support!=target_support or len(support)!=18:raise ValueError('Retain the exact bounded endpoint class')
    sphere=sphere_chain_certificate(discrepancy,max_letters=50000)
    if not sphere['certified']:raise ValueError('Keep separate complete sphere and chosen-lift checks')
    words={}
    for title,left,right in items:words.setdefault(tuple(left),title+' left');words.setdefault(tuple(right),title+' right')
    for f in tuple(by[x] for x in dict(plan))+ (c,h,D):words.setdefault(f.word,f.id)
    words.setdefault(discrepancy,'full disk conjugacy discrepancy')
    data=[]
    for w,title in words.items():
        if any(abs(x)<2 for x in w):raise ValueError('The specified proof lies in the embedded B5 subgroup')
        lower=tuple((1 if x>0 else -1)*(abs(x)-1) for x in w)
        images6=exact_action(w,6);images5=exact_action(lower,5)
        shifted=((1,),)+tuple(tuple((1 if x>0 else -1)*(abs(x)+1) for x in row) for row in images5)
        if images6!=shifted:raise ValueError('Retain every inverse-embedding meridian match')
        data.append(dict(title=title,B6_word=w,embedded_B5_word=lower,B6_images=images6,B5_images=images5,
            B6_stabilizer_or_full_action=full_kernel(w,6),B5_stabilizer_or_full_action=full_kernel(lower,5),
            inverse_embedding_scope='Known vertical first strand, checked on every meridian; not an applied deletion or sphere move.'))
    full=full_kernel(discrepancy,6)
    if not full['applicable'] or full['split'].kernel_loop or exact_action(full['split'].shadow_word,5)!=tuple((i,) for i in range(1,6)):
        raise ValueError('Retain the full nonabelian kernel and full shadow of the identity discrepancy')
    lower_discrepancy=tuple((1 if x>0 else -1)*(abs(x)-1) for x in discrepancy)
    embedded_full=full_kernel(lower_discrepancy,5)
    if not embedded_full['applicable'] or embedded_full['split'].kernel_loop or exact_action(embedded_full['split'].shadow_word,4)!=tuple((i,) for i in range(1,5)):
        raise ValueError('Retain the embedded full F4 kernel AND B4 shadow, not abelian exponents')
    single=tuple(replace(h,id=f.id) if f.id==a.id else f for f in source)
    bad=homology_action(product(single))
    if bad==IDENTITY:raise ValueError('Retain the nonclosure of an unsupported single-slot replacement')
    return dict(source_factors=source,source_half=a,source_half_position=next(i for i,f in enumerate(source) if f.id==a.id),
        reference_C7=c,target_Hstar=h,target_seven_factors=target,actual_P_word=P,actual_M_word=M,
        source_group_plan=tuple(dict(id=name,sign=sign,source_position=next(i for i,f in enumerate(source) if f.id==name),
            actual_factor=by[name]) for name,sign in plan),
        source_group_conjugator=R,group_factor_occurrences=len(plan),short_reference_conjugator=short_R,
        embedded_boundary=D,full_faithful_B6_equalities=proofs,
        hypothetical_conjugated_half=candidate,exact_endpoint_support=support,endpoint_support_length=len(support),
        exact_target_support=target_support,full_disk_discrepancy=discrepancy,
        necessary_sphere_character=character,full_sphere_certificate=sphere,chosen_lift_discrepancy=IDENTITY,
        all_actual_and_reference_word_stabilizers_or_full_actions=tuple(data),full_discrepancy_point_pushing=full,
        embedded_B5_discrepancy_point_pushing=embedded_full,
        hypothetical_single_slot_countercheck=dict(factors=single,full_Sp4_product=bad,applied=False),
        exact_source_B7_G_conjugacy_proved=True,exact_faithful_disk_conjugacy_proved=True,
        actual_source_moves=0,actual_source_factor_changes=0,source_ancestry_physically_supplied=False,
        bounded_Hurwitz_supplier_reached=False,seven_factor_gather_reached=False,residual_thirteen_closure_proved=False,
        reverse_fibration_equivalence_proved=False,preferred_proof_changed=False,adopted=False,
        scope='The exact new Hstar is G-conjugate to literal actual source B.7 by the explicit nine-occurrence SOURCE group word R=M a M^-1 P^-1. Every equality is faithful in B6; only the stated boundary/B.7 commutation is checked, no source centrality in B6 assumed. Negative powers occur solely inside the conjugator, never as Lefschetz factors. The normalized endpoint has disk support18. No intermediate source20 Hurwitz state, bounded physical supplier/gather, donor invariance, factor replacement, residual13-factor closure or fibration equivalence is asserted. Reference C.7 is a proof curve, never an invented source actor. The one-slot countercheck is hypothetical and nonclosing.')
