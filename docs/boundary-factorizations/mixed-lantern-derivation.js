(() => {
  const status=document.getElementById('status');
  const board=document.getElementById('storyboard');
  function equation(powers){
    return 'T₀²'+powers.map((power,i)=>power?` · T${i+1}${power===1?'':`^${power}`}`:'').join('');
  }
  function stageCard(stage,index){
    const card=document.createElement('section');card.className='stage';card.id=`stage-${index}`;
    const title=document.createElement('h2');title.textContent=stage.title;
    const left=document.createElement('p');left.className='equation';left.textContent=equation(stage.inner_powers);
    const equals=document.createElement('p');equals.textContent='= ordered product below';
    const rows=document.createElement('div');rows.className='factor-list';
    stage.rows.forEach((factor,position)=>{
      const row=document.createElement('div');row.className='factor-row';
      if(stage.highlight_rows.includes(position))row.classList.add('changed');
      const id=document.createElement('b');id.textContent=factor.id;
      const image=document.createElement('img');image.src=factor.svg;
      image.alt=`Curve enclosing inner boundaries ${factor.support.join(', ')}`;
      image.loading='lazy';
      const full=document.createElement('a');full.href=factor.svg;
      full.target='_blank';full.rel='noopener';full.title='Open full-size curve SVG';
      full.append(image);
      const label=document.createElement('span');label.className='block';
      label.textContent=`T{${factor.support.join(',')}}`;
      row.title=`Factor ${factor.id}; conjugator ${factor.conjugator.join(', ')||'identity'}`;
      row.append(id,full,label);rows.append(row);
    });
    card.append(title,left,equals,rows);return card;
  }
  function arrow(caption){
    const move=document.createElement('div');move.className='move';
    const mark=document.createElement('strong');mark.textContent='→';mark.setAttribute('aria-hidden','true');
    const label=document.createElement('span');label.textContent=caption;
    move.append(mark,label);return move;
  }
  async function load(){
    try{
      const requested=new URLSearchParams(location.search).get('type')||'26';
      const files={'21':'type21-lantern-states.json','26':'mixed-lantern-states.json','28':'type28-lantern-states.json','31':'type31-lantern-states.json','32':'type32-lantern-states.json'};
      if(!files[requested])throw Error('Choose one of the linked relation types');
      const response=await fetch(`data/${files[requested]}`);
      if(!response.ok)throw Error(`HTTP ${response.status}`);
      const data=await response.json();
      if(data.n!==5||!Array.isArray(data.stages)||!Array.isArray(data.moves)||
          data.stages.length<3||data.stages.length!==data.moves.length+1)
        throw Error('Incomplete certified state sequence');
      const catalog=document.getElementById('catalog-link');
      catalog.href=`double-outer.html?n=5#pattern-${data.target_pattern}`;
      catalog.textContent=`Five-boundary type ${data.target_pattern}`;
      document.title=`Type ${data.target_pattern}: five-boundary Hurwitz–lantern derivation`;
      document.getElementById('moving-factor').textContent=data.move_description;
      const twist=support=>`T{${support.join(',')}}`;
      document.getElementById('lantern-equation').textContent=
        `The final framed lantern is ${data.lantern_pair_supports.map(twist).join(' · ')} = ${twist(data.lantern_support)} · ${data.lantern_support.map(i=>`T${i}`).join(' · ')} for the routed curves shown. Replacing the three pair twists lowers the boundary powers at ${data.lantern_support.join(', ')} by one. This is a framed inner-boundary relation; its marked-point projection has different bookkeeping.`;
      const nav=document.getElementById('stage-nav');nav.replaceChildren();
      for(let index=0;index<data.stages.length;index++){
        if(index)board.append(arrow(data.moves[index-1]));
        board.append(stageCard(data.stages[index],index));
        const jump=document.createElement('a');jump.href=`#stage-${index}`;
        jump.textContent=index===0?'Start':index===data.stages.length-1?'Lantern':`Swap ${index}`;
        nav.append(jump);
      }
      status.textContent=`${data.stages.length} exact framed states · ${data.moves.length-1} Hurwitz moves · one inverse lantern`;
      if(location.hash)document.getElementById(location.hash.slice(1))?.scrollIntoView({block:'nearest'});
    }catch(error){status.textContent=`Could not load the derivation: ${error.message}`}
  }
  load();
})();
