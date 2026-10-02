"""Bounded search for a shorter positive twist presentation via its support.

This searches unoriented curve classes, not braid equality. Type and power stay
fixed, so exact support agreement proves equality of these supported twists.
"""
from dataclasses import replace
from functools import lru_cache
from heapq import heappush,heappop
from .braid_actions import _extend_action,inverse_word,free_homotopy_key
from .mapping_classes import supported_class,VerificationLimitError


@lru_cache(maxsize=8)
def _generator_maps(strands):
    identity=tuple((i,) for i in range(1,strands+1))
    result=[]
    for index in range(1,strands):
        for crossing in (index,-index):
            images=_extend_action(identity,(crossing,))
            mapping={k:images[k-1] if k>0 else inverse_word(images[-k-1])
                     for i in range(1,strands+1) for k in (i,-i)}
            result.append((crossing,mapping))
    return tuple(result)


def shorter_support_path(twist,*,strands=6,max_states=256):
    if not twist.conjugator: return twist
    try: original=supported_class(twist,strands)
    except VerificationLimitError: return twist
    if len(original)>4096: return twist
    goals={supported_class(replace(twist,conjugator=(),first=i),strands):i
           for i in range(1,strands-twist.points+2)}
    seen={original:0}; pending=[(len(original),0,(),original)]
    remaining_letters=2000000
    for unused in range(max_states):
        if not pending: break
        _,depth,path,word=heappop(pending)
        if seen[word]<depth: continue
        if word in goals:
            candidate=replace(twist,conjugator=path,first=goals[word])
            if supported_class(candidate,strands)!=original:
                raise ValueError('Support-path simplification failed its exact class check')
            return candidate
        if depth+1>=len(twist.conjugator): continue
        for crossing,mapping in _generator_maps(strands):
            next_word=free_homotopy_key(x for letter in word for x in mapping[letter])
            if (len(next_word)>len(original) or seen.get(next_word,float('inf'))<=depth+1
                    or len(next_word)>remaining_letters): continue
            remaining_letters-=len(next_word); seen[next_word]=depth+1
            # Left-applying crossing brings the support toward a standard
            # core; its inverse is appended to the recovered conjugator.
            heappush(pending,(len(next_word),depth+1,path+(-crossing,),next_word))
    return twist
