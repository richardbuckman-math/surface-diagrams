"""Diagram-led, reversed research route; never fills the uncomputed theorem bridge.

First build the checked research replay with build_six_seven_three_root_research.py.
This exporter reuses its support SVGs and the library's exact braid renderer.
Run with the bundled Python (reportlab and pypdf). All figures remain vector.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
import json
from math import ceil
from pathlib import Path
import re
import subprocess
import sys
from textwrap import wrap
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.factorization_geometry import braid_svg
from surface_diagrams.six_seven_structure import SignedResearchFactor


PHASES = (
    ('route', 'Recover the original thirteen factors',
     'Undo the initial consolidation, then recombine the split three-point roots.'),
    ('prefix_lantern', 'Undo the prefix sphere lantern',
     'Replace two boundary-pair twists by the transported root prefix.'),
    ('reduction', 'Undo the first cluster reductions',
     'Restore the cluster lantern and the complementary charts, retaining the lift signs.'),
    ('residual', 'Undo the residual lantern',
     'Reintroduce the cancelled pair, transport it backward, and restore the residual roots.'),
    ('compression', 'Undo the signed half-lantern compression',
     'Expand the signed root expression back into the transported half-lantern factors.'),
    ('petal_exchange', 'Undo the complementary petal exchange',
     'Restore the cancelled inverse pair and reverse the two cyclic PC rose substitutions.'),
    ('cross_petal_lantern', 'Open the cross-stage PC lantern',
     'Open the transported three-point root into its three petals and reverse the gathering moves.'),
    ('cross_cluster_lantern', 'Undo the common-chart cluster lantern',
     'Separate the matching pairs, restore the inverse pair, and reverse the {35},4,6 cluster move.'),
    ('alternate_half_lantern', 'Undo the alternate half lantern',
     'Restore the ordinary root, reverse the cancellation and half lantern, then return the five petals.'),
    ('last_separator_decomposition', 'Restore the last two separating twists',
     'Restore a cancelling pair and reverse the two-lantern consequence to recover the (26,2) checkpoint.'),
    ('positive_sphere_expansion', 'Contract the positive inverse replacement',
     'Use the squared sphere relation to replace eighteen positive half-twist units by one inverse pair twist.'),
)
IDENTITY4 = [[int(i == j) for j in range(4)] for i in range(4)]


def normalized(record):
    return dict(record, sign=record.get('sign', 1))


def factor(record):
    return SignedResearchFactor(**dict(normalized(record),
                                      conjugator=tuple(record['conjugator'])))


def factor_key(record):
    """Presentation key: deliberately does not identify sphere-only supports."""
    return json.dumps(normalized(record), sort_keys=True, separators=(',', ':'))


def artin_exponent(word):
    return sum(1 if x > 0 else -1 for x in word)


def changed_interval(before, after):
    """Smallest changed contiguous interval; its complement is literally fixed."""
    a, b = list(map(normalized, before)), list(map(normalized, after))
    prefix = 0
    while prefix < min(len(a), len(b)) and a[prefix] == b[prefix]:
        prefix += 1
    suffix = 0
    while suffix < min(len(a), len(b)) - prefix and a[-1-suffix] == b[-1-suffix]:
        suffix += 1
    return prefix, len(a)-suffix, len(b)-suffix


def reverse_route(report):
    """Join only the successful branch, checking every repeated endpoint."""
    chain = []
    for key, _, _ in PHASES:
        stages = report[key]['stages']
        if chain:
            if list(map(normalized, chain[-1][1]['factors'])) != list(map(normalized, stages[0]['factors'])):
                raise ValueError(f'Disconnected research branch: {key}')
        chain.extend((key, s) for s in stages[bool(chain):])
    steps = []
    for number, index in enumerate(range(len(chain)-1, 0, -1), 1):
        phase, applied = chain[index]
        before, after = applied['factors'], chain[index-1][1]['factors']
        prefix, end_before, end_after = changed_interval(before, after)
        sphere = applied['kind'] == 'sphere_rewrite'
        if sphere:
            if not applied.get('sphere_certificate', {}).get('certified'):
                raise ValueError('Sphere move without an exact sphere certificate')
            if applied.get('lift_homology') != IDENTITY4:
                raise ValueError('Sphere move without a positive genus-two lift check')
        steps.append(dict(number=number, phase=phase, original=applied,
                          before=before, after=after, prefix=prefix,
                          end_before=end_before, end_after=end_after,
                          sphere=sphere,
                          reverse_disk_discrepancy=list(inverse_word(tuple(applied.get('disk_discrepancy', ()))))))
    return steps


class ReplayPictures(HTMLParser):
    """Read cached picture assignments from the existing verified HTML replay."""
    def __init__(self):
        super().__init__()
        self.cards = []
        self.card = None
        self.row = None
        self.capture = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section' and 'stage' in attrs.get('class', '').split():
            self.card = dict(title='', rows=[])
        elif self.card is not None:
            if tag == 'h2':
                self.capture = 'title'
            elif tag == 'div' and 'factor' in attrs.get('class', '').split():
                self.row = dict(id='', picture=None)
            elif tag == 'b' and self.row is not None:
                self.capture = 'id'
            elif tag == 'img' and self.row is not None:
                self.row['picture'] = attrs.get('src')

    def handle_data(self, data):
        if self.capture == 'title':
            self.card['title'] += data
        elif self.capture == 'id':
            self.row['id'] += data

    def handle_endtag(self, tag):
        if tag in ('h2', 'b'):
            self.capture = None
        elif tag == 'div' and self.row is not None:
            self.card['rows'].append(self.row)
            self.row = None
        elif tag == 'section' and self.card is not None:
            self.cards.append(self.card)
            self.card = None


def picture_assignments(report, html):
    parser = ReplayPictures()
    parser.feed(html)
    result = {}
    for key, _, _ in PHASES:
        for stage in report[key]['stages']:
            ids = [r['id'] for r in stage['factors']]
            matches = [c for c in parser.cards
                       if re.sub(r'^\d+\. ', '', c['title']) == stage['title']
                       and [r['id'] for r in c['rows']] == ids]
            if not matches:
                raise ValueError(f'No cached support panel for {stage["title"]}')
            for record, row in zip(stage['factors'], matches[0]['rows']):
                k = factor_key(record)
                if k in result and result[k] != row['picture']:
                    raise ValueError('Conflicting support assignments')
                result[k] = row['picture']
    return result


def record_label(record):
    r = normalized(record)
    base = 'H' if r['half'] else f'T{r["points"]}'
    power = r['power'] * r['sign']
    return base if power == 1 else f'{base}^{power}'


def reverse_caption(step):
    original = step['original']
    if original['kind'] == 'disk_hurwitz':
        # State titles specify the fixed dragged factor in the forward move.
        return 'Reverse Hurwitz move: ' + original['title']
    return 'Undo: ' + original['title']


def certificate_scope(step):
    if step['sphere']:
        cert = step['original'].get('sphere_certificate', {})
        if cert.get('disk_identity') is False or step['original'].get('disk_nonidentity_witness'):
            disk = 'Disk equality: FALSE (nonidentity witness retained).'
        elif artin_exponent(step['reverse_disk_discrepancy']) != 0:
            disk = 'Disk equality: FALSE (nonzero exponent discrepancy).'
        else:
            disk = 'Disk equality: not separately asserted by this sphere certificate.'
        return ('SPHERE MOVE. Exact sphere action agrees; genus-two lift discrepancy is +I. '
                + disk)
    return 'DISK MOVE. The ordered disk braid product is unchanged by the recorded move.'


def vector_svg(svg):
    """Convert the shared renderers' limited SVG vocabulary without rasterizing.

    This is intentionally strict. Unknown primitives or transforms must fail
    rather than silently disappear from a mathematical support or braid.
    """
    from reportlab.graphics.shapes import Drawing, Group, Circle, Ellipse
    from reportlab.graphics.svgpath import SvgPath
    from reportlab.lib.colors import HexColor
    root = ElementTree.fromstring(svg)
    bounds = list(map(float, root.attrib['viewBox'].split()))
    if bounds[:2] != [0, 0]:
        raise ValueError('Expected a zero-origin shared SVG')
    width, height = bounds[2:]
    drawing = Drawing(width, height)
    down = Group(transform=(1, 0, 0, -1, 0, height))
    for e in root:
        tag = e.tag.rsplit('}', 1)[-1]
        if tag == 'title':
            continue
        color = lambda name, default: (None if e.get(name, default) == 'none'
                                       else HexColor(e.get(name, default)))
        kw = dict(fillColor=color('fill', '#000000'), strokeColor=color('stroke', 'none'),
                  strokeWidth=float(e.get('stroke-width', 1)))
        if tag == 'path':
            shape = SvgPath(e.attrib['d'], **kw)
            shape.strokeLineCap = 1 if e.get('stroke-linecap') == 'round' else 0
            shape.strokeLineJoin = 1 if e.get('stroke-linejoin') == 'round' else 0
        elif tag == 'circle':
            shape = Circle(float(e.get('cx')), float(e.get('cy')), float(e.get('r')), **kw)
        elif tag == 'ellipse':
            shape = Ellipse(float(e.get('cx')), float(e.get('cy')),
                            float(e.get('rx')), float(e.get('ry')), **kw)
        elif tag == 'rect' and kw['fillColor'] is None and kw['strokeColor'] is None:
            # Metadata rectangles in braid_svg have no visible geometry.
            continue
        else:
            raise ValueError(f'Unsupported shared SVG primitive: {tag}')
        group = Group(shape)
        transform = e.get('transform', '')
        matches = list(re.finditer(r'(translate|scale)\(([^)]+)\)', transform))
        if re.sub(r'(translate|scale)\([^)]+\)', '', transform).strip():
            raise ValueError(f'Unsupported SVG transform: {transform}')
        for m in matches:
            values = list(map(float, m.group(2).replace(',', ' ').split()))
            if m.group(1) == 'translate':
                group.translate(values[0], values[1] if len(values) > 1 else 0)
            else:
                group.scale(values[0], values[1] if len(values) > 1 else values[0])
        down.add(group)
    drawing.add(down)
    return drawing


class PDF:
    def __init__(self, path, image_dir, pictures, assets, sha):
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.lib.pagesizes import A3, landscape
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.styles import ParagraphStyle
        font_dir = Path('C:/Windows/Fonts')
        for name, filename in [('Body', 'arial.ttf'), ('Bold', 'arialbd.ttf'), ('Italic', 'ariali.ttf')]:
            pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
        pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold', italic='Italic', boldItalic='Bold')
        self.W, self.H = landscape(A3)
        self.c = Canvas(str(path), pagesize=(self.W, self.H), pageCompression=1)
        self.c.setTitle('Toward (6,7): a graphical reverse derivation')
        self.c.setAuthor('Richard Buckman - surface-diagrams research project')
        self.styles = {
            'body': ParagraphStyle('body', fontName='Body', fontSize=12.5, leading=18, textColor='#23354a'),
            'small': ParagraphStyle('small', fontName='Body', fontSize=9.5, leading=13, textColor='#42546a'),
            'caption': ParagraphStyle('caption', fontName='Body', fontSize=10.5, leading=14, textColor='#23354a'),
            'title': ParagraphStyle('title', fontName='Bold', fontSize=27, leading=32, textColor='#102942'),
            'h2': ParagraphStyle('h2', fontName='Bold', fontSize=18, leading=23, textColor='#102942'),
        }
        self.images = image_dir
        self.pictures = pictures
        self.assets = assets
        self.sha = sha
        self.page = 0
        self.page_index = []
        self.missing = set()
        self.forms = {}

    def form(self, svg_path, braid=False):
        from reportlab.graphics import renderPDF
        key = str(svg_path)
        if key not in self.forms:
            raw = svg_path.read_text(encoding='utf-8')
            if braid:
                # PDF print style only; crossing paths and their over/under
                # gaps are unchanged. At 52 pt wide, the lab's 1.3-unit
                # strokes are too faint on paper.
                raw = raw.replace('stroke-width="1.3"', 'stroke-width="2.6"')
            drawing = vector_svg(raw)
            name = f'vector-{len(self.forms)}'
            self.c.beginForm(name, 0, 0, drawing.width, drawing.height)
            renderPDF.draw(drawing, self.c, 0, 0)
            self.c.endForm()
            self.forms[key] = name, drawing.width, drawing.height
        return self.forms[key]

    def support(self, svg_path, x, y, width, height):
        name, sw, sh = self.form(svg_path)
        scale = min(width/sw, height/sh)
        self.c.saveState()
        self.c.translate(x+(width-sw*scale)/2, y+(height-sh*scale)/2)
        self.c.scale(scale, scale)
        self.c.doForm(name)
        self.c.restoreState()

    def text(self, text, x, top, width, style='body'):
        from reportlab.platypus import Paragraph
        p = Paragraph(text, self.styles[style])
        _, h = p.wrap(width, self.H)
        p.drawOn(self.c, x, top-h)
        return top-h

    def new(self, title, subtitle='', bookmark=None, level=1):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.c.setFillColorRGB(.975, .982, .988)
        self.c.rect(0, 0, self.W, self.H, fill=1, stroke=0)
        self.c.setFillColorRGB(.08, .17, .26)
        self.c.setFont('Bold', 9)
        self.c.drawString(42, self.H-30, 'SURFACE DIAGRAMS  /  GRAPHICAL RESEARCH DERIVATION')
        top = self.text(escape(title), 42, self.H-51, self.W-84, 'title')
        if subtitle:
            top = self.text(subtitle, 42, top-10, self.W-84, 'caption')
        self.c.setStrokeColorRGB(.78, .83, .88)
        self.c.line(42, 35, self.W-42, 35)
        self.c.setFont('Body', 9)
        self.c.setFillColorRGB(.3, .38, .46)
        self.c.drawString(42, 20, f'19 October 2026 | source {self.sha[:8]} | supports are individual disk charts')
        self.c.drawRightString(self.W-42, 20, str(self.page))
        if bookmark:
            self.c.bookmarkPage(bookmark)
            self.c.addOutlineEntry(title, bookmark, level=level, closed=level > 0)
        self.page_index.append(dict(page=self.page, title=title, bookmark=bookmark))
        return top-20

    def band(self, text, top, color='#dbeafe', height=45):
        from reportlab.lib.colors import HexColor
        self.c.setFillColor(HexColor(color))
        self.c.roundRect(42, top-height, self.W-84, height, 8, stroke=0, fill=1)
        self.text(text, 55, top-10, self.W-110, 'caption')
        return top-height-16

    def arrow(self, x, y, length=24):
        self.c.setStrokeColorRGB(.16, .34, .55)
        self.c.setLineWidth(1.5)
        self.c.line(x, y, x+length, y)
        self.c.line(x+length, y, x+length-6, y+4)
        self.c.line(x+length, y, x+length-6, y-4)

    def asset(self, record):
        return self.assets[factor_key(record)]

    def row_height(self, record):
        a = self.asset(record)
        return max(153, a['strip_height']*a['scale']+33)

    def row(self, record, position, x, top, width=530):
        from reportlab.lib.colors import HexColor
        r = normalized(record)
        height = self.row_height(record)
        self.c.setFillColor(HexColor('#fff4f0' if r['sign'] < 0 else '#ffffff'))
        self.c.roundRect(x, top-height+6, width, height-10, 6, stroke=0, fill=1)
        label = f'{position}. {r["id"]}   |   {record_label(r)}'
        self.text(escape(label), x+9, top-10, width-18, 'small')
        picture = self.pictures.get(factor_key(record))
        if picture:
            self.support(Path(picture), x+7, top-148, 235, 125.3)
        else:
            self.missing.add(r['id'])
            self.text('<b>Disk support picture unavailable.</b><br/>The exact braid is shown. '
                      'No sphere replacement is silently used here.', x+18, top-62, 205, 'caption')
        a = self.asset(record)
        bx = x+253
        name, sw, sh = self.form(self.images/f'{a["name"]}.svg', braid=True)
        for i in range(a['strips']):
            start, end = a['cuts'][i:i+2]
            px = bx+i*(a['width']+3)
            py = top-29-(end-start)*a['scale']
            self.c.saveState()
            clip = self.c.beginPath()
            clip.rect(px-1, py, a['width']+2, (end-start)*a['scale'])
            self.c.clipPath(clip, stroke=0)
            self.c.translate(px, py-(sh-end)*a['scale'])
            self.c.scale(a['scale'], a['scale'])
            self.c.doForm(name)
            self.c.restoreState()
            if a['strips'] > 1:
                self.c.setFont('Body', 7)
                self.c.setFillColor(HexColor('#42546a'))
                self.c.drawCentredString(bx+i*(a['width']+3)+a['width']/2,
                                         top-25, f'{i+1}/{a["strips"]}')
        self.c.setStrokeColorRGB(.15, .39, .88)
        self.c.setLineWidth(.65)
        self.c.setDash(2, 3)
        self.c.line(x+253, top-height+4, x+width-10, top-height+4)
        self.c.setDash()
        return top-height

    def checkpoint(self, records, name, bookmark=None, explanation=''):
        cursor = 0
        part = 0
        while cursor < len(records):
            part += 1
            top = self.new(name + (f' - continued {part}' if part > 1 else ''),
                           explanation if part == 1 else 'Continue downward in the left column, then the right.',
                           bookmark if part == 1 else None, level=1)
            top = self.band('FULL ORDERED CHECKPOINT. Read down the left column, then down the right. '
                            'Each support is paired with its disk braid; braid strips read down, then left to right.', top)
            for column in range(2):
                y = top
                while cursor < len(records) and y-self.row_height(records[cursor]) >= 52:
                    y = self.row(records[cursor], cursor+1, 42+column*554, y)
                    cursor += 1

    def move(self, step):
        p = step['prefix']
        left = step['before'][p:step['end_before']]
        right = step['after'][p:step['end_after']]
        li = ri = 0
        part = 0
        while part == 0 or li < len(left) or ri < len(right):
            part += 1
            title = f'Step {step["number"]:03d}' + (f' - continued {part}' if part > 1 else '')
            top = self.new(title, escape(reverse_caption(step)),
                           f'step-{step["number"]}' if part == 1 else None, level=2)
            top = self.band(escape(certificate_scope(step)), top,
                            '#ffe6ce' if step['sphere'] else '#e2edf9', height=47)
            unchanged_tail = len(step['before'])-step['end_before']
            context = (f'Only the changed interval is enlarged. {p} factors above and '
                       f'{unchanged_tail} factors below stay literally unchanged. '
                       f'Ordered state: {len(step["before"])} to {len(step["after"])} records.')
            top = self.text(context, 42, top, self.W-84, 'caption')-15
            self.text('<b>BEFORE</b>', 42, top, 510, 'caption')
            self.text('<b>AFTER</b>', 596, top, 510, 'caption')
            self.arrow(571, top-7, 15)
            top -= 22
            for side, records, start, x in [('left', left, li, 42), ('right', right, ri, 596)]:
                y = top
                cursor = start
                if not records and part == 1:
                    self.text('Identity: no factors in this interval.', x+12, y-30, 490)
                while cursor < len(records) and y-self.row_height(records[cursor]) >= 115:
                    y = self.row(records[cursor], p+cursor+1, x, y)
                    cursor += 1
                if cursor == start and cursor < len(records):
                    raise ValueError('Factor row does not fit on the move page')
                if side == 'left':
                    li = cursor
                else:
                    ri = cursor
            note = ('Braid strips preserve the exact displayed disk word and strand colors. '
                    'Read each strip down, then continue in the next strip to its right. '
                    'H is a half twist; T2 and T3 are full twists about two- and three-point supports. '
                    'Powers and signs are printed beside every support.')
            self.text(note, 42, 90, self.W-84, 'small')


def prepare_assets(report, steps, source, work):
    """Prepare shared vector SVGs and safe braid-fold boundaries."""
    records = {}
    for step in steps:
        for r in step['before'] + step['after']:
            records[factor_key(r)] = r
    for i in range(1, 6):
        for half in (True, False):
            r = dict(id=f'standard.{i}.{half}', conjugator=[], first=i, points=2,
                     power=1, half=half, sign=1)
            records[factor_key(r)] = r
    pictures = picture_assignments(report, (source / 'index.html').read_text(encoding='utf-8'))
    # Reuse matching cached supports for the standard reference factors.
    for k, r in records.items():
        if k in pictures:
            continue
        match = next((pictures[factor_key(x)] for x in records.values()
                      if factor_key(x) in pictures and x['first'] == r['first']
                      and x['half'] == r['half'] and not x['conjugator'] and x['points'] == 2), None)
        if match is None:
            from surface_diagrams.boundary_playground_geometry import support_svg
            filename = f'standard-{r["first"]}-{r["half"]}.svg'
            (work / filename).write_text(support_svg(factor(r), 6, mirror_vertical=True), encoding='utf-8')
            pictures[k] = filename
        else:
            pictures[k] = match
    pictures = {k: str(source/v if (source/v).exists() else work/v) if v else None
                for k, v in pictures.items()}
    assets = {}
    for index, (k, r) in enumerate(records.items()):
        name = f'braid-{index}'
        svg = braid_svg([factor(r)], compact=True)
        height = int(re.search(r'height="(\d+)"', svg).group(1))
        # All compact levels are twelve units apart. Fold at a midpoint between
        # levels, with one continuous color assignment from the original SVG.
        strips = max(1, ceil(height/744))
        # Long blocks use inset 18, step 12 in aligned_compact_steps. Their
        # level boundaries are 6 modulo 12, not multiples of 12 (the latter
        # would cut through the middle of a crossing).
        base_height = ceil(height/strips/12)*12
        cuts = [0] + [base_height*(i+1)+6 for i in range(strips-1)] + [height]
        strip_height = max(b-a for a, b in zip(cuts, cuts[1:]))
        width = min(52, (266-3*(strips-1))/strips)
        scale = width/240
        svg_path = work/f'{name}.svg'
        if not svg_path.exists() or svg_path.read_text(encoding='utf-8') != svg:
            svg_path.write_text(svg, encoding='utf-8')
        assets[k] = dict(name=name, height=height, strips=strips,
                         strip_height=strip_height, cuts=cuts, width=width, scale=scale)
    return pictures, assets


def build(report_path, output, work):
    report_bytes = report_path.read_bytes()
    report = json.loads(report_bytes)
    steps = reverse_route(report)
    if len(steps) != 145 or sum(s['sphere'] for s in steps) != 14:
        raise ValueError('Unexpected route size: review the document structure before exporting')
    recognition = report['standard_fifty_recognition']
    assert recognition['classification_hypotheses_verified']
    assert recognition['theorem_implies_hurwitz_equivalence']
    assert not recognition['explicit_hurwitz_route_found']
    work.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    pictures, assets = prepare_assets(report, steps, report_path.parent, work)
    temporary_pdf = work/'report-unattached.pdf'
    pdf = PDF(temporary_pdf, work, pictures, assets, sha)

    top = pdf.new('Toward (6,7)', 'A graphical reverse derivation, with exact disk braids beside the supports.',
                  'overview', level=0)
    top = pdf.text('The whole idea, very briefly', 42, top-10, 1000, 'h2')-14
    top = pdf.text('Start with the standard <b>20 + 30</b> positive factorization. A classification theorem '
                   'identifies it with our enlarged 50-twist word. From that word, reverse the checked '
                   'sphere, lantern, rose and Hurwitz moves until the original <b>six half twists and '
                   'seven squared three-point twists</b> reappear.', 42, top, 1030)-26
    top = pdf.band('<b>ONE EXPLICIT GAP:</b> the theorem proves a Hurwitz equivalence to the standard '
                   '20+30 word, but the individual moves realizing that bridge have not been computed. '
                   'The 145 moves after that bridge are shown in reverse order below.', top, '#fff0d5', 61)
    boxes = [('Standard W0 W1', '20 + 30 positive units'),
             ('Our positive word', '50 positive units'),
             ('Signed checkpoint', 'one inverse pair twist'),
             ('Original (6,7)', '13 displayed factors')]
    y = top-18
    for i, (title, caption) in enumerate(boxes):
        x = 42+i*281
        pdf.c.setFillColorRGB(.87, .92, .97)
        pdf.c.roundRect(x, y-88, 244, 88, 8, stroke=0, fill=1)
        pdf.text(escape(title), x+14, y-16, 216, 'h2')
        pdf.text(escape(caption), x+14, y-49, 216, 'caption')
        if i < 3:
            pdf.arrow(x+249, y-43, 24)
    top = y-111
    pdf.text('The first arrow is theorem-based. All later arrows expand into the recorded graphical moves. '
             'The original (6,7) denotes genus-two vanishing-cycle counts, not a genus-six fibration. '
             'The six-point sphere is the hyperelliptic quotient.', 42, top, 1060)
    pdf.text('Prepared for Richard Buckman | 19 October 2026<br/>'
             'Research status: a checked factor-level route with an uncomputed standard-target bridge. '
             'This report does not claim a fully explicit derivation from the standard word.',
             42, 155, 1050, 'caption')

    top = pdf.new('Roadmap: the work in reverse', 'The document follows this order. PDF bookmarks jump to each phase and move.',
                  'roadmap', level=0)
    for number, (key, title, description) in enumerate(reversed(PHASES), 1):
        matching = [s for s in steps if s['phase'] == key]
        line = (f'<b>{number:02d}. {escape(title)}</b> - steps {matching[0]["number"]:03d}'
                f'-{matching[-1]["number"]:03d}<br/>{escape(description)}')
        top = pdf.text(line, 42, top, 1080, 'caption')-13
    pdf.text('Before those phases: standard reference blocks, the theorem bridge, and the full positive-50 '
             'checkpoint. After them: the recovered thirteen factors, the sphere-move discrepancy ledger, '
             'and references. Complete machine-readable states and certificates are embedded in this PDF.',
             42, 105, 1050, 'caption')

    top = pdf.new('How to read the drawings', bookmark='reading', level=0)
    paragraphs = [
        '<b>Supports and powers.</b> A purple closed curve denotes a Dehn-twist support; an arc denotes a half-twist support. '
        'The label H, T2, T3, its power, and its sign specify the actual factor. A support is drawn once even when its power is two. '
        'A red-tinted factor row has negative sign. An ordinary T3 is a temporary root of a separating genus-two twist; '
        'it is not itself asserted to be one genus-two Dehn twist. The squared T3 is the separating factor.',
        '<b>Order.</b> Each vertical list is ordered from top to bottom. Full checkpoints continue down the left column, then the right, '
        'then onto the next page. At a local step, the surrounding unchanged factors are omitted and their counts are stated explicitly.',
        '<b>Braids.</b> Each support has the library-rendered braid for that exact factor immediately to its right. Long braids are folded '
        'into numbered strips: read down one strip, then continue at the top of the next. The fold retains strand colors and every crossing. '
        'Only independent crossings may share a level. Colors restart between separate factors. '
        'The blue dotted rules mark factor boundaries. All figures are vector graphics and remain sharp when zoomed.',
        '<b>Disk charts on a sphere.</b> The ellipse frames a planar chart for six marked points. It is not an extra physical boundary of the '
        'sphere. Points are numbered 1 through 6 from left to right; the support convention is the vertically reflected convention approved '
        'in the PC lantern lab. Braid signs have not been reflected.',
        '<b>What is certified.</b> DISK MOVE means equality of ordered disk braid products. SPHERE MOVE means exact sphere-action agreement '
        'with a separate +I genus-two lift check; its disk discrepancy remains recorded. A sphere move is never silently treated as a disk move.',
        '<b>What a support picture is not.</b> These are individual Arc/Loop support drawings from the surface library. They are not cumulative '
        'five-arc cut-complex certificates. One very complicated intermediate disk support exceeds the renderer limit and is explicitly marked '
        'unavailable; its exact braid remains visible.',
        '<b>Fibrations can change.</b> Lantern and other substitutions can change the fibration even when they preserve the required product. '
        'The goal here is a derivation of the relation, not a claim that every intermediate list defines the original fibration.',
    ]
    for text in paragraphs:
        top = pdf.text(text, 42, top, 1070)-22

    # Reference words are compressed only by the indicated repeat counts.
    reference = []
    for i in [1, 2, 3, 4, 5, 4, 3, 2, 1]:
        reference.append(dict(id=f'standard.{i}.{i != 5}', conjugator=[], first=i,
                              points=2, power=1, half=i != 5, sign=1))
    pdf.checkpoint(reference, 'Reference: W0, the twenty-unit block', 'reference-w0',
                   'Repeat this nine-record list TWICE. Its middle record is T2 = H5 squared. '
                   'Thus W0 = (1 2 3 4 5 5 4 3 2 1)^2. This is a reference target, not a performed move.')
    reference = [dict(id=f'standard.{i}.True', conjugator=[], first=i, points=2,
                      power=1, half=True, sign=1) for i in range(1, 6)]
    pdf.checkpoint(reference, 'Reference: W1, the thirty-unit block', 'reference-w1',
                   'Repeat this five-record list SIX TIMES. W1 = (1 2 3 4 5)^6. '
                   'Both W0 and W1 have identity sphere action and +I genus-two lift.')

    top = pdf.new('The theorem bridge: known to exist, not yet drawn', bookmark='bridge', level=0)
    top = pdf.band('<b>UNCOMPUTED HURWITZ ROUTE.</b> There is no invented sequence of intermediate drawings on this page.',
                   top, '#fff0d5', 50)
    for text in [
        'The expanded source is an identity factorization with fifty positive nonseparating genus-two twists. '
        'Its exact sphere action is identity, its lift check is +I, and explicit factors provide all five standard chain generators. '
        'Their permutation images generate the full symmetric group S6.',
        'The Siebert-Tian classification, stated as Theorem 9 in Auroux, puts such a transitive factorization in the Hurwitz normal form '
        '<b>W0^k W1^epsilon</b>, with epsilon equal to 0 or 1. Counting lengths gives '
        '<b>50 = 20k + 30epsilon</b>, so k = 1 and epsilon = 1.',
        'Therefore our positive word is Hurwitz equivalent to W0 W1 in closed genus two. This identifies the correct standard endpoint; '
        'it does not provide the individual Hurwitz moves, and it does not assert disk braid equality.',
        'The literal twenty-letter word (1 2 3 4)^5 is not interchangeable here with W0: its lift check is -I. '
        'The correct twenty-unit reference is the palindromic W0 block drawn in the preceding pages.',
        'From the next checkpoint onward, the report shows every checked reverse transition. The unresolved task is to replace this '
        'theorem bridge by an explicit graphical Hurwitz sequence.',
    ]:
        top = pdf.text(text, 42, top, 1070)-24
    pdf.text('Source: D. Auroux, <i>Fiber sums of genus 2 Lefschetz fibrations</i>, '
             'Definition 4 and Theorem 9 (printed pages 3 and 5).<br/>'
             '<link href="https://arxiv.org/pdf/math/0204285" color="#175a9e">https://arxiv.org/pdf/math/0204285</link>',
             42, top, 1060, 'caption')

    pdf.c.bookmarkPage('checked-route')
    pdf.c.addOutlineEntry('The checked reverse route', 'checked-route', level=0)
    pdf.checkpoint(steps[0]['before'], 'Starting checkpoint: our positive fifty-unit word', 'positive-50',
                   'Thirty-two displayed records contain fifty positive nonseparating units. The next move contracts the eighteen-unit replacement.')
    for key, title, description in reversed(PHASES):
        phase_steps = [s for s in steps if s['phase'] == key]
        top = pdf.new(title, description, 'phase-'+key, level=1)
        top = pdf.text(f'<b>Steps {phase_steps[0]["number"]:03d}-{phase_steps[-1]["number"]:03d}.</b> '
                       'Every local transition follows, with unchanged surrounding factors counted. '
                       'A complete ordered checkpoint closes the phase.', 42, top, 1060)-25
        for s in phase_steps:
            top = pdf.text(f'<b>{s["number"]:03d}</b> '
                           + ('<b>SPHERE MOVE</b> - ' if s['sphere'] else '')
                           + escape(reverse_caption(s)), 42, top, 1060, 'caption')-8
        for s in phase_steps:
            pdf.move(s)
        pdf.checkpoint(phase_steps[-1]['after'], 'Checkpoint: '+title,
                       explanation='The complete ordered factor list after this reverse phase.')

    top = pdf.new('Endpoint: the supplied (6,7) is recovered', bookmark='endpoint', level=0)
    pdf.text('The last checkpoint has exactly the original thirteen factors, in the supplied order: '
             '<b>six half twists and seven squared three-point twists</b>. Under the hyperelliptic lift, '
             'these give the six nonseparating and seven separating vanishing cycles.', 42, top, 1060)
    pdf.text('What is complete here is the reverse replay from the enlarged positive 50-unit word to the supplied factorization. '
             'What is still missing is a concrete Hurwitz replay from the standard reference W0 W1 to that enlarged word. '
             'Until that bridge is drawn, this remains a theorem-assisted graphical research derivation.', 42, top-90, 1060)

    top = pdf.new('Sphere-move ledger', 'Each entry inverts the stored forward disk discrepancy; its local chart/context is retained in the attached certificate.',
                  'ledger', level=0)
    for s in [s for s in steps if s['sphere']]:
        word = ' '.join(map(str, s['reverse_disk_discrepancy'])) or '(empty)'
        if top < 170:
            top = pdf.new('Sphere-move ledger - continued', 'Signed integers encode Artin generators; -i means sigma_i inverse.')
        top = pdf.text(f'<b>SPHERE MOVE {s["number"]:03d}</b> - {escape(s["original"]["title"])}<br/>'
                       f'Disk discrepancy length {len(s["reverse_disk_discrepancy"])}; '
                       f'exponent sum {artin_exponent(s["reverse_disk_discrepancy"])}; sphere identity and lift +I.',
                       42, top, 1070, 'caption')-8
        # Put long exact words on as many lines/pages as necessary, never truncate.
        chunks = wrap(word, width=150, break_long_words=False, break_on_hyphens=False)
        for chunk in chunks:
            if top < 75:
                top = pdf.new('Sphere-move ledger - continued', f'Continuation of SPHERE MOVE {s["number"]:03d}.')
            top = pdf.text(escape(chunk), 48, top, 1060, 'small')-3
        top -= 15

    top = pdf.new('Exact data and references', bookmark='references', level=0)
    paragraphs = [
        '<b>Embedded data.</b> The PDF contains research-certificate.json and reverse-route.json as file attachments. '
        'The first is the checked research report, including local certificates and the unused alternative branch. '
        'The second selects only this connected reverse route and records every full state, exact factor presentation, '
        'reverse discrepancy and page location. Signed integer lists encode Artin generators; negative integers mean inverses.',
        '<b>Reproducibility.</b> The exporter is examples/build_six_seven_derivation_pdf.py, using cached shared Arc/Loop support SVGs '
        'and the existing factorization_geometry.braid_svg renderer. Braid folding is only a page-layout operation. '
        f'Source commit: {sha}. Research certificate SHA-256: {sha256(report_bytes).hexdigest()}.',
        '<b>1. D. Auroux.</b> <i>Fiber sums of genus 2 Lefschetz fibrations</i>, Definition 4, Lemmas 5-7, Theorem 9. '
        '<link href="https://arxiv.org/pdf/math/0204285" color="#175a9e">https://arxiv.org/pdf/math/0204285</link>',
        '<b>2. B. Siebert and G. Tian.</b> <i>On the holomorphicity of genus two Lefschetz fibrations</i>, '
        'Annals of Mathematics 161 (2005). '
        '<link href="https://annals.math.princeton.edu/2005/161-2/p09" color="#175a9e">https://annals.math.princeton.edu/2005/161-2/p09</link>',
        '<b>3. H. Endo and Y. Gurtas.</b> <i>Lantern relations and rational blowdowns</i>. '
        'Background on how lantern substitutions change the total space. '
        '<link href="https://arxiv.org/abs/0808.0386" color="#175a9e">https://arxiv.org/abs/0808.0386</link>',
        '<b>Scope reminder.</b> Neither counts alone, endpoint agreement alone, nor a single support drawing proves an ordered relation. '
        'The explicit sphere labels and disk discrepancies are part of the derivation, not optional display decoration.',
    ]
    for text in paragraphs:
        top = pdf.text(text, 42, top, 1070)-25
    pdf.c.save()

    manifest = dict(title='Checked reverse route toward (6,7)', source_commit=sha,
                    certificate_sha256=sha256(report_bytes).hexdigest(),
                    theorem_bridge_explicit=False, steps=steps,
                    pages=pdf.page_index, missing_disk_supports=sorted(pdf.missing))
    manifest_bytes = json.dumps(manifest, separators=(',', ':')).encode()
    (work/'reverse-route.json').write_bytes(manifest_bytes)
    from pypdf import PdfReader, PdfWriter
    writer = PdfWriter(clone_from=temporary_pdf)
    writer.add_attachment('research-certificate.json', report_bytes)
    writer.add_attachment('reverse-route.json', manifest_bytes)
    with output.open('wb') as stream:
        writer.write(stream)
    reader = PdfReader(output)
    assert len(reader.pages) == pdf.page
    assert len(reader.attachments) == 2
    print(json.dumps(dict(pdf=str(output), pages=pdf.page, moves=len(steps),
                          sphere_moves=sum(s['sphere'] for s in steps),
                          missing_supports=sorted(pdf.missing), bytes=output.stat().st_size)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=ROOT/'.preview/six-seven-three-root-transport/certificate.json')
    parser.add_argument('--output', type=Path, default=ROOT/'output/pdf/six-seven-backward-graphical-derivation.pdf')
    parser.add_argument('--work', type=Path, default=ROOT/'tmp/pdfs/six-seven-derivation')
    args = parser.parse_args()
    build(args.certificate, args.output, args.work)
