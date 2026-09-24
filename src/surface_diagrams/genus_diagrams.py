"""Default-genus drawings carrying curves through a checked presentation mesh."""
from dataclasses import dataclass

from .genus_geometry import presentation
from .genus_mesh import genus_binding
from .mesh_atlas import cubic_point, _near, _segment_distance
from .primitives import Drawing, Path, Text, Ellipse
from .visuals import RAINBOW
from .disk_routes import DiskRoute, ItineraryError


@dataclass(frozen=True)
class BorderedReferenceDiagram:
    """Supplied closed curves and rim-to-rim perimeter reference arcs.

    This presentation is independent of the certified closed-surface mesh;
    it is not accepted as a CutSystem or as a DiskRoute chart binding.
    """
    surface: object
    pair_bank: str = "a"
    mark_positions: tuple = ()
    selection: tuple = None
    curves: tuple = ()
    show_reference_labels: bool = True
    allow_intersections: bool = False
    closed_curve_style: str = "solid"

    def with_curves(self, *curves, allow_intersections=None):
        """Add supplied straight MarkedArcs within a clear upper or lower band.

        Set allow_intersections=True for transverse crossings without over/under
        information. Overlapping segments and intervening marks remain invalid.
        Reference members are guides, not obstacles. This does not construct
        a cut-disk itinerary or certify a mapping-class action.
        """
        from dataclasses import replace
        if any(not isinstance(curve, MarkedArc) for curve in curves):
            raise TypeError('bordered supplied curves must be MarkedArc objects')
        if allow_intersections is None:
            allow_intersections = self.allow_intersections
        if type(allow_intersections) is not bool:
            raise TypeError('allow_intersections must be a boolean')
        return replace(self, curves=self.curves+tuple(curves),
                       allow_intersections=allow_intersections)

    def with_labels(self, *, reference=True):
        """Show or hide reference numbers while retaining marked-point names."""
        from dataclasses import replace
        if type(reference) is not bool:
            raise TypeError('reference must be a boolean')
        return replace(self, show_reference_labels=reference)

    @property
    def member_numbers(self):
        last=2*self.surface.genus+2
        outer=sum(b.slot in (1,last) for b in self.surface.type_i)+2*len(self.surface.type_ii)
        return tuple(range(1,last+outer+len(self.surface.marks)))

    def select(self, *numbers):
        """Isolate numbered members without rerouting or reassigning colors."""
        from dataclasses import replace
        if any(type(n) is not int or n not in self.member_numbers for n in numbers):
            raise ValueError('selected reference member number is outside this family')
        if len(set(numbers))!=len(numbers):
            raise ValueError('selected reference member numbers must be distinct')
        return replace(self,selection=tuple(numbers))

    def drawing(self, style):
        from dataclasses import replace
        surface=self.surface
        last=2*surface.genus+2
        side_pairs=[pair.side for pair in surface.type_ii if pair.side in ('left','right')]
        if len(side_pairs)!=len(set(side_pairs)):
            raise NotImplementedError('one Type II pair per side is currently supported')
        if any((fixed.slot==1 and 'left' in side_pairs) or (fixed.slot==last and 'right' in side_pairs)
               for fixed in surface.type_i):
            raise NotImplementedError('a Type I rim and Type II pair on the same end need separate binding')
        if self.pair_bank not in ('a','b'):
            raise ValueError("pair_bank must be 'a' or 'b'")
        positions=dict(self.mark_positions)
        if positions and set(positions)!=set(surface.marks):
            raise ValueError('provide mark_positions for exactly the surface mark IDs')
        outline=presentation(surface)
        base=outline.drawing(style)
        paths,texts=list(base.paths),[]
        rims={rim.id:rim for rim in outline.rims}
        vy=1 if surface.view_vertical=='above' else -1

        def endpoint(slot, bank):
            if f'fixed-{slot}' in rims:
                rim=rims[f'fixed-{slot}']
                return rim.point(0, rim.depth*(-1 if bank=='a' else 1))
            if slot in (1,last):
                tips=[path[0][1:] for path in outline.contours if abs(path[0][2])<1e-9]
                tips += [command[-2:] for path in outline.contours for command in path[1:]
                         if abs(command[-1])<1e-9]
                x,y=min(tips) if slot==1 else max(tips)
                # Leave stroke clearance at the silhouette's turning point.
                clearance=0 if self.closed_curve_style=='split' else (style.outline_width+style.curve_width)/2+.25
                return x+(1 if slot==1 else -1)*clearance,y
            hole=(slot-2)//2
            far=outline.handles[2*hole+1]
            return far[0][1:] if slot%2==0 else far[-1][-2:]

        members={}
        member_labels={}
        mark_labels=[]
        for number in range(1,2*surface.genus+2):
            begin=len(paths)
            label_begin=len(texts)
            color=RAINBOW[(number-1)%len(RAINBOW)]
            if number%2:
                # The corridor member joins consecutive vertical-plane slots.
                bordered=any(f'fixed-{slot}' in rims for slot in (number,number+1))
                for sign,bank in ((-vy,'a' if vy>0 else 'b'),(vy,'b' if vy>0 else 'a')):
                    start,end=endpoint(number,bank),endpoint(number+1,bank)
                    width=end[0]-start[0]
                    lift=sign*min(surface.height*.12,abs(width)*.32)
                    commands=(('M',*start),('C',start[0]+width/3,start[1]+lift,
                                end[0]-width/3,end[1]+lift,*end))
                    paths.append(Path(commands,color,style.curve_width,
                                      'boundary-reference-arc' if bordered else 'named-cut',
                                      sign==vy and (bordered or self.closed_curve_style=='split')))
                texts.append(Text((start[0]+end[0])/2,(start[1]+end[1])/2+4*vy,
                                  str(number),color,10))
            elif any(f'fixed-{slot}' in rims for slot in (number,number+1)):
                # An opened cusp is wider than the old cusp. A small rounded
                # rectangle encloses the actual hole/rim control hulls with a
                # uniform gap, rather than cutting through an opened rim.
                hole=number//2-1
                controls=[tuple(cmd[i:i+2]) for path in outline.handles[2*hole:2*hole+2]
                          for cmd in path for i in range(1,len(cmd),2)]
                xs=[p[0] for p in controls]; ys=[p[1] for p in controls]
                for slot in (number,number+1):
                    rim=rims.get(f'fixed-{slot}')
                    if rim:
                        xs.extend((rim.x-rim.depth,rim.x+rim.depth))
                        ys.extend((-rim.radius,rim.radius))
                gap=surface.handle_spacing*.035
                points=_rounded_enclosure(min(xs),max(xs),min(ys),max(ys),gap)
                pieces=(('front',points),)
                _append_paths(paths,pieces,color,style.curve_width,'named-cut')
                texts.append(Text((min(xs)+max(xs))/2,max(ys)+gap+9,str(number),color,10))
            else:
                center=(number//2-1-(surface.genus-1)/2)*surface.handle_spacing
                radius=surface.handle_spacing*.335
                ry=min(surface.height*.17,surface.handle_spacing*.17)
                points=_ellipse_reference(center,radius,ry)
                pieces=(('front',points),)
                _append_paths(paths,pieces,color,style.curve_width,'named-cut')
                texts.append(Text(center,ry+9,str(number),color,10))
            members[number]=tuple(paths[begin:])
            member_labels[number]=tuple(texts[label_begin:])
        perimeter, positions = _reference_perimeter(outline, surface, positions, style)
        ellipses=list(base.ellipses)
        for index, points in enumerate(perimeter):
            number=last+index
            color=RAINBOW[(number-1)%len(RAINBOW)]
            path=Path((('M',*points[0]),)+tuple(('L',*p) for p in points[1:]),
                      color,style.curve_width,'boundary-reference-perimeter')
            paths.append(path)
            x,y=points[len(points)//2]
            label=Text(x,y+(-9 if y>=0 else 9),str(number),color,9)
            texts.append(label)
            members[number]=(path,)
            member_labels[number]=(label,)
        for name in surface.marks:
            x,y=positions[name]
            radius=style.marked_point_radius
            ellipses.append(Ellipse(x,y,radius,radius,style.marked_point_color,'none',0,'marked-point'))
            mark_labels.append(Text(x+8,y-10 if abs(y)<1e-8 else y+3,name,style.marked_point_color,9))
        texts.extend(mark_labels)
        if self.selection is not None:
            if any(number not in members for number in self.selection):
                raise ValueError('selected reference member is not available')
            paths=list(base.paths)+[path for number in self.selection for path in members[number]]
            texts=mark_labels+[label for number in self.selection for label in member_labels[number]]
        if not self.show_reference_labels:
            texts=mark_labels
        if self.curves:
            # Straight supplied segments need a convex surface band; endpoint
            # containment alone cannot rule out crossing a genus opening.
            hole_height=max(abs(v) for h in outline.handles for c in h for v in c[2::2])
            hole_height=max([hole_height]+[r.radius for r in outline.rims
                            if r.role=='type-i-boundary' and r.id not in ('fixed-1',f'fixed-{last}')])
            clearance=max(style.marked_point_radius,style.curve_width/2)
            used={name for curve in self.curves for name in (curve.start,curve.end)}
            for name in used & positions.keys():
                x,y=positions[name]
                if not (abs(x)<surface.genus*surface.handle_spacing/2-clearance
                        and hole_height+clearance<abs(y)<surface.height*.44*.99-clearance):
                    raise ItineraryError('straight marked arc needs a clear upper or lower band')
        paths.extend(_bordered_marked_arcs(self.curves, positions, style, self.allow_intersections))
        return replace(base,paths=tuple(paths),texts=tuple(texts),ellipses=tuple(ellipses))


    def _repr_svg_(self):
        from .svg import render_svg
        return render_svg(self)


def _reference_perimeter(outline, surface, positions, style):
    """Follow the actual outer contour, stopping only at rims and marks.

    The inward offset preserves the necks and concave side recesses. Using the
    contour graph, rather than spokes to the chain, also joins the two halves
    of a side-pair arc across the symmetry axis.
    """
    from math import hypot
    from .model import _number
    supplied_positions=bool(positions)
    last=2*surface.genus+2
    rims=[r for r in outline.rims if r.role=='type-ii-boundary' or r.id in ('fixed-1',f'fixed-{last}')]
    if not rims and not surface.marks:
        return (), {}
    anchors=[p for r in rims for p in r.anchors]
    def samples(commands):
        result=[commands[0][1:]]
        for cmd in commands[1:]:
            if cmd[0]=='C':
                curve=(result[-1],cmd[1:3],cmd[3:5],cmd[5:7])
                result.extend(cubic_point(curve,i/32) for i in range(1,33))
            else:
                result.append(cmd[-2:])
        return result
    chunks=[samples(c) for c in outline.contours]
    edges=[(a,b) for chunk in chunks for a,b in zip(chunk,chunk[1:])]
    edges.extend(r.anchors for r in rims)
    def inside(p):
        x,y=p
        return sum((a[1]>y)!=(b[1]>y) and
                   a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1])>x
                   for a,b in edges)%2==1
    # Assemble through ordinary contour joins; rims terminate an arc.
    chains=[]
    while chunks:
        chain=chunks.pop(0)
        changed=True
        while changed:
            changed=False
            for reverse in (False,True):
                if reverse: chain.reverse()
                if not any(_near(chain[-1],a) for a in anchors):
                    for i,chunk in enumerate(chunks):
                        if _near(chain[-1],chunk[-1]): chunk=list(reversed(chunk))
                        if _near(chain[-1],chunk[0]):
                            chain.extend(chunk[1:]); chunks.pop(i); changed=True; break
                if reverse: chain.reverse()
        chains.append(chain)
    inset=(style.outline_width+style.curve_width)/2+5
    offset=[]
    for chain in chains:
        result=[]
        closed=_near(chain[0],chain[-1])
        for i,p in enumerate(chain):
            if any(_near(p,a) for a in anchors):
                result.append(p); continue
            a,b=(chain[-2],chain[1]) if closed and i in (0,len(chain)-1) else (chain[max(0,i-1)],chain[min(len(chain)-1,i+1)])
            dx,dy=b[0]-a[0],b[1]-a[1]
            length=hypot(dx,dy)
            normal=(-dy/length,dx/length)
            # Taper only near the actual rim endpoint, never near a join.
            gap=min([inset]+[hypot(p[0]-q[0],p[1]-q[1])*.35 for q in anchors])
            candidates=[(p[0]+sign*gap*normal[0],p[1]+sign*gap*normal[1]) for sign in (1,-1)]
            result.append(next((q for q in candidates if inside(q)),p))
        offset.append(result)
    # Deterministic traversal and numbering independent of the viewing tilt.
    chains=sorted(offset,key=lambda pts:(min(p[0] for p in pts),-sum(p[1] for p in pts)/len(pts)))
    if not positions:
        positions={}
        available=[p for chain in chains for p in chain[1:-1]]
        names=list(surface.marks)
        if len(names)%2:
            # The left end of the horizontal slice, slightly inside the edge.
            candidates=[p for p in available if abs(p[1])<1e-7]
            if not candidates:
                raise ItineraryError('automatic axial mark needs an unoccupied end; supply mark_positions')
            positions[names.pop(0)]=min(candidates)
        pairs=len(names)//2
        for i in range(pairs):
            target=(i-(pairs-1)/2)*surface.handle_spacing
            upper=min((p for p in available if p[1]>surface.height*.2),key=lambda p:abs(p[0]-target))
            positions[names[2*i]]=upper
            positions[names[2*i+1]]=(upper[0],-upper[1])
    for name,p in positions.items():
        if len(p)!=2: raise ValueError('mark position must contain x and y')
        for value in p: _number(value,'mark coordinate')
        if not inside(p): raise ItineraryError('marked point must lie inside the surface outline')
        for other,q in positions.items():
            if name!=other and hypot(p[0]-q[0],p[1]-q[1])<=2*style.marked_point_radius:
                raise ItineraryError('marked points overlap; separate their positions')
        # Reject points inside the displayed genus openings.
        for i in range(surface.genus):
            near,far=map(samples,outline.handles[2*i:2*i+2])
            polygon=near+list(reversed(far))
            x,y=p
            if sum((a[1]>y)!=(b[1]>y) and a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1])>x
                   for a,b in zip(polygon,polygon[1:]+polygon[:1]))%2:
                raise ItineraryError('marked point lies in a genus opening')
    assignments={i:[] for i in range(len(chains))}
    for name,p in positions.items():
        _,ci,pi=min((hypot(p[0]-q[0],p[1]-q[1]),ci,pi)
                    for ci,chain in enumerate(chains) for pi,q in enumerate(chain[1:-1],1))
        assignments[ci].append((pi,name,p))
    result=[]
    # Perimeter arcs are solid surface paths. A legal marked endpoint alone
    # does not guarantee that deforming the path to it avoids a handle opening.
    handle_edges=[edge for commands in outline.handles for edge in _path_segments(commands)]
    from .disk_routes import _orient
    for ci,chain in enumerate(chains):
        marks=sorted(assignments[ci])
        # Explicit coordinates deform the local perimeter smoothly instead of
        # adding a spur which ends on another curve. Marks split the arc itself.
        if len({pi for pi,_,_ in marks})!=len(marks):
            raise ItineraryError('marks project to the same perimeter location; separate their positions')
        controls=[(0,(0,0))]+[(pi,(p[0]-chain[pi][0],p[1]-chain[pi][1])) for pi,_,p in marks]+[(len(chain)-1,(0,0))]
        original=list(chain)
        for (a,da),(b,db) in zip(controls,controls[1:]):
            for j in range(a,b+1):
                t=(j-a)/(b-a); t=t*t*(3-2*t)
                chain[j]=tuple(original[j][k]+(1-t)*da[k]+t*db[k] for k in (0,1))
        for pi,_,p in marks: chain[pi]=p
        if any(not inside(p) for p in chain[1:-1]):
            raise ItineraryError('marked perimeter arc leaves the surface; change mark_positions')
        if marks and supplied_positions:
            for a,b in zip(chain,chain[1:]):
                for c,d,error in handle_edges:
                    margin=error+style.curve_width/2
                    if any(max(a[k],b[k])+margin<min(c[k],d[k]) or
                           max(c[k],d[k])+margin<min(a[k],b[k]) for k in (0,1)):
                        continue
                    o=(_orient(a,b,c),_orient(a,b,d),_orient(c,d,a),_orient(c,d,b))
                    crossing=o[0]*o[1]<0 and o[2]*o[3]<0
                    distance=min(_segment_distance(a,c,d),_segment_distance(b,c,d),
                                 _segment_distance(c,a,b),_segment_distance(d,a,b))
                    if crossing or distance<=margin:
                        raise ItineraryError('marked perimeter arc meets a genus opening; change mark_positions')
        splits=[0]+[pi for pi,_,_ in marks]+[len(chain)-1]
        pieces=[chain[a:b+1] for a,b in zip(splits,splits[1:])]
        if _near(chain[0],chain[-1]) and marks:
            pieces=[pieces[-1]+pieces[0][1:]]+pieces[1:-1]
        result.extend(pieces)
    return tuple(result),positions


