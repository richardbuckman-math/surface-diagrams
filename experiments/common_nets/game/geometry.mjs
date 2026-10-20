// The tree kinematics are independent of rendering and interaction.
export const add=(a,b)=>a.map((v,i)=>v+b[i]);
export const sub=(a,b)=>a.map((v,i)=>v-b[i]);
export const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0);
export const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
export const unit=a=>a.map(v=>v/Math.hypot(...a));
export const normal=t=>unit(cross(sub(t[1],t[0]),sub(t[2],t[0])));
const identity=()=>[[1,0,0],[0,1,0],[0,0,1]];
const mul=(m,p)=>m.map(row=>dot(row,p));
const matrix=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((s,v,k)=>s+v*b[k][j],0)));
function rotation([x,y,z],a){
  const c=Math.cos(a),s=Math.sin(a),d=1-c;
  return [[c+x*x*d,x*y*d-z*s,x*z*d+y*s],
          [y*x*d+z*s,c+y*y*d,y*z*d-x*s],
          [z*x*d-y*s,z*y*d+x*s,c+z*z*d]];
}
export function fold(net,angles){
  if(angles.length!==net.hinges.length)throw Error('Wrong hinge count');
  const poses=[{r:identity(),t:[0,0,0]}];
  net.hinges.forEach(([parent,child,edge],i)=>{
    if(!poses[parent]||poses[child])throw Error('Hinges must be a rooted tree');
    const p=poses[parent],a=net.faces[parent][edge],b=net.faces[parent][(edge+1)%3];
    const pivot=add(mul(p.r,a),p.t),axis=unit(mul(p.r,sub(b,a)));
    const r=matrix(rotation(axis,angles[i]),p.r);
    poses[child]={r,t:sub(pivot,mul(r,a))};
  });
  return net.faces.map((face,i)=>face.map(p=>add(mul(poses[i].r,p),poses[i].t)));
}
function basis(t){const u=unit(sub(t[1],t[0])),d=sub(t[2],t[0]);const v=unit(sub(d,u.map(x=>dot(d,u)*x)));return [u,v,cross(u,v)];}
// A rigid alignment from each target face flag to the fixed paper root
// accepts alternate panel assignments, paper sides, and mirror targets.
export function alignments(target,root){
  const output=[],b=basis(root);
  for(const face of target)for(const h of [1,-1])for(let r=0;r<3;r++){
    const a=[0,1,2].map(j=>face[(r+h*j+3)%3]),u=basis(a);
    for(const side of [1,-1])output.push(target.map(t=>t.map(p=>{
      const xyz=u.map(v=>dot(sub(p,a[0]),v));xyz[2]*=side;
      return root[0].map((v,i)=>v+xyz.reduce((s,x,k)=>s+x*b[k][i],0));
    })));
  }
  return output;
}
export function sameSurface(faces,targets,tolerance=.012){
  const limit=tolerance*tolerance;
  const close=(a,b)=>dot(sub(a,b),sub(a,b))<limit;
  return targets.some(target=>{
    if(target.length!==faces.length)return false;
    const used=new Set();
    return faces.every(face=>{
      const i=target.findIndex((t,j)=>!used.has(j)&&face.every(p=>t.some(q=>close(p,q))));
      if(i<0)return false;used.add(i);return true;
    });
  });
}
// Every crease around a polytet edge contains one through five units.
const tetraDihedral=Math.acos(1/3);
export const stops=[...new Set([0,Math.PI,-Math.PI,...[1,2,3,4,5].flatMap(k=>[Math.PI-k*tetraDihedral,k*tetraDihedral-Math.PI])])].sort((a,b)=>a-b);
export const clamp=a=>Math.max(-Math.PI,Math.min(Math.PI,a));
export function snap(a,threshold=4*Math.PI/180){const best=stops.reduce((b,v)=>Math.abs(v-a)<Math.abs(b-a)?v:b,stops[0]);return Math.abs(best-a)<=threshold?best:a;}
export function nextStop(a,direction){return direction>0?(stops.find(v=>v>a+1e-7)??Math.PI):([...stops].reverse().find(v=>v<a-1e-7)??-Math.PI);}
