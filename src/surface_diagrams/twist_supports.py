"""Recover shared Arc/Loop inputs, then use the established surface renderer.

Closed loops come from exact words; numerical deformation proposes arc itineraries.
Exact boundary-class agreement
and the shared noninterleaving route solver must accept it before it is drawn.
"""
from functools import lru_cache
from math import floor
from .curves import Arc,Loop
from .model import PlanarSurface,Style
from .svg import render_svg
from .braid_actions import arc_ray_word,loop_ray_word,free_homotopy_key,inverse_word


def loop_from_class(word):
    """Propose a Loop directly from an unoriented free-group boundary word.

    Consecutive ray crossings are upper segments; lower segments join their
    endpoints. The shared route solver must still certify embeddedness.
    """
    word=free_homotopy_key(word)
    if not word: raise ValueError('Empty boundary class has no essential loop')
    runs=[]
    for letter in word:
        if runs and (runs[-1][-1]>0)==(letter>0) and letter==runs[-1][-1]+1:
            runs[-1].append(letter)
        else: runs.append([letter])
    cuts=[]
    for run in runs:
        cuts.extend((run[0]-1,run[-1]) if run[0]>0 else (-run[0],-run[-1]-1))
    curve=Loop(tuple(cuts),start_up=True)
    if free_homotopy_key(loop_ray_word(6,curve))!=word:
        raise ValueError('Exact loop itinerary failed its boundary-word check')
    return curve


@lru_cache(maxsize=64)
def support_curve(twist):
    from .factorization_geometry import support_points
    from .mapping_classes import supported_class
    from .twist_simplify import simplify_twist
    if not twist.half:
        return loop_from_class(supported_class(twist))
    # Old saved explorations may retain long words. Use a verified shorter
    # representative for recovery without changing that saved factor record.
    proposal=simplify_twist(twist)
    pts=support_points(proposal.first,proposal.points,proposal.half,proposal.conjugator)
    nonzero=[p for p in pts if abs(p[1])>1e-8]
    cuts=[]
    if not nonzero:
        if not twist.half: raise ValueError('Cannot recover a closed itinerary on the axis')
        curve=Arc(round(pts[0][0])+1,round(pts[-1][0])+1)
    else:
        up=nonzero[0][1]>0
        pairs=zip(nonzero,nonzero[1:]) if twist.half else zip(nonzero,nonzero[1:]+nonzero[:1])
        for a,b in pairs:
            if (a[1]>0)==(b[1]>0): continue
            x=a[0]-a[1]*(b[0]-a[0])/(b[1]-a[1])
            if abs(x-round(x))<1e-8:
                raise ValueError('Support recovery meets a puncture; no itinerary asserted')
            cut=floor(x)+1
            if not 0<=cut<=6: raise ValueError('Recovered cut lies outside the marked disk')
            if not cuts and not twist.half: up=b[1]>0
            if cuts and cuts[-1]==cut: cuts.pop()
            else: cuts.append(cut)
        if twist.half:
            start,end=round(pts[0][0])+1,round(pts[-1][0])+1
            while cuts and cuts[0] in (start-1,start): cuts.pop(0); up=not up
            while cuts and cuts[-1] in (end-1,end): cuts.pop()
            curve=Arc(start,end,tuple(cuts),direction='up' if up else 'down')
        else:
            while len(cuts)>1 and cuts[0]==cuts[-1]: cuts=cuts[1:-1]; up=not up
            curve=Loop(tuple(cuts),start_up=up)
    if isinstance(curve,Arc):
        word=arc_ray_word(6,curve)
        observed=(curve.start,)+word+(curve.end,)+inverse_word(word)
    else: observed=loop_ray_word(6,curve)
    if free_homotopy_key(observed)!=supported_class(twist):
        raise ValueError('Recovered itinerary disagrees with the exact supported class')
    return curve



@lru_cache(maxsize=64)
def support_drawing(twist):
    curve=support_curve(twist)
    surface=PlanarSurface.row('PPPPPP',spacing=50,height=220,margin=55).with_curves(curve)
    return render_svg(surface,style=Style(curve_color='#a21caf',curve_width=1.5,marked_point_radius=3.5))
