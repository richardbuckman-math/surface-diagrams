"""Second geometric implementation for auditing the common-net results.

Target transitions are derived from shared 3D vertex coordinates, never from
engine.neighbor or its rotation arithmetic. Planar unfolding uses reflection
of the opposite vertex. Tree enumeration is shared with verify_six, so this
is an independent folding/unfolding implementation, not an external review.
"""
from itertools import permutations
from hashlib import sha256
import json
from pathlib import Path
import time

from .verify_six import trees


class Surface:
    def __init__(self, data):
        points = sorted({tuple(v) for face in data['faces'] for v in face})
        ids = {v: i for i, v in enumerate(points)}
        self.faces = [tuple(ids[tuple(v)] for v in face) for face in data['faces']]
        edges = {}
        for f, face in enumerate(self.faces):
            for i in range(3):
                edge = tuple(sorted((face[i], face[(i + 1) % 3])))
                edges.setdefault(edge, []).append(f)
        if any(len(pair) != 2 for pair in edges.values()):
            raise ValueError('Surface does not have two faces per edge')
        self.adjacency = []
        for f, face in enumerate(self.faces):
            row = []
            for i in range(3):
                edge = tuple(sorted((face[i], face[(i + 1) % 3])))
                other = next(g for g in edges[edge] if g != f)
                row.append((other, edge))
            self.adjacency.append(row)
        flags = [(f, p) for f, face in enumerate(self.faces) for p in permutations(face)]
        lookup = {flag: i for i, flag in enumerate(flags)}
        self.bits = [1 << f for f, _ in flags]
        self.transitions = []
        for f, vertices in flags:
            row = []
            for edge in range(3):
                a, b = vertices[edge], vertices[(edge + 1) % 3]
                other = next(g for g in edges[tuple(sorted((a, b)))] if g != f)
                c = next(v for v in self.faces[other] if v not in (a, b))
                row.append(lookup[(other, (b, a, c))])
            self.transitions.append(row)

    def folds(self, net):
        size = len(self.faces)
        if len(net['triangles']) != size:
            return False
        hinges = net['hinges']
        for root in range(6 * size):
            placement = [root]
            used = self.bits[root]
            for a, b, edge in hinges:
                if b != len(placement) or a >= b:
                    raise ValueError('Audit nets must be in rooted tree order')
                state = self.transitions[placement[a]][edge]
                bit = self.bits[state]
                if used & bit:
                    break
                used |= bit
                placement.append(state)
            else:
                return len(placement) == size
        return False


def unfold(surface, edges, selected):
    graph = [[] for _ in surface.faces]
    for e in selected:
        a, b = edges[e]
        graph[a].append(b)
        graph[b].append(a)
    # A source face's vertices and its paper triangle need not have the same
    # order; carry their explicit pairing instead of a rotation index.
    placed = [0]
    index = {0: 0}
    paper = [((0, 0), (1, 0), (0, 1))]
    vertex_orders = [surface.faces[0]]
    cells = {tuple(sorted(paper[0]))}
    hinges = []
    for a, face in enumerate(placed):
        for other in graph[face]:
            if other in index:
                continue
            shared = set(surface.faces[face]) & set(surface.faces[other])
            edge = next(i for i in range(3) if
                        {vertex_orders[a][i], vertex_orders[a][(i + 1) % 3]} == shared)
            u, v, w = (paper[a][(edge + j) % 3] for j in range(3))
            reflected = (u[0] + v[0] - w[0], u[1] + v[1] - w[1])
            triangle = (v, u, reflected)
            key = tuple(sorted(triangle))
            if key in cells:
                return None
            c = next(x for x in surface.faces[other] if x not in shared)
            order = (vertex_orders[a][(edge + 1) % 3], vertex_orders[a][edge], c)
            b = len(placed)
            index[other] = b
            placed.append(other)
            vertex_orders.append(order)
            paper.append(triangle)
            cells.add(key)
            hinges.append((a, b, edge))
    if len(placed) != len(surface.faces):
        raise ValueError('Selected edges do not span the surface')
    return dict(triangles=paper, hinges=hinges)


def canonical_net(net):
    """Paper triangles AND fixed hinge locations, modulo planar isometries."""
    def transform(p, rotation, reflected):
        x, y = p
        if reflected:
            x, y = x + y, -y
        for _ in range(rotation):
            x, y = -y, x + y
        return x, y
    results = []
    for reflection in (False, True):
        for rotation in range(6):
            cells = [[transform(p, rotation, reflection) for p in t] for t in net['triangles']]
            origin = min(p for cell in cells for p in cell)
            cells = [[(x - origin[0], y - origin[1]) for x, y in t] for t in cells]
            hinges = [tuple(sorted((cells[a][e], cells[a][(e + 1) % 3])))
                      for a, _, e in net['hinges']]
            results.append((tuple(sorted(tuple(sorted(t)) for t in cells)), tuple(sorted(hinges))))
    return min(results)


