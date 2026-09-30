"""Mapping classes represented as conjugates of standard supported twists.

The record retains the twist type and its core, independently of presentation
IDs, browser state, and SVG rendering. Braid words compose as in braid_actions.
"""
from dataclasses import dataclass
from functools import lru_cache
from .braid_actions import reduce_word,inverse_word,_extend_action,free_homotopy_key


class VerificationLimitError(ValueError):
    """An exact computation exhausted its bound, without proving inequality."""


@lru_cache(maxsize=128)
def supported_class(twist,strands=6):
    """Exact unoriented boundary class, without expanding unrelated meridians.

    Right composition applies the last generator first. Canonicalizing between
    substitutions discards only conjugation and orientation of this closed path;
    this function must not be used to test based actions or braid equality.
    """
    if type(strands) is not int or strands<2 or twist.first+twist.points-1>strands:
        raise ValueError('Twist support exceeds the marked disk')
    word=free_homotopy_key(tuple(range(twist.first,twist.first+twist.points)))
    for crossing in reversed(twist.conjugator):
        images=_extend_action(tuple((i,) for i in range(1,strands+1)),(crossing,))
        def letters():
            for letter in word:
                yield from images[letter-1] if letter>0 else inverse_word(images[-letter-1])
        word=free_homotopy_key(letters())
        if len(word)>400000:
            raise VerificationLimitError('Exact supported class reached the prototype word limit')
    return word


def exact_action(word,strands=6):
    word=tuple(word)
    if type(strands) is not int or strands<1:
        raise ValueError('strands must be a positive integer')
    if any(type(letter) is not int or not 1<=abs(letter)<strands for letter in word):
        raise ValueError('crossing index must be nonzero and smaller than strands')
    images=tuple((i,) for i in range(1,strands+1))
    for letter in word:
        images=_extend_action(images,(letter,))
        if sum(map(len,images))>400000:
            return _action_by_meridian(word,strands)
    return images


def _action_by_meridian(word,strands):
    """Equivalent based action, avoiding large intermediate prefix actions.

    No cyclic reduction: base paths are essential for braid equality. Each
    intermediate meridian and the final total retain the 400000-letter bound.
    """
    identity=tuple((i,) for i in range(1,strands+1))
    substitutions={}
    for crossing in set(word):
        images=_extend_action(identity,(crossing,))
        substitutions[crossing]={signed:images[signed-1] if signed>0 else inverse_word(images[-signed-1])
                                for i in range(1,strands+1) for signed in (i,-i)}
    result=[]; total=0
    for meridian in range(1,strands+1):
        current=(meridian,)
        for crossing in reversed(word):
            mapping=substitutions[crossing]
            current=reduce_word(x for letter in current for x in mapping[letter])
            if len(current)>400000:
                raise VerificationLimitError('Exact verification reached the prototype word limit; operation was not applied')
        total+=len(current)
        if total>400000:
            raise VerificationLimitError('Exact verification reached the prototype word limit; operation was not applied')
        result.append(current)
    return tuple(result)


@dataclass(frozen=True)
class ConjugatedTwist:
    conjugator: tuple
    first: int
    points: int
    power: int = 1
    half: bool = False

    def __post_init__(self):
        object.__setattr__(self,'conjugator',tuple(self.conjugator))
        if type(self.first) is not int or self.first<1 or type(self.points) is not int or self.points<2:
            raise ValueError('A twist needs a positive first position and at least two points')
        if type(self.power) is not int or self.power<1 or type(self.half) is not bool or (self.half and self.points!=2):
            raise ValueError('Invalid positive twist power or half-twist support')
        if any(type(x) is not int or x==0 for x in self.conjugator):
            raise ValueError('Conjugator letters must be signed nonzero integers')

    @property
    def core(self):
        if self.half: return (self.first,)*self.power
        return tuple(range(self.first,self.first+self.points-1))*(self.points*self.power)

    @property
    def word(self):
        return reduce_word(self.conjugator+self.core+inverse_word(self.conjugator))
