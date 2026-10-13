(() => {
  const n = Number(document.body.dataset.n);
  const list = document.getElementById('patterns');
  const status = document.getElementById('status');
  const jump = document.getElementById('jump');
  const source = 'https://www.math.fsu.edu/~hironaka/papers/lantern.pdf';
  let wanted = 0;

  function completeLines(large) {
    const used = new Set(), result = large.map(block => [...block]);
    for (const block of large) for (let i=0;i<block.length;i++) for(let j=i+1;j<block.length;j++)
      used.add(`${block[i]},${block[j]}`);
    for(let i=1;i<=n;i++) for(let j=i+1;j<=n;j++) if(!used.has(`${i},${j}`)) result.push([i,j]);
    return result.sort((a,b)=>b.length-a.length||a.join(',').localeCompare(b.join(',')));
  }
  function nameOf(large) {
    if(n<=2 || (large.length===1 && large[0].length===n)) return 'Exterior twist itself';
    if(!large.length) return n===3?'Lantern / rose':'Rose (generalized lantern)';
    if(large.length===1 && large[0].length===n-1) return 'Daisy';
    if(n>=5 && large.length===1 && large[0].length===n-2) return 'Doubled daisy';
    return 'Line-arrangement relation';
  }
  function sizeProfile(blocks) {
    return [...new Set(blocks.map(b=>b.length))].sort((a,b)=>b-a)
      .map(size=>`${size}×${blocks.filter(b=>b.length===size).length}`).join(' · ') || 'annulus';
  }
  function supportSvg(block) {
    const width=60+32*(n-1), xs=block.map(i=>30+32*(i-1)), left=xs[0], right=xs[xs.length-1];
    let path=`M${left-9} 12 H${right+9} V54 H${right-9} V26`;
    for(let i=xs.length-2;i>=0;i--) path+=` H${xs[i]+9} V54 H${xs[i]-9} V26`;
    path+=` H${left-9} V12 Z`;
    const holes=Array.from({length:n},(_,i)=>`<g><circle cx="${30+32*i}" cy="43" r="5" fill="${block.includes(i+1)?'#bcebdc':'white'}" stroke="#405d53" stroke-width="1.1"/><text x="${30+32*i}" y="61" text-anchor="middle" font-size="9" fill="#42574f">${i+1}</text></g>`).join('');
    return `<svg viewBox="0 0 ${width} 67" role="img" aria-label="Support schematic enclosing boundaries ${block.join(', ')}"><rect x="2" y="2" width="${width-4}" height="63" rx="24" fill="white" stroke="#607a6d" stroke-width="1.1"/><path d="${path}" fill="#f9dff4" fill-opacity=".65" stroke="#a3338f" stroke-width="1.6" stroke-linejoin="round"/>${holes}</svg>`;
  }
  function matrixDetails(blocks) {
    const details=document.createElement('details'); details.className='details';
    const summary=document.createElement('summary');summary.textContent='Show incidence matrix';details.append(summary);
    details.addEventListener('toggle',()=>{
      if(!details.open || details.querySelector('table'))return;
      const table=document.createElement('table');table.className='matrix';
      let row=document.createElement('tr');for(const label of ['Twist',...Array.from({length:n},(_,i)=>String(i+1))]){const cell=document.createElement('th');cell.textContent=label;row.append(cell)}table.append(row);
      blocks.forEach((block,i)=>{row=document.createElement('tr');const label=document.createElement('th');label.textContent=`${i+1}: {${block.join(',')}}`;row.append(label);for(let j=1;j<=n;j++){const cell=document.createElement('td');if(block.includes(j)){cell.className='on';cell.textContent='●'}row.append(cell)}table.append(row)});
      details.append(table);
    });
    return details;
  }
  function card(index,large,certificate) {
    const blocks=completeLines(large), section=document.createElement('section');section.className='pattern';section.id=`p${index+1}`;
    const title=document.createElement('h2');title.textContent=`${index+1}. ${sizeProfile(blocks)}`;section.append(title);
    const known=(n<=2 && index===0) || !!certificate;
    const badge=document.createElement('span');badge.className=`badge ${known?'found':'open'}`;badge.textContent=known?'Positive relation found':'Search open';title.append(badge);
    const placeholder=document.createElement('div');placeholder.className='blocks';
    const label=document.createElement('span');label.className='muted';label.textContent='Candidate rows:';placeholder.append(label);
    for(const block of blocks){const chip=document.createElement('span');chip.className='block';chip.textContent=`{${block.join(',')}}`;placeholder.append(chip)}
    if(!blocks.length){const chip=document.createElement('span');chip.className='block';chip.textContent='no non-singleton row';placeholder.append(chip)}
    section.append(placeholder,matrixDetails(blocks));
    if(!known){const p=document.createElement('p');p.className='muted';p.textContent='The pair counts fit, but the current bounded search has not found an ordered positive relation. This does not establish impossibility.';section.append(p);return section}
    const relation=document.createElement('div');relation.className='relation';
    const h=document.createElement('h3');h.textContent=nameOf(large);relation.append(h);
    const degrees=Array.from({length:n},(_,i)=>blocks.filter(b=>b.includes(i+1)).length);
    const powers=degrees.map(d=>d-1);
    const equation=document.createElement('p');equation.className='equation';
    equation.textContent=n===1?'T₀ = T₁':`T₀${powers.map((q,i)=>q>0?` · T${i+1}${q===1?'':`^${q}`}`:'').join('')} = ordered positive twists below`;
    relation.append(equation);
    const factors=certificate?certificate.ordered_factors:(n===1?[[1]]:[Array.from({length:n},(_,i)=>i+1)]);
    const rows=document.createElement('div');rows.className='factor-list';
    factors.forEach((block,i)=>{const item=document.createElement('div');item.className='factor-row';const number=document.createElement('b');number.textContent=String(i+1);item.append(number);item.insertAdjacentHTML('beforeend',supportSvg(block));rows.append(item)});
    relation.append(rows);
    const caution=document.createElement('p');caution.className='source';
    caution.textContent=certificate?'The vertical pictures show enclosed boundary sets schematically. The actual isotopy routes and this factor order come from the certified line arrangement; the drawn loop shape alone is not an equality proof.':'This is the tautological boundary twist.';
    relation.append(caution);
    if(certificate){const sourceLine=document.createElement('p');sourceLine.className='source';sourceLine.innerHTML=`Exact real-line certificate · <a href="${source}">Hironaka, Theorem 1.2</a>`;relation.append(sourceLine);
      const details=document.createElement('details');details.className='details';const summary=document.createElement('summary');summary.textContent='Show exact line equations and crossing order';details.append(summary);
      const pre=document.createElement('pre');pre.className='coordinates';pre.textContent=certificate.slopes.map((m,i)=>`L${i+1}: y = (${m})x + (${certificate.intercepts[i]})`).join('\n')+'\nIncreasing x order: '+certificate.ordered_factors.map(b=>'{'+b.join(',')+'}').join(' → ');
      details.append(pre);relation.append(details)}
    section.append(relation);return section;
  }
  async function load() {
    try {
      const response=await fetch(`data/${n}.json`);if(!response.ok)throw Error(`catalog HTTP ${response.status}`);
      const data=await response.json();if(data.n!==n)throw Error('catalog size mismatch');
      let certificates={};try{const relationResponse=await fetch(`data/${n}-relations.json`);if(relationResponse.ok)certificates=await relationResponse.json()}catch{}
      let index=0;const total=data.types.length,found=Object.keys(certificates).length+(n<=2?1:0);
      status.textContent=`${total} patterns · ${found} positive relations found · drawing page…`;
      function batch(){const fragment=document.createDocumentFragment(),end=Math.min(index+75,total);
        for(;index<end;index++)fragment.append(card(index,data.types[index],certificates[String(index)]));
        list.append(fragment);status.textContent=`${index} of ${total} patterns drawn · ${found} positive relations found`;
        if(wanted && document.getElementById(`p${wanted}`)) {document.getElementById(`p${wanted}`).scrollIntoView();wanted=0}
        if(index<total)requestAnimationFrame(batch);else status.textContent=`All ${total} patterns shown · ${found} positive relations found`}
      requestAnimationFrame(batch);
    } catch(error) {status.textContent=`Catalog failed to load: ${error.message}`}
  }
  jump.addEventListener('change',()=>{const value=Number(jump.value);if(!Number.isInteger(value)||value<1)return;const target=document.getElementById(`p${value}`);if(target)target.scrollIntoView();else wanted=value});
  load();
})();
