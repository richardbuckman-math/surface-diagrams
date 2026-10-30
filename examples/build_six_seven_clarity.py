"""Build a separate clarity payload without rebuilding the79-operation archive."""
from dataclasses import asdict,replace
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from surface_diagrams.clarity_derivation import factor_from_data,refine_sphere_moves,parallel_rounds,PeripheralFactor,preferred_clarity_source
from surface_diagrams.mapping_classes import exact_action,supported_class
from surface_diagrams.twist_simplify import simplify_twist
from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.factorization_geometry import number_support_points
from surface_diagrams.compact_svg import compact_support_svg
from surface_diagrams.braid_stack import braid_fragment_svg


def build():
    folder=ROOT/'docs/proofs/six-seven-fifty-blocks';original=(folder/'certificate.json').read_bytes()
    c=json.loads(original);old=json.loads((folder/'display-pure.json').read_text(encoding='utf-8'))
    early=json.loads((folder/'display-early.json').read_text(encoding='utf-8'))
    pool={}
    def converted(raw):
        s=dict(raw)
        for k in ('factors','local_before','local_after'):
            if k in s:s[k]=tuple(factor_from_data(f) for f in s[k])
        return s
    for records,shown,owner in ((c['named_full_route']['stages'],old['routes']['namedfull'],old),(c['early_boundary']['stages'],early['routes']['early'],early)):
        for raw,view in zip(records,shown):
            for f,j in zip(converted(raw)['factors'],view['factors']):pool[f]=(owner,owner['rows'][j])
    meeting_path=folder.parent/'six-seven-fixed-half-meeting.json';meeting=json.loads(meeting_path.read_text(encoding='utf-8'))
    if meeting['source_archive_sha256']!=hashlib.sha256(original).hexdigest():raise ValueError('Use the pinned source-exact meeting report')
    late_path=folder.parent/'six-seven-preferred-late45.json';late=json.loads(late_path.read_text(encoding='utf-8'))
    if late['source_archive_sha256']!=hashlib.sha256(original).hexdigest() or late['source_meeting_sha256']!=hashlib.sha256(meeting_path.read_bytes()).hexdigest():raise ValueError('Use the pinned source-exact late45 report')
    preferred=preferred_clarity_source(c,meeting,late);source=preferred['stages']
    if preferred['late45_adoption']['source_sha256']!=hashlib.sha256(late_path.read_bytes()).hexdigest():raise ValueError('Keep the exact external late45 source bytes')
    def half_score(records):
        fs=[factor_from_data(f) for f in records];values={f.id:len(supported_class(f.mapping_class,6)) for f in fs if f.half}
        return dict(lengths=values,total=sum(values.values()),maximum=max(values.values()))
    preference=dict(shorter79=half_score(c['named_full_route']['stages'][10]['factors']),clearer82=half_score(c['early_boundary']['stages'][12]['factors']),
        choice='Use the longer prefix: F2 neighborhood length12->4 and half-neighborhood total80->72; maximum30 is unchanged. These are chart-specific support lengths, not minimal crossing counts.')
    refined=refine_sphere_moves(source,c['early_boundary']['chart']['factor_certificates'])
    stages=refined['stages'];rounds=parallel_rounds(stages)
    rows=[];supports=[];braids=[];sc={};bc={};rc={}
    def intern(values,cache,value):
        if value not in cache:cache[value]=len(values);values.append(value)
        return cache[value]
    def row(f):
        if f is None:return None
        if f in rc:return rc[f]
        if f in pool:
            owner,oldrow=pool[f];svg=owner['supports'][oldrow['support']];braid=owner['braids'][oldrow['braid']]
            data={k:v for k,v in oldrow.items() if k not in ('support','braid')}
        else:
            if isinstance(f,PeripheralFactor):candidate=f
            else:
                t=simplify_twist(f.mapping_class,strands=6);candidate=replace(f,conjugator=t.conjugator,first=t.first)
                if exact_action(f.word,6)!=exact_action(candidate.word,6):raise ValueError('A new picture changed its disk word')
            svg=compact_support_svg(number_support_points(support_svg(candidate,6)))
            fragment=braid_fragment_svg(candidate.word,compact=True);braid=fragment['svg']
            data=dict(id=f.id,label=('peripheral' if isinstance(f,PeripheralFactor) else 'H' if f.half else 'T'+str(f.points))+('^'+str(f.power) if f.power>1 else ''),
                units=len(f.core),word=candidate.word,height=fragment['height'],sphere_rechart=False,peripheral=isinstance(f,PeripheralFactor))
        data.update(support=intern(supports,sc,svg),braid=intern(braids,bc,braid))
        rc[f]=len(rows);rows.append(data);return rc[f]
    def state(s,title=''):
        lengths=[len(supported_class(f.mapping_class,6)) for f in s['factors']]
        half=[n for n,f in zip(lengths,s['factors']) if f.half]
        return dict(title=title,factors=[row(f) for f in s['factors']],ledger=row(s.get('ledger')),
            support_score=dict(maximum=max(lengths,default=0),total=sum(lengths),half_maximum=max(half,default=0),half_total=sum(half)),
            caption='Support lengths in this chart: max '+str(max(lengths,default=0))+', total '+str(sum(lengths))+'. '+str(sum(f.half for f in s['factors']))+' half twists. Counts are not a geometric simplification claim.')
    shown=[dict(state(stages[0],stages[0]['title']),kind='start')]
    for r in rounds:
        moves=[]
        for j,card in enumerate(r['cards']):
            op=stages[card['move_index']];a=state(card['before']);b=state(card['after'])
            moves.append(dict(letter=chr(97+j),title=op['title'],kind=op['kind'],before=a,after=b,
                framing_increment=op.get('framing_increment',0),disk_discrepancy=card.get('disk_discrepancy',op.get('disk_discrepancy',())),
                corrected_local_disk_discrepancy=op.get('corrected_local_disk_discrepancy',()),
                chosen_lift_verified=bool(card.get('sphere_certificate',op.get('sphere_certificate',{})).get('certified'))))
        title=(str(len(moves))+' independent '+('redraws' if r['family']=='redraw' else 'disk moves')+' in parallel') if len(moves)>1 else moves[0]['title']
        shown.append(dict(state(r['after'],title),kind='clarity_step',family=r['family'],parallel_moves=moves,
            simultaneous=r['simultaneous'],sphere_redraw_count=sum(m['kind']=='sphere_redraw' for m in moves),
            move_count=len(moves),independence_verified=all(w['literal_two_order_equality'] for w in r['independence_witnesses'])))
    summary=dict(source_operations=len(source)-1,archived_source_operations=79,geometry_preference=preference,listed_moves=refined['clarified_moves'],parallel_steps=len(rounds),
        genuine_sphere_redraws=refined['sphere_redraw_moves'],sphere_redraws_mix_substitutions=False,
        framing_ledger_explicit=True,framing_corrections=6,peripheral_cleanup_separate=True,lower_half_meeting=preferred['meeting_adoption']['geometry'],
        late45_return=preferred['late45_adoption']['geometry'],previous_preferred_source_operations=85,previous_preferred_listed_moves=101,previous_preferred_parallel_steps=71,
        late45_source_sha256=hashlib.sha256(late_path.read_bytes()).hexdigest(),
        priority='Clarity and less tangled geometry before smaller step counts.',mathematical_shortening_claimed=False,
        source_sha256=hashlib.sha256(original).hexdigest())
    certificate=dict(summary=summary,stages=stages,parallel_rounds=rounds,source_certificate='certificate.json',source_route='preferred_clarity_source: delayed daisies, lower fixed-half meeting, and returned45 late clarity',delayed_daisy_adoption=preferred['adoption'],lower_half_meeting_adoption=preferred['meeting_adoption'],late45_adoption=preferred['late45_adoption'],
        scope='Parallel means independent factor-interval edits with literal two-order certificates; it does not assert a simultaneous ambient isotopy of a joint cut system. The framing ledger is multiplied on the left and is never silently discarded.')
    (folder/'clarity-certificate.json').write_text(json.dumps(certificate,default=asdict,separators=(',',':')),encoding='utf-8')
    payload=dict(routes=dict(clearfull=shown),rows=rows,supports=supports,braids=braids,summary=summary)
    encoded=json.dumps(payload,separators=(',',':'));(folder/'display-clear.json').write_text(encoded,encoding='utf-8')
    # Compile the shared template; only read archived payloads, never rebuild them.
    current=(ROOT/'examples/fifty_twenty_extraction.html').read_text(encoding='utf-8')
    for token,name in (('EARLYVERSION','display-early.json'),('PUREVERSION','display-pure.json'),('CLEARVERSION','display-clear.json')):
        current=current.replace(token,hashlib.sha256((folder/name).read_bytes()).hexdigest()[:16])
    current=current.replace('v=VERSION','v='+hashlib.sha256((folder/'display.json').read_bytes()).hexdigest()[:16])
    current=re.sub(r'CLARITY FIRST: \d+ independent steps, \d+ listed moves','CLARITY FIRST: '+str(len(rounds))+' independent steps, '+str(refined['clarified_moves'])+' listed moves',current)
    (folder/'index.html').write_text(re.sub(r'((?:display-clear|clarity-certificate)\.json\?v=)(?:CLEARVERSION|[a-f0-9]+)',lambda m:m.group(1)+hashlib.sha256(encoded.encode()).hexdigest()[:16],current),encoding='utf-8')
    print('Clarity layer:',summary,'rows',len(rows),'bytes',len(encoded))
    return payload,certificate


if __name__=='__main__':build()
