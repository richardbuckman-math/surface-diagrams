'use strict';
// Sphere cut rows are calculated independently of the factor supports. Each
// server result contains a certified joint five-arc chart, or an explicit
// warning. The split changes only which exact braid action is displayed.
const sphereCuts = document.getElementById('sphere-cuts-column');
const sphereSplit = document.getElementById('sphere-split');
const sphereDialog = document.getElementById('sphere-cut-inspector');
const sphereCutFit = document.getElementById('sphere-cut-fit');
const sphereCutSave = document.getElementById('save-sphere-cut');
let sphereCutRequest = 0, sphereCutKey = '', sphereCutRows = new Map();
let sphereCutFitOverview = false;
const sphereCutResize = new ResizeObserver(() => {
  document.querySelectorAll('#sphere-cuts-column .sphere-cut-row').forEach((row, index) => {
    row.style.height = `${document.querySelectorAll('#factors .factor')[index]?.offsetHeight || 160}px`;
  });
});

function sphereArcVisibility() {
  return [...document.querySelectorAll('#sphere-arc-toggles input')].map(input => input.checked);
}
function filterSpherePaths(root) {
  const visible = sphereArcVisibility();
  root.querySelectorAll('path.arc[data-owner]').forEach(path => {
    path.style.display = visible[Number(path.dataset.owner) - 1] ? '' : 'none';
  });
}
function updateSphereArcVisibility() {
  document.querySelectorAll('#sphere-cuts-column, #sphere-cut-inspector').forEach(filterSpherePaths);
}
const sphereToggles = document.getElementById('sphere-arc-toggles');
for (let index=1; index<=5; index++) {
  const label=document.createElement('label');
  const input=document.createElement('input');input.type='checkbox';input.checked=true;
  input.setAttribute('aria-label',`Show arc ${index} to ${index+1}`);
  input.onchange=updateSphereArcVisibility;
  label.append(input,document.createTextNode(`${index}–${index+1}`));sphereToggles.append(label);
}
document.getElementById('sphere-show-all').onclick=() => {
  sphereToggles.querySelectorAll('input').forEach(input => input.checked=true);
  updateSphereArcVisibility();
};
document.getElementById('sphere-hide-all').onclick=() => {
  sphereToggles.querySelectorAll('input').forEach(input => input.checked=false);
  updateSphereArcVisibility();
};
document.getElementById('sphere-show-column').onchange=event => {
  document.body.classList.toggle('sphere-hide-column',!event.target.checked);
};
document.getElementById('close-sphere-cut').onclick=() => sphereDialog.close();
sphereCutFit.onclick=() => {
  sphereCutFitOverview=!sphereCutFitOverview;
  sphereCutFit.setAttribute('aria-pressed',String(sphereCutFitOverview));
  sphereCutFit.textContent=sphereCutFitOverview?'Show detail':'Fit overview';
  document.getElementById('sphere-cut-large').classList.toggle('sphere-cut-fit',sphereCutFitOverview);
  document.getElementById('sphere-cut-meet').classList.toggle('sphere-cut-fit',sphereCutFitOverview);
};

