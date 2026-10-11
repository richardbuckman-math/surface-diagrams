"""Route-free calculation and certificate for a collection of normal Arcs.

The result retains the labeled local connections and ordered triangle sides
needed by a renderer. It certifies their joint noncrossing pairing and exact
Arc itineraries, but makes no assertion about minimal position or SVG geometry.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .curves import Arc
from .normal_certificate import certify_arc_orders
from .normal_gluing import GluedArc, NormalTriangle, arc_triangles
from .normal_itinerary import LocalTriangleConnection, arc_local_connections
from .normal_strands import NormalTriangleError
from .normal_suffix_rank import resolve_connection_orders


@dataclass(frozen=True)
class CertifiedCutSystem:
    """Ordered local data and exact labeled paths for selected Arc owners.

    ``owners`` and ``paths`` follow the requested owner order. The complete
    ray/cut maps contain empty edges as well as visited edges. Their visits
    keep one-based arc owners and original itinerary crossing IDs.
    """

    arcs: tuple[Arc, ...]
    owners: tuple[int, ...]
    points: int
    connections: tuple[LocalTriangleConnection, ...]
    ray_orders: Mapping[tuple[str, int], tuple]
    cut_orders: Mapping[int, tuple]
    triangles: tuple[NormalTriangle, ...]
    paths: tuple[GluedArc, ...]


def calculate_cut_system(arcs, *, owners=None, points=6):
    """Derive and certify a joint normal placement from exact Arc itineraries.

    Every supplied arc is selected by default. A partial ``owners`` selection
    may omit only straight adjacent chain arcs, as required by the triangle
    assembler. Unresolved or conflicting local orders raise
    ``NormalTriangleError`` instead of choosing an arbitrary placement.
    No route or drawing coordinates are consulted.
    """
    if type(points) is not int or points < 2:
        raise ValueError('points must be at least two')
    arcs = tuple(arcs)
    if not arcs or any(not isinstance(arc, Arc) for arc in arcs):
        raise NormalTriangleError('expected one or more Arc itineraries')
    owners = (tuple(range(1, len(arcs) + 1)) if owners is None
              else tuple(owners))
    if (not owners or any(type(owner) is not int
                          or not 1 <= owner <= len(arcs) for owner in owners)
            or len(set(owners)) != len(owners)):
        raise ValueError('owners must be distinct one-based arc labels')
    selected = set(owners)
    if any(owner not in selected and not (
            arc.is_straight(points) and abs(arc.start - arc.end) == 1)
           for owner, arc in enumerate(arcs, 1)):
        raise NormalTriangleError('omitted arc is not an edge-parallel chain arc')

    connections = tuple(connection for owner in owners
                        for connection in arc_local_connections(
                            arcs[owner - 1], points=points, owner=owner))
    rays, cuts = resolve_connection_orders(connections, points=points)
    # The exact-itinerary certificate is the required gate before any ordered
    # triangle data is handed to a renderer.
    paths = certify_arc_orders(arcs, rays, cuts, owners=owners)
    triangles, _ = arc_triangles(arcs, rays, cuts, owners=owners)
    return CertifiedCutSystem(
        arcs, owners, points, connections, MappingProxyType(rays),
        MappingProxyType(cuts), triangles, paths)
