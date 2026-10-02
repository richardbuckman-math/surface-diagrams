"""Exact positive certificates for trivial six-punctured-sphere outer action.

The disk's boundary word D=x1...x6 becomes trivial on the punctured sphere,
so x6=(x1...x5)^-1. A simultaneous inner conjugation on the resulting F5 is
the identity outer action. This is an action certificate, not a braid-relation
derivation or a geometric cut-system drawing. In particular, the outer action
cannot distinguish the central order-two spherical braid from the identity.
"""
from functools import lru_cache

from .braid_actions import inverse_word,reduce_word
from .mapping_classes import exact_action


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
