// Offline, dependency-free inspection of the certified target meshes.
(() => {
  const models=JSON.parse(document.getElementById('models').textContent);
  const dialog=document.getElementById('viewer'),canvas=document.getElementById('model-canvas');
  const gl=canvas.getContext('webgl',{antialias:true});
  let yaw=.61,pitch=.44,mesh=null,buffers=[],drag=null;
  document.getElementById('viewer-close').onclick=()=>dialog.close();
  document.addEventListener('click',event=>{
    const link=event.target.closest('a');if(!link||!models[link.getAttribute('href')])return;
    if(!gl)return; // Keep the ordinary SVG link usable without WebGL.
    event.preventDefault();const file=link.getAttribute('href');
    const parts=file.match(/^(tetra|cube)-(\d+)-shape-(\d+)\.svg$/);
    document.getElementById('viewer-title').textContent=models[file].title || (parts?
      `${parts[2]} ${parts[1]==='tetra'?'tetrahedra':'cubes'} - shape ${Number(parts[3])}`:file);
    document.getElementById('viewer-download').href=file;
    mesh=models[file];yaw=.61;pitch=.44;dialog.showModal();upload();draw();
  });
  if(!gl){document.getElementById('viewer-status').textContent='3D rendering is unavailable here; use the SVG download.';return;}
  function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;}
  const program=gl.createProgram();
  gl.attachShader(program,shader(gl.VERTEX_SHADER,`attribute vec3 p,c,n; uniform mat3 view; uniform vec2 scale,shift; varying vec3 shade; void main(){vec3 q=view*p;gl_Position=vec4(q.xy*scale+shift,-q.z*.5,1.);shade=c*(.76+.24*max(0.,dot(normalize(view*n),normalize(vec3(.35,.4,.85)))));}`));
  gl.attachShader(program,shader(gl.FRAGMENT_SHADER,`precision mediump float;varying vec3 shade;uniform bool edge;void main(){gl_FragColor=vec4(edge?vec3(.15,.22,.29):shade,1.);}`));
  gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(program));gl.useProgram(program);
  const locations=Object.fromEntries(['p','c','n'].map(x=>[x,gl.getAttribLocation(program,x)]));
  const uniforms=Object.fromEntries(['view','scale','shift','edge'].map(x=>[x,gl.getUniformLocation(program,x)]));
  function normal(f){const a=f[1].map((x,i)=>x-f[0][i]),b=f[2].map((x,i)=>x-f[0][i]);const n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],s=Math.hypot(...n);return n.map(x=>x/s);}
  function upload(){
    if(!gl||!mesh)return;buffers.forEach(b=>gl.deleteBuffer(b.buffer));buffers=[];
    const triangles=[],lines=[];
    mesh.faces.forEach((f,i)=>{const n=normal(f),color=mesh.colors[i],vertex=p=>[...p,...color,...n];
      for(let j=1;j<f.length-1;j++)triangles.push(...vertex(f[0]),...vertex(f[j]),...vertex(f[j+1]));
      f.forEach((p,j)=>lines.push(...vertex(p),...vertex(f[(j+1)%f.length])));
    });
    for(const values of [triangles,lines]){const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(values),gl.STATIC_DRAW);buffers.push({buffer,count:values.length/9});}
  }
  function draw(){
    if(!gl||!mesh)return;
    const ratio=Math.min(2,devicePixelRatio||1);canvas.width=canvas.clientWidth*ratio;canvas.height=canvas.clientHeight*ratio;gl.viewport(0,0,canvas.width,canvas.height);
    const u=[-Math.sin(yaw),Math.cos(yaw),0],v=[-Math.cos(yaw)*Math.sin(pitch),-Math.sin(yaw)*Math.sin(pitch),Math.cos(pitch)],w=[Math.cos(yaw)*Math.cos(pitch),Math.sin(yaw)*Math.cos(pitch),Math.sin(pitch)];
    const points=mesh.faces.flat().map(p=>[p.reduce((s,x,i)=>s+x*u[i],0),p.reduce((s,x,i)=>s+x*v[i],0)]);
    const low=[0,1].map(i=>Math.min(...points.map(p=>p[i]))),high=[0,1].map(i=>Math.max(...points.map(p=>p[i]))),aspect=canvas.width/canvas.height;
    const scale=Math.min(1.65*aspect/(high[0]-low[0]),1.65/(high[1]-low[1]));
    gl.uniformMatrix3fv(uniforms.view,false,new Float32Array([u[0],v[0],w[0],u[1],v[1],w[1],u[2],v[2],w[2]]));
    gl.uniform2f(uniforms.scale,scale/aspect,scale);gl.uniform2f(uniforms.shift,-(low[0]+high[0])*scale/aspect/2,-(low[1]+high[1])*scale/2);
    gl.clearColor(.97,.98,.99,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);
    buffers.forEach((b,i)=>{gl.bindBuffer(gl.ARRAY_BUFFER,b.buffer);['p','c','n'].forEach((name,j)=>{gl.enableVertexAttribArray(locations[name]);gl.vertexAttribPointer(locations[name],3,gl.FLOAT,false,36,j*12);});gl.uniform1i(uniforms.edge,i);if(!i){gl.enable(gl.POLYGON_OFFSET_FILL);gl.polygonOffset(1,1);}else gl.disable(gl.POLYGON_OFFSET_FILL);gl.drawArrays(i?gl.LINES:gl.TRIANGLES,0,b.count);});
  }
  canvas.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId);});
  canvas.addEventListener('pointermove',e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.012;pitch=Math.max(-1.45,Math.min(1.45,pitch+(e.clientY-drag[1])*.012));drag=[e.clientX,e.clientY];draw();});
  canvas.addEventListener('pointerup',()=>drag=null);canvas.addEventListener('pointercancel',()=>drag=null);
  document.getElementById('viewer-left').onclick=()=>{yaw-=Math.PI/6;draw();};
  document.getElementById('viewer-right').onclick=()=>{yaw+=Math.PI/6;draw();};
  document.getElementById('viewer-above').onclick=()=>{pitch=Math.min(1.4,pitch+.2);draw();};
  document.getElementById('viewer-below').onclick=()=>{pitch=Math.max(-1.4,pitch-.2);draw();};
  window.addEventListener('resize',()=>{if(dialog.open)draw();});
})();
