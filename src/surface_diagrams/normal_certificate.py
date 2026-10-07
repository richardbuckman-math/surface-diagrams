"""Check a supplied joint normal placement against exact Arc itineraries.

This verifies labeled combinatorics, not minimal position or the geometry of
an SVG. The crossing orders must be supplied or derived elsewhere.
"""

from .normal_gluing import TerminalVisit, arc_triangles, glue_triangles
from .normal_itinerary import arc_local_connections
from .normal_strands import NormalTriangleError


def certify_arc_orders(arcs, ray_orders, cut_orders, *, owners=None):
    """Glue a joint placement and match every selected arc's exact events.

    Omitted arcs must be straight edge-parallel components as required by
    ``arc_triangles``. The returned paths retain their one-based owner IDs.
    This certificate does not assert that a given itinerary is in minimal
    position relative to the triangulation.
    """
    arcs = tuple(arcs)
    owners = tuple(range(1, len(arcs) + 1)) if owners is None else tuple(owners)
    triangles, expected = arc_triangles(arcs, ray_orders, cut_orders,
                                        owners=owners)
    paths = glue_triangles(triangles, expected)
    for path in paths:
        connections = arc_local_connections(
            arcs[path.owner - 1], points=len(cut_orders) - 1,
            owner=path.owner)
        if (path.start != connections[0].first
                or path.end != connections[-1].second):
            raise NormalTriangleError(
                f'owner {path.owner} terminal mismatch after gluing')
        itinerary = tuple(connection.second for connection in connections
                          if not isinstance(connection.second, TerminalVisit))
        if path.crossings != itinerary:
            raise NormalTriangleError(
                f'owner {path.owner} itinerary mismatch after gluing')
    return paths
