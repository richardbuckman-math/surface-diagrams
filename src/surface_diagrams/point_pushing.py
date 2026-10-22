"""Exact last-strand stabilizer splitting in the DISK braid group.

A braid fixing the last strand splits as push(loop) * embedded_shadow.
Deleting that strand alone is only a quotient.  The free point-pushing loop
is retained, and its braid uses the canonical under-passing pair twists.
Nothing here changes a disk into a sphere or drops boundary framing terms.
"""
from dataclasses import dataclass
from itertools import chain

from .braid_actions import inverse_word
from .mapping_classes import VerificationLimitError


@dataclass(frozen=True)
class SchreierEdge:
    position: int
    crossing: int
    next_position: int
    kind: str
    generator: int


@dataclass(frozen=True)
class PointPushingSplit:
    strands: int
    source_word: tuple
    shadow_word: tuple
    kernel_loop: tuple
    kernel_braid: tuple
    reconstructed_word: tuple
    edges: tuple
    work: int


class _Budget:
    def __init__(self, max_letters, max_work):
        if any(type(x) is not int or x < 1 for x in (max_letters, max_work)):
            raise ValueError('word and work bounds must be positive integers')
        self.max_letters, self.max_work, self.work = max_letters, max_work, 0

    def charge(self, amount=1):
        self.work += amount
        if self.work > self.max_work:
            raise VerificationLimitError('Point-pushing splitting exhausted its work bound')

    def append(self, stack, letter):
        self.charge()
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
            if len(stack) > self.max_letters:
                raise VerificationLimitError('Point-pushing splitting exhausted its word bound')

    def reduce(self, letters):
        result = []
        for letter in letters:
            self.append(result, letter)
        return tuple(result)


def _word(word, strands, budget):
    if type(strands) is not int or strands < 2:
        raise ValueError('Use an integer strand count at least two')
    result = []
    for letter in word:
        budget.charge()
        if type(letter) is not int or not 1 <= abs(letter) < strands:
            raise ValueError('Crossing indices must be nonzero integers smaller than strands')
        result.append(letter)
        if len(result) > budget.max_letters:
            raise VerificationLimitError('Point-pushing input exhausted its word bound')
    if strands - 1 > budget.max_letters:
        raise VerificationLimitError('Point-pushing meridians exceed the word bound')
    return tuple(result)


def point_push_generator(strands, meridian):
    """Canonical under-passing pair twist P_i, with pushing loop x_i.

    P_i = sigma_(n-1)^-1 ... sigma_(i+1)^-1 sigma_i^2
          sigma_(i+1) ... sigma_(n-1).
    The map from loops to braids reverses multiplication order in the
    package's right-composition convention: push(a b) = push(b) push(a).
    """
    if type(strands) is not int or strands < 2 or type(meridian) is not int or not 1 <= meridian < strands:
        raise ValueError('Choose a meridian numbered 1 through strands minus one')
    frame = tuple(range(1 - strands, -meridian))
    return frame + (meridian, meridian) + inverse_word(frame)


def point_push_braid(loop, strands, *, max_letters=100000, max_work=2000000):
    """Embed a signed free loop as its actual disk point-pushing braid."""
    budget = _Budget(max_letters, max_work)
    loop = _word(loop, strands, budget)
    return _push(loop, strands, budget)


def _push(loop, strands, budget):
    def letters():
        for letter in reversed(loop):
            word = point_push_generator(strands, abs(letter))
            yield from word if letter > 0 else inverse_word(word)
    return budget.reduce(letters())


