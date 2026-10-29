"""A12 rose loan reconstructs an equal125 root near the residual daisy."""
from dataclasses import replace

from .early_boundary_pure import _PositiveReplay
from .factorization_explorer import Factor
from .outside_half_lantern import _matches
from .outside_rose_return import _terms, _transport, _witness
from .posthalf_cyclic_rose import cyclic_pattern
from .posthalf_exterior import _outputs
from .posthalf_outer import _certify, _preview
from .projected_relations import pc_rose_terms, pc_daisy_terms
from .six_seven_structure import research_hurwitz_move


def expose_hybrid_third_exterior(factors, canonical_lantern_witness):
    source = tuple(factors)
    if len(source) != 13 or tuple(f.id for f in source[:2]) != ('upper.O1234', 'upper.I24'):
        raise ValueError('Use the reached upper-cabled13-record endpoint')
    r = _PositiveReplay(source)
    r.stages[0]['title'] = 'The reached upper-cabled two-exterior source'
    previews = []

    def drag(name, target, *, after=False, title):
        p = _preview(r, name, target, after=after)
        if not p['bounded']:
            raise ValueError('Reject the FULL proposed gather before application')
        previews.append(p)
        r.drag(name, target, after=after, title=title)
        if r.factors != p['factors']:
            raise ValueError('The bounded whole gather must rejoin literally')

    parent = next(f for f in source if f.id == 'reflected.inner125')
    canonical = Factor('canonical.R123', (), 1, 3)
    rose = _terms(canonical.mapping_class, 'canonical.rose.', pc_rose_terms)
    loan = _terms(parent.mapping_class, 'hybrid.first.', pc_rose_terms)
    r.substitute(r.position(parent.id), 1, loan,
                 'The ACTUAL125 PC rose lends12 and retains both other petals', 'disk_pc_rose')
    _witness(r, (canonical,), parent.conjugator, canonical_rose=rose)
    _outputs(r, rose, parent.conjugator)
    drag('hybrid.first.0', 'outer.loan.2', after=True,
         title='SAME12 UP2 across only the commuting exterior and45')
    restored = replace(parent, id='hybrid.R125')
    terms = _terms(parent.mapping_class, 'canonical.tail.', pc_rose_terms)
    pattern, cycle = cyclic_pattern(parent, terms, 1)
    i = r.position('outer.loan.1')
    _matches(r.factors[i:i + 3], pattern)
    r.substitute(i, 3, (restored,),
                 'ACTUAL older15,older25,NEW12 contract by the cyclic125 rose', 'disk_pc_rose')
    _witness(r, pattern, canonical_parent=parent, canonical_rose=terms,
             internal_cyclic_certificate=cycle)
    _outputs(r, (parent,))
    chart = parent.conjugator + (1,)
    rechart = replace(restored, conjugator=chart)
    parent_matches = _matches((restored,), (rechart,))
    second = _terms(rechart.mapping_class, 'hybrid.second.', pc_rose_terms)
    r.substitute(r.position(restored.id), 1, second,
                 'ACTUAL internal(+1)125 rose supplies neededNEW15', 'disk_pc_rose')
    _witness(r, (canonical,), chart, canonical_rose=rose,
             source_parent=restored, individual_parent_rechart=parent_matches)
    _outputs(r, rose, chart)
    drag('hybrid.second.2', 'alternative.return.2', after=True,
         title='SAME NEW15 UP2 through its actual donor leftovers')
    parent4 = Factor('canonical.D2345', (), 2, 4)
    daisy4 = _terms(parent4.mapping_class, 'canonical.D4.', pc_daisy_terms)
    internal = research_hurwitz_move(daisy4, 1, 0)
    pattern4, cycle4 = cyclic_pattern(parent4, internal['factors'], 1)
    g = (1, 2, 3)
    i = r.position('alternative.return.0')
    _matches(r.factors[i:i + 4], _transport(pattern4, g))
    outer = Factor('hybrid.O1345', (1,), 2, 4)
    r.substitute(i, 4, (outer,),
                 'FOUR ACTUAL inputs contract by the matched modified cyclic PC daisy', 'disk_pc_daisy')
    _witness(r, pattern4, g, canonical_parent=parent4, canonical_daisy=daisy4,
             retained_internal_interchange=internal, internal_cyclic_certificate=cycle4)
    _outputs(r, (parent4,), g)
    drag('upper.I24', 'upper.O1234',
         title='Commute the SAME I24 UP across the standard outer')
    drag('hybrid.second.1', 'hybrid.second.0',
         title='Carry the SAME changed25 UP across the changed12 leftover')
    base = tuple(canonical_lantern_witness['canonical_base'])
    if tuple((f.conjugator, f.first, f.points) for f in base) != (((), 1, 4), ((), 4, 2), ((-4,), 1, 4)):
        raise ValueError('Retain the complete saved D4,Q45,Ominus named lantern')
    interchange = research_hurwitz_move(base, 2, 1)
    g = (-2, -3)
    i = r.position('upper.O1234')
    _matches(r.factors[i:i + 3], _transport(interchange['factors'], g))
    outputs = (Factor('hybrid.exterior', (), 1, 5),
               r.normalize(Factor('hybrid.inner134', g, 1, 3)))
    r.substitute(i, 3, outputs,
                 'ACTUAL1234,1345,changed25 contract by the matched cabled PC lantern', 'disk_cluster_lantern')
    _witness(r, interchange['factors'], g,
             retained_named_canonical_base=canonical_lantern_witness,
             retained_internal_interchange=interchange)
    _outputs(r, (Factor('canonical.D5', (), 1, 5), canonical), g)
    result = _certify(r)
    result.update(preapplication_previews=tuple(previews), named_substitutions=5,
                  selected=False, complete_hybrid_join_reached=False,
                  scope='NINE positive DISK operations/SIX external adjacent checks reach a '
                        'third standard unit exterior using an explicitly consumed12 rose loan. '
                        'The older15/25 are consumed; the first125 donor remains two15/25 '
                        'petals, while the second125 and134/45/35/NEW15 become an outer '
                        'and then the third exterior/inner134. No sphere redraw or cap. '
                        'Both earlier unit exteriors remain explicit. No complete suffix '
                        'join or preferred adoption is claimed.')
    return result


