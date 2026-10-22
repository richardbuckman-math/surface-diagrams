"""Positive, bounded elimination of all half twists in the early B5 chart.

Every retained arrow is a split, a fixed-factor drag, a combine, a PC daisy,
a central cyclic start, or an explicit common frame.  This advances the
geometric research; it does not supply a named proof of the boundary product.
"""
from dataclasses import replace

from .braid_actions import inverse_word, reduce_word
from .factorization_explorer import Factor, product
from .framed_boundary_relations import enclosed_boundaries, framed_outer_certificate
from .mapping_classes import exact_action, supported_class
from .projected_relations import pc_daisy_terms
from .puncture_boundary import BOUNDARY_WORD
from .six_seven_structure import research_hurwitz_move
from .twist_simplify import simplify_twist


def _score(factors):
    lengths = tuple(len(supported_class(f.mapping_class, 5)) for f in factors)
    return dict(max_support_word=max(lengths), total_support_word=sum(lengths),
                braid_letters=len(product(factors)))


class _PositiveReplay:
    def __init__(self, factors):
        self.expected = exact_action(BOUNDARY_WORD * 4, 5)
        self.factors = self.check(tuple(factors))
        self.stages = [dict(kind='start', title='The positive cluster-lantern endpoint',
                            factors=self.factors, score=_score(self.factors),
                            half_twists=sum(f.half for f in self.factors))]

    def position(self, name):
        return next(i for i, f in enumerate(self.factors) if f.id == name)

    def check(self, factors):
        if any(getattr(f, 'sign', 1) != 1 for f in factors):
            raise ValueError('The purification route requires positive factors')
        if exact_action(product(factors), 5) != self.expected:
            raise ValueError('The purification route changed the fourth-boundary product')
        if _score(factors)['max_support_word'] > 20:
            raise ValueError('The purification route exceeded its support-word bound of 20')
        return tuple(factors)

    def normalize(self, factor):
        twist = simplify_twist(factor.mapping_class, strands=5)
        result = replace(factor, conjugator=twist.conjugator, first=twist.first)
        if exact_action(factor.word, 5) != exact_action(result.word, 5):
            raise ValueError('A purification presentation changed the disk action')
        return result

    def record(self, title, kind, **extra):
        self.stages.append(dict(title=title, kind=kind, factors=self.factors,
                                score=_score(self.factors),
                                half_twists=sum(f.half for f in self.factors), **extra))

    def substitute(self, index, count, terms, title, kind):
        before = self.factors[index:index + count]
        terms = tuple(terms)
        if exact_action(product(before), 5) != exact_action(product(terms), 5):
            raise ValueError('The proposed positive local substitution failed in B5')
        self.factors = self.check(self.factors[:index] + terms + self.factors[index + count:])
        self.record(title, kind, local_before=before, local_after=terms,
                    exact_disk_equality=True)

    def split(self, name, left, right):
        i = self.position(name)
        f = self.factors[i]
        if f.half or f.power != 2:
            raise ValueError('This power split needs a squared Dehn twist')
        self.substitute(i, 1, (replace(f, id=left, power=1), replace(f, id=right, power=1)),
                        'Split ' + name + ' into its two positive units', 'disk_split')

    def drag(self, name, target_name, *, after=False, title=None):
        source, target = self.position(name), self.position(target_name)
        if after:
            target += 1
        if source == target:
            raise ValueError('A recorded drag must cross at least one neighbor')
        original = self.factors[source]
        atomic = []
        while source != target:
            neighbor = source + (1 if source < target else -1)
            move = research_hurwitz_move(self.factors, source, neighbor)
            fs = list(move['factors'])
            fs[source] = self.normalize(fs[source])
            self.factors = self.check(tuple(fs))
            atomic.append(dict(move, factors=self.factors))
            source = neighbor
        if self.factors[target] != original:
            raise ValueError('A fixed-factor drag changed the dragged factor')
        self.record(title or ('Drag ' + name + (' down' if atomic[0]['source'] < atomic[0]['target'] else ' up')),
                    'disk_hurwitz_block', adjacent_moves=len(atomic), atomic_steps=tuple(atomic))

    def combine(self, left, right, name):
        i, j = self.position(left), self.position(right)
        if j != i + 1:
            raise ValueError('Matching factors must be adjacent before combining')
        a, b = self.factors[i:j + 1]
        if a.half != b.half or a.points != b.points or exact_action(
                replace(a, power=1).word, 5) != exact_action(replace(b, power=1).word, 5):
            raise ValueError('The factors do not have the same positive supported twist')
        if a.half:
            if a.power != 1 or b.power != 1:
                raise ValueError('The arc consolidation needs two unit half twists')
            term = replace(a, id=name, half=False)
        else:
            term = replace(a, id=name, power=a.power + b.power)
        self.substitute(i, 2, (term,), 'Combine the matching ' + left + ' and ' + right,
                        'disk_combine')