def split_fixed_last_strand(word, strands, *, max_letters=100000, max_work=2000000):
    """Return the full F_(n-1) point-push and B_(n-1) shadow, not just deletion.

    Schreier representatives r_j = sigma_(n-1)^-1 ... sigma_j^-1 track
    the selected strand.  Each edge is an ordinary shadow generator, a
    canonical P_i, or the identity.  Collecting those edges uses only the
    exact Artin action of the smaller shadow on free meridians.  No action
    of the complete source braid and no route/drawing search is needed.

    The retained edges and explicit reconstructed disk word are a replayable
    algebraic decomposition, NOT a positive Hurwitz/substitution route.
    Limits raise VerificationLimitError; no truncated answer is returned.
    """
    budget = _Budget(max_letters, max_work)
    source = _word(word, strands, budget)
    position = strands
    edges = []
    for crossing in source:
        budget.charge()
        i = abs(crossing)
        next_position = i + 1 if position == i else i if position == i + 1 else position
        # A negative edge is the inverse positive edge based at its endpoint.
        base = position if crossing > 0 else next_position
        sign = 1 if crossing > 0 else -1
        if i == base:
            kind, generator = 'identity', 0
        elif i == base - 1:
            kind, generator = 'point_push', sign * i
        else:
            kind, generator = 'shadow', sign * (i - int(i > base))
        edges.append(SchreierEdge(position, crossing, next_position, kind, generator))
        position = next_position
    if position != strands:
        raise ValueError('The braid must fix the last strand; use an explicit common frame first')

    images = [(i,) for i in range(1, strands)]
    shadow, reverse_loop = [], []
    for edge in edges:
        g = edge.generator
        if edge.kind == 'shadow':
            budget.append(shadow, g)
            i = abs(g) - 1
            u, v = images[i:i + 2]
            if g > 0:
                images[i:i + 2] = (budget.reduce(chain(u, v, (-x for x in reversed(u)))), u)
            else:
                images[i:i + 2] = (v, budget.reduce(chain((-x for x in reversed(v)), u, v)))
            if sum(map(len, images)) > max_letters:
                raise VerificationLimitError('Point-pushing shadow action exhausted its word bound')
        elif edge.kind == 'point_push':
            image = images[abs(g) - 1]
            # Prepend A(shadow)(x_i) to the loop.  A reversed reduction stack
            # makes this linear in the inserted image, rather than the prefix.
            for x in (reversed(image) if g > 0 else (-x for x in image)):
                budget.append(reverse_loop, x)
    loop = tuple(reversed(reverse_loop))
    kernel = _push(loop, strands, budget)
    shadow = tuple(shadow)
    reconstructed = budget.reduce(chain(kernel, shadow))
    return PointPushingSplit(strands, source, shadow, loop, kernel, reconstructed,
                             tuple(edges), budget.work)


def common_shadow_obstruction(splits):
    """A necessary-condition obstruction to ONE common embedded subdisk.

    A common conjugation fixing strand n could place every input in the
    embedded B_(n-1) only if (D_i-I) Z = L_i for all i.  Here D_i permutes
    meridian exponents by the shadow and L_i abelianizes its retained push.
    These are integer difference constraints; an inconsistent cycle is an
    exact exclusion.  Consistency returns INCONCLUSIVE, never equivalence.
    Hurwitz transports and substitutions are not excluded by this test.
    """
    splits = tuple(splits)
    if not splits or any(not isinstance(s, PointPushingSplit) for s in splits):
        raise ValueError('Supply one or more exact point-pushing splits')
    n = splits[0].strands
    if any(s.strands != n for s in splits):
        raise ValueError('All splits must use the same disk')
    rank = n - 1
    parent, size, weight = list(range(rank)), [1] * rank, [0] * rank
    forest = [[] for _ in range(rank)]
    constraints = []

    def find(x):
        if parent[x] != x:
            ancestor = parent[x]
            parent[x], above = find(ancestor)
            weight[x] += above
        return parent[x], weight[x]

    for source, split in enumerate(splits):
        permutation = list(range(rank))
        for crossing in split.shadow_word:
            j = abs(crossing) - 1
            permutation[j], permutation[j + 1] = permutation[j + 1], permutation[j]
        exponents = [0] * rank
        for letter in split.kernel_loop:
            exponents[abs(letter) - 1] += 1 if letter > 0 else -1
        for v, u in enumerate(permutation):
            c = exponents[u]
            edge = dict(source=source, start=u + 1, end=v + 1, difference=c)
            constraints.append(edge)
            ru, du = find(u)
            rv, dv = find(v)
            if ru == rv:
                if dv - du == c:
                    continue
                # The spanning forest supplies a short, independently
                # replayable cycle of integer equations with nonzero sum.
                pending, previous = [u], {u: None}
                for vertex in pending:
                    if vertex == v:
                        break
                    for target, evidence in forest[vertex]:
                        if target not in previous:
                            previous[target] = (vertex, evidence)
                            pending.append(target)
                path, vertex = [], v
                while previous[vertex] is not None:
                    vertex, evidence = previous[vertex]
                    path.append(evidence)
                cycle = tuple(reversed(path)) + (dict(edge, start=v + 1, end=u + 1, difference=-c),)
                return dict(status='obstructed', common_conjugation_excluded=True,
                            cycle=cycle, cycle_sum=sum(e['difference'] for e in cycle),
                            constraints=tuple(constraints),
                            scope='No simultaneous conjugation fixing the last strand puts all these disk braids in the embedded smaller braid group. This does not exclude Hurwitz transports or substitutions.')
            if size[ru] < size[rv]:
                parent[ru], weight[ru] = rv, dv - du - c
                size[rv] += size[ru]
            else:
                parent[rv], weight[rv] = ru, c + du - dv
                size[ru] += size[rv]
            forest[u].append((v, edge))
            forest[v].append((u, dict(edge, start=v + 1, end=u + 1, difference=-c)))
    return dict(status='inconclusive', common_conjugation_excluded=False,
                cycle=(), cycle_sum=0, constraints=tuple(constraints),
                scope='The abelian necessary conditions are consistent. No common subdisk, conjugation, or braid equivalence is certified.')
