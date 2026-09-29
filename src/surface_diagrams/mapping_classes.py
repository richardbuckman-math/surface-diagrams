"""Mapping classes represented as conjugates of standard supported twists.

The record retains the twist type and its core, independently of presentation
IDs, browser state, and SVG rendering. Braid words compose as in braid_actions.
"""
from dataclasses import dataclass
from .braid_actions import reduce_word,inverse_word,_extend_action


def exact_action(word,strands=6):
    images=tuple((i,) for i in range(1,strands+1))
    for letter in word:
        images=_extend_action(images,(letter,))
        if sum(map(len,images))>400000:
            raise ValueError('Exact verification reached the prototype word limit; operation was not applied')
    return images


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
