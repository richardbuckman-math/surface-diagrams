from __future__ import annotations

from typing import Iterable, Sequence, Tuple

from .mapping_class import PlanarMappingClass
from .surface import SurfaceSpec


def artin_generator(surface: SurfaceSpec, index: int) -> PlanarMappingClass:
    return PlanarMappingClass.from_artin_word(surface, [index])


def half_twist(surface: SurfaceSpec, start: int, end: int) -> PlanarMappingClass:
    """Half twist between two strands, represented as a band-generator braid."""

    if start <= 0 or end <= 0 or start > surface.total_strands or end > surface.total_strands:
        raise ValueError("strand indices must lie on the surface")
    if start == end:
        raise ValueError("a half twist requires two distinct strands")
    if start > end:
        start, end = end, start

    word = []
    for index in range(start, end - 1):
        word.append(-index)
    word.append(end - 1)
    for index in range(end - 2, start - 1, -1):
        word.append(index)
    return PlanarMappingClass.from_artin_word(surface, word)


def _normalized_subset(
    surface: SurfaceSpec, strands: Iterable[int]
) -> Tuple[int, ...]:
    subset = tuple(sorted(dict.fromkeys(int(value) for value in strands)))
    if len(subset) < 2:
        raise ValueError("a subset twist requires at least two strands")
    if subset[0] <= 0 or subset[-1] > surface.total_strands:
        raise ValueError("subset strands must lie on the surface")
    return subset


def _consecutive_block_word(start: int, size: int) -> Tuple[int, ...]:
    block = tuple(range(start, start + size - 1))
    return block * size


def _subset_conjugation_word(strands: Sequence[int]) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    positive = []
    negative = []
    next_strand = strands[0] + 1
    for strand in strands[1:]:
        positive.extend(range(strand - 1, next_strand - 1, -1))
        negative.extend(range(-strand + 1, -next_strand + 1))
        next_strand += 1
    negative.reverse()
    return tuple(positive), tuple(negative)


def subset_transport_word(
    surface: SurfaceSpec,
    strands: Iterable[int],
) -> Tuple[int, ...]:
    """Return a braid word transporting a consecutive block to `strands`.

    If `strands` has size `k` and begins at `i`, the returned word transports
    the standard loop around `(i, ..., i + k - 1)` to the standard loop around
    `strands`. Equivalently, conjugating the consecutive full twist by this
    word gives `subset_full_twist(surface, strands)`.
    """

    subset = _normalized_subset(surface, strands)
    if all(
        subset[index] + 1 == subset[index + 1]
        for index in range(len(subset) - 1)
    ):
        return ()
    _, transport = _subset_conjugation_word(subset)
    return transport


def subset_full_twist(
    surface: SurfaceSpec, strands: Iterable[int], power: int = 1
) -> PlanarMappingClass:
    """Full twist on an arbitrary subset of strands.

    Geometrically this is the braid representative of a Dehn twist around the
    selected subset of punctures or inner boundaries.
    """

    subset = _normalized_subset(surface, strands)
    center = _consecutive_block_word(subset[0], len(subset))
    transport = subset_transport_word(surface, subset)
    if transport:
        base = tuple(-value for value in reversed(transport)) + center + transport
    else:
        base = center
    mapping_class = PlanarMappingClass.from_artin_word(surface, base)
    if power == 0:
        return PlanarMappingClass.identity(surface)
    if power < 0:
        mapping_class = mapping_class.inverse()
        power = -power
    total = PlanarMappingClass.identity(surface)
    for _ in range(power):
        total = total * mapping_class
    return total


def outer_boundary_twist(surface: SurfaceSpec, power: int = 1) -> PlanarMappingClass:
    return subset_full_twist(surface, range(1, surface.total_strands + 1), power=power)
