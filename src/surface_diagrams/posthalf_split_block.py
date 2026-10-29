"""Split the two actual daisy blocks so the late35 stays short."""
from dataclasses import replace
from .braid_actions import inverse_word, reduce_word
from .early_boundary_pure import _PositiveReplay
from .factorization_explorer import Factor, product
from .outside_half_lantern import _matches
from .outside_rose_return import _terms, _transport, _witness
from .posthalf_exterior import _cyclic, _outputs
from .posthalf_outer import _certify, _preview
from .projected_relations import pc_daisy_terms
from .six_seven_structure import research_hurwitz_move


def close_hybrid_split_block(factors, *, inverse_preparation=True):
    """A complete positive closure; internal preparation and undo are actual moves."""
    source = tuple(factors)
    expected = ('upper.I24','hybrid.exterior','hybrid.inner134','hybrid.second.0',
                'cyclic135.supply.2','reflected.exterior','hybrid.first.1',
                'hybrid.first.2','reflected.output.1','posthalf.exterior','reflected.loan.2')
    if tuple(f.id for f in source) != expected or any(f.half or f.power != 1 for f in source):
        raise ValueError('Use the reached eleven-record hybrid third-exterior source')
    before = {f.id:f for f in source}
    left = tuple(before[n] for n in ('hybrid.inner134','hybrid.second.0'))
    right = tuple(before[n] for n in ('reflected.loan.2','upper.I24'))
    r = _PositiveReplay(source)
    r.stages[0]['title'] = 'The reached hybrid third-exterior source'
    previews = []
    def move(name, target, title):
        p = _preview(r,name,target)
        if not p['bounded']:
            raise ValueError('Reject the complete proposed crossing before application')
        previews.append(p)
        r.drag(name,target,title=title)
        if r.factors != p['factors']:
            raise ValueError('Bounded raw preview and normalized replay must join literally')
    _cyclic(r,'hybrid.inner134')
    left_crossed = ('cyclic135.supply.2','reflected.exterior','hybrid.first.1','hybrid.first.2')
    for neighbor in left_crossed:
        for actor in ('hybrid.second.0','hybrid.inner134'):
            move(actor,neighbor,'SAME '+actor+' DOWN across '+neighbor)
    if tuple(r.factors[r.position(f.id)] for f in left) != left:
        raise ValueError('Both left block actors must remain literal')
    if inverse_preparation:
        move('upper.I24','reflected.loan.2','INVERSE preparation of the actual old23/I24 block')
        names = ('upper.I24','reflected.loan.2')
    else:
        names = ('reflected.loan.2','upper.I24')
    prepared = tuple(r.factors[r.position(n)] for n in names)
    preparation_product_matches = _matches_word(product(prepared),product(right))
    right_crossed = ('posthalf.exterior','reflected.output.1')
    for neighbor in right_crossed:
        for actor in names:
            move(actor,neighbor,'SAME '+actor+' UP across '+neighbor)
    if tuple(r.factors[r.position(f.id)] for f in prepared) != prepared:
        raise ValueError('Both prepared right block actors must stay literal during transport')
    if inverse_preparation:
        move('upper.I24','reflected.loan.2','UNDO the actual inverse preparation')
    restored = tuple(r.factors[r.position(f.id)] for f in right)
    restored_matches = _matches(restored,right)
    after = {f.id:f for f in r.factors}
    actions = []
    for names, frame in ((left_crossed,product(left)),(right_crossed,inverse_word(product(right)))):
        for name in names:
            raw = replace(before[name],conjugator=reduce_word(frame+before[name].conjugator))
            actions.append(dict(source=before[name],actual=after[name],raw_target=raw,
                                individual_match=_matches((after[name],),(raw,))))
    d4 = Factor('split.O1234',(),1,4)
    terms4 = _terms(d4.mapping_class,'canonical.D4.',pc_daisy_terms)
    chart4 = (1,-3,-3,1,2,3,1,2,1)
    i = r.position('hybrid.inner134')
    _matches(r.factors[i:i+4],_transport(terms4,chart4))
    r.substitute(i,4,(d4,),'FOUR actual inputs contract by the matched PC daisy','disk_pc_daisy')
    _witness(r,terms4,chart4,canonical_parent=d4,canonical_daisy=terms4)
    _outputs(r,(d4,),chart4)
    move('reflected.exterior','reflected.output.1','SAME odd exterior DOWN4 across commuting residual inputs')
    d5 = Factor('canonical.D5',(),1,5)
    terms5 = _terms(d5.mapping_class,'canonical.D5.',pc_daisy_terms)
    pattern = terms5
    internal = []
    for a,b in ((3,4),(3,2),(4,3),(0,1),(1,2),(2,3)):
        step = research_hurwitz_move(pattern,a,b)
        internal.append(step)
        pattern = step['factors']
    chart5 = inverse_word(product(right))
    _matches(r.factors[:5],_transport(pattern,chart5))
    output = Factor('split.exterior',(),1,5)
    r.substitute(0,5,(output,),'FIVE actual mixed-block inputs contract by the modified PC D5 daisy','disk_pc_daisy')
    _witness(r,pattern,chart5,canonical_parent=d5,canonical_daisy=terms5,
             retained_internal_interchanges=tuple(internal))
    _outputs(r,(d5,),chart5)
    result = _certify(r)
    end = {f.id:f for f in r.factors}
    exteriors = tuple(f for f in source if f.points == 5)
    if any(end[f.id] != f for f in exteriors):
        raise ValueError('All three earlier odd exteriors stay literal')
    result.update(preapplication_previews=tuple(previews),actual_left_actors=left,
                  original_right_actors=right,actual_prepared_right_actors=prepared,
                  prepared_product_matches_original=preparation_product_matches,
                  restored_right_actors=restored,restored_right_individual_matches=restored_matches,
                  restored_right_literal=tuple(a==b for a,b in zip(restored,right)),
                  left_crossed_neighbors=left_crossed,right_crossed_neighbors=right_crossed,
                  full_block_conjugation_matches=tuple(actions),inverse_preparation=inverse_preparation,
                  retained_three_exteriors=exteriors,named_substitutions=2,
                  terminal_standard_unit_matches=_matches(r.factors,(d5,)*4),
                  useful_complete_join_reached=True,selected=False,
                  scope='Complete split-block positive DISK closure. The left block changes '
                        '45/15/25; the right block changes only other35. Both crossed exteriors '
                        'are checked. Inverse preparation and undo are actual moves when chosen. '
                        'The restored old23 is B5-exact in a different normalized presentation, '
                        'not a claimed literal source tuple. No sphere move, cap, global frame '
                        'or preferred adoption; support words are chart-specific diagnostics.')
    return result


def _matches_word(left,right):
    from .mapping_classes import exact_action
    equal = exact_action(left,5)==exact_action(right,5)
    if not equal:raise ValueError('The full ordered block product changed')
    return dict(left=left,right=right,exact_disk_equal=equal,
                scope='Faithful B5 equality, not asserted raw free-word cancellation')
