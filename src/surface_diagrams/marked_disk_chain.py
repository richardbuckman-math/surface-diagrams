"""Exact boundary-to-first, then adjacent-point chains on a marked disk.

Unlike a sphere chain, the initial arc has a fixed outer-boundary endpoint.
It detects the exterior boundary twist even when every point-to-point arc
returns to its starting isotopy class.
"""

from .based_cut_system import based_arc_from_meridian
from .boundary_playground_geometry import _arc_from_class
from .braid_actions import reduce_word
from .curves import Arc


def _puncture(image, points):
    image = reduce_word(image)
    start, end = 0, len(image)
    while end - start > 1 and image[start] == -image[end - 1]:
        start += 1
        end -= 1
    if end - start != 1 or not 1 <= image[start] <= points:
        raise ValueError('Expected a transported positive puncture meridian')
    return image[start]


def marked_disk_chain(images):
    """Recover the full disk chain from an exact Artin meridian action.

    Each edge is reconstructed independently from its exact boundary class.
    Call ``calculate_cut_system(..., points=len(images))`` to certify their
    simultaneous local placement before drawing them together.
    """
    images = tuple(tuple(image) for image in images)
    points = len(images)
    if points < 2:
        raise ValueError('A marked disk chain needs at least two meridians')
    endpoints = tuple(_puncture(image, points) for image in images)
    if set(endpoints) != set(range(1, points + 1)):
        raise ValueError('Meridian images do not permute all marked points')
    arcs = [based_arc_from_meridian(images[0], points=points)]
    for index in range(points - 1):
        boundary = reduce_word(images[index] + images[index + 1])
        arc = _arc_from_class(boundary, endpoints[index], endpoints[index + 1], points)
        arcs.append(Arc(arc.start, arc.end) if not arc.cuts and
                    abs(arc.start - arc.end) == 1 else arc)
    return tuple(arcs)
