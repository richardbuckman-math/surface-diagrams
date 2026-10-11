'use strict';
// The shared factor UI owns edits. This panel shows every exact prefix beside
// its factor and braid interval, without modifying a braid word or strand.
const pcElement = id => document.getElementById(id);
const pcArcVisible = () => [1, 2, 3].map(n => pcElement(`pc-arc-${n}`).checked);
const pcMirrored = () => pcElement('pc-orientation').value === 'mirrored';
const pcRowResizeObserver = new ResizeObserver(syncPcRowHeights);

function syncPcRowHeights() {
  const factors = document.querySelectorAll('#factors .factor');
  document.querySelectorAll('#pc-cuts-column .pc-cut-row').forEach((row, index) => {
    row.style.height = `${factors[index]?.offsetHeight || state.factors[index].height}px`;
  });
}

function filterPcArcs(svg) {
  const visible = pcArcVisible();
  svg.querySelectorAll('path.arc').forEach((path, index) => {
    path.style.display = visible[index] ? '' : 'none';
  });
}

function refreshPcCutViews() {
  if (!state?.pc_lantern) return;
  document.body.classList.toggle('pc-hide-cuts', !pcElement('pc-show-column').checked);
  const mirrored = pcMirrored();
  const steps = state.cut_steps.slice(1, -1);
  const column = pcElement('pc-cuts-column');
  const factorCards = document.querySelectorAll('#factors .factor');
  column.replaceChildren();
  steps.forEach((step, index) => {
    const card = document.createElement('article');
    card.className = 'pc-cut-row';
    card.style.height = `${factorCards[index]?.offsetHeight || state.factors[index].height}px`;
    card.dataset.prefix = String(index + 1);
    const heading = document.createElement('strong');
    heading.textContent = `F${index + 1} · after ${state.factors[index].id}`;
    const drawing = document.createElement('div');drawing.className = 'pc-cut-row-drawing';
    const picture = mirrored ? step.svg : step.svg_unmirrored;
    if (picture) {drawing.innerHTML = picture;filterPcArcs(drawing);}
    else drawing.textContent = step.warning || 'Cut picture unavailable';
    card.append(heading, drawing);column.append(card);
  });
  pcRowResizeObserver.disconnect();
  factorCards.forEach(card => pcRowResizeObserver.observe(card));
  const target = state.cut_steps.at(-1);
  const targetBox = pcElement('pc-target-drawing');
  targetBox.innerHTML = mirrored ? target.svg : target.svg_unmirrored;
  filterPcArcs(targetBox);
  const final = state.cut_steps.at(-2);
  pcElement('pc-match').textContent = final.arcs.length &&
    JSON.stringify(final.arcs) === JSON.stringify(target.arcs) ?
    'All three final arc itineraries agree exactly with the direct twist.' :
    'The exact braid target is checked; the final arc picture needs inspection.';

  // The Python backend provides both support orientations. Select only these
  // SVGs; never transform the braid column or invert algebraic generators.
  document.querySelectorAll('#factors .factor .support').forEach((host, index) => {
    const factor = state.factors[index];
    const picture = mirrored ? factor.svg_mirrored : factor.svg_unmirrored;
    if (picture) host.innerHTML = picture;
    else host.textContent = factor.warning || 'Support picture unavailable';
  });
}

for (const id of ['pc-show-column', 'pc-arc-1', 'pc-arc-2', 'pc-arc-3'])
  pcElement(id).onchange = refreshPcCutViews;
pcElement('pc-orientation').onchange = refreshPcCutViews;
pcElement('pc-show-all').onclick = () => {
  pcElement('pc-show-column').checked = true;
  for (const n of [1, 2, 3]) pcElement(`pc-arc-${n}`).checked = true;
  refreshPcCutViews();
};
pcElement('pc-hide-all').onclick = () => {
  for (const n of [1, 2, 3]) pcElement(`pc-arc-${n}`).checked = false;
  refreshPcCutViews();
};
new MutationObserver(refreshPcCutViews).observe(pcElement('factors'), {childList:true});