def _bordered_marked_arcs(arcs, positions, style, allow_intersections=False):
    """Both endpoints lie in the already-checked convex mark bands."""
    from .disk_routes import _orient
    if any(not isinstance(arc, MarkedArc) for arc in arcs):
        raise TypeError('bordered supplied curves must be MarkedArc objects')
    if len({arc.id for arc in arcs}) != len(arcs):
        raise ValueError('marked arc IDs must be distinct')
    segments, paths = [], []
    for arc in arcs:
        if arc.start not in positions or arc.end not in positions:
            raise ValueError('unknown marked arc endpoint')
        a,b=positions[arc.start],positions[arc.end]
        if a[1]*b[1] <= 0:
            raise ItineraryError('bordered marked arc endpoints must lie in the same upper or lower band')
        # Mark placement is checked with reference-curve clearance; wider route
        # strokes also need clearance from the band's edges. Reuse the existing
        # position constraints rather than extrapolating across holes.
        for name,point in positions.items():
            if name not in (arc.start,arc.end) and _segment_distance(point,a,b)<=style.marked_point_radius+style.curve_width/2:
                raise ItineraryError('straight marked arc meets another mark; use consecutive marks')
        for c,d in segments:
            o=(_orient(a,b,c),_orient(a,b,d),_orient(c,d,a),_orient(c,d,b))
            if not allow_intersections and o[0]*o[1]<-1e-10 and o[2]*o[3]<-1e-10:
                raise ItineraryError('supplied bordered marked arcs intersect; set allow_intersections=True for an overlay')
            if max(abs(v) for v in o)<1e-8:
                axis=0 if abs(b[0]-a[0])>=abs(b[1]-a[1]) else 1
                if min(max(a[axis],b[axis]),max(c[axis],d[axis]))-max(min(a[axis],b[axis]),min(c[axis],d[axis]))>1e-8:
                    raise ItineraryError('supplied bordered marked arcs overlap')
        segments.append((a,b))
        paths.append(Path((('M',*a),('L',*b)),arc.color if arc.color is not None else style.curve_color,style.curve_width,'surface-route'))
    return paths


