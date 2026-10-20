"""Maximize six-tetrahedron coverage, with a finite global upper bound.

After exhaustively handling K source solids, a net not handled yet can cover
at most N-K targets. Thus best >= N-K certifies global optimality, without
requiring enumeration of every source. Pruning rejects only nets whose count
of already failed targets prevents a strict improvement.
"""
import json
from pathlib import Path
import time
if __package__:
    from .engine import fold_net,verify_net,spanning_tree_count,common_tree_search
    from .verify_six import trees,unfold
else:
    from engine import fold_net,verify_net,spanning_tree_count,common_tree_search
    from verify_six import trees,unfold


def run(seconds=240):
    path=Path('.preview/common-nets/tetrahedra.json');report=json.loads(path.read_text());row=report['levels']['6']
    surfaces=row['surfaces'];n=len(surfaces);start=time.monotonic();best=row['net'];score=len(best['coverage'])
    completed=[];source_results=[];timed_out=False
    ranking=sorted(range(n),key=lambda i:spanning_tree_count(surfaces[i]['adjacency']))
    for source in ranking:
        tested=0;valid=0;failures=[0]*n;others=[i for i in range(n) if i!=source]
        for edges,selected in trees(surfaces[source]['adjacency']):
            tested+=1
            if tested%512==0 and time.monotonic()-start>seconds:
                timed_out=True;break
            net=unfold(surfaces[source]['adjacency'],edges,selected)
            if net is None:continue
            valid+=1;covered=[source];misses=0;maps=[None]*n
            for target in others:
                mapping=fold_net(net,surfaces[target],check=False)
                if mapping is None:
                    misses+=1;failures[target]+=1
                    if n-misses<=score:break
                else:covered.append(target);maps[target]=mapping
            else:
                if len(covered)>score:
                    maps[source]=fold_net(net,surfaces[source]);assert maps[source] is not None
                    net.update(mappings=maps,coverage=sorted(covered))
                    for i in covered:verify_net(net,surfaces[i],maps[i])
                    best=net;score=len(covered);print('new best',score,'source',source,'tree',tested,flush=True)
            if tested%256==0:others.sort(key=lambda i:-failures[i])
        total=spanning_tree_count(surfaces[source]['adjacency'])
        complete=tested==total and not timed_out
        source_results.append(dict(source=source,tested=tested,spanning_trees=total,planar_nets=valid,
                                   complete=complete,coverage_upper_bound=score if complete else n))
        if complete:completed.append(source)
        print('source finished',source_results[-1],flush=True)
        if timed_out or score>=n-len(completed):break
    row['best_single_net']=best
    row['single_net_optimization']=dict(best=score,complete_sources=completed,
        global_upper_bound=max(score,n-len(completed)),globally_optimal=score>=n-len(completed),
        source_results=source_results,seconds=round(time.monotonic()-start,3),timed_out=timed_out)
    missing=[i for i in range(n) if i not in best['coverage']]
    if missing:
        completion=common_tree_search([surfaces[i] for i in missing],seconds=30)
        if completion['found']:
            other=completion['found'];other['mappings']=[fold_net(other,s) for s in surfaces]
            other['coverage']=[i for i,m in enumerate(other['mappings']) if m is not None]
            row['previous_two_net_cover']=row['two_net_cover']
            row['two_net_cover']=[best,other]
    path.write_text(json.dumps(report,separators=(',',':')))
    print(row['single_net_optimization'],flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=float,default=240)
    run(parser.parse_args().seconds)
