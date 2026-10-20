import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fold,alignments,sameSurface,stops,snap,nextStop,sub,dot} from '../experiments/common_nets/game/geometry.mjs';
const data=JSON.parse(readFileSync(new URL('../experiments/common_nets/game/data.json',import.meta.url)));
test('every published challenge is reconstructed from hinge angles',()=>{
  let count=0;
  for(const net of data.puzzles)for(const target of net.targets){
    const faces=fold(net,target.angles);
    faces.forEach((t,i)=>t.forEach((p,j)=>assert.ok(Math.hypot(...sub(p,target.faces[i][j]))<1e-7,net.id+'/'+target.id)));
    target.angles.forEach(a=>assert.ok(stops.some(s=>Math.abs(a-s)<1e-7),'Valid crease must exist'));
    assert.ok(sameSurface(faces,[target.faces],1e-7));count++;
  }
  assert.equal(count,321);assert.equal(data.puzzles.length,11);
});
test('all hinges retain both endpoints and all panels stay rigid',()=>{
  for(const net of data.puzzles){
    const flat=fold(net,net.hinges.map(()=>0));assert.deepEqual(flat,net.faces);
    const faces=fold(net,net.hinges.map((_,i)=>Math.sin(i+1)*2));
    faces.forEach(t=>t.forEach((p,j)=>assert.ok(Math.abs(dot(sub(p,t[(j+1)%3]),sub(p,t[(j+1)%3]))-1)<1e-9)));
    net.hinges.forEach(([a,b,e])=>{
      for(const j of [e,(e+1)%3]){
        const local=net.faces[b].findIndex(p=>Math.hypot(...sub(p,net.faces[a][j]))<1e-10);
        assert.ok(local>=0);assert.ok(Math.hypot(...sub(faces[a][j],faces[b][local]))<1e-9);
      }
    });
  }
});
test('success accepts rigid reorientation and mirrors, rejects wrong geometry',()=>{
  const net=data.puzzles[0],target=net.targets[0];
  const moved=target.faces.map(t=>t.map(([x,y,z])=>[2-z,y+1,x-4]));
  assert.ok(sameSurface(target.faces,alignments(moved,net.faces[0])));
  const mirrored=target.faces.map(t=>t.map(([x,y,z])=>[-x,y,z]));
  assert.ok(sameSurface(target.faces,alignments(mirrored,net.faces[0])));
  assert.equal(sameSurface(net.faces,alignments(target.faces,net.faces[0])),false);
  const bad=target.faces.map(t=>t.map(p=>p.map(v=>v*1.02)));
  assert.equal(sameSurface(bad,[target.faces],.001),false);
});
test('snapping and key stepping can leave flat and traverse every crease',()=>{
  assert.equal(nextStop(0,1),stops.find(a=>a>0));
  assert.equal(nextStop(0,-1),[...stops].reverse().find(a=>a<0));
  assert.equal(nextStop(Math.PI,1),Math.PI);
  assert.equal(nextStop(-Math.PI,-1),-Math.PI);
  assert.equal(snap(stops[3]+.01),stops[3]);
  assert.equal(snap(.2),.2);
});
