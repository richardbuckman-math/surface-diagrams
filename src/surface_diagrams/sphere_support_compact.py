"""Bounded, lift-preserving support simplification in a six-point sphere chart.

This changes a disk representative, not necessarily a disk mapping class.
Every accepted replacement has a five-arc sphere certificate and trivial
genus-two lift discrepancy. The drawing cap counts visits to the horizontal
reference cuts; it is neither braid length nor a global minimality claim.
"""
from dataclasses import asdict, replace
from functools import lru_cache
from heapq import heappop, heappush

from .braid_actions import inverse_word, reduce_word
from .hyperelliptic_homology import IDENTITY, homology_action
from .mapping_classes import supported_class
from .sphere_actions import sphere_chain_certificate, sphere_supported_class
from .sphere_arc_simplify import _act, _sphere_maps
from .twist_supports import support_curve


def _positive_bound(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(name + ' must be a positive integer')


def half_endpoints(twist):
    """Unordered marked endpoints; the rightmost permutation acts first."""
    a, b = twist.first, twist.first + 1
    for letter in reversed(twist.conjugator):
        i = abs(letter)
        a = i + 1 if a == i else i if a == i + 1 else a
        b = i + 1 if b == i else i if b == i + 1 else b
    return tuple(sorted((a, b)))


def check_support_replacement(source, candidate, *, max_cuts=40):
    """Check a supplied positive support replacement; never silently relax a cap.

    Signed research factors apply the same sign to both positive words. That
    does not change this equality check. In particular, equal complementary
    three-point curves alone do NOT certify equal unsquared lifted twists.
    """
    _positive_bound(max_cuts, 'max_cuts')
    if (source.points, source.power, source.half) != (
            candidate.points, candidate.power, candidate.half):
        raise ValueError('A replacement must retain the core type and power')
    if sphere_supported_class(source) != sphere_supported_class(candidate):
        raise ValueError('Different sphere support classes')
    if source.half and half_endpoints(source) != half_endpoints(candidate):
        raise ValueError('Different half-twist endpoints')
    discrepancy = reduce_word(source.word + inverse_word(candidate.word))
    lift = homology_action(discrepancy)
    if lift != IDENTITY:
        raise ValueError('Support replacement changes the genus-two lift')
    cuts = len(support_curve(candidate).cuts)
    if cuts > max_cuts:
        raise ValueError('Support replacement exceeds the cut-visit cap')
    certificate = sphere_chain_certificate(discrepancy)
    if not certificate['certified']:
        raise ValueError('Support replacement fails the five-arc sphere check')
    # Same twist type/power on the same disk support gives disk equality.
    # Comparing support classes avoids expanding unrelated based meridians.
    disk_equal = supported_class(source) == supported_class(candidate)
    return dict(candidate=asdict(candidate), cuts=cuts, max_cuts=max_cuts,
                disk_equal=disk_equal,
                kind='disk_support' if disk_equal else 'sphere_rewrite',
                disk_discrepancy=discrepancy, sphere_certificate=certificate,
                lift_homology=lift)


@lru_cache(maxsize=512)
def compact_sphere_support(twist, *, max_cuts=40, max_states=2500, max_depth=32):
    """Find an accepted short chart representative, or return a bounded failure.

    Search only nonexpanding sphere classes, with a fixed work/depth budget.
    Failure says nothing about existence below the requested drawing cap.
    Independent recovered supports are not a joint cut-system certificate.
    """
    for name, bound in [('max_cuts', max_cuts), ('max_states', max_states),
                        ('max_depth', max_depth)]:
        _positive_bound(bound, name)
    start = sphere_supported_class(twist)
    goals = {}
    for first in range(1, 8 - twist.points):
        core = replace(twist, conjugator=(), first=first)
        goals.setdefault(sphere_supported_class(core), []).append(first)
    pending = [(len(start), 0, (), start)]
    seen = {start: 0}
    visited = 0
    while pending and visited < max_states:
        _, depth, path, word = heappop(pending)
        visited += 1
        if seen[word] < depth:
            continue
        for first in goals.get(word, ()):
            # Traversal generators act successively on the LEFT. Inverting
            # that composite produces these negated letters, without reversal.
            candidate = replace(twist, first=first,
                                conjugator=tuple(-letter for letter in path))
            try:
                result = check_support_replacement(twist, candidate, max_cuts=max_cuts)
            except ValueError:
                continue
            return dict(result, states=visited, depth=depth, status='certified')
        if depth >= max_depth:
            continue
        for generator, mapping in _sphere_maps():
            image = _act(word, mapping)
            if len(image) > len(start) or seen.get(image, max_depth + 1) <= depth + 1:
                continue
            seen[image] = depth + 1
            heappush(pending, (len(image), depth + 1, path + (generator,), image))
    return dict(candidate=None, status='bounded_failure', states=visited,
                max_cuts=max_cuts, source_class_length=len(start))


def reframe_factors(factors, frame):
    """Explicit global conjugation, with an exact telescoping word certificate.

    This is a change of the whole column. It is not a per-factor disk equality.
    """
    factors, frame = tuple(factors), tuple(frame)
    if any(type(x) is not int or not 1 <= abs(x) <= 5 for x in frame):
        raise ValueError('A six-point frame uses generators 1 through 5')
    after = tuple(replace(f, conjugator=reduce_word(frame + tuple(f.conjugator)))
                  for f in factors)
    before_word = tuple(x for f in factors for x in f.word)
    after_word = tuple(x for f in after for x in f.word)
    discrepancy = reduce_word(after_word + inverse_word(
        frame + before_word + inverse_word(frame)))
    if discrepancy:
        raise ValueError('Global conjugation failed its telescoping word check')
    return dict(kind='global_conjugation', frame=frame, factors=after,
                word_certificate=dict(method='free reduction', discrepancy=discrepancy))
