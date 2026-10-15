(() => {
  const size = document.getElementById('size');
  const list = document.getElementById('relations');
  const status = document.getElementById('status');
  const source = 'https://www.math.fsu.edu/~hironaka/papers/lantern.pdf';
  const names = {
    3: ['Exterior twist itself', 'Lantern'],
    4: ['Exterior twist itself', 'Daisy', 'Rose'],
    5: ['Exterior twist itself', 'Daisy', 'Two triple supports', 'Doubled daisy', 'Rose'],
  };
  const requestedSize = Number(new URLSearchParams(location.search).get('n'));
  if (names[requestedSize]) size.value = String(requestedSize);
  let generation = 0;

  function supportSvg(n, block) {
    const width=60+32*(n-1), xs=block.map(i=>30+32*(i-1)), left=xs[0], right=xs[xs.length-1];
    let path=`M${left-9} 12 H${right+9} V54 H${right-9} V26`;
    for(let i=xs.length-2;i>=0;i--) path+=` H${xs[i]+9} V54 H${xs[i]-9} V26`;
    path+=` H${left-9} V12 Z`;
    const holes=Array.from({length:n},(_,i)=>`<g><circle cx="${30+32*i}" cy="43" r="5" fill="${block.includes(i+1)?'#bcebdc':'white'}" stroke="#405d53" stroke-width="1.1"/><text x="${30+32*i}" y="61" text-anchor="middle" font-size="9" fill="#42574f">${i+1}</text></g>`).join('');
    return `<svg viewBox="0 0 ${width} 67" role="img" aria-label="Support schematic enclosing boundaries ${block.join(', ')}"><rect x="2" y="2" width="${width-4}" height="63" rx="24" fill="white" stroke="#607a6d" stroke-width="1.1"/><path d="${path}" fill="#f9dff4" fill-opacity=".65" stroke="#a3338f" stroke-width="1.6" stroke-linejoin="round"/>${holes}</svg>`;
  }
  function powers(n, factors) {
    return Array.from({length:n},(_,i)=>factors.filter(block=>block.includes(i+1)).length-1);
  }
  function renderPair(n, i, j, first, second, index=null) {
    const factors=[...first.ordered_factors,...second.ordered_factors];
    const a=powers(n,first.ordered_factors), b=powers(n,second.ordered_factors);
    const section=document.createElement('section');section.className='pattern';
    const title=document.createElement('h2');title.textContent=`${index===null?'':`${index}. `}${names[n][i]} + ${names[n][j]}`;section.append(title);
    const badge=document.createElement('span');badge.className='badge found';badge.textContent='Certified composition';title.append(badge);
    const equation=document.createElement('p');equation.className='equation';
    equation.textContent=`T₀²${a.map((v,k)=>v+b[k]>0?` · T${k+1}${v+b[k]===1?'':`^${v+b[k]}`}`:'').join('')} = ${factors.length} positive twists below`;
    section.append(equation);
    const lists=document.createElement('div');lists.className='double-pair';
    for(const [label,relation,offset] of [['First exterior twist',first,0],['Second exterior twist',second,first.ordered_factors.length]]) {
      const group=document.createElement('div');const heading=document.createElement('h3');heading.textContent=label;group.append(heading);
      const rows=document.createElement('div');rows.className='factor-list';
      relation.ordered_factors.forEach((block,index)=>{const row=document.createElement('div');row.className='factor-row';const number=document.createElement('b');number.textContent=String(offset+index+1);row.append(number);row.insertAdjacentHTML('beforeend',supportSvg(n,block));rows.append(row)});
      group.append(rows);lists.append(group);
    }
    section.append(lists);
    const note=document.createElement('p');note.className='source';note.textContent='Factor order is top to bottom, first relation followed by second. Curves are support schematics; the exact line equations for each component are on its single-twist page.';section.append(note);
    return section;
  }
  function renderOpen(n, blocks, index) {
    const section=document.createElement('section');section.className='pattern';
    const title=document.createElement('h2');title.textContent=`${index}. Additional pair-twice candidate`;section.append(title);
    const badge=document.createElement('span');badge.className='badge open';badge.textContent='Relation open';title.append(badge);
    const degrees=Array.from({length:n},(_,i)=>blocks.filter(block=>block.includes(i+1)).length-2);
    const equation=document.createElement('p');equation.className='equation';
    equation.textContent=`Candidate: T₀²${degrees.map((power,i)=>power>0?` · T${i+1}${power===1?'':`^${power}`}`:'').join('')}`;
    section.append(equation);
    const rows=document.createElement('div');rows.className='blocks';
    const label=document.createElement('span');label.className='muted';label.textContent='Unordered support rows:';rows.append(label);
    blocks.forEach(block=>{const chip=document.createElement('span');chip.className='block';chip.textContent=`{${block.join(',')}}`;rows.append(chip)});
    section.append(rows);
    const note=document.createElement('p');note.className='source';note.textContent='Every pair occurs twice, but no ordered mapping-class equality has been certified for this type yet.';section.append(note);
    return section;
  }
  function renderDirect(n, direct, index) {
    const section=document.createElement('section');section.className='pattern';
    const title=document.createElement('h2');
    title.textContent=direct.hurwitz_positions ? `${index}. Hurwitz–lantern reduction` :
      n===5 ? `${index}. Five-boundary lift of ${direct.core_factor_count}-factor relation` :
      `${index}. ${direct.factors.length===4?'Four-triple relation':
      direct.factors.length===6?'One lantern expansion':'Two lantern expansions'}`;
    const badge=document.createElement('span');badge.className='badge found';
    badge.textContent='Exact framed relation';title.append(badge);section.append(title);
    const equation=document.createElement('p');equation.className='equation';
    equation.textContent=`T₀²${direct.inner_powers.map((power,i)=>power>0?
      ` · T${i+1}${power===1?'':`^${power}`}`:'').join('')} = ${direct.factors.length} positive twists below`;
    section.append(equation);
    const rows=document.createElement('div');rows.className='factor-list';
    direct.factors.forEach((factor,position)=>{
      if(n===5 && !direct.hurwitz_positions &&
          [0,direct.core_factor_count,direct.core_factor_count+4].includes(position)){
        const group=document.createElement('div');group.className='group-label';
        group.textContent=position===0?'Four-boundary core':
          position===direct.core_factor_count?'First daisy petal cycle':'Second daisy petal cycle';
        rows.append(group);
      }
      const row=document.createElement('div');row.className='factor-row';
      const number=document.createElement('b');number.textContent=String(position+1);
      const picture=document.createElement('img');picture.src=factor.svg;
      picture.alt=`Twist enclosing boundaries ${factor.support.join(', ')}`;
      picture.loading='lazy';
      row.title=`T${factor.support.join('')}; braid conjugator ${factor.conjugator.join(', ')||'identity'}`;
      const support=document.createElement('span');support.className='block';
      support.textContent=`T{${factor.support.join(',')}}`;
      row.append(number,picture,support);rows.append(row);
    });
    section.append(rows);
    if(n===4 || n===5){
      const derivation=document.createElement('p');derivation.className='source';
      const link=document.createElement('a');
      link.href=`four-triple-derivation.html#stage-${n===4?direct.factors.length:
        direct.hurwitz_positions?6:direct.core_factor_count}`;
      link.textContent=n===4?'View this relation in the graphical four-triple derivation':
        direct.hurwitz_positions?'View the six-factor four-boundary source relation':
        'View the four-boundary core and its lantern substitutions';
      derivation.append(link);section.append(derivation);
    }
    if(direct.hurwitz_positions){
      const replay=document.createElement('p');replay.className='source';
      const link=document.createElement('a');link.href='mixed-lantern-derivation.html';
      link.textContent='Replay every Hurwitz move and the inverse lantern graphically';
      replay.append(link);section.append(replay);
    }
    const note=document.createElement('p');note.className='source';
    note.textContent=direct.hurwitz_positions?
      'Starting from the 14-factor five-boundary lift, move its fourth twist downward across the next three factors by exact Hurwitz moves. The resulting consecutive T{2,3}, T{3,5}, T{2,5} are the puncture-capped lantern for T{2,3,5}; the framed replacement lowers the boundary powers at 2, 3, and 5 by one. Exact B₅ action and all five framings certify the final product.':
      n===5?
      'The framed five-boundary daisy gives P·L = T₀·T₁·T₂·T₃·T₄·T₅³, with P the four-boundary outer twist and L the four-petal cycle. The products P and L commute. Replacing P² by the four-triple relation gives the displayed correction powers. Exact B₅ Artin action and all five boundary framings certify the order; every curve is rendered from its individual isotopy class.':
      'The exact B₄ Artin action equals the double exterior twist. Inner-boundary framing counts agree as shown on the left; the capping kernel then certifies the framed equality. These curves are rendered from their individual exact isotopy classes.';
    section.append(note);
    return section;
  }
  async function load() {
    const request=++generation,n=Number(size.value);
    status.textContent='Loading certified relations…';list.replaceChildren();
    try {
      const response=await fetch(`data/${n}-relations.json`);if(!response.ok)throw Error(`HTTP ${response.status}`);
      const data=await response.json();if(request!==generation)return;
      const expected=names[n].length;
      for(let i=0;i<expected;i++)if(!data[String(i)])throw Error(`missing relation ${i+1}`);
      const intro=document.createElement('p');intro.className='source';intro.innerHTML=`Certified compositions use <a href="${source}">Hironaka’s line-arrangement theorem</a>; their exact line equations are on <a href="${n}.html">the ${n}-boundary page</a>. Direct four- and five-inner relations use exact braid and framing checks. Pair-twice candidates without a certificate are kept separate.`;list.append(intro);
      const fragment=document.createDocumentFragment();let found=0,total=0;
      if(n<=5){
        const candidatesResponse=await fetch(`data/${n}-double.json`);if(!candidatesResponse.ok)throw Error(`catalog HTTP ${candidatesResponse.status}`);
        const candidates=await candidatesResponse.json();if(request!==generation)return;
        for(const [index,pattern] of candidates.patterns.entries()){
          let entry;
          if(pattern.direct){entry=renderDirect(n,pattern.direct,index+1);found++}
          else if(pattern.composition){const [i,j]=pattern.composition;entry=renderPair(n,i,j,data[String(i)],data[String(j)],index+1);found++}
          else entry=renderOpen(n,pattern.blocks,index+1);
          entry.id=`pattern-${index+1}`;fragment.append(entry);
          total++;
        }
      } else {
        for(let i=0;i<expected;i++)for(let j=i;j<expected;j++){fragment.append(renderPair(n,i,j,data[String(i)],data[String(j)]));total++;found++}
      }
      list.append(fragment);status.textContent=`${total} pair-twice types · ${found} certified positive relations`;
      if(location.hash)document.getElementById(location.hash.slice(1))?.scrollIntoView();
    } catch(error) {if(request===generation)status.textContent=`Could not load relations: ${error.message}`}
  }
  size.addEventListener('change',load);
  load();
})();
