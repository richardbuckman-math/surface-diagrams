import {normal,dot,sub} from './geometry.mjs?v=2';

export class View {
  constructor(canvas){
    this.canvas=canvas;this.yaw=.7;this.pitch=.65;this.faces=[];
    const gl=this.gl=canvas.getContext('webgl',{antialias:true});
    if(!gl)throw Error('This browser cannot start WebGL. Please try another browser; the PDF remains available.');
    function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;}
    this.program=gl.createProgram();
    gl.attachShader(this.program,shader(gl.VERTEX_SHADER,`attribute vec3 p,c,n; uniform mat3 view; uniform vec2 scale,shift,depth; varying vec3 shade; void main(){vec3 q=view*p;gl_Position=vec4(q.xy*scale+shift,q.z*depth.x+depth.y,1.);shade=c*(.73+.27*abs(dot(normalize(view*n),normalize(vec3(.35,.4,.85)))));}`));
    gl.attachShader(this.program,shader(gl.FRAGMENT_SHADER,`precision mediump float; varying vec3 shade; uniform bool edge; void main(){gl_FragColor=vec4(edge?vec3(.17,.25,.3):shade,1.);}`));
    gl.linkProgram(this.program);if(!gl.getProgramParameter(this.program,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(this.program));
    this.attributes=['p','c','n'].map(s=>gl.getAttribLocation(this.program,s));
    this.uniforms=Object.fromEntries(['view','scale','shift','depth','edge'].map(s=>[s,gl.getUniformLocation(this.program,s)]));
    this.buffers=[gl.createBuffer(),gl.createBuffer()];
    let drag=null;
    canvas.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId);canvas.focus({preventScroll:true});});
    canvas.addEventListener('pointermove',e=>{if(!drag)return;this.yaw+=(e.clientX-drag[0])*.01;this.pitch=Math.max(-1.5,Math.min(1.5,this.pitch+(e.clientY-drag[1])*.01));drag=[e.clientX,e.clientY];this.draw();});
    for(const event of ['pointerup','pointercancel'])canvas.addEventListener(event,()=>drag=null);
  }
  setMesh(faces,colors){this.faces=faces;this.colors=colors;this.draw();}
  project(p){
    const q=this.basis.map(v=>dot(v,p));
    return [(q[0]*this.scale[0]+this.shift[0]+1)*this.canvas.clientWidth/2,
            (1-q[1]*this.scale[1]-this.shift[1])*this.canvas.clientHeight/2,q[2]];
  }
  draw(){
    if(!this.faces.length)return;
    const {gl,canvas}=this;gl.useProgram(this.program);
    const ratio=Math.min(2,devicePixelRatio||1);canvas.width=Math.round(canvas.clientWidth*ratio);canvas.height=Math.round(canvas.clientHeight*ratio);
    gl.viewport(0,0,canvas.width,canvas.height);
    const u=[-Math.sin(this.yaw),Math.cos(this.yaw),0],v=[-Math.cos(this.yaw)*Math.sin(this.pitch),-Math.sin(this.yaw)*Math.sin(this.pitch),Math.cos(this.pitch)],w=[Math.cos(this.yaw)*Math.cos(this.pitch),Math.sin(this.yaw)*Math.cos(this.pitch),Math.sin(this.pitch)];
    this.basis=[u,v,w];const points=this.faces.flat().map(p=>[dot(p,u),dot(p,v)]);
    const low=[0,1].map(i=>Math.min(...points.map(p=>p[i]))),high=[0,1].map(i=>Math.max(...points.map(p=>p[i]))),aspect=canvas.width/canvas.height;
    const s=Math.min(1.65*aspect/Math.max(.001,high[0]-low[0]),1.65/Math.max(.001,high[1]-low[1]));
    this.scale=[s/aspect,s];this.shift=low.map((n,i)=>-(n+high[i])*this.scale[i]/2);
    gl.uniformMatrix3fv(this.uniforms.view,false,new Float32Array([u[0],v[0],w[0],u[1],v[1],w[1],u[2],v[2],w[2]]));
    gl.uniform2f(this.uniforms.scale,...this.scale);gl.uniform2f(this.uniforms.shift,...this.shift);
    const depths=this.faces.flat().map(p=>dot(p,w)),near=Math.min(...depths),far=Math.max(...depths),range=Math.max(1,far-near);
    gl.uniform2f(this.uniforms.depth,-1.8/range,(near+far)*.9/range);
    gl.clearColor(.984,.989,.992,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);
    const triangles=[],lines=[];
    this.faces.forEach((face,i)=>{const n=normal(face),vertex=p=>[...p,...this.colors[i],...n];for(let j=1;j<face.length-1;j++)triangles.push(...vertex(face[0]),...vertex(face[j]),...vertex(face[j+1]));face.forEach((p,j)=>lines.push(...vertex(p),...vertex(face[(j+1)%face.length])));});
    [triangles,lines].forEach((values,i)=>{
      gl.bindBuffer(gl.ARRAY_BUFFER,this.buffers[i]);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(values),gl.DYNAMIC_DRAW);
      this.attributes.forEach((a,j)=>{gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,3,gl.FLOAT,false,36,12*j);});
      gl.uniform1i(this.uniforms.edge,i);if(!i){gl.enable(gl.POLYGON_OFFSET_FILL);gl.polygonOffset(1,1);}else gl.disable(gl.POLYGON_OFFSET_FILL);
      gl.drawArrays(i?gl.LINES:gl.TRIANGLES,0,values.length/9);
    });
    if(this.onDraw)this.onDraw();
  }
  pickHinge(hinges,x,y){
    let best=-1,distance=24;
    hinges.forEach(([parent,child,e],i)=>{
      const a=this.project(this.faces[parent][e]),b=this.project(this.faces[parent][(e+1)%this.faces[parent].length]);
      const d=sub(b,a),t=Math.max(0,Math.min(1,((x-a[0])*d[0]+(y-a[1])*d[1])/(d[0]*d[0]+d[1]*d[1]||1)));
      const gap=Math.hypot(x-a[0]-t*d[0],y-a[1]-t*d[1]);
      if(gap<distance){distance=gap;best=i;}
    });return best;
  }
}
