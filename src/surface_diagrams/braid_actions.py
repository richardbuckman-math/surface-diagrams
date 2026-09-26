"""Exact free-group actions of disk braids, separate from drawing geometry.

Words are read left to right with right composition: A(uv)=A(u) composed
with A(v). The generator sends x_i to x_i x_(i+1) x_i^-1 and x_(i+1)
to x_i. This explicit algebraic convention must be matched to a drawing's
base loops before interpreting images as a geometric action.
No sphere quotient or conversion from planar arc itineraries is performed.
"""


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
    for letter in word:
        if type(letter) is not int or not 1 <= abs(letter) < strands:
            raise ValueError('crossing index must be nonzero and smaller than strands')
        i=abs(letter)-1
        u,v=images[i:i+2]
        images[i:i+2]=(reduce_word(u+v+inverse_word(u)),u) if letter>0 else (
            v,reduce_word(inverse_word(v)+u+v))
    return tuple(images)


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