def purify_early_cluster(factors):
    """Remove all eight halves of the positive branch in 24 explicit operations.

    First eliminate the ORIGINAL F3/F9 pair.  A daisy then consolidates the
    four extra halves introduced by the earlier round-square split.  Finally
    a real cyclic start brings a T12 square around the short side to match
    F6/F11.  A common frame and a root reorder keep the final gather bounded.
    No inverse factor or sphere move is used.  The remaining named boundary
    derivation is still open; its based-action certificate is independent.
    """
    factors = tuple(factors)
    expected_ids = ('early.K.2', 'early.K.1', 'prefix.P12', 'early.R123.remaining',
                    'early.tail.1', 'early.tail.2', 'early.tail.T12', 'F3', 'F5',
                    'early.O1345', 'early.P35', 'F6', 'F8.2', 'F9', 'F10.2',
                    'F11', 'F12', 'F13')
    if tuple(f.id for f in factors) != expected_ids or sum(f.half for f in factors) != 8:
        raise ValueError('Use the saved positive early cluster endpoint')
    r = _PositiveReplay(factors)

    # The exposed P35 really matches F3/F9 after these two root transports.
    r.split('F5', 'early.F5.1', 'early.F5.2')
    r.drag('early.F5.1', 'F3', title='Carry one F5 root up across F3')
    r.split('F13', 'early.F13.1', 'early.F13.2')
    r.drag('early.F13.1', 'F9', title='Carry one F13 root up across four neighbors')
    r.drag('early.P35', 'F3', title='P35 transports F3 to exactly the current F9 arc')
    a, b = (r.factors[r.position(name)] for name in ('F3', 'F9'))
    if exact_action(a.word, 5) != exact_action(b.word, 5):
        raise ValueError('The original F3/F9 half twists did not become equal')
    # Stop immediately BEFORE F9; the dragged F3 remains fixed.
    destination = r.factors[r.position('F9') - 1].id
    r.drag('F3', destination, title='Drag the matched F3 down to F9; F6 becomes short')
    r.combine('F3', 'F9', 'early.P13.pair')
    first_pair_end = len(r.stages) - 1

    # The alternate daisy's last petal is exactly the saved Q14.
    i = r.position('early.O1345')
    outer = r.factors[i]
    terms = tuple(Factor('early.daisy.' + str(j + 1), (-4,) + t.conjugator,
                         t.first, t.points, t.power, t.half)
                  for j, t in enumerate(pc_daisy_terms(outer.mapping_class)))
    q = Factor('target.Q14', (-4, 1, 2, 3), 4, 2)
    if exact_action(terms[-1].word, 5) != exact_action(q.word, 5):
        raise ValueError('The alternate daisy did not expose the actual Q14')
    r.substitute(i, 1, terms, 'PC daisy of O1345, conjugated inside by sigma4 inverse', 'disk_pc_daisy')
    r.drag('early.daisy.4', 'prefix.P12', title='Carry the actual Q14 petal up; the two H12 arcs match')
    r.drag('early.tail.1', 'early.K.1', after=True, title='Gather the two exact H12 arcs')
    r.combine('early.K.1', 'early.tail.1', 'early.H12.pair')
    r.drag('early.tail.2', 'early.K.2', after=True, title='Gather the two exact H23 arcs')
    r.combine('early.K.2', 'early.tail.2', 'early.H23.pair')
    extra_pairs_end = len(r.stages) - 1

    # Short side of the central boundary product, NOT a new sphere move.
    r.split('F12', 'early.F12.1', 'early.F12.2')
    r.drag('early.F12.1', 'F11', title='One C12 root shortens the final F11 arc')
    r.drag('early.tail.T12', 'prefix.P12', after=True, title='Gather the two round T12 twists across R123')
    r.combine('prefix.P12', 'early.tail.T12', 'early.T12.square')
    r.drag('early.T12.square', 'early.H23.pair', title='Carry the round T12 square to the top')
    moved = r.factors[0]
    r.factors = r.check(r.factors[1:] + r.factors[:1])
    r.record('Rotate the first factor to the bottom of the central product', 'disk_cyclic_start',
             moved_factor=moved, central_product=BOUNDARY_WORD * 4, exact_disk_equality=True)
    r.drag('early.T12.square', 'F11', title='Carry T12 squared up the short side; F11 now equals F6')
    a, b = (r.factors[r.position(name)] for name in ('F6', 'F11'))
    if exact_action(a.word, 5) != exact_action(b.word, 5):
        raise ValueError('The cyclic transport did not match the last two halves')
    frame = (3, 4, 4)
    r.factors = r.check(tuple(r.normalize(replace(f, conjugator=reduce_word(frame + f.conjugator)))
                              for f in r.factors))
    r.record('Common disk frame removes the shared winding before the last gather',
             'global_conjugation', frame=frame, central_product=BOUNDARY_WORD * 4,
             exact_disk_equality=True)
    r.drag('early.F12.1', 'F10.2', title='Reorder C12 before C10 to keep the next transport bounded')
    r.drag('F11', 'F6', after=True, title='Bring the last matched half twists together')
    r.combine('F6', 'F11', 'early.P24.pair')

    units = tuple(replace(f.mapping_class, power=1) for f in r.factors for _ in range(f.power))
    inner_powers = framed_outer_certificate(5, units, 4)
    if any(f.half for f in r.factors) or len(r.stages) != 25:
        raise ValueError('The purification did not reach its declared all-Dehn-twist endpoint')
    by_id = {f.id: f for f in r.factors}
    q = Factor('pure.target.Q15', (-4, 3, -2), 1, 2)
    outer = Factor('pure.target.O1245', (3, 4), 1, 4)
    inner = Factor('pure.target.T24', (3,), 2, 2)
    next_before = (by_id['early.R123.remaining'], by_id['early.F5.1'], q)
    next_after = (outer, inner)
    petal_source = by_id['early.F12.2']
    petals = pc_daisy_terms(petal_source.mapping_class)
    if (exact_action(product(next_before), 5) != exact_action(product(next_after), 5)
            or exact_action(petals[-1].word, 5) != exact_action(q.word, 5)):
        raise ValueError('The next cluster-lantern target failed its exact ordered check')
    chapters = (('earlypair', 0, first_pair_end),
                ('earlydaisy', first_pair_end, extra_pairs_end),
                ('earlypure', extra_pairs_end, len(r.stages) - 1))
    phases = {name: (dict(r.stages[start], kind='start'),) + tuple(r.stages[start + 1:end + 1])
              for name, start, end in chapters}
    return dict(stages=tuple(r.stages), phases=phases, factors=r.factors,
                graphical_steps=24, adjacent_checks=sum(s.get('adjacent_moves', 0) for s in r.stages),
                sphere_move_count=0, all_factors_positive=True, half_twists_remaining=0,
                before_score=_score(factors), after_score=_score(r.factors), peak_support_bound=20,
                boundary_power=4, disk_action_verified=True, complete_named_derivation=False,
                next_lantern=dict(local_before=next_before, local_after=next_after,
                    source_root=petal_source, daisy_terms=petals, exact_disk_equality=True,
                    applied_to_replay=False, requires_gathering=True),
                framed_boundary=dict(inner_boundaries=5, outer_power=4, inner_powers=inner_powers,
                    supports=tuple(enclosed_boundaries(t, 5) for t in units),
                    exact_capped_action_and_framing=True,
                    scope='A separately framed five-hole relation; the new disk moves do not silently turn the sphere points into holes.'),
                scope='All eight halves in this branch have become positive full twists. This is not the missing short named derivation of the fourth-boundary product.')


