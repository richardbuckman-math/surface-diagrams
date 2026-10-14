(() => {
  const holder=document.getElementById('derivation');
  const status=document.getElementById('status');
  const stages=[
    {index:3,count:4,title:'Four triple twists',note:'Seed relation; each of the four three-boundary supports occurs once.',changed:[]},
    {index:4,count:6,title:'Expand the fourth triple',note:'The twist on {2,3,4} becomes three pair twists.',changed:[3,4,5]},
    {index:6,count:8,title:'Expand the third triple',note:'The twist on {1,3,4} also becomes three pair twists.',changed:[2,3,4]},
  ];
  function equation(powers){
    return 'T₀²'+powers.map((p,i)=>p?` · T${i+1}${p===1?'':`^${p}`}`:'').join('');
  }
  function factorRow(factor,index,changed){
    const row=document.createElement('div');row.className='factor-row'+(changed?' expanded':'');
    const number=document.createElement('b');number.textContent=String(index+1);
    const img=document.createElement('img');img.src=factor.svg;img.alt=`Curve enclosing inner boundaries ${factor.support.join(', ')}`;img.loading='lazy';
    const support=document.createElement('span');support.className='block';support.textContent=`T{${factor.support.join(',')}}`;
    row.append(number,img,support);
    row.title=`Exact twist; conjugator ${factor.conjugator.join(', ')||'identity'}`;
    return row;
  }
  function stageCard(spec,relation){
    const card=document.createElement('section');card.className='stage';card.id=`stage-${spec.count}`;
    const heading=document.createElement('h2');heading.textContent=spec.title;
    const left=document.createElement('p');left.className='equation';left.textContent=equation(relation.inner_powers);
    const equals=document.createElement('p');equals.textContent='= ordered product below';
    const rows=document.createElement('div');rows.className='factor-list';
    relation.factors.forEach((factor,index)=>rows.append(factorRow(factor,index,spec.changed.includes(index))));
    const note=document.createElement('p');note.className='source';note.textContent=spec.note;
    card.append(heading,left,equals,rows,note);return card;
  }
  function arrow(text){
    const move=document.createElement('div');move.className='move';
    const mark=document.createElement('strong');mark.textContent='→';mark.setAttribute('aria-hidden','true');
    const caption=document.createElement('span');caption.textContent=text;
    move.append(mark,caption);return move;
  }
  async function load(){
    try{
      const response=await fetch('data/4-double.json');if(!response.ok)throw Error(`HTTP ${response.status}`);
      const data=await response.json();
      const relations=stages.map(spec=>data.patterns[spec.index]?.direct);
      if(relations.some((relation,i)=>!relation||relation.factors.length!==stages[i].count))
        throw Error('The three certified columns are unavailable');
      holder.append(stageCard(stages[0],relations[0]),arrow('Framed lantern at Q₄'),
        stageCard(stages[1],relations[1]),arrow('Framed lantern at Q₃'),
        stageCard(stages[2],relations[2]));
      status.textContent='Three exact framed relations · two checked lantern substitutions';
      if(location.hash)document.getElementById(location.hash.slice(1))?.scrollIntoView({block:'nearest'});
    }catch(error){status.textContent=`Could not load the derivation: ${error.message}`}
  }
  load();
})();
