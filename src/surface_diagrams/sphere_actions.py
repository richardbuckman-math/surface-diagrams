"""Exact positive certificates for trivial six-punctured-sphere outer action.

The disk's boundary word D=x1...x6 becomes trivial on the punctured sphere,
so x6=(x1...x5)^-1. A simultaneous inner conjugation on the resulting F5 is
the identity outer action. This is an action certificate, not a braid-relation
derivation or a geometric cut-system drawing. In particular, the outer action
cannot distinguish the central order-two spherical braid from the identity.
"""
from functools import lru_cache
from collections import OrderedDict
from threading import Lock

from .braid_actions import free_homotopy_key,inverse_word,reduce_word
from .mapping_classes import ConjugatedTwist,VerificationLimitError,exact_action


# Successful five-arc certificates have small immutable tuple payloads even
# when their intermediate curve words are large. Failed/unknown results are
# never retained. Returned dictionaries are copies, and bounds are in the key.
_sphere_chain_cache = OrderedDict()
_sphere_chain_cache_lock = Lock()
_SPHERE_CHAIN_CACHE_SIZE = 128
_SPHERE_CHAIN_CACHE_MAX_WORD = 8192

def sphere_reduce(word):
    """Reduce a based six-meridian word in F5 using x1...x6=1."""
    boundary=tuple(range(1,6))
    def letters():
        for letter in word:
            if type(letter) is not int or not 1<=abs(letter)<=6:
                raise ValueError('Sphere meridian letters must be signed 1..6')
            yield from (letter,) if abs(letter)<6 else (
                inverse_word(boundary) if letter>0 else boundary)
    return reduce_word(letters())


def _meridian_whisker(image,meridian):
    start,end=0,len(image)
    while end-start>1 and image[start]==-image[end-1]:
        start+=1;end-=1
    return image[:start] if image[start:end]==(meridian,) else None


def sphere_inner_certificate(braid):
    """Certify that this disk braid acts trivially in Out(F5), if possible.

    Returns complete reduced images and a candidate common whisker. A failed
    search returns certified=False, not a proof of nonidentity. Every positive
    result explicitly verifies all six images in F5, including x6.
    """
    return dict(_cached_certificate(tuple(braid)))


@lru_cache(maxsize=1)
def _curve_maps():
    maps = {}
    for crossing in (*range(1, 6), *range(-5, 0)):
        images = exact_action((crossing,))
        mapping = {i: sphere_reduce(images[i - 1]) for i in range(1, 6)}
        mapping.update({-i: inverse_word(mapping[i]) for i in range(1, 6)})
        maps[crossing] = mapping
    return maps


def sphere_curve_action(braid, boundary_word, *, max_letters=400000):
    """Exact unoriented free-homotopy class of an image curve on S² minus W.

    Normalize in F5 after each substitution, avoiding unrelated based
    meridian images. Equality checks isotopy for essential simple curves;
    it does not by itself certify a braid identity or a genus-two lift.
    For a two-puncture boundary, also retain its endpoints when using this
    to check the corresponding arc. A computation at the bound is unknown.
    """
    braid = tuple(braid)
    if any(type(letter) is not int or not 1 <= abs(letter) <= 5 for letter in braid):
        raise ValueError('six-strand braid letters must be signed 1..5')
    if type(max_letters) is not int or max_letters < 1:
        raise ValueError('max_letters must be a positive integer')
    current = free_homotopy_key(sphere_reduce(tuple(boundary_word)))
    if len(current) > max_letters:
        raise VerificationLimitError('Sphere curve action reached its word bound')
    for crossing in reversed(braid):
        mapping = _curve_maps()[crossing]
        current = free_homotopy_key(reduce_word(
            letter for symbol in current for letter in mapping[symbol]))
        if len(current) > max_letters:
            raise VerificationLimitError('Sphere curve action reached its word bound')
    return current


def sphere_supported_class(twist, *, max_letters=400000):
    """Unoriented sphere boundary class of a supported twist, directly in F5.

    Start from the standard support and normalize after every conjugator
    generator. No intermediate disk support or based whisker is expanded.
    Twist power and half/full type do not affect this boundary class; it
    alone certifies neither a twist equality in the disk nor a lift sign.
    """
    if not isinstance(twist, ConjugatedTwist) or twist.first + twist.points - 1 > 6:
        raise ValueError('Sphere supports need a twist within the six-point chart')
    return sphere_curve_action(twist.conjugator,
        tuple(range(twist.first, twist.first + twist.points)), max_letters=max_letters)


