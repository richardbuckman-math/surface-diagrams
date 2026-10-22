"""Exact geometric intersections of supported closed curves on a marked disk.

Cut along the left curve.  The disk group splits as A *_<z> B, with A the
inside free group and z its boundary word.  The cyclically reduced syllable
length is the intersection number.  No drawing or candidate-route search is
used.  See docs/proofs/disk-curve-intersection.md for the normal-form proof.
"""
from collections import deque
from dataclasses import replace

from .braid_actions import free_homotopy_key, inverse_word, reduce_word
from .mapping_classes import ConjugatedTwist, VerificationLimitError, supported_class


def _round_normal_form(word, first, points, strands, max_letters):
    inside = set(range(first, first + points))
    edge = tuple(range(first, first + points))
    inverse_edge = inverse_word(edge)
    marker = strands + 1
    blocks = deque()
    work = 0

    def spend(size):
        nonlocal work
        work += size
        if work > max(256, 32 * max_letters):
            raise VerificationLimitError('Disk intersection normal form reached its work bound')

    def membership(tag, current):
        spend(len(current))
        if tag == 'A':
            if len(current) % points:
                return None
            base = edge if current[0] > 0 else inverse_edge
            if current == base * (len(current) // points):
                return (1 if current[0] > 0 else -1) * (len(current) // points)
        elif all(abs(x) == marker for x in current):
            return sum(1 if x > 0 else -1 for x in current)
        return None

    def edge_in(tag, power):
        return ((edge if power > 0 else inverse_edge) * abs(power) if tag == 'A'
                else (marker if power > 0 else -marker,) * abs(power))

    def insert(tag, current):
        if tag != 'E':
            spend(len(current))
            current = reduce_word(current)
        while current:
            if tag != 'E':
                power = membership(tag, current)
                if power is not None:
                    tag, current = 'E', power
            if tag == 'E':
                if not blocks:
                    blocks.append(('E', current))
                    return
                previous_tag, previous = blocks.pop()
                if previous_tag == 'E':
                    current += previous
                else:
                    tag, current = previous_tag, previous + edge_in(previous_tag, current)
                    spend(len(current))
                    current = reduce_word(current)
            elif blocks and blocks[-1][0] == 'E':
                power = blocks.pop()[1]
                current = reduce_word(edge_in(tag, power) + current)
                spend(len(current))
            elif blocks and blocks[-1][0] == tag:
                current = reduce_word(blocks.pop()[1] + current)
                spend(len(current))
            else:
                blocks.append((tag, current))
                return

    tag, run = None, []
    for letter in word:
        next_tag = 'A' if abs(letter) in inside else 'B'
        if run and next_tag != tag:
            insert(tag, tuple(run))
            run = []
        tag = next_tag
        run.append(letter)
    if run:
        insert(tag, tuple(run))
    while len(blocks) > 1 and blocks[0][0] == blocks[-1][0]:
        first_tag, first_word = blocks.popleft()
        _, last_word = blocks.pop()
        insert(first_tag, last_word + first_word)

    def expand(tag, current):
        if tag == 'E':
            return edge_in('A', current)
        return tuple(x for letter in current for x in
                     ((edge if letter > 0 else inverse_edge) if abs(letter) == marker else (letter,)))

    embedded = tuple(x for tag, current in blocks for x in expand(tag, current))
    if free_homotopy_key(embedded) != free_homotopy_key(word):
        raise ValueError('Disk intersection normal form changed the original closed path')
    if len(blocks) > 1 and (len(blocks) % 2 or any(
            tag == 'E' or membership(tag, current) is not None for tag, current in blocks)):
        raise ValueError('Disk intersection syllables are not cyclically reduced')
    return tuple(blocks)


def disk_intersection_certificate(left, right, *, strands=6, max_letters=400000):
    """Return a normal-form certificate for two simple closed supporting curves.

    Inputs must be full ConjugatedTwist records: an arc and the boundary of
    its neighborhood have different intersection counts.  Twist powers do
    not change these curve counts.  A bound failure raises, never reports zero.
    Scope is the marked disk, without any spherical or framed substitution.
    """
    if (type(strands) is not int or strands < 2 or type(max_letters) is not int
            or max_letters < 1):
        raise ValueError('Choose a disk with at least two points and a positive word bound')
    for curve in (left, right):
        if not isinstance(curve, ConjugatedTwist) or curve.half:
            raise ValueError('Disk intersections require supported closed curves, not half-twist arcs')
        if (curve.first + curve.points - 1 > strands
                or any(abs(x) >= strands for x in curve.conjugator)):
            raise ValueError('Curve lies outside the marked disk')
    relative = replace(right, conjugator=reduce_word(inverse_word(left.conjugator) + right.conjugator))
    word = supported_class(relative, strands)
    if len(word) > max_letters:
        raise VerificationLimitError('Disk intersection reached its closed-word bound')
    # The exterior boundary is disjoint from every essential disk curve.
    normal = (('A', word),) if left.points == strands else _round_normal_form(
        word, left.first, left.points, strands, max_letters)
    return dict(intersection_number=len(normal) if len(normal) > 1 else 0,
                strands=strands, interval=(left.first, left.first + left.points - 1),
                edge_word=tuple(range(left.first, left.first + left.points)),
                outside_edge_marker=strands + 1, relative_curve_word=word,
                cyclic_normal_form=normal, exact=True,
                method='Cyclic normal form in the disk group split along the left curve')


def disk_curve_intersection(left, right, *, strands=6, max_letters=400000):
    """Minimal crossings of two supported closed curves in the marked disk."""
    return disk_intersection_certificate(left, right, strands=strands,
                                         max_letters=max_letters)['intersection_number']
