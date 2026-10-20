import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fold,alignments,sameSurface,stopsFor,nextStop,sub,dot} from '../experiments/common_nets/game/geometry.mjs';
const base=new URL('../experiments/common_nets/game/',import.meta.url);
const index=JSON.parse(readFileSync(new URL('cubes-index.json',base)));
const nets=index.puzzles.map(p=>JSON.parse(readFileSync(new URL(p.file,base))));
test('all square-panel targets reconstruct from their signed hinge angles',()=>{
  let count=0;
  for(const net of nets){
    assert.equal(net.family,'cubes');assert.equal(net.allowMirrors,false);
    assert.equal(net.faces.length,4*net.units+2);
    assert.deepEqual(fold(net,net.hinges.map(()=>0)),net.faces);
    for(const target of net.targets){
      const faces=fold(net,target.angles);assert.equal(faces.length,target.faces.length);
      faces.forEach((f,i)=>{assert.equal(f.length,4);f.forEach((p,j)=>assert.ok(Math.hypot(...sub(p,target.faces[i][j]))<1e-7,net.id+'/'+target.id));});
      target.angles.forEach(a=>assert.ok(stopsFor(net).some(s=>Math.abs(a-s)<1e-7)));
      assert.ok(sameSurface(faces,[target.faces],1e-7));count++;
    }
  }
  assert.equal(count,796);assert.equal(nets.length,35);
});
test('square hinges preserve both endpoints and every panel edge at arbitrary angles',()=>{
  for(const net of nets){
    const faces=fold(net,net.hinges.map((_,i)=>Math.sin(i+1)*2));
    faces.forEach(face=>face.forEach((p,j)=>{const d=sub(p,face[(j+1)%4]);assert.ok(Math.abs(dot(d,d)-1)<1e-9);}));
    net.hinges.forEach(([a,b,e])=>{
      for(const j of [e,(e+1)%4]){
        const local=net.faces[b].findIndex(p=>Math.hypot(...sub(p,net.faces[a][j]))<1e-10);
        assert.ok(local>=0);assert.ok(Math.hypot(...sub(faces[a][j],faces[b][local]))<1e-9);
      }
    });
  }
});
test('classic sets, larger examples, and chirality have explicit scope',()=>{
  const classic=nets.find(n=>n.id==='C4A'),five=nets.find(n=>n.id==='C5A');
  assert.equal(classic.targets.length,7);assert.equal(five.targets.length,23);
  assert.equal(nets.filter(n=>n.units===1).length,11);
  for(let n=1;n<=8;n++)assert.ok(nets.some(p=>p.units===n));
  assert.ok(nets.find(n=>n.units===8&&n.targets.length===241));
  let chiral=0;
  for(const t of classic.targets){
    const mirror=t.faces.map(f=>f.map(([x,y,z])=>[-x,y,z]));
    if(!sameSurface(t.faces,alignments(mirror,classic.faces[0],false)))chiral++;
    assert.ok(sameSurface(t.faces,alignments(mirror,classic.faces[0],true)));
  }
  assert.equal(chiral,2,'The classic seven include one chiral pair');
  assert.equal(nextStop(0,1,stopsFor(classic)),Math.PI/2);
  assert.equal(nextStop(0,-1,stopsFor(classic)),-Math.PI/2);
});