def _path_segments(commands):
    """Line approximation with a conservative cubic interpolation error bound."""
    from math import hypot
    point=None
    for command in commands:
        if command[0]=='M': point=command[1:]; continue
        end=command[-2:]
        if command[0]=='L':
            yield point,end,0.
        elif command[0]=='C':
            curve=(point,command[1:3],command[3:5],end)
            bound=6*max(hypot(*(curve[i+2][j]-2*curve[i+1][j]+curve[i][j] for j in (0,1))) for i in (0,1))
            previous=point
            for i in range(1,33):
                current=cubic_point(curve,i/32)
                yield previous,current,bound/(8*32**2)
                previous=current
        else:
            raise ItineraryError('unsupported reference geometry')
        point=end


def _ellipse_reference(center,rx,ry):
    """The standard even wrap, sampled from its four cubic quarters."""
    k=.5522847498307936
    quarters=(((rx,0),(rx,k*ry),(k*rx,ry),(0,ry)),
              ((0,ry),(-k*rx,ry),(-rx,k*ry),(-rx,0)),
              ((-rx,0),(-rx,-k*ry),(-k*rx,-ry),(0,-ry)),
              ((0,-ry),(k*rx,-ry),(rx,-k*ry),(rx,0)))
    points=[]
    for quarter in quarters:
        for i in range(25):
            x,y=cubic_point(quarter,i/24)
            points.append((center+x,y))
    return tuple(points)