def contract_pure_clusters(factors):
    """Compute two positive cluster contractions; the caller controls publication.

    Two actual daisy petals supply a cluster lantern and a three-point PC
    lantern.  The canonical OUTER frame (-4,-3) is essential: using the
    unframed cyclic gather peaks at 36, whereas this route stays at most 20.
    This is additional geometric progress, not the missing named closure.
    """
    factors = tuple(factors)
    if (len(factors) != 19 or any(f.half for f in factors)
            or factors[-2].id != 'early.F12.2' or factors[-1].id != 'early.F13.2'):
        raise ValueError('Use the all-pure endpoint of purify_early_cluster')
    r = _PositiveReplay(factors)
    r.stages[0]['title'] = 'The all-pure nineteen-factor endpoint'
    frame = (-4, -3)
    source_root = factors[-2]
    r.factors = r.check(tuple(r.normalize(replace(f, conjugator=reduce_word(frame + f.conjugator)))
                              for f in r.factors))
    r.record('Put the next four-point outer curve in its round disk chart',
             'global_conjugation', frame=frame, central_product=BOUNDARY_WORD * 4,
             exact_disk_equality=True)
    terms = tuple(r.normalize(Factor('pure.next.' + str(j + 1), frame + t.conjugator,
                                    t.first, t.points, t.power, t.half))
                  for j, t in enumerate(pc_daisy_terms(source_root.mapping_class)))
    r.substitute(r.position(source_root.id), 1, terms,
                 'PC daisy of the actual C12 unit exposes Q15', 'disk_pc_daisy')
    r.drag('pure.next.3', 'early.F13.2', title='Carry Q15 past the final three-point root')
    moved = r.factors[-1]
    r.factors = r.check(r.factors[-1:] + r.factors[:-1])
    r.record('Rotate the last Q15 to the top of the central disk product', 'disk_cyclic_start',
             moved_factor=moved, central_product=BOUNDARY_WORD * 4, exact_disk_equality=True)
    r.drag('pure.next.3', 'early.F5.1', title='Bring Q15 through the leading pair curves and the two roots')
    outer = Factor('pure.O1234', (), 1, 4)
    inner = Factor('pure.T23', (), 2, 2)
    r.substitute(r.position('early.R123.remaining'), 3, (outer, inner),
                 'PC cluster lantern produces a round four-point curve and T23',
                 'disk_cluster_lantern')
    first_contraction = len(r.stages) - 1

    source_root = r.factors[-1]
    terms = tuple(r.normalize(Factor('pure.prefix.daisy.' + str(j + 1), t.conjugator,
                                    t.first, t.points, t.power, t.half))
                  for j, t in enumerate(pc_daisy_terms(source_root.mapping_class)))
    r.substitute(len(r.factors) - 1, 1, terms,
                 'The final C13 daisy supplies the precise missing prefix petal', 'disk_pc_daisy')
    r.drag('pure.prefix.daisy.1', 'pure.prefix.daisy.3',
           title='Carry the first petal through the other two daisy petals')
    moved = r.factors[-1]
    r.factors = r.check(r.factors[-1:] + r.factors[:-1])
    r.record('Rotate this last petal to the top of the central product', 'disk_cyclic_start',
             moved_factor=moved, central_product=BOUNDARY_WORD * 4, exact_disk_equality=True)
    r.drag('pure.prefix.daisy.1', 'early.H12.pair',
           title='The supplied petal joins the two leading pair curves')
    root = Factor('pure.prefix.root', (-3, -2, 1), 2, 3)
    r.substitute(0, 3, (root,), 'PC lantern contracts the two long prefix curves and their actual petal',
                 'disk_cluster_lantern')
    r.drag('early.T12.square', 'F8.2',
           title='Carry the fixed pair square up across five neighbors; geometric crossings drop')
    by_id = {f.id: f for f in r.factors}
    target = Factor('outer.target.C145', (-3, -3, -1, 2), 3, 3)
    q23 = Factor('outer.target.Q23', (-3, -1, -1, -3), 2, 2)
    q14 = Factor('outer.target.Q14', (-3, -3, -1, -3), 2, 2)
    exterior = Factor('outer.boundary', (), 1, 5)
    next_before = (by_id['pure.O1234'], target, by_id['early.F13.1'])
    next_after = (exterior, q23, q14)
    if exact_action(product(next_before), 5) != exact_action(product(next_after), 5):
        raise ValueError('The constructed exterior-lantern target failed its ordered B5 check')
    actual_middle = by_id['early.F12.1']
    return dict(stages=tuple(r.stages), factors=r.factors, graphical_steps=len(r.stages) - 1,
                adjacent_checks=sum(s.get('adjacent_moves', 0) for s in r.stages),
                first_contraction=first_contraction, sphere_move_count=0,
                next_exterior_lantern=dict(local_before=next_before, local_after=next_after,
                    actual_middle=actual_middle, current_middle_already_matches=
                    exact_action(actual_middle.word, 5) == exact_action(target.word, 5),
                    exact_disk_equality=True, requires_transport=True, applied_to_replay=False),
                all_factors_positive=True, half_twists_remaining=0,
                before_score=_score(factors), after_score=_score(r.factors), peak_support_bound=20,
                boundary_power=4, disk_action_verified=True, complete_named_derivation=False,
                applied_to_public_replay=False,
                scope='Two positive lantern contractions and a geometric unwinding are exactly replayed; the named boundary closure remains open.')