def three_point_curve_fixedness_certificate(twist, boundary_word, *, max_letters=400000):
    """Decide whether a three-point twist fixes an unoriented sphere class.

    In the standard T123 chart, F5=F(1,2,3)*F(4,5). The twist conjugates
    the first factor by u=123 and fixes the second. A cyclic word in one
    factor is therefore fixed up to conjugacy. A mixed cyclic word is
    fixed iff every first-factor syllable is a power of u. Indeed, free
    product conjugacy permits only cyclic permutations of mixed syllables;
    a finite orbit under conjugation by u^power forces each inner syllable
    into the centralizer <u>. An unoriented fixed class has an oriented
    period at most two, giving the same criterion.

    Only the change of chart is expanded. This is a sphere curve-class
    certificate, not a disk action or genus-two lift certificate. A chart
    exceeding max_letters raises VerificationLimitError, never False.
    """
    if (not isinstance(twist, ConjugatedTwist) or twist.points != 3 or
            twist.first + 2 > 6):
        raise ValueError('Use a three-point twist within the six-point chart')
    # delta^(first-1) T123 delta^-(first-1) is the standard interval twist.
    chart = twist.conjugator + tuple(range(1, 6)) * (twist.first - 1)
    word = sphere_curve_action(inverse_word(chart), boundary_word, max_letters=max_letters)
    inside = lambda letter: abs(letter) <= 3
    mixed = bool(word and any(inside(x) for x in word) and any(not inside(x) for x in word))
    bad = ()
    syllables = []
    if mixed:
        start = next(i for i in range(len(word)) if inside(word[i]) and not inside(word[i - 1]))
        rotated = word[start:] + word[:start]
        blocks = []
        for letter in rotated:
            if not blocks or inside(letter) != inside(blocks[-1][0]):
                blocks.append([])
            blocks[-1].append(letter)
        syllables = [tuple(block) for block in blocks[::2]]
        for block in syllables:
            if (block != (1, 2, 3) * (len(block) // 3) and
                    block != (-3, -2, -1) * (len(block) // 3)):
                bad = block
                break
    return dict(fixed=not bad, method='three-point free-product normal form',
                chart_conjugator=chart, chart_class=word, mixed=mixed,
                inner_syllable_count=len(syllables), first_noncommuting_syllable=bad,
                scope='Unoriented sphere curve class only; no disk action or lift sign implied')


def sphere_chain_certificate(braid, *, max_letters=400000):
    """Check sphere identity using the five adjacent-point arc classes.

    Endpoints are checked individually, and each arc is identified by the
    exact boundary of its two-point neighborhood. The five arcs form an
    embedded tree through all six punctures; its sphere complement is a
    disk. Fixing their isotopy classes and endpoints therefore fixes the
    whole sphere mapping class (straighten the tree, then use the disk
    Alexander trick). This uses no numerical placement or joint drawing.

    Like the outer-action certificate, this cannot distinguish the central
    order-two spherical braid. A genus-two lift needs its separate sign check.
    No disk action is expanded: a large disk point-push whisker cannot by
    itself exhaust this check. A bounded arc computation raises an unknown,
    never a claimed identity or inequality.
    """
    from .hyperelliptic_homology import braid_permutation
    braid = tuple(braid)
    permutation = braid_permutation(braid)
    if type(max_letters) is not int or max_letters < 1:
        raise ValueError('max_letters must be a positive integer')
    key = (braid, max_letters)
    cacheable = len(braid) <= _SPHERE_CHAIN_CACHE_MAX_WORD
    if cacheable:
        with _sphere_chain_cache_lock:
            cached = _sphere_chain_cache.get(key)
            if cached is not None:
                _sphere_chain_cache.move_to_end(key)
                return dict(cached)
    pairs = tuple((i, i + 1) for i in range(1, 6))
    reference = tuple(sphere_curve_action((), pair, max_letters=max_letters) for pair in pairs)
    images = tuple(sphere_curve_action(braid, pair, max_letters=max_letters) for pair in pairs)
    endpoints_fixed = permutation == tuple(range(1, 7))
    result = dict(certified=endpoints_fixed and images == reference,
                method='five exact sphere chain arcs', permutation=permutation,
                endpoints_fixed=endpoints_fixed, arc_pairs=pairs,
                reference_classes=reference, image_classes=images,
                scope='Sphere mapping class; no disk action or genus-two lift sign implied')
    if cacheable and result['certified']:
        with _sphere_chain_cache_lock:
            _sphere_chain_cache[key] = dict(result)
            _sphere_chain_cache.move_to_end(key)
            while len(_sphere_chain_cache) > _SPHERE_CHAIN_CACHE_SIZE:
                _sphere_chain_cache.popitem(last=False)
    return result


@lru_cache(maxsize=16)
def _cached_certificate(braid):
    disk_images=exact_action(braid)
    disk_identity=disk_images==tuple((i,) for i in range(1,7))
    images=tuple(sphere_reduce(image) for image in disk_images)
    paths=tuple(_meridian_whisker(images[i],i+1) for i in range(5))
    if paths[0] is None or paths[1] is None:
        return dict(certified=False,conjugator=(),images=images,expected=(),disk_identity=disk_identity)
    # If w sends both x1 and x2 correctly, their canonical whiskers differ
    # only by terminal powers of x1 and x2. The initial x2 run in p2^-1 p1
    # determines the power needed to recover the common whisker.
    bridge=reduce_word(inverse_word(paths[1])+paths[0])
    power=0
    for letter in bridge:
        if abs(letter)!=2 or (power and (letter>0)!=(power>0)): break
        power+=1 if letter>0 else -1
    tail=(2,)*power if power>=0 else (-2,)*(-power)
    common=reduce_word(paths[1]+tail)
    standard=tuple((i,) for i in range(1,6))+(inverse_word(tuple(range(1,6))),)
    expected=tuple(reduce_word(common+meridian+inverse_word(common)) for meridian in standard)
    if images!=expected:
        return dict(certified=False,conjugator=(),images=images,expected=(),disk_identity=disk_identity)
    return dict(certified=True,conjugator=common,images=images,expected=expected,disk_identity=disk_identity)
