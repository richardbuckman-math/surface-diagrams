"""A genuine (4,3) target using six existing curves; not an extraction."""
from dataclasses import replace
from .factorization_explorer import Factor,product
from .braid_actions import reduce_word,inverse_word
from .mapping_classes import exact_action,supported_class
from .hyperelliptic_homology import IDENTITY,homology_action,half_twist_class
from .small_fibration_derivations import action_match,full_kernel,score
from .six_seven_structure import research_hurwitz_move
from .sphere_actions import sphere_chain_certificate,sphere_curve_action
from .sphere_linking import sphere_linking_character


def short_four_three_target(source,reference_c):
    """Recognize the target against the independently known C block.

    The four accepted Hurwitz moves are INTERNAL to that reference (4,3),
    not moves on the twenty-factor source. Six source records are literal;
    the seventh half is only a desired class and has not been supplied.
    """
    source=tuple(source);reference_c=tuple(reference_c)
    if len(source)!=20 or len(reference_c)!=7:raise ValueError('Use the pinned twenty-factor source and seven-factor C block')
    by={f.id:f for f in source}
    c=tuple(replace(f,first=f.first+1,conjugator=tuple((1 if x>0 else -1)*(abs(x)+1) for x in f.conjugator)) for f in reference_c)
    g=(-5,)*4+(-2,)*2
    parent=by['four_three_C.5']
    h=replace(by['four_three_A.6'],id='target.Hstar',conjugator=reduce_word(g+parent.conjugator),first=parent.first)
    if half_twist_class(h.conjugator,h.first)!=(1,-6,-2,-1):raise ValueError('Keep the explicitly solved primitive homology target')
    target=tuple(by[name] for name in ('four_three_B.1','four_three_B.2','four_three_B.3','four_three_B.4'))+(h,by['four_three_C.5'],by['four_three_C.6'])
    boundary=Factor('embedded.D5.squared',(),2,5,power=2)
    if any(not ((f.half and f.points==2 and f.power==1) or (not f.half and f.points==3 and f.power==2)) for f in target):
        raise ValueError('Retain four positive halves and three positive separating twists')
    target_character=sphere_linking_character(product(target))
    if target_character['nonidentity_sphere_proved']:raise ValueError('Pass the necessary marked-sphere characters before action expansion')
    half_match=action_match(h.word,g+parent.word+inverse_word(g),6)
    previews=[]
    for name,steps in (
        ('direct_two',((5,6),(4,5))),
        ('inverse_preparation',((5,4),(5,6),(4,5),(5,6))),
        ('forward_preparation',((4,5),(5,6),(4,5),(6,5)))):
        current=c;atomic=[];failure=None
        for a,b in steps:
            raw=research_hurwitz_move(current,a,b)
            if raw['disk_word_certificate']['discrepancy']:raise ValueError('Raw free equality must precede all presentation checks')
            s=score(raw['factors'],6)
            if s['maximum']>20:
                failure=dict(source=a,target=b,raw_move=raw,raw_score=s,rejected_before_application=True)
                break
            atomic.append(dict(raw_move=raw,raw_score=s,preapplication_bound=20,factors=raw['factors']))
            current=raw['factors']
        previews.append(dict(name=name,steps=steps,reference_input=c,bounded_prefix_preview=tuple(atomic),
            failure=failure,whole_preview_passed=failure is None,reference_endpoint=current,
            selected=name=='forward_preparation',source_twenty_applied=False))
    if previews[0]['failure']['raw_score']['maximum']!=22 or previews[1]['failure']['raw_score']['maximum']!=106:
        raise ValueError('Preserve the direct22 and inverse106 bounded rejections')
    chosen=previews[2]
    if not chosen['whole_preview_passed']:raise ValueError('The entire chosen reference proof must pass before acceptance')
    states=(c,)+tuple(x['factors'] for x in chosen['bounded_prefix_preview'])
    matches=tuple(dict(target=a,reference=b,**action_match(a.word,b.word,6)) for a,b in zip(target,states[-1]))
    certificates=[]
    for factors in states+(target,):
        w=product(factors);disk=action_match(w,boundary.word,6)
        sphere=sphere_chain_certificate(w,max_letters=50000)
        lift=homology_action(w)
        if not sphere['certified'] or lift!=IDENTITY or score(factors,6)['maximum']>20:
            raise ValueError('Keep full disk, separate marked-sphere/+I and bounded reference-state checks')
        certificates.append(dict(factors=factors,score=score(factors,6),disk_boundary_match=disk,
            full_disk_discrepancy=reduce_word(w+inverse_word(boundary.word)),sphere=sphere,chosen_lift=lift))

    def restrict_vertical_first(word):
        if any(abs(x)<2 for x in word):raise ValueError('This inverse embedding requires a literally vertical first strand')
        lowered=tuple((1 if x>0 else -1)*(abs(x)-1) for x in word)
        images6=exact_action(word,6);images5=exact_action(lowered,5)
        shifted=((1,),)+tuple(tuple((1 if x>0 else -1)*(abs(x)+1) for x in row) for row in images5)
        if images6!=shifted:raise ValueError('The complete embedded actions must match')
        return dict(B6_word=word,embedded_B5_word=lowered,B6_images=images6,B5_images=images5,
            exact_inverse_embedding=True,scope='Restriction to the known embedded B5 subgroup with a vertical first strand; not deletion, a sphere move or a claim of centrality in B6.')
    unique={}
    for factors in states+(target,):
        for f in factors:unique.setdefault((f.word,f.half,f.points,f.power),f)
    individual=[]
    for f in unique.values():
        embedding=restrict_vertical_first(f.word)
        individual.append(dict(factor=f,embedding=embedding,full_B6_stabilizer_data=full_kernel(f.word,6),
            full_B5_stabilizer_data=full_kernel(embedding['embedded_B5_word'],5)))
    embedded=restrict_vertical_first(product(target));embedded_boundary=restrict_vertical_first(boundary.word)
    pure_products=[]
    for n,a,b in ((6,product(target),boundary.word),(5,embedded['embedded_B5_word'],embedded_boundary['embedded_B5_word'])):
        actual=full_kernel(a,n);reference=full_kernel(b,n)
        if not actual['applicable'] or not reference['applicable']:raise ValueError('The full product is pure')
        if actual['split'].kernel_loop!=reference['split'].kernel_loop:raise ValueError('Retain the complete nonabelian point-pushing loop')
        shadow=action_match(actual['split'].shadow_word,reference['split'].shadow_word,n-1)
        pure_products.append(dict(strands=n,actual=actual,reference=reference,nonabelian_kernel_literal=True,full_shadow_match=shadow))
    six=tuple(f for f in target if f.id!='target.Hstar')
    if any(by[f.id]!=f for f in six):raise ValueError('Keep all six published records literally')
    present=tuple(f.id for f in source if f.half and homology_action(f.word)==homology_action(h.word))
    if present:raise ValueError('This missing homology target should not already be a current half factor')
    # Same half target and character data, but the other source separator
    # with the same labeled support gives a genuinely different sphere word.
    alternative=(by['four_three_C.2'],by['four_three_B.1'],by['four_three_B.3'],by['four_three_B.4'],h,by['four_three_C.5'],by['four_three_C.6'])
    alternative_word=product(alternative)
    alt_character=sphere_linking_character(alternative_word)
    if alt_character['nonidentity_sphere_proved'] or homology_action(alternative_word)!=IDENTITY:
        raise ValueError('This comparison must pass the two necessary quotients first')
    pair=(1,2);image=sphere_curve_action(alternative_word,pair,max_letters=50000)
    reference=sphere_curve_action((),pair,max_letters=50000)
    if image==reference:raise ValueError('Keep the complete changed arc witness for the nearby target')
    old_images,new_images=exact_action(by['four_three_B.2'].word,6),exact_action(by['four_three_C.2'].word,6)
    if old_images==new_images:raise ValueError('Same labeled support is not curve equality')
    return dict(source_factors=source,reference_C_factors=c,reference_boundary=boundary,
        target_factors=target,missing_half=h,missing_half_parent=parent,missing_half_transport_word=g,
        missing_half_raw_conjugation_match=half_match,missing_half_homology_vector=(1,-6,-2,-1),
        target_sphere_character=target_character,
        proposed_source_ancestry='four_three_A.6',source_ancestry_supplied=False,
        current_half_homology_matches=present,
        six_literal_source_records=six,source_positions=tuple((f.id,next(i for i,x in enumerate(source) if x.id==f.id)) for f in six),
        target_supports=tuple(supported_class(f.mapping_class,6) for f in target),
        reference_previews=tuple(previews),chosen_internal_reference_states=states,
        internal_reference_adjacent_checks=4,reference_peak_support=18,
        all_seven_individual_reference_matches=matches,reference_and_target_certificates=tuple(certificates),
        every_actual_factor_stabilizer_or_full_action=tuple(individual),full_product_point_pushing=tuple(pure_products),
        embedded_B5_product=embedded,embedded_B5_boundary=embedded_boundary,
        nearby_unselected_target=dict(factors=alternative,character=alt_character,chosen_lift=IDENTITY,
            full_sphere_nonidentity_witness=dict(pair=pair,full_image=image,reference_class=reference),
            B2_images=old_images,C2_images=new_images,
            first_differing_meridian=next(i for i,(a,b) in enumerate(zip(old_images,new_images),1) if a!=b)),
        standalone_target_relation_complete=True,known_C_Hurwitz_equivalence_complete=True,
        source_twenty_actual_moves=0,source_twenty_target_gathered=False,whole_twenty_modified_sphere_relation_assumed=False,
        source_twenty_reverse_equivalence_proved=False,preferred_proof_changed=False,adopted=False,
        scope='A genuine bounded seven-factor (4,3) identity, recognized against known C by four bounded INTERNAL reference Hurwitz moves. Six records are copied literally from the published (10,10); the seventh is a desired half class, not supplied or reached. The C reference ID-to-target map is recognition only, not an ancestry transfer in the twenty-factor source. No whole-source gather, donor change, residual13-factor closure or reverse fiber-sum equivalence is asserted. Embedded D5^2 is checked faithfully, never assumed central in B6.')
