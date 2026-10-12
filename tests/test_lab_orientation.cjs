'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '..', 'src',
  'surface_diagrams', 'lab_assets', 'lab.js'), 'utf8');
const helpers = source.slice(source.indexOf('const originalPathTransforms='),
  source.indexOf('const braidLayout='));
const hosts = new Map();
const controls = {hidden: false};
const toggleAttributes = new Map();
const toggle = {
  textContent: 'Hide controls',
  setAttribute: (name, value) => toggleAttributes.set(name, value),
};
const headerClasses = new Set();
const header = {classList: {toggle: (name, present) =>
  present ? headerClasses.add(name) : headerClasses.delete(name)}};
const context = vm.createContext({
  $: id => ({'top-controls': controls, 'toggle-controls': toggle})[id] ?? hosts.get(id),
  document: {querySelector: selector => selector === 'header' ? header : null},
  WeakMap,
  Number,
  DOMParser: class {},
  XMLSerializer: class {},
  download: () => {},
});
vm.runInContext(helpers, context);
const apply = vm.runInContext('applyPlanarOrientation', context);

function route(role, rowY, transform = null) {
  const attributes = new Map();
  if (transform !== null) attributes.set('transform', transform);
  const svg = {
    querySelector: selector => selector === 'circle.marked-point'
      ? {getAttribute: name => name === 'cy' ? String(rowY) : null}
      : null,
  };
  return {
    role,
    attributes,
    closest: selector => selector === 'svg' ? svg : null,
    getAttribute: name => attributes.get(name) ?? null,
    setAttribute: (name, value) => attributes.set(name, value),
    removeAttribute: name => attributes.delete(name),
  };
}

const arc = route('arc', 122.75);
const loop = route('closed-curve', 130, 'rotate(10)');
const braid = route('braid', 122.75);
const root = {querySelectorAll: selector => {
  assert.equal(selector, 'svg path.arc, svg path.closed-curve');
  return [arc, loop];
}};
apply(root);
assert.equal(arc.getAttribute('transform'), 'translate(0 245.5) scale(1 -1)');
assert.equal(loop.getAttribute('transform'),
  'translate(0 260) scale(1 -1) rotate(10)');
apply(root);
assert.equal(arc.getAttribute('transform'), 'translate(0 245.5) scale(1 -1)');
assert.equal(loop.getAttribute('transform'),
  'translate(0 260) scale(1 -1) rotate(10)');

const setControlsExpanded = vm.runInContext('setControlsExpanded', context);
setControlsExpanded(false);
assert.equal(controls.hidden, true);
assert.equal(toggle.textContent, 'Show controls');
assert.equal(toggleAttributes.get('aria-expanded'), 'false');
assert.equal(headerClasses.has('controls-collapsed'), true);
toggle.onclick();
assert.equal(controls.hidden, false);
assert.equal(toggle.textContent, 'Hide controls');
assert.equal(toggleAttributes.get('aria-expanded'), 'true');
assert.equal(headerClasses.has('controls-collapsed'), false);

const layoutHelper = source.slice(source.indexOf('function setBraidLayout(){'),
  source.indexOf('function paint(){'));
const cards = [{style: {}}, {style: {}}];
const braidHost = {innerHTML: ''};
const braidLayout = {value: 'compact'};
let selected = 1;
let chosen;
const layoutContext = vm.createContext({
  braidLayout,
  state: {
    factors: [{height: 210, height_compact: 180},
      {height: 300, height_compact: 220}],
    braid: '<svg>classic</svg>',
    braid_compact: '<svg>compact</svg>',
  },
  document: {querySelectorAll: () => cards},
  $: () => braidHost,
  choose: index => {chosen = index;},
  selected,
});
vm.runInContext(layoutHelper, layoutContext);
const setLayout = vm.runInContext('setBraidLayout', layoutContext);
setLayout();
assert.deepEqual(cards.map(card => card.style.height), ['180px', '220px']);
assert.equal(braidHost.innerHTML, '<svg>compact</svg>');
assert.equal(chosen, selected);

braidLayout.value = 'classic';
setLayout();
assert.deepEqual(cards.map(card => card.style.height), ['210px', '300px']);
assert.equal(braidHost.innerHTML, '<svg>classic</svg>');
assert.equal(chosen, selected);
assert.equal(braid.getAttribute('transform'), null);
