"""Frame-free thumbnails, without changing any routed curve or mark.

Bounds use the control hull of each Bezier, so trimming whitespace cannot
clip a bend. Unsupported primitives retain the original viewport instead.
"""
import re
from math import cos, sin, radians, sqrt, hypot
from xml.etree import ElementTree as ET


def compact_support_svg(svg, *, padding=7, hide_cut_guides=False):
    root = ET.fromstring(svg)
    x, y, width, height = map(float, root.attrib['viewBox'].split())
    bounds = []
    safe = True

    def visit(node, sx=1, sy=1, tx=0, ty=0):
        nonlocal safe
        tag = node.tag.rsplit('}', 1)[-1]
        if (node.get('class') == 'outer-boundary' or tag in ('title', 'desc')
                or hide_cut_guides and node.get('class') == 'cut-guides'):
            return
        if tag == 'rect' and node.get('width') == '100%':
            return
        transform = node.get('transform', '')
        for op, args in re.findall(r'(translate|scale)\(([^)]+)\)', transform):
            values = list(map(float, args.replace(',', ' ').split()))
            if op == 'translate':
                tx += sx * values[0]; ty += sy * (values[1] if len(values) > 1 else 0)
            else:
                sx *= values[0]; sy *= values[1] if len(values) > 1 else values[0]
        if transform and re.sub(r'(translate|scale)\([^)]+\)', '', transform).strip():
            safe = False
        stroke = float(node.get('stroke-width', '0')) / 2

        def point(px, py, margin=stroke):
            px, py = sx * px + tx, sy * py + ty
            margin *= max(abs(sx), abs(sy))
            bounds.extend(((px-margin, py-margin), (px+margin, py+margin)))

        if tag in ('svg', 'g'):
            for child in node:
                visit(child, sx, sy, tx, ty)
        elif tag == 'path':
            data = node.get('d', '')
            if re.search(r'[a-zHVST]', data.replace('e', '').replace('E', '')):
                safe = False
                return
            current = (0., 0.)
            for op, args in re.findall(r'([MLCQAZ])([^MLCQAZ]*)', data):
                values = list(map(float, re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?', args)))
                if op == 'A':
                    if len(values) != 7:
                        safe = False; return
                    rx,ry,angle,large,sweep,px,py=values
                    rx,ry=abs(rx),abs(ry)
                    if rx and ry and current != (px,py):
                        c,s=cos(radians(angle)),sin(radians(angle))
                        dx,dy=(current[0]-px)/2,(current[1]-py)/2
                        ax,ay=c*dx+s*dy,-s*dx+c*dy
                        enlargement=max(1.,sqrt((ax/rx)**2+(ay/ry)**2))
                        rx*=enlargement;ry*=enlargement
                        denominator=rx*rx*ay*ay+ry*ry*ax*ax
                        ratio=max(0.,(rx*rx*ry*ry-denominator)/denominator) if denominator else 0
                        coefficient=(-1 if bool(large)==bool(sweep) else 1)*sqrt(ratio)
                        bx,by=coefficient*rx*ay/ry,-coefficient*ry*ax/rx
                        cx,cy=c*bx-s*by+(current[0]+px)/2,s*bx+c*by+(current[1]+py)/2
                        ex,ey=hypot(rx*c,ry*s),hypot(rx*s,ry*c)
                        point(cx-ex,cy-ey);point(cx+ex,cy+ey)
                    point(px,py);current=(px,py)
                elif op != 'Z':
                    if len(values)%2:
                        safe=False;return
                    for px,py in zip(values[::2],values[1::2]):point(px,py)
                    if values:current=tuple(values[-2:])
        elif tag in ('circle', 'ellipse'):
            px, py = float(node.get('cx', 0)), float(node.get('cy', 0))
            rx = float(node.get('r', node.get('rx', 0)))
            ry = float(node.get('r', node.get('ry', 0)))
            point(px-rx, py-ry); point(px+rx, py+ry)
        elif tag == 'text':
            px, py = float(node.get('x', 0)), float(node.get('y', 0))
            size = float(node.get('font-size', 12))
            span = size * .7 * len(''.join(node.itertext()))
            anchor = node.get('text-anchor', 'start')
            left = px - (span/2 if anchor == 'middle' else span if anchor == 'end' else 0)
            point(left, py-size); point(left+span, py+size*.3)
        else:
            safe = False

    visit(root)
    if safe and bounds:
        left = min(p[0] for p in bounds)-padding
        top = min(p[1] for p in bounds)-padding
        width = max(p[0] for p in bounds)+padding-left
        height = max(p[1] for p in bounds)+padding-top
    else:
        left, top = x, y
    # Keep the original path serialization and normalize the new viewport to
    # zero for both browser SVG and the vector PDF renderer.
    body = svg.split('>', 1)[1].rsplit('</svg>', 1)[0]
    body = re.sub(r'<(?:ellipse|rect|path)\b[^>]*class="outer-boundary"[^>]*/>', '', body)
    if hide_cut_guides:
        body = re.sub(r'<g\b[^>]*class="cut-guides"[^>]*>.*?</g>', '', body, flags=re.S)
    body = re.sub(r'<rect\b[^>]*width="100%"[^>]*/>', '', body)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.6f}" height="{height:.6f}" '
            f'viewBox="0 0 {width:.6f} {height:.6f}" role="img">'
            f'<g transform="translate({-left:.6f} {-top:.6f})">{body}</g></svg>')
