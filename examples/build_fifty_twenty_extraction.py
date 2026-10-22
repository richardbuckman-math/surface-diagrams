"""Precalculate the certified fifty -> thirty + standard-twenty extraction."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.puncture_boundary import early_boundary_derivation
from surface_diagrams.early_boundary_cluster import positive_early_cluster
from surface_diagrams.braid_stack import braid_fragment_svg
from surface_diagrams.compact_svg import compact_support_svg
from surface_diagrams.sphere_arc_simplify import _sphere_chain_certificate
from surface_diagrams.peripheral_sphere import five_point_cap_certificate
from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.factorization_geometry import number_support_points
from surface_diagrams.fifty_decomposition import extract_twenty_block,recognize_thirty_boundary,working_seed_to_legacy_chart,compact_thirty_boundary_chart,transport_round_half_lantern,align_f6_half_lantern,unwind_f9_pair_square,round_f11_half_twist
from surface_diagrams.hyperelliptic_homology import homology_action
from surface_diagrams.six_seven_structure import SignedResearchFactor
from surface_diagrams.sphere_actions import sphere_supported_class
from surface_diagrams.sphere_support_compact import check_support_replacement,reframe_factors
from surface_diagrams.twist_simplify import simplify_twist
from surface_diagrams.based_cut_system import based_arc_from_meridian
from surface_diagrams.twist_supports import arc_from_class
from surface_diagrams.normal_cut_engine import calculate_cut_system
from surface_diagrams.normal_cut_preview import render_normal_cut_preview


def build():
    parent=ROOT/'docs/proofs/six-seven-compact';out=ROOT/'docs/proofs/six-seven-fifty-blocks';out.mkdir(exist_ok=True)
    source=(parent/'source-route.json').read_bytes();report=json.loads(source)
    records=report['positive_sphere_expansion']['stages'][-1]['factors']
    fs=tuple(SignedResearchFactor(**dict(f,conjugator=tuple(f['conjugator']))) for f in records)
    route=extract_twenty_block(fs)
    thirty=recognize_thirty_boundary(route['thirty_factors'])
    working=working_seed_to_legacy_chart()
    # Closing the twenty is an actual sphere step, not an implicit phase jump.
    thirty_replay=dict(thirty,stages=(route['stages'][-1],route['twenty_closure'])+thirty['stages'][1:])
    compact=compact_thirty_boundary_chart(thirty['five_point_factors'])
    transport=transport_round_half_lantern(compact['factors'])
    alignment=align_f6_half_lantern(transport['factors'])
    unwinding=unwind_f9_pair_square(alignment['factors'])
    rounding=round_f11_half_twist(unwinding['factors'])
    transport_replay=dict(transport,stages=transport['stages']+alignment['stages'][1:]+unwinding['stages'][1:]+rounding['stages'][1:])
    early=early_boundary_derivation()
    earlycluster=positive_early_cluster(early['chart']['factors'])
    routes=dict(extract=route,thirty=thirty_replay,working=working,compact=compact,transport=transport_replay,early=early,earlycluster=earlycluster)
    data=json.loads((parent/'display.json').read_text());first=data['states'][0]
    candidates=tuple(SignedResearchFactor(**dict(data['rows'][i]['factor'],conjugator=tuple(data['rows'][i]['factor']['conjugator']))) for i in first['factors'])
    candidates=reframe_factors(candidates,inverse_word(first['frame']))['factors']
    pool={}
    def key(t):return t.points,t.power,t.half,sphere_supported_class(t),homology_action(t.word)
    def offer(f):
        t=simplify_twist(f.mapping_class);f=replace(f,conjugator=t.conjugator,first=t.first);k=key(t)
        if k not in pool or (len(f.conjugator),len(f.word))<(len(pool[k].conjugator),len(pool[k].word)):pool[k]=f
    extra=tuple(thirty['five_point_factors'])+(thirty['boundary'],)+tuple(
        f for stage in working['stages'] for f in stage['factors'])+compact['factors']
    for f in candidates+extra:
        for prefix in ((),(5,5),(-5,-5)):
            offer(replace(f,conjugator=reduce_word(prefix+f.conjugator)))
        for i in range(1,8-f.points):offer(replace(f,first=i,conjugator=()))
    supports=[];braids=[];rows=[];recharts=[];support_cache={};braid_cache={};row_cache={};display_routes={}
    for name,replay in routes.items():
        if name=='early':base_sizes=(len(rows),len(supports),len(braids))
        states=[]
        for stage in replay['stages']:
            ids=[]
            for f in stage['factors']:
                row_key=(f,name in ('transport','early','earlycluster'))
                if row_key not in row_cache:
                    # The geometric transport shows actual disk supports,
                    # without the other phases' labeled sphere display charts.
                    if name in ('transport','early','earlycluster'):
                        t=simplify_twist(f.mapping_class)
                        candidate=replace(f,conjugator=t.conjugator,first=t.first)
                    else:
                        candidate=replace(pool[key(f.mapping_class)],id=f.id)
                    check=check_support_replacement(f.mapping_class,candidate.mapping_class,max_cuts=40)
                    if name in ('transport','early','earlycluster') and not check['disk_equal']:
                        raise ValueError('The disk-only transport acquired a sphere display chart')
                    sk=(candidate.half,candidate.points,candidate.first,candidate.conjugator)
                    if sk not in support_cache:
                        support_cache[sk]=len(supports);supports.append(compact_support_svg(number_support_points(support_svg(candidate,6,mirror_vertical=False))))
                    if candidate.word not in braid_cache:
                        braid_cache[candidate.word]=len(braids);braids.append(braid_fragment_svg(candidate.word,compact=True)['svg'])
                    row_cache[row_key]=len(rows)
                    rows.append(dict(id=f.id,label=('H' if f.half else 'T'+str(f.points))+('^'+str(f.power) if f.power>1 else ''),
                        units=len(f.core),word=candidate.word,height=braid_fragment_svg(candidate.word,compact=True)['height'],
                        support=support_cache[sk],braid=braid_cache[candidate.word],sphere_rechart=not check['disk_equal']))
                    recharts.append(dict(source=asdict(f),displayed=asdict(candidate),certificate=check))
                ids.append(row_cache[row_key])
            shown=dict(title=stage['title'],kind=stage['kind'],factors=ids,
                       disk_discrepancy=stage.get('disk_discrepancy',()),disk_equality=stage.get('disk_equality'))
            if stage.get('caption'):shown['caption']=stage['caption']
            if stage.get('boundary_power'):shown['boundary_power']=stage['boundary_power']
            if stage.get('adjacent_moves'):shown['adjacent_moves']=stage['adjacent_moves']
            if name=='transport':shown['temporary_root']=any(f.id=='transport.R234' for f in stage['factors'])
            states.append(shown)
        display_routes[name]=states
    # One readable chain through the already certified route. These arrows
    # summarize retained atomic moves; they are never called single moves.
    legacy=tuple(s for phase in report.values() if isinstance(phase,dict) and 'stages' in phase
                 for s in phase['stages'][1:])
    spans=(
        (working['stages'][1:],'?phase=working&step=0'),
        (legacy,'../six-seven-compact/index.html'),
        (route['stages'][1:],'?phase=extract&step=0'),
        (thirty_replay['stages'][1:-2],'?phase=thirty&step=0'),
        ((thirty_replay['stages'][-2],),'?phase=thirty&step=17'),
        ((thirty_replay['stages'][-1],),'?phase=thirty&step=18'))
    checkpoints=(
        ('working',0,'The working (6,7)','Six half twists and seven squared three-point twists'),
        ('working',-1,'The saved calculation chart','The same (6,7), after explicit disk moves and a common frame'),
        ('extract',0,'The actual positive fifty','Fifty positive half-twist units, in 32 supported factors'),
        ('extract',-1,'Thirty plus a standard twenty','Upper thirty; standard twenty below, highlighted green'),
        ('thirty',-3,'The five-point disk model','Forty positive disk-core letters after the complementary four-point rechart'),
        ('thirty',-2,'Double outer-boundary twist','The ordered five-point action agrees with the double boundary twist'),
        ('thirty',-1,'Sphere identity','The twenty was removed by its sphere relation; the double boundary has now been capped'))
    overview=[]
    for i,(name,n,title,caption) in enumerate(checkpoints):
        state=dict(display_routes[name][n],title=title,caption=caption,kind='start')
        if i:
            span_records,href=spans[i-1]
            state.update(kind='summary_span',detail_href=href,
                moves=[dict(number=j+1,title=s['title'],kind=s['kind'],
                            disk_discrepancy=s.get('disk_discrepancy',())) for j,s in enumerate(span_records)])
        overview.append(state)
    counts=tuple(len(s.get('moves',())) for s in overview[1:])
    if counts!=(5,145,8,17,1,1):raise ValueError('The unified overview lost an atomic proof span')
    overview_summary=dict(checkpoints=7,atomic_moves=sum(counts),span_counts=counts,
        sphere_moves=sum(m['kind']=='sphere_rewrite' for s in overview for m in s.get('moves',())),
        source_sha256=sha256(source).hexdigest(),is_shorter_derivation=False)
    if overview_summary['sphere_moves']!=28:raise ValueError('The overview hid a source sphere move')
    display_routes['overview']=overview
    early_ids=sorted({i for name in ('early','earlycluster') for state in display_routes[name] for i in state['factors']})
    early_support_ids=sorted({rows[i]['support'] for i in early_ids})
    early_braid_ids=sorted({rows[i]['braid'] for i in early_ids})
    early_rows=[]
    for i in early_ids:
        row=dict(rows[i]);row.update(support=early_support_ids.index(row['support']),braid=early_braid_ids.index(row['braid']));early_rows.append(row)
    early_states={name:[dict(state,factors=[early_ids.index(i) for i in state['factors']]) for state in display_routes[name]] for name in ('early','earlycluster')}
    early_display=dict(routes=early_states,rows=early_rows,
        supports=[supports[i] for i in early_support_ids],braids=[braids[i] for i in early_braid_ids])
    early_encoded=json.dumps(early_display,separators=(',',':'));early_version=sha256(early_encoded.encode()).hexdigest()[:16]
    (out/'display-early.json').write_text(early_encoded,encoding='utf-8')
    display=dict(states=display_routes['extract'],routes={k:v for k,v in display_routes.items() if k not in ('early','earlycluster')},rows=rows[:base_sizes[0]],supports=supports[:base_sizes[1]],
                 braids=braids[:base_sizes[2]],split=len(route['thirty_factors']),overview_summary=overview_summary)
    encoded=json.dumps(display,separators=(',',':'));version=sha256(encoded.encode()).hexdigest()[:16]
    (out/'display.json').write_text(encoded,encoding='utf-8')
    (out/'certificate.json').write_text(json.dumps(dict(source_sha256=sha256(source).hexdigest(),source_phase='positive_sphere_expansion',
        source=records,route=route,thirty_boundary=thirty,working_seed_bridge=working,compact_boundary_chart=compact,half_lantern_transport=transport,f6_alignment=alignment,f9_unwinding=unwinding,f11_rounding=rounding,early_boundary=early,early_positive_cluster=earlycluster,
        independent_sphere_identity_certificate=True,explicit_w0_w1_hurwitz_route=False,overview_summary=overview_summary,
        display_recharts=recharts),default=asdict,separators=(',',':')),encoding='utf-8')
    images=tuple(map(tuple,thirty['disk_boundary_action']))
    arcs=(based_arc_from_meridian(images[0]),)+tuple(
        arc_from_class(reduce_word(images[i]+images[i+1]),i+1,i+2) for i in range(4))
    cuts=calculate_cut_system(arcs,points=5)
    (out/'boundary-cut.svg').write_text(render_normal_cut_preview(cuts,projection='smooth',mirror_vertical=True),encoding='utf-8')
    (out/'boundary-cut-certificate.json').write_text(json.dumps(dict(points=5,arcs=[asdict(a) for a in arcs],
        owners=cuts.owners,joint_verified=True,actual_images=images,
        expected_images=thirty['stages'][-2]['disk_action_certificate']['expected']),separators=(',',':')),encoding='utf-8')
    sphere_images=images+((6,),)
    sphere_cuts,sphere_arcs,depths,method=_sphere_chain_certificate(sphere_images)
    (out/'sphere-cut.svg').write_text(compact_support_svg(render_normal_cut_preview(
        sphere_cuts,projection='smooth',mirror_vertical=True),hide_cut_guides=True),encoding='utf-8')
    (out/'sphere-cut-certificate.json').write_text(json.dumps(dict(points=6,
        arcs=[asdict(a) for a in sphere_arcs],owners=sphere_cuts.owners,
        joint_verified=True,actual_disk_images_embedded=sphere_images,
        sphere_search_depths=depths,method=method,
        single_cap=five_point_cap_certificate(),double_cap=five_point_cap_certificate(2)),separators=(',',':')),encoding='utf-8')
    early_images=tuple(map(tuple,early['chart']['normalized_disk_action']))+((6,),)
    early_cuts,early_arcs,early_depths,early_method=_sphere_chain_certificate(early_images)
    (out/'early-sphere-cut.svg').write_text(compact_support_svg(render_normal_cut_preview(
        early_cuts,projection='smooth',mirror_vertical=True),hide_cut_guides=True),encoding='utf-8')
    (out/'early-sphere-cut-certificate.json').write_text(json.dumps(dict(points=6,
        arcs=[asdict(a) for a in early_arcs],owners=early_cuts.owners,joint_verified=True,
        actual_disk_images_embedded=early_images,sphere_search_depths=early_depths,
        method=early_method,boundary_power=4,fixed_working_point=2,
        source='early_boundary_derivation',source_identity_assumed=False),separators=(',',':')),encoding='utf-8')
    (out/'index.html').write_text((ROOT/'examples/fifty_twenty_extraction.html').read_text(encoding='utf-8').replace('EARLYVERSION',early_version).replace('VERSION',version),encoding='utf-8')
    print('Saved',out,'states',{name:len(states) for name,states in display_routes.items()},'supports',len(supports),'braids',len(braids),'bytes',len(encoded.encode()),'version',version)
    return out


if __name__=='__main__':build()