def mabry_five_reference():
    """Lattice transcription of commonT5net.png on Mabry's common8V page.

    All shared triangle edges are hinges: this picture has no internal slit.
    Used only as a paper-pattern reference, not a root-ordered fold record.
    """
    cells = [[(i, 0), (i + 1, 0), (i + 1, -1)] for i in range(4)]
    cells += [[(i, -1), (i + 1, -1), (i, 0)] for i in range(1, 4)]
    cells += [[(2, -3), (3, -3), (2, -2)],
              [(3, -3), (2, -2), (3, -2)],
              [(3, -3), (4, -3), (3, -2)],
              [(2, -2), (3, -2), (2, -1)],
              [(2, -2), (1, -1), (2, -1)]]
    edges = {}
    hinges = []
    for a, triangle in enumerate(cells):
        for e in range(3):
            edge = tuple(sorted((triangle[e], triangle[(e + 1) % 3])))
            if edge in edges:
                b, entry = edges[edge]
                hinges.append((b, a, entry))
            else:
                edges[edge] = (a, e)
    assert len(hinges) == 11
    return dict(triangles=cells, hinges=hinges)


def calibrate(row):
    surfaces = [Surface(s) for s in row['surfaces']]
    source = min(range(len(surfaces)), key=lambda i: row['tree_counts'][i])
    found = {}
    tested = planar = 0
    for edges, selected in trees(surfaces[source].adjacency):
        tested += 1
        net = unfold(surfaces[source], edges, selected)
        if net is None:
            continue
        planar += 1
        if all(s.folds(net) for s in surfaces):
            found.setdefault(canonical_net(net), net)
    assert tested == row['tree_counts'][source]
    return dict(source=source, tested=tested, planar=planar,
                common_net_count=len(found),
                common_footprints=len({key[0] for key in found}),
                common_nets=list(found.values()))


def single_surface_inventories(row):
    counts = []
    for data in row['surfaces']:
        surface = Surface(data)
        inventory = set()
        for edges, selected in trees(surface.adjacency):
            net = unfold(surface, edges, selected)
            if net is not None:
                inventory.add(canonical_net(net))
        counts.append(len(inventory))
    return counts


def audit_bound(row, sources, maximum=19):
    surfaces = [Surface(s) for s in row['surfaces']]
    results = []
    for source in sources:
        tested = planar = 0
        failures = [0] * len(surfaces)
        targets = [i for i in range(len(surfaces)) if i != source]
        for edges, selected in trees(surfaces[source].adjacency):
            tested += 1
            net = unfold(surfaces[source], edges, selected)
            if net is None:
                continue
            planar += 1
            missing = 0
            for i in targets:
                if not surfaces[i].folds(net):
                    failures[i] += 1
                    missing += 1
                    if len(surfaces) - missing <= maximum:
                        break
            else:
                raise AssertionError('A net exceeds the proposed coverage bound')
            if tested % 256 == 0:
                targets.sort(key=lambda i: -failures[i])
        assert tested == row['tree_counts'][source]
        result = dict(source=source, trees=tested, planar=planar, coverage_upper_bound=maximum)
        results.append(result)
        print('audited', result, flush=True)
    global_bound = max(maximum, len(surfaces) - len(sources))
    return dict(source_results=results, global_upper_bound=global_bound)


def run(source, destination, six=True):
    from .engine import spanning_tree_count  # determinant only, not folding
    data = json.loads(source.read_text())
    started = time.monotonic()
    for row in data['levels'].values():
        row['tree_counts'] = [spanning_tree_count(s['adjacency']) for s in row['surfaces']]
    result = {'scope': 'Second geometric folding/unfolding implementation; shared tree enumerator and input catalog. Not an external review.',
              'input_sha256': sha256(source.read_bytes()).hexdigest()}
    for n in ('4', '5'):
        result[n] = calibrate(data['levels'][n])
        print('common nets', n, result[n]['common_net_count'], flush=True)
    counts = single_surface_inventories(data['levels']['4'])
    assert sorted(counts) == [203, 280, 452]
    result['4']['single_surface_inventory_counts'] = counts
    from .catalog_compare import apply_comparison
    reference = Path(__file__).parent / 'reference/mabry-four-comparison.json'
    apply_comparison(result['4'], json.loads(reference.read_text()))
    result['5']['matches_mabry_reference'] = (
        canonical_net(result['5']['common_nets'][0]) == canonical_net(mabry_five_reference()))
    assert result['5']['matches_mabry_reference']
    if six:
        row = data['levels']['6']
        sources = row['single_net_optimization']['complete_sources']
        result['6'] = audit_bound(row, sources)
        best = row['best_single_net']
        covered = [i for i, s in enumerate(row['surfaces']) if Surface(s).folds(best)]
        assert covered == best['coverage'] and len(covered) == result['6']['global_upper_bound']
        result['6']['positive_coverage'] = covered
    result['seconds'] = round(time.monotonic() - started, 3)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, separators=(',', ':')))
    print('saved', destination, 'seconds', result['seconds'], flush=True)
    return result


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=Path('.preview/common-nets/tetrahedra.json'))
    parser.add_argument('--destination', type=Path, default=Path('.preview/common-nets/independent-audit.json'))
    parser.add_argument('--small-only', action='store_true')
    args = parser.parse_args()
    run(args.source, args.destination, not args.small_only)
