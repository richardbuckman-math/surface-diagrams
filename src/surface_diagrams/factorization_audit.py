"""Compare sampled support boundary words with exact transported curve classes.

Agreement checks free homotopy of a closed support (or the boundary of a
half-twist arc's neighborhood). It does not certify embeddedness, resolve
near-overlapping strands, or identify a drawing in the original PDF.
"""
from functools import lru_cache
from math import hypot
from .braid_actions import free_homotopy_key,inverse_word
from .factorization_explorer import exact_action
from .factorization_geometry import support_points


def polyline_ray_word(points,open_arc=False):
    """Read upward puncture rays at x=0,...,5 from the displayed polyline."""
    word=[]
    for segment,(a,b) in enumerate(zip(points,points[1:])):
        dx,dy=b[0]-a[0],b[1]-a[1]
        length2=dx*dx+dy*dy
        if not length2: continue
        for puncture in (range(6) if dx>=0 else range(5,-1,-1)):
            nearest=max(0.,min(1.,((puncture-a[0])*dx-a[1]*dy)/length2))
            distance=hypot(a[0]+nearest*dx-puncture,a[1]+nearest*dy)
            endpoint=open_arc and ((segment==0 and nearest==0.) or
                                   (segment==len(points)-2 and nearest==1.))
            if distance<1e-8 and not endpoint:
                raise ValueError('Displayed support touches a marked point away from its endpoints')
            if dx and min(a[0],b[0])<=puncture<max(a[0],b[0]):
                t=(puncture-a[0])/dx
                if a[1]+t*dy>1e-8:
                    letter=(puncture+1)*(1 if dx>0 else -1)
                    if word and word[-1]==-letter: word.pop()
                    else: word.append(letter)
    return tuple(word)


def audit_points(factor,points):
    # Use exactly the coordinate rounding in support_svg, not finer hidden data.
    points=tuple(((float(f'{50+x*48:.3f}')-50)/48,
                  (88-float(f'{88-y*48:.3f}'))/48) for x,y in points)
    try:
        if not factor.half and hypot(points[0][0]-points[-1][0],points[0][1]-points[-1][1])>1e-7:
            raise ValueError('Displayed closed support is not closed')
        observed=polyline_ray_word(points,factor.half)
        if factor.half:
            start,end=round(points[0][0])+1,round(points[-1][0])+1
            if not all(1<=j<=6 and hypot(p[0]-(j-1),p[1])<1e-7
                       for p,j in ((points[0],start),(points[-1],end))):
                raise ValueError('Displayed arc endpoints do not match marked points')
            observed=(start,)+observed+(end,)+inverse_word(observed)
        action=exact_action(factor.conjugator)
        expected=tuple(letter for i in range(factor.first-1,factor.first+factor.points-1) for letter in action[i])
        actual_key=free_homotopy_key(observed); expected_key=free_homotopy_key(expected)
        matches=actual_key==expected_key
        return dict(status='match' if matches else 'mismatch',matches=matches,
                    actual=actual_key,expected=expected_key,
                    message=('Sampled boundary word agrees with the exact transported class.' if matches else
                             'Sampled boundary word disagrees with the exact transported class; do not rely on this preview.'))
    except ValueError as error:
        return dict(status='unavailable',matches=None,actual=None,expected=None,message=str(error))


@lru_cache(maxsize=64)
def support_audit(factor):
    try: points=support_points(factor.first,factor.points,factor.half,factor.conjugator)
    except ValueError as error:
        return dict(status='unavailable',matches=None,actual=None,expected=None,message=str(error))
    return audit_points(factor,points)
