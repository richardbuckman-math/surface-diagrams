"""Exact free-group actions of disk braids, separate from drawing geometry.

Words are read left to right with right composition: A(uv)=A(u) composed
with A(v). The generator sends x_i to x_i x_(i+1) x_i^-1 and x_(i+1)
to x_i. This explicit algebraic convention must be matched to a drawing's
base loops before interpreting images as a geometric action.
No sphere quotient or conversion from planar arc itineraries is performed.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ArcTransportAudit:
    """Exact evidence for an anchored endpoint-meridian comparison.

    A mismatch is not a general disproof of support equivalence: the chosen
    base paths must have this anchored form. No embeddedness is certified.
    """
    transport: tuple
    actual: tuple
    expected: tuple
    start_path: tuple = ()

    @property
    def matches(self):
        return self.actual == self.expected


def audit_arc_transport(points, conjugator, generator, arc, *, start_path=()):
    """Compare A(g)(x_i,x_(i+1)) with p(x_start,t x_end t^-1)p^-1.

    Here t is the supplied arc's ray word, i is a positive generator index,
    and g is the conjugator in g sigma_i g^-1. The supplied start_path p is
    a free-group word, not a braid word; its default is the empty base path.
    It returns
    both pairs for inspection; it neither reconstructs arcs nor verifies an
    entire factorization, sphere relation, or arbitrary support equivalence.
    """
    transport=arc_ray_word(points,arc)
    if type(generator) is not int or not 1 <= generator < points:
        raise ValueError('generator must be a positive index smaller than points')
    images=artin_action(points,conjugator)
    start_path=tuple(start_path)
    if any(type(i) is not int or not 1 <= abs(i) <= points for i in start_path):
        raise ValueError('start_path letters must be nonzero integers within the free-group rank')
    start_path=reduce_word(start_path)
    back=inverse_word(start_path)
    expected=(reduce_word(start_path+(arc.start,)+back),
              reduce_word(start_path+transport+(arc.end,)+inverse_word(transport)+back))
    return ArcTransportAudit(transport,images[generator-1:generator+1],expected,start_path)


def reduce_word(word):
    """Freely reduce a word in nonzero signed integer letters."""
    result=[]
    for letter in word:
        if type(letter) is not int or letter == 0:
            raise ValueError('free-group letters must be nonzero integers')
        if result and result[-1] == -letter:
            result.pop()
        else:
            result.append(letter)
    return tuple(result)


def inverse_word(word):
    return tuple(-i for i in reversed(reduce_word(word)))


def artin_action(strands, word):
    """Return exact reduced images of x_1,...,x_n for a disk braid word."""
    if type(strands) is not int or strands < 1:
        raise ValueError('strands must be a positive integer')
    images=[(i,) for i in range(1,strands+1)]
    return _extend_action(images,word)


def _extend_action(images, word):
    images=list(images)
    strands=len(images)
    for letter in word:
        if type(letter) is not int or not 1 <= abs(letter) < strands:
            raise ValueError('crossing index must be nonzero and smaller than strands')
        i=abs(letter)-1
        u,v=images[i:i+2]
        images[i:i+2]=(reduce_word(u+v+inverse_word(u)),u) if letter>0 else (
            v,reduce_word(inverse_word(v)+u+v))
    return tuple(images)


def action_checkpoints(strands, factors):
    """Identity followed by the action of each concatenated factor prefix.

    This uses the same right-composition convention as artin_action. Empty
    factors retain a checkpoint. Earlier snapshots are immutable tuples.
    """
    current=artin_action(strands,())
    result=[current]
    for factor in factors:
        current=_extend_action(current,factor)
        result.append(current)
    return tuple(result)


def conjugate_factors(factors, conjugator):
    """Replace every f by g f g^-1, so the product becomes g P g^-1.

    This changes the product by conjugation, not by a product-preserving move.
    Only free cancellation is performed; support curves are not computed.
    """
    g=reduce_word(conjugator)
    gi=inverse_word(g)
    return tuple(reduce_word(g+reduce_word(factor)+gi) for factor in factors)


def arc_ray_word(points, arc):
    """Read an Arc against upward vertical rays from the marked points.

    Crossing a ray left-to-right contributes +j, right-to-left -j. Endpoint
    rays are excluded at the endpoint itself. This is a relative path encoding,
    not a Dehn-twist automorphism or a conversion to braid generators.
    Only point-to-point arcs on a row of punctures are supported.
    """
    return reduce_word(letter for segment in arc_ray_segments(points,arc) for letter in segment)


def arc_ray_segments(points, arc):
    """Return unreduced ray letters for each segment, retaining empty segments.

    Entry zero starts at the first endpoint; successive entries start at each
    cut. Lower segments have empty words. Flatten and freely reduce these
    contributions to obtain arc_ray_word. Uses the same input validation.
    """
    from .curves import Arc
    if type(points) is not int or points < 2:
        raise ValueError('points must be an integer at least two')
    if not isinstance(arc,Arc):
        raise TypeError('arc must be an Arc')
    if not 1 <= arc.start <= points or not 1 <= arc.end <= points:
        raise ValueError('arc endpoints must be marked points')
    if any(c > points for c in arc.cuts):
        raise ValueError('cut index exceeds the marked row')
    if arc.start_side is not None or arc.end_side is not None:
        raise ValueError('boundary rim endpoints are not supported')
    # Points are at 2j; gap c is at 2c+1, including exterior gaps 0,n.
    locations=(2*arc.start,)+tuple(2*c+1 for c in arc.cuts)+(2*arc.end,)
    segments=[]
    for index,(a,b) in enumerate(zip(locations,locations[1:])):
        if (index%2==0) != arc.initial_up:
            segments.append(())
            continue
        crossed=[j for j in range(1,points+1) if min(a,b)<2*j<max(a,b)]
        segments.append(tuple(crossed if a<b else [-j for j in reversed(crossed)]))
    return tuple(segments)


def loop_ray_word(points, loop):
    """Read a closed Loop against upward rays, starting at its first cut.

    The returned word retains a chosen traversal/base cut. Use
    free_homotopy_key to compare unbased unoriented loop words. This does not
    validate embeddedness or calculate the Dehn twist about the loop.
    """
    from .curves import Loop
    if type(points) is not int or points < 1:
        raise ValueError('points must be a positive integer')
    if not isinstance(loop,Loop):
        raise TypeError('loop must be a Loop')
    if any(c > points for c in loop.cuts):
        raise ValueError('cut index exceeds the marked row')
    letters=[]
    for index,(a,b) in enumerate(zip(loop.cuts,loop.cuts[1:]+loop.cuts[:1])):
        if (index%2==0) != loop.start_up:
            continue
        letters.extend(range(a+1,b+1) if a<b else (-j for j in range(a,b,-1)))
    return reduce_word(letters)


def _least_rotation(word):
    """Lexicographically least cyclic rotation using linear candidate elimination."""
    n=len(word)
    i,j,offset=0,1,0
    while i<n and j<n and offset<n:
        a,b=word[(i+offset)%n],word[(j+offset)%n]
        if a==b:
            offset+=1
            continue
        # A losing start and the next offset starts cannot be minimal: each
        # shares the compared prefix and loses to the corresponding other start.
        if a>b:
            i+=offset+1
            if i<=j:
                i=j+1
        else:
            j+=offset+1
            if j<=i:
                j=i+1
        offset=0
    start=min(i,j)
    return word[start:]+word[:start]


def free_homotopy_key(word):
    """Canonical free-group conjugacy key, identifying reversed orientation.

    This is for unoriented closed paths in the punctured disk, not based loops
    or braid equality. It does not quotient out the outer boundary word.
    """
    word=reduce_word(word)
    start,end=0,len(word)
    while end-start>1 and word[start]==-word[end-1]:
        start+=1
        end-=1
    word=word[start:end]
    if not word:
        return ()
    reverse=inverse_word(word)
    return min(_least_rotation(word),_least_rotation(reverse))


def act_on_loop_word(strands, braid, word):
    """Substitute exact Artin images into a supplied free-group loop word.

    Returns a based word; free_homotopy_key deliberately remains a separate
    operation so boundary twisting is not silently discarded.
    """
    images=artin_action(strands,braid)
    word=reduce_word(word)
    if any(abs(i)>strands for i in word):
        raise ValueError('loop letter exceeds the free-group rank')
    def letters():
        for i in word:
            yield from images[i-1] if i>0 else inverse_word(images[-i-1])
    return reduce_word(letters())


def hurwitz_move(factors, index, *, inverse=False):
    """Move an adjacent pair at zero-based index, preserving concatenation.

    Forward: (u,v) -> (v,v^-1 u v). Inverse: (u,v) -> (u v u^-1,u).
    Output is braid words, not transformed planar support curves.
    """
    factors=tuple(reduce_word(word) for word in factors)
    if type(index) is not int or not 0 <= index < len(factors)-1:
        raise ValueError('index must select an adjacent pair of factors')
    if type(inverse) is not bool:
        raise TypeError('inverse must be a boolean')
    u,v=factors[index:index+2]
    pair=(reduce_word(u+v+inverse_word(u)),u) if inverse else (
        v,reduce_word(inverse_word(v)+u+v))
    return factors[:index]+pair+factors[index+2:]


def substitute_factors(strands, factors, start, stop, replacement):
    """Replace a nonempty factor slice only when its exact disk action agrees.

    start/stop are zero-based, with stop excluded. Empty replacement permits
    checked cancellation. This validates disk braid equality, not a sphere or
    boundary-framed mapping-class relation. No relation is discovered for you.
    """
    factors=tuple(tuple(word) for word in factors)
    replacement=tuple(tuple(word) for word in replacement)
    if type(start) is not int or type(stop) is not int or not 0 <= start < stop <= len(factors):
        raise ValueError('start/stop must select a nonempty factor slice')
    # Validate original letters before reduction, including untouched factors.
    for word in factors+replacement:
        for i in word:
            if type(i) is not int or type(strands) is not int or not 1 <= abs(i) < strands:
                raise ValueError('crossing index must be nonzero and smaller than strands')
    before=artin_action(strands,(i for word in factors[start:stop] for i in word))
    after=artin_action(strands,(i for word in replacement for i in word))
    if before != after:
        raise ValueError('replacement does not preserve the exact disk braid action')
    return factors[:start]+tuple(reduce_word(word) for word in replacement)+factors[stop:]
