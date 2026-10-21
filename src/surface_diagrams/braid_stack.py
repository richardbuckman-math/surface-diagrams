"""Factor-aligned fragments of one braid, using the shared crossing renderer.

Fragments have no end labels or margins. Their vertical strands reach both
edges, so stacking them and carrying strand identities creates one braid.
Signed words, positive crossings and factor order are never changed here.
"""
from html import escape

from .model import Style
from .visuals import RAINBOW, _braid_paths


def stack_row_height(word):
    return max(130, len(tuple(word)) * 5 + 20)


def braid_fragment_svg(word, *, order=None):
    """Six-strand fragment, ready for continuous stacking at 86px width."""
    word = tuple(word)
    if any(type(x) is not int or not 1 <= abs(x) <= 5 for x in word):
        raise ValueError('A six-strand braid uses signed generators 1 through 5')
    order = tuple(range(6)) if order is None else tuple(order)
    if sorted(order) != list(range(6)):
        raise ValueError('Strand order must permute the six starting identities')
    height = stack_row_height(word)
    if word:
        step = min(12., (height - 20.) / len(word))
        inset = (height - step * len(word)) / 2
        levels = (0., -inset) + tuple(-inset - (i+1)*step for i in range(len(word))) + (-height,)
        crossings = (None,) + word + (None,)
    else:
        levels, crossings = (0., -height), (None,)
    # Local colors identify the source strand within this fragment. A browser
    # may remap these six identities using the previous fragment's exit order.
    paths, exit_order = _braid_paths(6, crossings, levels, 12, RAINBOW,
                                     Style(curve_width=.8), 'smooth')
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="86" height="{height}" '
           f'viewBox="0 0 86 {height}" data-word="{escape(" ".join(map(str,word)))}">']
    for path in paths:
        local = RAINBOW.index(path.stroke)
        commands = []
        for op, *values in path.commands:
            coords = [43 + x if i % 2 == 0 else -x for i,x in enumerate(values)]
            commands.append(op + ' ' + ' '.join(f'{x:.3f}' for x in coords))
        out.append(f'<path data-strand="{local}" d="{" ".join(commands)}" '
                   f'stroke="{RAINBOW[order[local]]}" stroke-width=".8" fill="none"/>')
    out.append('</svg>')
    return dict(svg=''.join(out), height=height,
                exit_order=tuple(order[i] for i in exit_order), word=word)


def connected_braid_svg(words):
    """Reference assembly with strand colors carried over factor separators."""
    words = tuple(tuple(word) for word in words)
    height = sum(stack_row_height(word) for word in words)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="86" height="{height}" '
           f'viewBox="0 0 86 {height}" role="img" aria-label="Continuous six-strand braid">']
    order, top = tuple(range(6)), 0
    for i, word in enumerate(words):
        fragment = braid_fragment_svg(word, order=order)
        content = fragment['svg'].split('>',1)[1].rsplit('</svg>',1)[0]
        out.append(f'<g data-factor="{i}" transform="translate(0 {top})">{content}</g>')
        top += fragment['height']
        order = fragment['exit_order']
        if i + 1 < len(words):
            out.append(f'<path class="factor-separator" d="M 3 {top} H 83" '
                       'stroke="#2563eb" stroke-width=".8" stroke-dasharray="2 3"/>')
    out.append('</svg>')
    return ''.join(out)
