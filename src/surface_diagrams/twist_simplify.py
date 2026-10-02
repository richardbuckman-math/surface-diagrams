"""Bounded braid-relation search preserving a conjugated twist's type.

Search can change the standard core and discard suffixes stabilizing its
support. Every result is checked exactly. This is not a shortest-word oracle.
"""
from dataclasses import replace
from functools import lru_cache
from heapq import heappush,heappop
from .braid_actions import reduce_word,inverse_word
from .mapping_classes import ConjugatedTwist,exact_action,supported_class,VerificationLimitError


def _relations(strands):
    table={}
    for a in range(1,strands-1):
        b=a+1; relator=(a,b,a,-b,-a,-b)
        for rel in (relator,inverse_word(relator)):
            for k in range(6):
                r=rel[k:]+rel[:k]
                table.setdefault(r[:3],set()).add(inverse_word(r[3:]))
    return table


@lru_cache(maxsize=4096)
def _transported_core(suffix,first,points,power,half,strands):
    core=ConjugatedTwist((),first,points,power,half)
    action=exact_action(suffix+core.core+inverse_word(suffix),strands)
    return tuple(j for j in range(1,strands-points+2)
                 if action==exact_action(ConjugatedTwist((),j,points,power,half).core,strands))


def simplify_twist(twist,*,strands=6,max_states=256):
    if type(max_states) is not int or max_states<1: raise ValueError('max_states must be positive')
    if twist.first+twist.points-1>strands or any(abs(x)>=strands for x in twist.conjugator):
        raise ValueError('Twist lies outside the strand range')
    rules=_relations(strands)
    start=replace(twist,conjugator=reduce_word(twist.conjugator))
    # In the punctured disk a positive twist is determined by its supporting
    # curve (and power); a positive half twist by the two-point neighborhood.
    # Thus an exact match to a standard support can remove the entire
    # conjugator, even when bounded braid rewrites cannot expose cancellation.
    if start.conjugator:
        try:
            boundary=supported_class(start,strands)
            for first in range(1,strands-start.points+2):
                standard=replace(start,conjugator=(),first=first)
                if boundary==supported_class(standard,strands): return standard
        except VerificationLimitError:
            pass  # The existing bounded local rewrite proof remains available.
    def score(t): return (len(t.conjugator),len(t.word),t.conjugator,t.first)
    best=start; pending=[]; seen=set(); parents={}
    def add(g,first,parent=None,step=None):
        key=(reduce_word(g),first)
        if key in seen or len(seen)>=max_states*8: return
        seen.add(key); candidate=replace(start,conjugator=key[0],first=first)
        parents[key]=(parent,step)
        heappush(pending,(score(candidate),candidate))
    add(start.conjugator,start.first)
    for unused in range(max_states):
        if not pending: break
        _,candidate=heappop(pending)
        if score(candidate)<score(best): best=candidate
        g=candidate.conjugator
        parent=(g,candidate.first)
        if not g: break
        # Trimming a conjugator tail may commute through the core, or move the
        # core to a different standard interval. Both are checked, not assumed.
        for size in range(1,min(4,len(g))+1):
            for first in _transported_core(g[-size:],candidate.first,candidate.points,candidate.power,candidate.half,strands):
                add(g[:-size],first,parent,('core',size))
        for i in range(len(g)-1):
            if abs(abs(g[i])-abs(g[i+1]))>1:
                add(g[:i]+(g[i+1],g[i])+g[i+2:],candidate.first,parent,('rewrite',i,2,(g[i+1],g[i])))
        for i in range(len(g)-2):
            for replacement in rules.get(g[i:i+3],()):
                add(g[:i]+replacement+g[i+3:],candidate.first,parent,('rewrite',i,3,replacement))
    # Verify the complete chain locally. Expanding a huge common conjugator
    # can exceed the action limit even when every intervening rewrite is tiny.
    key=(best.conjugator,best.first)
    while parents[key][0] is not None:
        parent,step=parents[key];g,first=parent;child,child_first=key
        if step[0]=='core':
            size=step[1]
            valid=(child==reduce_word(g[:-size]) and child_first in
                   _transported_core(g[-size:],first,start.points,start.power,start.half,strands))
        else:
            _,i,size,replacement=step
            valid=(child_first==first and child==reduce_word(g[:i]+replacement+g[i+size:]) and
                   exact_action(g[i:i+size],strands)==exact_action(replacement,strands))
        if not valid:raise ValueError('Twist simplification failed local proof verification')
        key=parent
    from .support_simplify import shorter_support_path
    return shorter_support_path(best,strands=strands,max_states=max_states)
