"""Recover exact Arc/Loop itineraries and use the shared surface renderer.

Boundary words determine topology; the shared noninterleaving route solver
must additionally accept the proposed itinerary before it is drawn.
"""
from functools import lru_cache
from .curves import Arc,Loop
from .model import PlanarSurface,Style
from .svg import render_svg
from .braid_actions import arc_ray_word,loop_ray_word,free_homotopy_key,inverse_word
from .mapping_classes import supported_class


def _ray_cuts(word):
    """Upper ray-crossing runs joined by lower segments."""
    runs=[]
    for letter in word:
        if runs and (runs[-1][-1]>0)==(letter>0) and letter==runs[-1][-1]+1:
            runs[-1].append(letter)
        else: runs.append([letter])
    cuts=[]
    for run in runs:
        cuts.extend((run[0]-1,run[-1]) if run[0]>0 else (-run[0],-run[-1]-1))
    return cuts


def loop_from_class(word):
    """Propose a Loop with this exact class; routing still checks embeddedness."""
    word=free_homotopy_key(word)
    if not word: raise ValueError('Empty boundary class has no essential loop')
    curve=Loop(tuple(_ray_cuts(word)),start_up=True)
    if free_homotopy_key(loop_ray_word(6,curve))!=word:
        raise ValueError('Exact loop itinerary failed its boundary-word check')
    return curve


def arc_from_class(word,start,end):
    """Recover an arc from its two-puncture neighborhood boundary.

    Search the cyclic word for x_start t x_end t^-1 in either orientation.
    The path t crosses upward rays; lower segments join consecutive runs.
    This proposes an itinerary, not an embeddedness certificate.
    """
    word=free_homotopy_key(word)
    if len(word)<2 or len(word)%2:
        raise ValueError('Boundary class cannot represent a two-point arc')
    # A 64-cut itinerary has at most 33 upper segments, each crossing at
    # most six rays. A larger reduced boundary cannot fit the shared limit.
    if len(word)>2+2*33*6:
        raise ValueError('Exact arc topology exceeds the shared 64-cut drawing limit')
    size=(len(word)-2)//2
    for oriented in (word,inverse_word(word)):
        for index,letter in enumerate(oriented):
            if letter!=start: continue
            rotated=oriented[index:]+oriented[:index]
            transport=rotated[1:size+1]
            if rotated[size+1]!=end or rotated[size+2:]!=inverse_word(transport): continue
            cuts=_ray_cuts(transport); up=False
            # Endpoint meridian turns are immaterial to an unframed point arc.
            while cuts and cuts[0] in (start-1,start): cuts.pop(0); up=not up
            while cuts and cuts[-1] in (end-1,end): cuts.pop()
            curve=Arc(start,end,tuple(cuts),direction='up' if up else 'down')
            actual=arc_ray_word(6,curve)
            observed=(start,)+actual+(end,)+inverse_word(actual)
            if free_homotopy_key(observed)==word: return curve
    raise ValueError('Exact boundary class has no recovered endpoint path')


@lru_cache(maxsize=64)
def support_curve(twist):
    word=supported_class(twist)
    if not twist.half: return loop_from_class(word)
    start,end=twist.first,twist.first+1
    # A(uv)=A(u) composed with A(v), so the last permutation acts first.
    for crossing in reversed(twist.conjugator):
        index=abs(crossing)
        start=index+1 if start==index else index if start==index+1 else start
        end=index+1 if end==index else index if end==index+1 else end
    return arc_from_class(word,start,end)


@lru_cache(maxsize=64)
def support_drawing(twist):
    curve=support_curve(twist)
    surface=PlanarSurface.row('PPPPPP',spacing=50,height=220,margin=55).with_curves(curve)
    return render_svg(surface,style=Style(curve_color='#a21caf',curve_width=1.5,marked_point_radius=3.5))