def close_hybrid_residual(factors):
    """A longer explicit closure; keep its late retangling visible."""
    from .braid_actions import inverse_word
    from .factorization_explorer import product
    from .posthalf_exterior import _cyclic
    source = tuple(factors)
    if len(source) != 11 or tuple(f.id for f in source[:4]) != (
            'upper.I24', 'hybrid.exterior', 'hybrid.inner134', 'hybrid.second.0'):
        raise ValueError('Use the reached hybrid third-exterior endpoint')
    r = _PositiveReplay(source)
    r.stages[0]['title'] = 'The reached hybrid third-exterior endpoint'
    previews = []
    _cyclic(r, 'hybrid.inner134')
    names = ('reflected.loan.2', 'upper.I24')
    actors = tuple(next(f for f in source if f.id == n) for n in names)
    crossed = []
    while r.factors[r.position(names[0]) - 1].id != 'hybrid.second.0':
        neighbor = r.factors[r.position(names[0]) - 1].id
        crossed.append(neighbor)
        for name in names:
            p = _preview(r, name, neighbor)
            if not p['bounded']:
                raise ValueError('Reject the complete ordered-block closure before application')
            previews.append(p)
            r.drag(name, neighbor, title='SAME ' + name + ' UP across ' + neighbor)
            if r.factors != p['factors']:
                raise ValueError('The bounded block replay must rejoin literally')
    if tuple(crossed) != ('posthalf.exterior', 'reflected.output.1', 'hybrid.first.2',
                          'hybrid.first.1', 'reflected.exterior', 'cyclic135.supply.2'):
        raise ValueError('Retain the entire six-neighbor block trajectory')
    d4 = Factor('hybrid.final.O1234', (), 1, 4)
    daisy4 = _terms(d4.mapping_class, 'canonical.final.D4.', pc_daisy_terms)
    chart4 = (1, -3, -3, 1, 2, 3, 1, 2, 1)
    _matches(r.factors[:4], _transport(daisy4, chart4))
    r.substitute(0, 4, (d4,), 'FOUR ACTUAL residual inputs contract by the matched PC daisy', 'disk_pc_daisy')
    _witness(r, daisy4, chart4, canonical_parent=Factor('canonical.D4', (), 1, 4),
             canonical_daisy=daisy4)
    _outputs(r, (Factor('canonical.D4', (), 1, 4),), chart4)
    p = _preview(r, 'reflected.exterior', 'reflected.output.1')
    if not p['bounded']:
        raise ValueError('Reject the exterior gather before application')
    previews.append(p)
    r.drag('reflected.exterior', 'reflected.output.1',
           title='SAME odd exterior DOWN3 through only commuting residual petals')
    if r.factors != p['factors']:
        raise ValueError('The complete exterior gather must rejoin literally')
    d5 = Factor('canonical.D5', (), 1, 5)
    daisy5 = _terms(d5.mapping_class, 'canonical.final.D5.', pc_daisy_terms)
    pattern = daisy5
    internal = []
    for a, b in ((3, 4), (3, 2), (4, 3)):
        m = research_hurwitz_move(pattern, a, b)
        internal.append(m)
        pattern = m['factors']
    chart5 = inverse_word(product(actors))
    _matches(r.factors[:5], _transport(pattern, chart5))
    output = Factor('hybrid.fourth.exterior', (), 1, 5)
    r.substitute(0, 5, (output,), 'FIVE ACTUAL residual inputs contract by the modified PC D5 daisy', 'disk_pc_daisy')
    _witness(r, pattern, chart5, canonical_parent=d5, canonical_daisy=daisy5,
             retained_internal_interchanges=tuple(internal))
    _outputs(r, (d5,), chart5)
    result = _certify(r)
    if len(r.factors) != 4:
        raise ValueError('Retain FOUR visible standard unit exteriors')
    matches = _matches(r.factors, (d5,) * 4)
    result.update(preapplication_previews=tuple(previews), actual_ordered_actors=actors,
                  crossed_neighbors=tuple(crossed), named_substitutions=2,
                  terminal_standard_unit_matches=matches, useful_complete_join_reached=True,
                  selected=False, scope='SIXTEEN positive DISK operations/FIFTEEN external '
                  'adjacent checks reach FOUR visible standard unit exteriors. The '
                  'longer late block visibly retangles several curves and is not a '
                  'claim of uniform clarity improvement or a preferred adoption. '
                  'Every full context and named input/output is retained; no cap.')
    return result
