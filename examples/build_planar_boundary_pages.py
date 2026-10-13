"""Build one browsable static page per number of inner boundaries."""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'docs' / 'boundary-factorizations'


def build():
    for n in range(1, 11):
        navigation = ' · '.join(
            f'<a href="{k}.html" aria-current="page">{k} inner</a>' if k == n
            else f'<a href="{k}.html">{k} inner</a>'
            for k in range(1, 11))
        html = f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{n} inner boundaries · positive factorization catalog</title>
<link rel="stylesheet" href="size.css">
<body data-n="{n}"><header>
<p><a href="../../index.html">Surface diagrams</a> / <a href="index.html">Boundary catalog</a></p>
<h1>{n} inner boundaries</h1>
<p class="toplinks">{navigation} · <a href="double-outer.html">Double exterior twist</a></p>
<p class="notice">Every candidate pattern for this size is below, ordered by its counts of the largest twist supports first. For each row, the exterior twist is multiplied by the <em>minimum nonnegative powers</em> of the inner-boundary twists needed to make all twists on the factor side positive. Matching these counts alone does not prove a relation.</p>
<p>For a pattern with non-singleton blocks <i>C</i>, let <i>r<sub>i</sub></i> count the blocks containing boundary <i>i</i>. The target is <i>T<sub>0</sub> ∏ T<sub>i</sub><sup>r<sub>i</sub>−1</sup></i>. A relation is displayed only when an exact real-line arrangement supplies a positive factorization through <a href="https://www.math.fsu.edu/~hironaka/papers/lantern.pdf">Hironaka’s theorem</a>, or when it is the trivial exterior twist. The small vertical drawings indicate factor supports; their loop routing is schematic, while the line equations and crossing order form the certificate.</p>
</header><main><div class="search"><strong id="status" role="status">Loading patterns…</strong><label>Jump to pattern <input id="jump" type="number" min="1" step="1"></label></div><div id="patterns"></div></main>
<script src="size.js"></script></body></html>'''
        (OUT / f'{n}.html').write_text(html, encoding='utf-8')
        print(f'Built {n}.html')


if __name__ == '__main__':
    build()
