"""A bounded opposite ordered-block closure with two fully matched daisies."""
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


def close_hybrid_opposite_block(factors):
    """Carry the actual R134/12 block DOWN and retain both matched daisies."""
    from .braid_actions import reduce_word
    from .factorization_explorer import product
    from .posthalf_exterior import _cyclic
    source = tuple(factors)
    expected = ('upper.I24', 'hybrid.exterior', 'hybrid.inner134', 'hybrid.second.0',
                'cyclic135.supply.2', 'reflected.exterior', 'hybrid.first.1',
                'hybrid.first.2', 'reflected.output.1', 'posthalf.exterior', 'reflected.loan.2')
    if tuple(f.id for f in source) != expected or any(f.half or f.power != 1 for f in source):
        raise ValueError('Use the reached eleven-record hybrid third-exterior source')
    r = _PositiveReplay(source)
    r.stages[0]['title'] = 'The reached hybrid third-exterior source'
    before = {f.id: f for f in source}
    actors = tuple(before[n] for n in ('hybrid.inner134', 'hybrid.second.0'))
    chart = product(actors)
    previews = []
    def drag(name, target):
        p = _preview(r, name, target)
        if not p['bounded']:
            raise ValueError('Reject the complete proposed crossing before application')
        previews.append(p)
        r.drag(name, target)
        if r.factors != p['factors']:
            raise ValueError('The raw bounded preview and normalized replay must join literally')
    _cyclic(r, 'hybrid.inner134')
    crossed = ('cyclic135.supply.2', 'reflected.exterior', 'hybrid.first.1',
               'hybrid.first.2', 'reflected.output.1', 'posthalf.exterior')
    for neighbor in crossed:
        # For [a,b,x], moving b THEN a DOWN gives [ab x (ab)^-1,a,b].
        for name in ('hybrid.second.0', 'hybrid.inner134'):
            drag(name, neighbor)
    after = {f.id: f for f in r.factors}
    if tuple(after[f.id] for f in actors) != actors:
        raise ValueError('Both actual block actors remain literal')
    actions = tuple(dict(source=before[n], actual=after[n],
                    raw_target=replace(before[n], conjugator=reduce_word(chart + before[n].conjugator)),
                    individual_match=_matches((after[n],), _transport((before[n],), chart)))
                    for n in crossed)
    d4 = Factor('opposite.O1234', (), 1, 4)
    daisy4 = _terms(d4.mapping_class, 'canonical.D4.', pc_daisy_terms)
    chart4 = (1, -3, -3, 1, 2, 3, 1, 2, 1)
    i = r.position('hybrid.inner134')
    _matches(r.factors[i:i+4], _transport(daisy4, chart4))
    r.substitute(i, 4, (d4,), 'FOUR actual residual inputs contract by the matched PC daisy', 'disk_pc_daisy')
    _witness(r, daisy4, chart4, canonical_parent=d4, canonical_daisy=daisy4)
    _outputs(r, (d4,), chart4)
    drag('reflected.exterior', 'reflected.output.1')
    drag('opposite.O1234', 'reflected.exterior')
    d5 = Factor('canonical.D5', (), 1, 5)
    daisy5 = _terms(d5.mapping_class, 'canonical.D5.', pc_daisy_terms)
    pattern = daisy5
    internal = []
    for a, b in ((3, 4), (3, 2), (4, 3)):
        move = research_hurwitz_move(pattern, a, b)
        internal.append(move)
        pattern = move['factors']
    pattern, cycle = cyclic_pattern(d5, pattern, 1)
    _matches(r.factors[:5], _transport(pattern, chart))
    output = Factor('opposite.exterior', (), 1, 5)
    r.substitute(0, 5, (output,), 'FIVE actual inputs contract by the cyclic modified PC D5 daisy', 'disk_pc_daisy')
    _witness(r, pattern, chart, canonical_parent=d5, canonical_daisy=daisy5,
             retained_internal_interchanges=tuple(internal), internal_cyclic_certificate=cycle)
    _outputs(r, (d5,), chart)
    result = _certify(r)
    exteriors = tuple(f for f in source if f.points == 5)
    end = {f.id: f for f in r.factors}
    if any(end[f.id] != f for f in exteriors):
        raise ValueError('All THREE earlier odd unit exteriors remain literal')
    result.update(preapplication_previews=tuple(previews), actual_ordered_actors=actors,
                  crossed_neighbors=crossed, full_block_conjugation_matches=actions,
                  terminal_standard_unit_matches=_matches(r.factors, (d5,)*4),
                  retained_three_exteriors=exteriors, named_substitutions=2,
                  useful_complete_join_reached=True, selected=False,
                  scope='Seventeen positive DISK operations/seventeen external adjacent checks '
                        'close the actual third-exterior source to four visible standard units. '
                        'The opposite ordered block has support peak12 rather than the saved '
                        'closure peak18; its four changed curves have mixed endpoint tradeoffs. '
                        'No arc/joint-minimum/whole-proof bound, sphere move, cap, global frame '
                        'or preferred adoption is claimed.')
    return result
