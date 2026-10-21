/* Stack shared Python-rendered fragments; no crossing geometry or algebra is recomputed. */
(function(root){
 'use strict';
 const colors=['#d73027','#e08214','#b59b00','#23964f','#168aad','#5254c8'];
 function assemble(factors,fragments){
  let order=[0,1,2,3,4,5],top=0;const parts=[];
  factors.forEach((factor,index)=>{
   const fragment=fragments[factor.braid],height=factor.height;
   if(typeof fragment!=='string')throw Error('Missing braid fragment');
   const declared=fragment.match(/data-word="([^"]*)"/);
   if(!declared||declared[1]!==factor.word.join(' '))throw Error('Braid fragment does not match its factor word');
   const declaredHeight=fragment.match(/height="(\d+)"/);
   if(!declaredHeight||Number(declaredHeight[1])!==height)throw Error('Braid fragment height does not match its factor row');
   let content=fragment.slice(fragment.indexOf('>')+1,fragment.lastIndexOf('</svg>'));
   content=content.replace(/<path data-strand="(\d+)"([^>]*?)stroke="[^"]+"/g,(_,identity,rest)=>
    `<path data-strand="${identity}"${rest}stroke="${colors[order[Number(identity)]]}"`);
   parts.push(`<g data-factor="${index}" transform="translate(0 ${top})">${content}</g>`);
   for(const letter of factor.word){const i=Math.abs(letter)-1;if(!Number.isInteger(letter)||i<0||i>=5)throw Error('Invalid braid generator');[order[i],order[i+1]]=[order[i+1],order[i]];}
   top+=height;
   if(index+1<factors.length)parts.push(`<path class="factor-separator" d="M 3 ${top} H 83" stroke="#2563eb" stroke-width=".8" stroke-dasharray="2 3"/>`);
  });
  return {svg:`<svg xmlns="http://www.w3.org/2000/svg" width="86" height="${top}" viewBox="0 0 86 ${top}" role="img" aria-label="Continuous six-strand braid">${parts.join('')}</svg>`,height:top,exitOrder:order};
 }
 if(typeof module!=='undefined'&&module.exports)module.exports={assemble};
 else root.connectedBraid={assemble};
})(typeof window==='undefined'?globalThis:window);
