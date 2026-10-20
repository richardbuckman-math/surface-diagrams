"""Vector nets and occlusion-correct BSP views for the common-net experiment."""
from collections import defaultdict
import colorsys
from math import cos,sin,sqrt,pi


def color(index):
    from reportlab.lib.colors import Color
    return Color(*colorsys.hls_to_rgb(((index*137.508+205)%360)/360,.74,.59))


def net_drawing(net,width,height,kind='triangle'):
    from reportlab.graphics.shapes import Drawing,Polygon,Line,String
    from reportlab.lib.colors import HexColor
    drawing=Drawing(width,height)
    if kind=='triangle':
        cells=[list(map(tuple,t)) for t in net['triangles']]
        xy=lambda p:(p[0]+p[1]/2,p[1]*sqrt(3)/2)
    else:
        cells=[[(x,y),(x+1,y),(x+1,y+1),(x,y+1)] for x,y in net['cells']]
        xy=lambda p:p
    raw=[xy(p) for cell in cells for p in cell]
    low=[min(p[i] for p in raw) for i in (0,1)];high=[max(p[i] for p in raw) for i in (0,1)]
    scale=min((width-24)/(high[0]-low[0]),(height-24)/(high[1]-low[1]))
    ox=(width-(high[0]-low[0])*scale)/2;oy=(height-(high[1]-low[1])*scale)/2
    def point(p):
        x,y=xy(p);return (ox+(x-low[0])*scale,oy+(y-low[1])*scale)
    hinge_edges=set()
    for hinge in net['hinges']:
        parent,_,edge=hinge[:3];cell=cells[parent]
        hinge_edges.add(tuple(sorted((cell[edge],cell[(edge+1)%len(cell)]))))
    edges=defaultdict(int)
    for index,cell in enumerate(cells):
        ps=[point(p) for p in cell]
        drawing.add(Polygon([v for p in ps for v in p],fillColor=color(index),strokeColor=None))
        center=[sum(p[i] for p in ps)/len(ps) for i in (0,1)]
        drawing.add(String(center[0],center[1]-3,str(index+1),fontName='Helvetica',
                           fontSize=max(7,min(10,scale*.25)),textAnchor='middle',fillColor=HexColor('#17304b')))
        for i in range(len(cell)):edges[tuple(sorted((cell[i],cell[(i+1)%len(cell)])))]+=1
    slits=0
    for edge,count in edges.items():
        a,b=map(point,edge)
        if edge in hinge_edges:
            line=Line(*a,*b,strokeColor=HexColor('#1876b8'),strokeWidth=.7,strokeDashArray=[3,2])
        else:
            if count==2:slits+=1
            line=Line(*a,*b,strokeColor=HexColor('#cc382a' if count==2 else '#172c3f'),strokeWidth=1.05)
        drawing.add(line)
    drawing._slits=slits
    return drawing


def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def normal(poly):
    n=cross(sub(poly[1],poly[0]),sub(poly[2],poly[0]));size=sqrt(dot(n,n))
    return tuple(x/size for x in n)


def clip(poly,n,d,positive):
    result=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        da,db=dot(a,n)-d,dot(b,n)-d
        inside=da>=-1e-9 if positive else da<=1e-9
        other=db>=-1e-9 if positive else db<=1e-9
        if inside:result.append(a)
        if inside!=other:
            t=da/(da-db);result.append(tuple(a[i]+t*(b[i]-a[i]) for i in range(3)))
    clean=[]
    for p in result:
        if not clean or dot(sub(p,clean[-1]),sub(p,clean[-1]))>1e-18:clean.append(p)
    if len(clean)>1 and dot(sub(clean[0],clean[-1]),sub(clean[0],clean[-1]))<1e-18:clean.pop()
    changed=True
    while changed and len(clean)>3:
        changed=False
        for i in range(len(clean)):
            turn=cross(sub(clean[i],clean[i-1]),sub(clean[(i+1)%len(clean)],clean[i]))
            if dot(turn,turn)<1e-18:
                clean.pop(i);changed=True;break
    if len(clean)<3:return []
    turn=cross(sub(clean[1],clean[0]),sub(clean[2],clean[0]))
    return clean if dot(turn,turn)>1e-18 else []