function sphereSplitDescription(split,count) {
  document.getElementById('sphere-split-description').textContent=
    `F1–F${split}: after each forward factor. F${split+1}–F${count}: before each factor, worked back from the end. `+
    `After F${split} and before F${split+1} meet at the same sphere cut system.`;
}
function openSphereCut(row) {
  const data=sphereCutRows.get(row);
  if (!data) return;
  document.getElementById('sphere-cut-title').textContent=
    `${data.direction==='forward'?'After':'Before'} factor ${row} · ${data.direction==='forward'?'forward prefix':'inverse suffix'}`;
  document.getElementById('sphere-cut-explanation').textContent=
    `Five arcs join the consecutive original marked points. ${data.joint_certified ?
    'Their shared crossing order and exact Arc itineraries pass the joint normal-placement check.' :
    'A jointly certified chart is unavailable.'} `+
    `The bounded sphere search finds short representatives; it does not certify global shortest length. `+
    `Arc cut visits: ${data.cut_counts?.join(', ') || 'unavailable'}. `+
    (data.warning||'');
  const large=document.getElementById('sphere-cut-large');
  large.innerHTML=data.svg||'';
  if (!data.svg) large.textContent=data.warning||'Drawing unavailable';
  sphereCutSave.disabled=!data.svg;
  sphereCutSave.onclick=()=>{
    if (data.svg) download(data.svg,'image/svg+xml',
      `sphere-cut-${data.direction==='forward'?'after':'before'}-F${row}.svg`);
  };
  const meet=document.getElementById('sphere-cut-meet');meet.replaceChildren();
  if (row===data.split) {
    const note=document.createElement('p');
    note.textContent=data.meet_certified ?
      `Exact sphere midpoint check passed. The two disk braids ${data.meet_disk_equal?'also agree':'can differ'}; their sphere actions agree up to one common basepoint whisker (${data.meet_whisker_length} letters). `+
      (data.meet_picture_equal?'The two five-arc chart drawings coincide exactly.':'The chart representatives need not coincide visually.') :
      `Midpoint check unavailable: ${data.meet_warning||'the sphere images did not match'}`;
    meet.append(note);
    if (data.meet_backward?.svg) {
      const disclosure=document.createElement('details');
      const label=document.createElement('summary');label.textContent='Show inverse-suffix chart';
      const picture=document.createElement('div');picture.className='prefix-drawing';
      picture.innerHTML=data.meet_backward.svg;disclosure.append(label,picture);meet.append(disclosure);
    }
  }
  filterSpherePaths(sphereDialog);
  sphereDialog.showModal();
}
function renderSphereCut(row,data) {
  const card=sphereCuts.children[row-1];
  if (!card) return;
  const drawing=card.querySelector('.sphere-cut-thumbnail');
  const heading=card.querySelector('strong');
  heading.textContent=`${data.direction==='forward'?'Forward · after':'From end · before'} F${row}`;
  drawing.innerHTML=data.svg||'';
  if (!data.svg) drawing.textContent=data.warning||'Joint chart unavailable';
  filterSpherePaths(drawing);
  const note=card.querySelector('small');
  note.textContent=data.meet_certified ? 'Meet A ✓ · click to compare' :
    data.meet_warning ? 'Meet check unavailable' :
    data.joint_certified ? `${data.method==='sphere-short'?'Sphere-short':'Joint chart'} · ${data.cut_counts.reduce((a,b)=>a+b,0)} cuts` :
    'No joint chart';
  sphereCutRows.set(row,data);
  if (row===data.split+1) {
    const forward=sphereCutRows.get(data.split);
    if (forward?.meet_certified && data.joint_certified && forward.svg===data.svg)
      note.textContent='Meet B ✓ · same five-arc drawing';
    else if (forward?.meet_certified && data.joint_certified)
      note.textContent='Meet B · exact sphere match; chart differs';
    card.classList.add('sphere-meeting-row');
  }
  if (row===data.split) card.classList.add('sphere-meeting-row');
}
function refreshSphereCuts() {
  if (!state || !sphereCuts) return;
  const count=state.factors.length;
  if (count<2) return;
  const old=Number(sphereSplit.value);
  if (sphereSplit.options.length!==count-1) {
    sphereSplit.replaceChildren();
    for (let split=1;split<count;split++) {
      const option=document.createElement('option');option.value=String(split);
      option.textContent=`F${split} (${split} + ${count-split})`;sphereSplit.append(option);
    }
    sphereSplit.value=String(old>=1&&old<count?old:Math.min(7,count-1));
  }
  const split=Number(sphereSplit.value);
  sphereSplitDescription(split,count);
  const key=`${state.revision}/${split}/${count}`;
  if (key===sphereCutKey) {sphereCutResize.disconnect();
    document.querySelectorAll('#factors .factor').forEach(card=>sphereCutResize.observe(card));return;}
  sphereCutKey=key;sphereCutRows=new Map();
  const request=++sphereCutRequest;
  sphereCuts.replaceChildren();
  const factors=[...document.querySelectorAll('#factors .factor')];
  for (let row=1;row<=count;row++) {
    const card=document.createElement('article');card.className='sphere-cut-row';
    card.style.height=`${factors[row-1]?.offsetHeight||state.factors[row-1].height}px`;
    card.tabIndex=0;card.setAttribute('aria-label',`Inspect sphere cut complex ${row<=split?'after':'before'} factor ${row}`);
    card.innerHTML=`<strong>${row<=split?'After':'Before'} F${row}</strong><div class="sphere-cut-thumbnail">Calculating five arcs…</div><small></small>`;
    card.onclick=()=>openSphereCut(row);
    card.onkeydown=event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();openSphereCut(row);}};
    sphereCuts.append(card);
  }
  sphereCutResize.disconnect();factors.forEach(card=>sphereCutResize.observe(card));
  const revision=state.revision;
  (async()=>{
    for (let row=1;row<=count;row++) {
      try {
        const response=await fetch(`/api/sphere-cut?row=${row}&split=${split}&revision=${revision}`);
        const data=await response.json();
        if (request!==sphereCutRequest || revision!==state.revision) return;
        if (!response.ok) throw new Error(data.error||'Cut calculation failed');
        renderSphereCut(row,data);
      } catch(error) {
        if (request!==sphereCutRequest) return;
        const card=sphereCuts.children[row-1];
        if (card) card.querySelector('.sphere-cut-thumbnail').textContent=error.message;
      }
    }
  })();
}
sphereSplit.onchange=refreshSphereCuts;
new MutationObserver(refreshSphereCuts).observe(document.getElementById('factors'),{childList:true});
