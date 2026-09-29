"""Sampled planar representatives and aligned continuous braid for the lab.

Exact word algebra is separate. Curves are numerical representatives obtained
by compactly supported half rotations, not certified itinerary reconstruction.
"""
from functools import lru_cache
from math import sin,cos,pi,hypot,ceil
from .model import Style
from .visuals import _braid_paths, RAINBOW


def turn(point,letter):
    return regional_turn(point,abs(letter)-.5,.55,.95,-pi if letter>0 else pi)


def regional_turn(point,center,inner,outer,angle):
    x,y=point[0]-center,point[1]
    r=hypot(x,y)
    if r>=outer: return point
    t=max(0,min(1,(r-inner)/(outer-inner)))
    amount=1-t*t*(3-2*t)
    angle*=amount
    return center+x*cos(angle)-y*sin(angle),x*sin(angle)+y*cos(angle)


def geometric_blocks(word):
    """Recognize complete triple twists, avoiding needless geometric stretching."""
    blocks=[]; i=0
    while i<len(word):
        letter=word[i]; block=None
        if i+6<=len(word):
            pair=word[i:i+2]
            if pair[1]==pair[0]+1 and pair[0]>0 and word[i:i+6]==pair*3:
                block=(pair[0],1.05,1.45,-2*pi)
            elif pair[0]<-1 and pair[1]==pair[0]+1 and word[i:i+6]==pair*3:
                block=(-pair[1],1.05,1.45,2*pi)
        if block is not None:
            i+=6
            if blocks and blocks[-1][:3]==block[:3]:
                blocks[-1]=block[:3]+(blocks[-1][3]+block[3],)
            else: blocks.append(block)
        else:
            block=(abs(letter)-.5,.55,.95,-pi if letter>0 else pi)
            if blocks and blocks[-1][:3]==block[:3]:
                blocks[-1]=block[:3]+(blocks[-1][3]+block[3],)
            else: blocks.append(block)
            i+=1
    return blocks


def simplify(points,tolerance=.001):
    # Iterative Douglas-Peucker; fixed endpoint order and closed-loop endpoint.
    keep={0,len(points)-1}; pending=[(0,len(points)-1)]
    while pending:
        a,b=pending.pop()
        if b<=a+1: continue
        x,y=points[a]; dx=points[b][0]-x; dy=points[b][1]-y
        length=dx*dx+dy*dy
        best=-1; index=a
        for j in range(a+1,b):
            px,py=points[j]; t=max(0,min(1,((px-x)*dx+(py-y)*dy)/length)) if length else 0
            d=(px-x-t*dx)**2+(py-y-t*dy)**2
            if d>best: best,index=d,j
        if best>tolerance*tolerance:
            keep.add(index); pending.extend(((a,index),(index,b)))
    return tuple(points[i] for i in sorted(keep))


@lru_cache(maxsize=256)
def support_points(first,count,half,conjugator):
    if half:
        points=tuple((first-1+t/40,0.) for t in range(41))
    else:
        center=first-1+(count-1)/2
        rx=(count-1)/2+.27
        points=tuple((center+rx*cos(2*pi*t/100),.28*sin(2*pi*t/100)) for t in range(101))
    for block in reversed(geometric_blocks(conjugator)):
        dense=[]
        for a,b in zip(points,points[1:]):
            resolution=.02/(1+abs(block[3])/pi/4)
            steps=max(1,ceil(hypot(b[0]-a[0],b[1]-a[1])/resolution))
            for k in range(steps):
                t=k/steps
                dense.append(regional_turn((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])),*block))
                if len(dense)>200000:
                    raise ValueError('Support preview exceeded its sampling limit; exact braid is still available')
        dense.append(regional_turn(points[-1],*block))
        points=simplify(dense,.0015)
    return points


def support_svg(factor):
    points=support_points(factor.first,factor.points,factor.half,factor.conjugator)
    path='M '+' L '.join(f'{50+x*48:.3f} {88-y*48:.3f}' for x,y in points)
    dots=''.join(f'<circle cx="{50+i*48}" cy="88" r="3.5" fill="#1767cd"/><text x="{50+i*48}" y="106" text-anchor="middle" font-size="10" fill="#17416e">{i+1}</text>' for i in range(6))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176" role="img" aria-label="Numerical support representative"><ellipse cx="170" cy="88" rx="164" ry="84" fill="#fff" stroke="#475569"/><path d="{path}" fill="none" stroke="#a21caf" stroke-width="1.5" stroke-linejoin="round"/>{dots}</svg>'


def row_height(factor):
    return max(210, len(factor.word)*12+36)


def braid_svg(factors):
    levels=[0.]; letters=[]; boundaries=[]; offset=0
    for factor in factors:
        height=row_height(factor)
        letters.append(None); levels.append(-offset-18)
        for j,letter in enumerate(factor.word):
            letters.append(letter); levels.append(-offset-18-(j+1)*12)
        offset+=height
        letters.append(None); levels.append(-offset)
        boundaries.append(offset)
    paths,_=_braid_paths(6,letters,levels,28,RAINBOW,Style(curve_width=1.3),'smooth')
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="240" height="{offset}" viewBox="0 0 240 {offset}" role="img" aria-label="Continuous six-strand braid">']
    for path in paths:
        commands=[]
        for op,*values in path.commands:
            coords=[120+v if i%2==0 else -v for i,v in enumerate(values)]
            commands.append(op+' '+' '.join(f'{v:.3f}' for v in coords))
        svg.append(f'<path d="{" ".join(commands)}" stroke="{path.stroke}" stroke-width="1.3" fill="none"/>')
    for y in boundaries[:-1]:
        svg.append(f'<path d="M 12 {y} H 228" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="3 5"/>')
    svg.append('</svg>')
    return ''.join(svg)