def bsp(polygons):
    if not polygons:return None
    first=polygons[0];n=normal(first[0]);d=dot(n,first[0][0]);same=[first];front=[];back=[]
    for poly,original,index in polygons[1:]:
        distances=[dot(p,n)-d for p in poly]
        if max(distances)<=1e-8 and min(distances)>=-1e-8:same.append((poly,original,index))
        elif min(distances)>=-1e-8:front.append((poly,original,index))
        elif max(distances)<=1e-8:back.append((poly,original,index))
        else:
            for positive,bucket in [(True,front),(False,back)]:
                p=clip(poly,n,d,positive)
                if len(p)>=3:bucket.append((p,original,index))
    return (n,d,same,bsp(front),bsp(back))


def ordered(tree,view):
    if not tree:return []
    n,d,same,front,back=tree
    return (ordered(back,view)+same+ordered(front,view) if dot(n,view)>0
            else ordered(front,view)+same+ordered(back,view))


def on_edge(a,b,original):
    for p,q in zip(original,original[1:]+original[:1]):
        direction=sub(q,p);length=dot(direction,direction)
        def contains(v):
            delta=sub(v,p);c=cross(delta,direction)
            return dot(c,c)<1e-14 and -1e-8<=dot(delta,direction)<=length+1e-8
        if contains(a) and contains(b):return True
    return False


def shape_drawing(surface,mapping,width,height,yaw=35,elevation=25):
    from reportlab.graphics.shapes import Drawing,Polygon,Line
    from reportlab.lib.colors import Color,HexColor
    allpoints=[p for f in surface['faces'] for p in f]
    low=[min(p[i] for p in allpoints) for i in range(3)];high=[max(p[i] for p in allpoints) for i in range(3)]
    center=[(a+b)/2 for a,b in zip(low,high)];length=max(b-a for a,b in zip(low,high))
    faces=[[tuple((p[i]-center[i])/length for i in range(3)) for p in f] for f in surface['faces']]
    face_colors={m[0]:i for i,m in enumerate(mapping)} if mapping else {i:i for i in range(len(faces))}
    yaw*=pi/180;elevation*=pi/180
    view=(cos(yaw)*cos(elevation),sin(yaw)*cos(elevation),sin(elevation))
    u=(-sin(yaw),cos(yaw),0);v=(-cos(yaw)*sin(elevation),-sin(yaw)*sin(elevation),cos(elevation))
    projected=[(dot(p,u),dot(p,v)) for f in faces for p in f]
    lx,ly=min(p[0] for p in projected),min(p[1] for p in projected)
    hx,hy=max(p[0] for p in projected),max(p[1] for p in projected)
    scale=min((width-16)/(hx-lx),(height-16)/(hy-ly))
    ox=(width-(hx-lx)*scale)/2;oy=(height-(hy-ly)*scale)/2
    def xy(p):return (ox+(dot(p,u)-lx)*scale,oy+(dot(p,v)-ly)*scale)
    visible=[(f,f,i) for i,f in enumerate(faces) if dot(normal(f),view)>1e-7]
    tree=bsp(visible);drawing=Drawing(width,height)
    light=(.35,-.15,.92)
    for poly,original,index in ordered(tree,view):
        n=normal(original);base=color(face_colors[index]);shade=.76+.24*max(0,dot(n,light))
        shade_color=Color(base.red*shade,base.green*shade,base.blue*shade)
        ps=[xy(p) for p in poly]
        drawing.add(Polygon([q for p in ps for q in p],fillColor=shade_color,
                            strokeColor=shade_color,strokeWidth=.25))
        for a,b in zip(poly,poly[1:]+poly[:1]):
            if on_edge(a,b,original):drawing.add(Line(*xy(a),*xy(b),strokeColor=HexColor('#35475b'),strokeWidth=.55))
    return drawing
