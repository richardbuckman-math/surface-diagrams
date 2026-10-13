"""Short sphere-equivalent disk-chart representatives of five sphere chain arcs.

The boundary of a two-point arc is tracked in the five-generator sphere
quotient. A bounded search applies exact Artin generator actions there, then
reconstructs a disk Arc and checks its quotient boundary class and endpoints.
This is a search for a shorter representative, not a claim of global
minimality or a proof that arbitrary independently chosen arcs fit together.
"""
from functools import lru_cache
from heapq import heappop, heappush
from itertools import product

from .braid_actions import free_homotopy_key, reduce_word
from .chain_cut_system import chain_arc, chain_words
from .mapping_classes import ConjugatedTwist, supported_class
from .normal_cut_engine import calculate_cut_system
from .normal_cut_preview import render_normal_cut_preview
from .normal_strands import NormalTriangleError
from .sphere_actions import sphere_reduce
from .support_simplify import _generator_maps
from .twist_supports import support_curve


@lru_cache(maxsize=1)
def _sphere_maps():
    return tuple((generator, {letter: sphere_reduce(mapping[letter])
                               for letter in (*range(1, 6), *range(-5, 0))})
                 for generator, mapping in _generator_maps(6))


def _act(word, mapping):
    return free_homotopy_key(reduce_word(letter
                                        for symbol in word
                                        for letter in mapping[symbol]))


_GOALS = {free_homotopy_key((index, index + 1)): index for index in range(1, 5)}
_GOALS[free_homotopy_key(sphere_reduce((5, 6)))] = 5


@lru_cache(maxsize=256)
def short_sphere_arc(boundary_word, endpoints, *, max_states=5000, max_depth=32):
    """Recover a verified sphere-equivalent two-point Arc, or raise a limit.

    ``endpoints`` fixes the marked points; the quotient class alone would not
    be enough to accept a representative involving a complementary pair.
    The search is deliberately bounded so edited lab sessions remain usable.
    """
    start = free_homotopy_key(sphere_reduce(tuple(boundary_word)))
    endpoints = tuple(endpoints)
    if len(endpoints) != 2 or not all(1 <= point <= 6 for point in endpoints):
        raise ValueError('A sphere chain arc needs two marked-point endpoints')
    todo = [(len(start), 0, (), start)]
    seen = {start}
    for _ in range(max_states):
        if not todo:
            break
        _, depth, path, word = heappop(todo)
        if word in _GOALS:
            # Maps along path apply in traversal order; the conjugator that
            # carries the standard support back to start is their inverse.
            twist = ConjugatedTwist(tuple(-step for step in path),
                                    _GOALS[word], 2, 1, True)
            arc = support_curve(twist)
            if ({arc.start, arc.end} == set(endpoints) and
                    free_homotopy_key(sphere_reduce(supported_class(twist))) == start):
                return arc, len(path)
        if depth >= max_depth:
            continue
        for generator, mapping in _sphere_maps():
            image = _act(word, mapping)
            if image in seen or len(image) > len(start) + 10:
                continue
            seen.add(image)
            heappush(todo, (len(image) + depth // 4,
                            depth + 1, path + (generator,), image))
    raise ValueError(f'No short sphere-equivalent arc found within {max_states} states')


def short_sphere_chain(images):
    """Return the five individual edges between consecutive original points."""
    words, endpoints = chain_words(images)
    return tuple(short_sphere_arc(words[index], endpoints[index])
                 for index in range(1, 6))


@lru_cache(maxsize=128)
def sphere_chain_drawing(images):
    """Return the usual fan and vertical-ray views of five certified arcs."""
    certificate, arcs, depths, method = _sphere_chain_certificate(images)
    return _drawing(certificate, arcs, depths, method)


@lru_cache(maxsize=128)
def sphere_chain_smooth_drawing(images):
    """Render the optional smooth view only after it is requested."""
    certificate, _, _, _ = _sphere_chain_certificate(images)
    return render_normal_cut_preview(certificate, projection='smooth',
                                     mirror_vertical=True)


@lru_cache(maxsize=128)
def _sphere_chain_certificate(images):
    """Certify and draw five sphere arcs in one disk chart.

    Independent short representatives can conflict at the chart's ray orders.
    In that case, try the exact disk representatives in combinations, ranked
    by crossing count, and accept only a complete joint normal certificate.
    """
    images = tuple(tuple(image) for image in images)
    short = []
    for index, (word, endpoints) in enumerate(zip(*chain_words(images))):
        if index == 0:
            continue  # A sphere has no distinguished boundary-to-first arc.
        try:
            short.append(short_sphere_arc(word, endpoints))
        except ValueError:
            short.append(None)
    if all(item is not None for item in short):
        arcs = tuple(item[0] for item in short)
        try:
            certificate = calculate_cut_system(arcs)
            return certificate, arcs, tuple(item[1] for item in short), 'sphere-short'
        except (ValueError, NormalTriangleError):
            pass
    raw = tuple(chain_arc(images, index) for index in range(1, 6))
    options = sorted(product((0, 1), repeat=5),
                     key=lambda bits: (sum(len((raw[index] if bit or short[index] is None
                                                else short[index][0]).cuts)
                                           for index, bit in enumerate(bits)), sum(bits)))
    for bits in options:
        arcs = tuple(raw[index] if bit or short[index] is None else short[index][0]
                     for index, bit in enumerate(bits))
        try:
            certificate = calculate_cut_system(arcs)
            return (certificate, arcs,
                    tuple(0 if bit or short[index] is None else short[index][1]
                          for index, bit in enumerate(bits)),
                    'sphere-short' if not any(bits) and all(short) else 'joint-chart')
        except (ValueError, NormalTriangleError):
            continue
    raise ValueError('No jointly certified five-arc chart found among the bounded sphere and disk representatives')


def _drawing(certificate, arcs, depths, method):
    return dict(svg=render_normal_cut_preview(certificate, projection='fan',
                                              mirror_vertical=True),
                svg_strip=render_normal_cut_preview(certificate, projection='strip',
                                                    mirror_vertical=True),
                cut_counts=tuple(len(arc.cuts) for arc in arcs),
                endpoints=tuple((arc.start, arc.end) for arc in arcs),
                sphere_search_depths=depths, method=method,
                joint_certified=True)
