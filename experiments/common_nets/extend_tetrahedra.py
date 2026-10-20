"""Complete the small cluster catalog; sample useful larger puzzle nets.

Search limits control exploration only. Every retained net is subsequently
tested against the complete target catalog with exact folding certificates.
No optimality claim is made for the sampled seven- and eight-unit puzzles.
"""
from copy import deepcopy
import json
from pathlib import Path
import random
import time
from . import engine
from .audit import Surface,unfold,canonical_net

EXPECTED_COUNTS = [1,1,1,3,7,23,89,398]


def random_tree(surface, rng):
    edges = [(a,b) for a,neighbors in enumerate(surface.adjacency)
             for b,_ in neighbors if a < b]
    order = list(range(len(edges)))
    rng.shuffle(order)
    roots = list(range(len(surface.faces)))
    def find(a):
        while roots[a] != a:
            roots[a] = roots[roots[a]]
            a = roots[a]
        return a
    selected = []
    for i in order:
        a,b = map(find,edges[i])
        if a != b:
            roots[a] = b
            selected.append(i)
    assert len(selected) == len(surface.faces)-1
    return edges,selected


def compactness(net):
    points = [p for t in net['triangles'] for p in t]
    x = [p[0]+p[1]/2 for p in points]
    y = [p[1] for p in points]
    return (max(x)-min(x)+1)*(max(y)-min(y)+1)


def sample_puzzles(surfaces, attempts=500, seed=20261020, keep=8):
    rng = random.Random(seed)
    targets = [Surface(s) for s in surfaces]
    seen = set()
    pool = []
    planar = duplicates = 0
    started = time.monotonic()
    for trial in range(attempts):
        source = rng.randrange(len(targets))
        edges,selected = random_tree(targets[source],rng)
        net = unfold(targets[source],edges,selected)
        if net is None:
            continue
        planar += 1
        key = canonical_net(net)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        coverage = [i for i,target in enumerate(targets) if target.folds(net)]
        assert source in coverage
        net.update(coverage=coverage,source=source,trial=trial)
        pool.append(net)
        pool.sort(key=lambda n:(-len(n['coverage']),compactness(n),n['trial']))
        pool = pool[:keep]
        if pool[0] is net:
            print('best',len(surfaces[0]['faces']),'panels:',len(coverage),'targets; trial',trial,flush=True)
        if trial % 100 == 0:
            print('sampled',trial+1,'/',attempts,'elapsed',round(time.monotonic()-started,1),flush=True)
    for net in pool:
        mappings = [None]*len(surfaces)
        # The original kernel and independent face/hinge verifier confirm
        # every retained target, rather than trusting the sample's score.
        actual = []
        for i,surface in enumerate(surfaces):
            mapping = engine.fold_net(net,surface)
            if mapping is not None:
                engine.verify_net(net,surface,mapping)
                mappings[i] = mapping
                actual.append(i)
        assert actual == net['coverage']
        net['mappings'] = mappings
    return dict(candidates=pool,attempts=attempts,planar_samples=planar,
                distinct_planar_samples=len(seen),duplicate_samples=duplicates,
                seconds=round(time.monotonic()-started,3),seed=seed,
                optimality_proved=False,scope='Sampled source spanning trees; exact coverage over every target. Folded end states only.')


def run(attempts=500):
    folder = Path('.preview/common-nets')
    destination = folder/'tetrahedra-through-eight.json'
    if destination.exists():
        report = json.loads(destination.read_text())
    else:
        report = deepcopy(json.loads((folder/'tetrahedra.json').read_text()))
        levels = engine.enumerate_polytets(8)
        assert [len(levels[n]) for n in range(1,9)] == EXPECTED_COUNTS
        for n in range(1,7):
            assert json.loads(json.dumps(levels[n])) == report['levels'][str(n)]['clusters']
        for n in (7,8):
            clusters = levels[n]
            report['levels'][str(n)] = dict(units=n,faces=2*n+2,shapes=len(clusters),
                clusters=clusters,surfaces=[engine.surface(c) for c in clusters],catalog_complete=True)
        destination.write_text(json.dumps(report,separators=(',',':')))
    for n in (7,8):
        row = report['levels'][str(n)]
        if row.get('puzzle_search',{}).get('attempts',0) >= attempts:
            continue
        row['puzzle_search'] = sample_puzzles(row['surfaces'],attempts,seed=20261020+n)
        destination.write_text(json.dumps(report,separators=(',',':')))
        print('saved',n,'units; best',len(row['puzzle_search']['candidates'][0]['coverage']),flush=True)
    return report


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempts',type=int,default=500)
    args = parser.parse_args()
    run(args.attempts)