def _vertical_hits(commands,x):
    """Exact line hits and bisected monotone cubic hits, retaining actual paths."""
    point=None
    for command in commands:
        if command[0]=='M':
            point=command[1:]
            continue
        end=command[-2:]
        if min(point[0],end[0])-1e-9 <= x <= max(point[0],end[0])+1e-9:
            if abs(end[0]-point[0])<1e-10:
                if abs(x-point[0])<1e-9:
                    yield point
                    yield end
            elif command[0]=='L':
                t=(x-point[0])/(end[0]-point[0])
                yield (x,point[1]+t*(end[1]-point[1]))
            elif command[0]=='C':
                curve=(point,command[1:3],command[3:5],end)
                low,high=0.,1.
                increasing=end[0]>point[0]
                for _ in range(48):
                    mid=(low+high)/2
                    if (cubic_point(curve,mid)[0]<x)==increasing: low=mid
                    else: high=mid
                yield cubic_point(curve,(low+high)/2)
            else:
                raise ItineraryError('unsupported reference-spoke target geometry')
        point=end


def _rounded_enclosure(left,right,bottom,top,gap):
    """Polyline of a rounded offset box; the supplied hull stays inside it."""
    from math import cos,sin,pi
    points=[]
    for cx,cy,angle in ((right,top,0),(left,top,90),(left,bottom,180),(right,bottom,270)):
        for i in range(13):
            t=(angle+90*i/12)*pi/180
            points.append((cx+gap*cos(t),cy+gap*sin(t)))
    points.append(points[0])
    return tuple(points)


