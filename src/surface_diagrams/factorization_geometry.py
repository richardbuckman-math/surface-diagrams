"""Sampled planar representatives and aligned continuous braid for the lab.

Exact word algebra is separate. Curves are numerical representatives obtained
by compactly supported half rotations, not certified itinerary reconstruction.
"""
from functools import lru_cache
from html import escape
from math import sin,cos,pi,hypot,ceil,sqrt
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


def deform_polyline(points,block):
    """Sample only portions inside the moving disk; its exterior is fixed.

    Intersect each chord with the disk before sampling. Long, complicated
    portions outside this particular twist need no new vertices at all.
    This remains a numerical polyline preview, not a topological certificate.
    """
    center,inner,outer,angle=block
    dense=[]; chunks=[]; samples=0
    resolution=.02/(1+abs(angle)/pi/4)
    for a,b in zip(points,points[1:]):
        dense.append(regional_turn(a,*block))
        dx,dy=b[0]-a[0],b[1]-a[1]
        length2=dx*dx+dy*dy
        if not length2: continue
        projection=-((a[0]-center)*dx+a[1]*dy)/length2
        distance2=(a[0]-center+projection*dx)**2+(a[1]+projection*dy)**2
        if distance2>=outer*outer: continue
        radius=sqrt((outer*outer-distance2)/length2)
        lo,hi=max(0.,projection-radius),min(1.,projection+radius)
        if hi<=lo: continue
        steps=max(1,ceil((hi-lo)*sqrt(length2)/resolution))
        for k in range(steps+1):
            t=lo+(hi-lo)*k/steps
            if 0<t<1:
                dense.append(regional_turn((a[0]+t*dx,a[1]+t*dy),*block))
        samples+=steps+1
        if len(dense)>12000:
            reduced=simplify(dense,.0015)
            chunks.extend(reduced[:-1]); dense=[reduced[-1]]
        if len(chunks)>200000 or samples>2000000:
            raise ValueError('Support preview exceeded its sampling limit; exact braid is still available')
    dense.append(regional_turn(points[-1],*block))
    chunks.extend(simplify(dense,.0015))
    # Chunk boundaries remain vertices: do not compound simplification error.
    return tuple(chunks)


@lru_cache(maxsize=256)
def support_points(first,count,half,conjugator):
    if half:
        points=tuple((first-1+t/40,0.) for t in range(41))
    else:
        center=first-1+(count-1)/2
        rx=(count-1)/2+.27
        points=tuple((center+rx*cos(2*pi*t/100),.28*sin(2*pi*t/100)) for t in range(101))
    for block in reversed(geometric_blocks(conjugator)):
        points=deform_polyline(points,block)
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


def factorization_svg(factors):
    """Portable paired export, retaining numerical-preview labels and failures."""
    height=sum(row_height(f) for f in factors)
    body=[]; y=0
    for f in factors:
        label=f'{f.id} · {f.label}'
        body.append(f'<g transform="translate(0 {y})"><title>{escape(label)}</title>'
                    f'<text x="12" y="20" font-family="sans-serif" font-size="12">{escape(label[:52])}</text>')
        try:
            svg=support_svg(f).replace('<svg ','<svg width="340" height="176" ',1)
            body.append(f'<g transform="translate(0 30)">{svg}</g>')
        except ValueError as error:
            body.append(f'<desc>{escape(str(error))}</desc><text x="12" y="80" fill="#a14b20" '
                        'font-family="sans-serif" font-size="12">Support preview unavailable.</text>'
                        '<text x="12" y="100" font-family="sans-serif" font-size="12">Exact braid remains in the right column.</text>')
        body.append('</g>'); y+=row_height(f)
    body.append(f'<g transform="translate(360 0)">{braid_svg(factors)}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="620" height="{height+28}" viewBox="0 0 620 {height+28}">'
            '<title>Factorization Lab paired export</title><rect width="100%" height="100%" fill="white"/>'
            '<text x="12" y="18" font-family="sans-serif" font-size="12" fill="#526880">'
            'Numerical support previews · exact braid words</text><g transform="translate(0 28)">'
            +''.join(body)+'</g></svg>')
