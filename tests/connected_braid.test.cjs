const test=require('node:test');
const assert=require('node:assert/strict');
const fixture=require('./fixtures/connected-braid.json');
const {assemble}=require('../src/surface_diagrams/lab_assets/connected-braid.js');

test('browser assembly equals the independent shared Python continuous renderer',()=>{
 const result=assemble(fixture.factors,fixture.fragments);
 assert.equal(result.svg,fixture.expected);
 assert.equal(result.height,fixture.height);
 assert.deepEqual(result.exitOrder,fixture.exit_order);
 assert.equal((result.svg.match(/class="factor-separator"/g)||[]).length,fixture.factors.length-1);
});
test('a stale or mismatched fragment cannot silently draw the wrong factor',()=>{
 const rows=structuredClone(fixture.factors);rows[0].word=[4,-5,-4];
 assert.throws(()=>assemble(rows,fixture.fragments),/does not match/);
 const heights=structuredClone(fixture.factors);heights[0].height++;
 assert.throws(()=>assemble(heights,fixture.fragments),/height does not match/);
 assert.throws(()=>assemble(fixture.factors,[]),/Missing braid/);
});