@dataclass(frozen=True)
class BoundaryGuide:
    """A visual inventory of actual vertical-plane rim attachments."""
    surface: object

    def drawing(self, style):
        from dataclasses import replace
        from .visuals import _shift
        if self.surface.marks:
            raise NotImplementedError('bordered marked-point plane bindings are not implemented yet')
        outline=presentation(self.surface)
        base=outline.drawing(style)
        if not outline.rims:
            return base
        rows=len(outline.rims)
        extra=20*rows+18
        moved=_shift(base,0,extra/2)
        ellipses,texts=list(moved.ellipses),list(moved.texts)
        for i,rim in enumerate(outline.rims,1):
            color=RAINBOW[(i-1)%len(RAINBOW)]
            for bank,point,direction in zip(('a','b'),rim.anchors,(-1,1)):
                x,y=point
                ellipses.append(Ellipse(x,y+extra/2,2,2,color,'none',0,'boundary-anchor'))
                texts.append(Text(x+direction*10*rim.tangent[0]+8*rim.normal[0],
                                  y+extra/2+direction*10*rim.tangent[1]+8*rim.normal[1]-3,
                                  str(i)+bank,color,8))
            y=-base.height/2+extra/2-20*i
            texts.append(Text(0,y,f'{i} = {rim.id}   (a / b)',color,10))
        width=max(base.width,max(len(r.id) for r in outline.rims)*8+120)
        return replace(moved,width=width,height=base.height+extra,
                       ellipses=tuple(ellipses),texts=tuple(texts))

    def _repr_svg_(self):
        from .svg import render_svg
        return render_svg(self)


