"""Exact sphere comparison across a six-strand factorization split.

A factor prefix and the inverse of its suffix need not agree as disk braids.
On the sphere their actions differ only by the common basepoint whisker of a
certified full product. Retaining the actual meridian images makes the
comparison independently checkable. The five reported arc counts belong to
consecutive-puncture edges in a disk chart of the sphere; no artificial
boundary-to-first-puncture edge is part of the sphere cut system.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .braid_actions import inverse_word, reduce_word
from .chain_cut_system import chain_arc
from .factorization_explorer import Factor, initial_factors, product, validate_size
from .mapping_classes import exact_action
from .sphere_actions import sphere_inner_certificate, sphere_reduce


@dataclass(frozen=True)
class SphereSplitCertificate:
    split_index: int
    forward_factor_ids: tuple[str, ...]
    backward_inverse_factor_ids: tuple[str, ...]
    forward_braid: tuple[int, ...]
    backward_inverse_braid: tuple[int, ...]
    common_whisker: tuple[int, ...]
    forward_disk_images: tuple[tuple[int, ...], ...]
    backward_disk_images: tuple[tuple[int, ...], ...]
    forward_sphere_images: tuple[tuple[int, ...], ...]
    backward_sphere_images: tuple[tuple[int, ...], ...]
    expected_sphere_images: tuple[tuple[int, ...], ...]
    forward_pairwise_chart_cut_counts: tuple[int | None, ...]
    backward_pairwise_chart_cut_counts: tuple[int | None, ...]
    arc_count_limit_notes: tuple[str, ...]

    @property
    def sphere_equal(self):
        return self.forward_sphere_images == self.expected_sphere_images

    @property
    def disk_equal(self):
        return self.forward_disk_images == self.backward_disk_images

    @property
    def forward_sphere_meridian_lengths(self):
        return tuple(map(len, self.forward_sphere_images))

    @property
    def backward_sphere_meridian_lengths(self):
        return tuple(map(len, self.backward_sphere_images))


def _individual_arc_cut_counts(images, label):
    counts = []
    notes = []
    for index in range(1, 6):
        try:
            counts.append(len(chain_arc(images, index).cuts))
        except ValueError as exc:
            # Arc's finite drawing representation is independent of the exact
            # sphere comparison; preserve the certificate when only this cap
            # is exceeded, without hiding unrelated recovery errors.
            if 'cut drawing limit' not in str(exc) and 'cut visits are supported' not in str(exc):
                raise
            counts.append(None)
            notes.append(f'{label} arc {index}-{index + 1}: {exc}')
    return tuple(counts), tuple(notes)


def sphere_split_certificate(factors, split_index):
    """Compare a verified six-strand factor prefix with its inverse suffix.

    Artin words compose right-first: A(P S) = A(P) composed with A(S).
    The certified full sphere action is inner conjugation by ``w``, hence
    A(P)(x_i) = w A(S^-1)(x_i) w^-1 after the sphere boundary relation.
    ``inverse_word`` reverses the factor order as well as every generator.
    The five consecutive-puncture arcs are recovered independently in a disk
    chart; the sphere has no boundary-to-first-puncture arc. A missing cut
    count records only Arc's finite representation limit; exact images are
    never truncated or compared approximately.
    """
    factors = tuple(factors)
    if not factors or any(not isinstance(factor, Factor) for factor in factors):
        raise TypeError('Expected a nonempty list of six-strand Factor records')
    if type(split_index) is not int or not 1 <= split_index < len(factors):
        raise ValueError('Split index must leave at least one factor on each side')
    validate_size(factors)
    forward_factors, suffix_factors = factors[:split_index], factors[split_index:]
    forward = product(forward_factors)
    backward = inverse_word(product(suffix_factors))
    full = sphere_inner_certificate(product(factors))
    if not full['certified']:
        raise ValueError('Full product has no certified sphere identity action')
    whisker = full['conjugator']

    forward_disk = exact_action(forward)
    backward_disk = exact_action(backward)
    forward_sphere = tuple(map(sphere_reduce, forward_disk))
    backward_sphere = tuple(map(sphere_reduce, backward_disk))
    expected = tuple(reduce_word(whisker + image + inverse_word(whisker))
                     for image in backward_sphere)
    forward_counts, forward_notes = _individual_arc_cut_counts(forward_disk, 'forward')
    backward_counts, backward_notes = _individual_arc_cut_counts(backward_disk, 'backward')
    certificate = SphereSplitCertificate(
        split_index,
        tuple(f.id for f in forward_factors),
        tuple(f.id for f in reversed(suffix_factors)),
        forward, backward, whisker, forward_disk, backward_disk,
        forward_sphere, backward_sphere, expected,
        forward_counts, backward_counts, forward_notes + backward_notes,
    )
    if not certificate.sphere_equal:
        raise ValueError('The split failed its exact six-meridian sphere comparison')
    return certificate


@lru_cache(maxsize=1)
def six_seven_midpoint_certificate():
    """Convenience certificate for F1..F7 versus (F8..F13)^-1."""
    return sphere_split_certificate(initial_factors(), 7)