@dataclass(frozen=True)
class NamedCut:
    number: int

    def __post_init__(self):
        if type(self.number) is not int or self.number < 1:
            raise ValueError('named cut number must be a positive integer')


@dataclass(frozen=True)
class MarkedArc:
    """A straight visual arc between genus marks in a clear surface band.

    This is a supplied presentation arc, not a cut-disk itinerary. DiskRoute
    remains available when a particular winding/crossing sequence is required.
    Closed surfaces use automatic upper-band marks; bordered reference families
    accept explicit upper or lower marks, with each arc confined to one band.
    """
    start: str
    end: str
    id: str = None
    color: str = None

    def __post_init__(self):
        if self.color is not None:
            from .model import Style
            Style(curve_color=self.color)
        if self.id is None:
            object.__setattr__(self,'id',f'{self.start}-{self.end}')
        if any(not isinstance(s,str) or not s for s in (self.start,self.end,self.id)):
            raise ValueError('mark names and arc ID must be nonempty strings')
        if self.start == self.end:
            raise ValueError('a marked arc needs distinct endpoints')


@dataclass(frozen=True)
class GenusDiagram:
    surface: object
    curves: tuple = ()
    show_cuts: bool = False
    intersections: tuple = ()
    closed_curve_style: str = "solid"

    def __post_init__(self):
        if self.closed_curve_style not in ('solid','split'):
            raise ValueError("closed_curve_style must be 'solid' or 'split'")

    def with_curves(self, *curves, intersections=()):
        from dataclasses import replace
        return replace(self,curves=self.curves+tuple(curves),
                       intersections=self.intersections+tuple(intersections))

    def drawing(self, style):
        binding=genus_binding(self.surface)
        atlas,_=binding.charts()
        base=presentation(self.surface).drawing(style)
        paths,texts=list(base.paths),list(base.texts)
        ellipses=list(base.ellipses)
        parents={p.number:p for p in binding.system.cellulation.parents}
        numbers=list(parents) if self.show_cuts else []
        for curve in self.curves:
            if isinstance(curve,NamedCut):
                if curve.number not in parents:
                    raise ValueError('named cut number is outside the standard system')
                if curve.number not in numbers:
                    numbers.append(curve.number)
            elif not isinstance(curve,(DiskRoute,MarkedArc)):
                raise TypeError('genus curves must be NamedCut, MarkedArc or DiskRoute objects')
        geometry={t.face:t for t in binding.triangles}
        side_map={s:(geometry[f.id],i) for f in binding.system.cellulation.faces for i,s in enumerate(f.sides)}
        mark_points={}
        for mark in binding.system.cellulation.marks:
            triangle,index=side_map[mark.corner]
            x,y=triangle.points[index]
            mark_points[mark.id]=(x,y)
            ellipses.append(Ellipse(x,y,style.marked_point_radius,style.marked_point_radius,
                                    style.marked_point_color,style.marked_point_color,0,'marked-point'))
            texts.append(Text(x+7,y+2,mark.id,style.marked_point_color,9))
        for number in numbers:
            parent=parents[number]
            color=RAINBOW[(number-1)%len(RAINBOW)] if self.show_cuts else style.curve_color
            pieces=[]
            for side in parent.walk:
                triangle,i=side_map[side]
                pts=(triangle.points[i],triangle.points[(i+1)%3])
                if i==0 and triangle.curved:
                    pts=tuple(cubic_point(triangle.curved,t/12) for t in range(13))
                pieces.append((triangle.sheet,pts))
            # Styling must not change the mesh walk or invent visibility
            # transitions on enclosing loops which never reach a silhouette.
            displayed=pieces
            if parent.kind=='closed' and (number%2==0 or self.closed_curve_style=='solid'):
                displayed=[('front',pts) for _,pts in pieces]
            _append_paths(paths,displayed,color,style.curve_width,'named-cut')
            if self.show_cuts:
                front=[p for sheet,pts in pieces if sheet=='front' for p in pts]
                if parent.kind == 'arc':
                    x,y=front[len(front)//2]
                    x+=9
                    y-=5
                elif number%2:
                    x,y=front[len(front)//2]
                    y+=9*(1 if self.surface.view_vertical=='above' else -1)
                else:
                    x,y=max(front,key=lambda p:p[1])
                    y+=9
                texts.append(Text(x,y,str(number),color,10))
        marked_arcs=tuple(c for c in self.curves if isinstance(c,MarkedArc))
        routes=tuple(c for c in self.curves if isinstance(c,DiskRoute))
        if marked_arcs and (routes or self.intersections):
            raise ItineraryError('use separate panels for visual MarkedArc and explicit DiskRoute families')
        if len({a.id for a in marked_arcs}) != len(marked_arcs):
            raise ValueError('marked arc IDs must be distinct')
        # Every allowed straight segment lies in this convex rectangle, which
        # is above all hole control hulls and below the flat body's top contour.
        outline=presentation(self.surface)
        hole_top=max(v for c in outline.handles for command in c for v in command[2::2])
        upper=self.surface.height*.44*.99
        drawn_arcs=[]
        for arc in marked_arcs:
            if arc.start not in mark_points or arc.end not in mark_points:
                raise ValueError('unknown marked arc endpoint')
            a,b=mark_points[arc.start],mark_points[arc.end]
            if not all(abs(x)<self.surface.genus*self.surface.handle_spacing/2
                       and hole_top+style.curve_width/2<y<upper-style.curve_width/2 for x,y in (a,b)):
                raise ItineraryError('straight marked arc needs a clear upper corridor; use an explicit DiskRoute')
            for name,point in mark_points.items():
                if name not in (arc.start,arc.end) and _segment_distance(point,a,b)<=style.marked_point_radius+style.curve_width/2:
                    raise ItineraryError('straight marked arc meets another mark; use consecutive marks or an explicit DiskRoute')
            from .disk_routes import _orient
            for c,d in drawn_arcs:
                orientations=(_orient(a,b,c),_orient(a,b,d),_orient(c,d,a),_orient(c,d,b))
                if orientations[0]*orientations[1]<-1e-10 and orientations[2]*orientations[3]<-1e-10:
                    raise ItineraryError('straight marked arcs intersect; use explicit DiskRoutes for declared intersections')
                if max(abs(v) for v in orientations)<1e-8:
                    axis=0 if abs(b[0]-a[0])>=abs(b[1]-a[1]) else 1
                    lo=max(min(a[axis],b[axis]),min(c[axis],d[axis]))
                    hi=min(max(a[axis],b[axis]),max(c[axis],d[axis]))
                    if hi-lo>1e-8:
                        raise ItineraryError('straight marked arcs overlap')
            drawn_arcs.append((a,b))
            paths.append(Path((('M',*a),('L',*b)),arc.color if arc.color is not None else style.curve_color,style.curve_width,'surface-route'))
        atlas.family(routes,intersections=self.intersections)
        for route in routes:
            pieces=binding.project(route)
            _append_paths(paths,[(p.sheet,p.points) for p in pieces],style.curve_color,style.curve_width,'surface-route')
        return Drawing(base.width,base.height,tuple(ellipses),tuple(paths),tuple(texts))

    def _repr_svg_(self):
        from .svg import render_svg
        return render_svg(self)


def _append_paths(paths,pieces,color,width,role):
    sheet,commands=None,[]
    previous=None
    for current,points in pieces:
        if previous is not None and not _near(previous,points[0]):
            raise ItineraryError('projected route pieces do not join')
        previous=points[-1]
        if current!=sheet:
            if commands:
                paths.append(Path(tuple(commands),color,width,role,sheet=='back'))
            commands=[('M',*points[0])]
            sheet=current
        commands.extend(('L',*p) for p in points[1:])
    if commands:
        paths.append(Path(tuple(commands),color,width,role,sheet=='back'))
