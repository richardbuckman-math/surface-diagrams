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
from surface_diagrams.early_alternative import expose_alternative_early_daisy
from surface_diagrams.early_alternative_transport import transport_alternative_roots
from surface_diagrams.early_alternative_exterior import expose_second_alternative_exterior
from surface_diagrams.early_alternative_closure import close_alternative_boundary
from surface_diagrams.named_disk_frames import shorten_named_disk_frames
from surface_diagrams.named_cyclic_start import shorten_named_cyclic_start
from surface_diagrams.named_unaligned_daisies import shorten_named_daisy_closure
from surface_diagrams.named_expanded_loan import shorten_expanded_loan_return
from surface_diagrams.named_upward_daisies import shorten_named_upward_daisies
from surface_diagrams.named_positive_frame import merge_positive_T45_frame
from surface_diagrams.named_repeated_petal import shorten_repeated_petal_daisy
from surface_diagrams.early_boundary_pure import purify_early_cluster, contract_pure_clusters
from surface_diagrams.early_exterior_lantern import extract_positive_exterior, contract_exterior_petals, contract_transported_cluster, contract_second_exterior, rebuild_round_four_point
from surface_diagrams.early_boundary_closure import close_round_boundary
from surface_diagrams.braid_stack import braid_fragment_svg
from surface_diagrams.disk_intersection import disk_curve_intersection
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
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.based_cut_system import based_arc_from_meridian
from surface_diagrams.twist_supports import arc_from_class
from surface_diagrams.normal_cut_engine import calculate_cut_system
from surface_diagrams.normal_cut_preview import render_normal_cut_preview


def build_exterior_target(target, out, version):
    """Show the actual missing curve without suggesting a route has reached it."""
    columns=dict(present=(target['actual_middle'],),needed=(target['local_before'][1],),
                 left=target['local_before'],right=target['local_after'])
    data={};fragments=[]
    for name,factors in columns.items():
        data[name]=[]
        for f in factors:
            fragment=braid_fragment_svg(f.word,compact=True)
            data[name].append(dict(id=f.id,word=f.word,units=len(f.core),height=fragment['height'],
                braid=len(fragments),support=compact_support_svg(number_support_points(support_svg(f,6,mirror_vertical=False)))))
            fragments.append(fragment['svg'])
    payload=json.dumps(dict(columns=data,braids=fragments),separators=(',',':')).replace('<',chr(92)+'u003c')
    html="""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The missing exterior-lantern curve</title><style>
*{box-sizing:border-box}body{margin:24px auto;padding:0 20px;max-width:1400px;font:16px/1.5 system-ui;color:#18384d;background:#f3f6f9}h1{font-size:26px}.notice{padding:14px;background:#fff0d2;border-left:4px solid #b37620}.comparison{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}.column{padding:12px;background:white;border:1px solid #c9d5df;border-radius:8px;min-width:0}.aligned{display:grid;grid-template-columns:minmax(0,1fr) 86px}.row{display:grid;grid-template-columns:100px minmax(0,1fr);align-items:center;border-bottom:1px dotted #7caafa;min-width:0}.label{font-size:11px;color:#08628e;overflow-wrap:anywhere}.support{height:100%;min-width:0;min-height:0;display:flex;align-items:center;overflow:hidden}.support img{height:auto;max-height:100%;width:100%;object-fit:contain;display:block}.braid svg{display:block;width:86px;height:auto}h2{font-size:18px}@media(max-width:700px){.comparison{grid-template-columns:1fr}.aligned{grid-template-columns:minmax(0,1fr) 86px}.row{grid-template-columns:80px minmax(0,1fr)}}
</style><h1>The missing exterior-lantern curve</h1><p><a href="index.html?phase=earlycontracts&amp;step=11">Return to the latest reached endpoint</a></p>
<p><a href="index.html?phase=earlyexterior&amp;step=0">A different exterior lantern has now been reached in six positive operations</a>: retain the actual C below and transport B using one unit of the existing square. This older required-C target remains unapplied.</p>
<p class="notice"><b>TARGET ONLY: the required middle curve has not been reached.</b> Both middle curves contain points 1,4,5, but their actual isotopy classes differ. No Hurwitz transport between them is claimed.</p>
<div class="comparison"><section class="column"><h2>Current middle curve: F12.1</h2><div id="present"></div></section><section class="column"><h2>Required middle curve: not yet present</h2><div id="needed"></div></section></div>
<h2>The exact local relation available if that curve is exposed</h2><p>The ordered products below agree exactly in B5: O1234, required C145, current B235 = exterior twist, Q23, Q14. The exterior twist is retained visibly. No sphere cap or framed-boundary substitution is applied.</p>
<div class="comparison"><section class="column"><h2>Hypothetical local input</h2><div id="left"></div></section><section class="column"><h2>Checked replacement</h2><div id="right"></div></section></div>
<p>The pictures are individual disk-exact supports, with corresponding connected braids. They are not cumulative joint cut-system certificates. The reached factorization still requires a named boundary closure. <a href="certificate.json">Full checked target and actual curve records</a>.</p>
<script src="../six-seven-compact/connected-braid.js?v=VERSION"></script><script>
const targetData=PAYLOAD;
for(const [id,rows] of Object.entries(targetData.columns)){
 const supports=rows.map(f=>`<div class="row" style="height:${f.height}px"><div class="label">${f.id}</div><div class="support"><img src="data:image/svg+xml,${encodeURIComponent(f.support)}" alt="Exact support of ${f.id}"></div></div>`).join('');
 document.getElementById(id).innerHTML=`<div class="aligned"><div>${supports}</div><div class="braid">${connectedBraid.assemble(rows,targetData.braids).svg}</div></div>`;
}
</script></html>"""
    (out/'exterior-target.html').write_text(html.replace('VERSION',version).replace('PAYLOAD',payload),encoding='utf-8')


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
    alternative=expose_alternative_early_daisy(early['chart']['factors'])
    alttransport=transport_alternative_roots(early['chart']['factors'])
    altexterior=expose_second_alternative_exterior(alttransport['factors'])
    altclosed=close_alternative_boundary(altexterior['factors'])
    named_disk=shorten_named_disk_frames(alttransport['stages']+altexterior['stages'][1:]+altclosed['stages'][1:])
    named_current=shorten_named_cyclic_start(named_disk['stages'])
    named_latest=shorten_named_daisy_closure(named_current['stages'])
    named_expanded=shorten_expanded_loan_return(named_latest['stages'])
    named_upward=shorten_named_upward_daisies(named_expanded['stages'])
    named_positive=merge_positive_T45_frame(named_upward['stages'])
    named_final=shorten_repeated_petal_daisy(named_positive['stages'])
    purification=purify_early_cluster(earlycluster['factors'])
    pure_contractions=contract_pure_clusters(purification['factors'])
    exterior=extract_positive_exterior(pure_contractions['factors'])
    residual=contract_exterior_petals(exterior['factors'])
    second=contract_transported_cluster(residual['factors'])
    outer_two=contract_second_exterior(second['factors'])
    rebuilt=rebuild_round_four_point(outer_two['factors'])
    closed=close_round_boundary(rebuilt['factors'])
    pure_phases=dict(purification['phases'],earlycontracts=pure_contractions['stages'],
                    earlyexterior=exterior['stages']+residual['stages'][1:],earlysecond=second['stages'],earlytwo=outer_two['stages'],earlyround=rebuilt['stages'])
    pure_phases.update(closed['phases'])
    routes=dict(extract=route,thirty=thirty_replay,working=working,compact=compact,transport=transport_replay,early=early,earlycluster=earlycluster)
    routes.update({name:dict(stages=stages) for name,stages in pure_phases.items()})
    routes['earlyalternate']=alternative
    routes['earlyalttransport']=alttransport
    routes['earlyaltexterior']=altexterior
    routes['earlyaltclosed']=altclosed
    routes['_named_disk']=named_final
    pure_names=tuple(pure_phases)
    disk_phases=('_named_disk','earlyalternate','earlyalttransport','earlyaltexterior','earlyaltclosed')+('transport','early','earlycluster')+pure_names
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
    intersection_cache={}
    for name,replay in routes.items():
        if name=='early':base_sizes=(len(rows),len(supports),len(braids))
        states=[]
        for stage in replay['stages']:
            ids=[]
            for f in stage['factors']:
                row_key=(f,name in disk_phases)
                if row_key not in row_cache:
                    # The geometric transport shows actual disk supports,
                    # without the other phases' labeled sphere display charts.
                    if name in disk_phases:
                        t=simplify_twist(f.mapping_class)
                        candidate=replace(f,conjugator=t.conjugator,first=t.first)
                    else:
                        candidate=replace(pool[key(f.mapping_class)],id=f.id)
                    check=check_support_replacement(f.mapping_class,candidate.mapping_class,max_cuts=40)
                    if name in disk_phases and not check['disk_equal']:
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
            if name in pure_names+('_named_disk','earlyalternate','earlyalttransport','earlyaltexterior','earlyaltclosed'):
                shown['caption']=str(stage['half_twists'])+' half twists remaining; '+str(len(stage['factors']))+' positive factors; support-word maximum '+str(stage['score']['max_support_word'])
                if not any(f.half for f in stage['factors']):
                    curves=tuple(replace(f.mapping_class,power=1) for f in stage['factors'])
                    crossings=[]
                    for j,a in enumerate(curves):
                        for b in curves[j+1:]:
                            pair_key=frozenset((a,b))
                            if pair_key not in intersection_cache:intersection_cache[pair_key]=disk_curve_intersection(a,b,strands=5)
                            crossings.append(intersection_cache[pair_key])
                    shown['curve_intersections']=dict(maximum=max(crossings,default=0),total=sum(crossings),pairs=len(crossings))
                    shown['caption']+='; pairwise curve crossings max '+str(max(crossings,default=0))+' / sum '+str(sum(crossings))
            if stage.get('daisy_frame'):
                shown['daisy_frame']=stage['daisy_frame']
                shown['caption']+='; exact PC daisy chart '+str(stage['daisy_frame'])
            if stage.get('boundary_power'):shown['boundary_power']=stage['boundary_power']
            if stage.get('adjacent_moves'):shown['adjacent_moves']=stage['adjacent_moves']
            if stage.get('inverse_hurwitz_transport'):shown['inverse_hurwitz_transport']=True
            if stage.get('named_pattern_witness',{}).get('repeated_petal_pattern'):
                shown['repeated_petal_daisy']=True;shown['internal_spare_transports']=2
            if name=='transport':shown['temporary_root']=any(f.id=='transport.R234' for f in stage['factors'])
            states.append(shown)
        display_routes[name]=states
    # The NEW complete named route replaces the old action-only boundary
    # recognition by the actual positive research route and its four exteriors.
    named_raw = list(early['stages'][:18])
    named_shown = list(display_routes['early'][:18])
    if named_raw[-1]['factors'] != named_final['stages'][0]['factors']:
        raise ValueError('The shortened disk tail has a discontinuous source join')
    named_raw.extend(named_final['stages'][1:])
    named_shown.extend(display_routes['_named_disk'][1:])
    fourth = early['stages'][-2]['factors'][0]
    if exact_action(tuple(x for f in named_final['factors'] for x in f.word), 5) != exact_action(fourth.word, 5):
        raise ValueError('Four identical visible exteriors did not combine to their fourth power')
    combine = dict(kind='disk_combine', title='Combine the FOUR identical visible exterior twists',
                   factors=(fourth,), local_before=named_final['factors'], local_after=(fourth,),
                   exact_disk_equality=True, not_an_action_recognition=True)
    named_raw.extend((combine, early['stages'][-1]))
    named_shown.extend((dict(display_routes['early'][-2], kind='disk_combine',
                            title=combine['title'], caption='Four identical round twists combine; this is not a whole-product action recognition.'),
                        display_routes['early'][-1]))
    # Record every cyclic start as a common conjugation, so this proof does
    # not assume centrality of the SOURCE product to justify a cyclic start.
    audited = []
    for i, original in enumerate(named_raw):
        stage = dict(original)
        if i and stage['kind'] == 'disk_cyclic_start':
            before = named_raw[i - 1]['factors']; after = stage['factors']
            before_ids = tuple(f.id for f in before); after_ids = tuple(f.id for f in after)
            shift = next((j for j in range(len(before)) if before_ids[j:] + before_ids[:j] == after_ids), None)
            if shift is None:
                raise ValueError('A named cyclic start is not the claimed cyclic ordering')
            stage['frame'] = inverse_word(tuple(x for f in before[:shift] for x in f.word))
            stage['exact_conjugation'] = True
        audited.append(stage)
    named_raw = tuple(audited)
    named_summary = dict(graphical_steps=len(named_raw) - 1,
        sphere_moves=sum(s['kind'] == 'sphere_rewrite' for s in named_raw),
        action_only_boundary_recognitions=sum(s['kind'] == 'disk_boundary_relation' for s in named_raw),
        complete_named_derivation=True, complete_under_twenty_derivation=False,
        cyclic_starts_are_explicit_conjugations=True, terminal_exteriors=4,
        previous_graphical_steps=89, mathematical_steps_saved=3, route_parts=(17,67,1,1),
        unshortened_route_parts=(17,51,8,23,1,1), equivariant_frame_operations_removed=1, historical_frame_component_operations_removed=2, cyclic_start_operations_removed=1, raw_closure_operations_removed=9, historical_direct_daisy_operations_removed=6, expanded_loan_operations_removed=1, upward_daisy_operations_removed=1, positive_T45_frame_operations_removed=1, repeated_petal_operations_removed=3, external_adjacent_checks=106, repeated_petal_expansion_transports=2)
    if named_summary['graphical_steps'] != 86 or named_summary['sphere_moves'] != 4 or named_summary['action_only_boundary_recognitions']:
        raise ValueError('The new named proof lost a step, sphere move, or reintroduced action-only recognition')
    display_routes['namedfull'] = [dict(state, title=('The complete NAMED derivation: ' + state['title']) if i == 0 else state['title'])
                                   for i, state in enumerate(named_shown)]
    pure_names += ('namedfull','earlyalternate','earlyalttransport','earlyaltexterior','earlyaltclosed')
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
    pure_ids=sorted({i for name in pure_names for state in display_routes[name] for i in state['factors']})
    pure_support_ids=sorted({rows[i]['support'] for i in pure_ids})
    pure_braid_ids=sorted({rows[i]['braid'] for i in pure_ids})
    pure_rows=[]
    for i in pure_ids:
        row=dict(rows[i]);row.update(support=pure_support_ids.index(row['support']),braid=pure_braid_ids.index(row['braid']));pure_rows.append(row)
    pure_display=dict(routes={name:[dict(state,factors=[pure_ids.index(i) for i in state['factors']]) for state in display_routes[name]] for name in pure_names},
        rows=pure_rows,supports=[supports[i] for i in pure_support_ids],braids=[braids[i] for i in pure_braid_ids])
    pure_encoded=json.dumps(pure_display,separators=(',',':'));pure_version=sha256(pure_encoded.encode()).hexdigest()[:16]
    (out/'display-pure.json').write_text(pure_encoded,encoding='utf-8')
    display=dict(states=display_routes['extract'],routes={k:v for k,v in display_routes.items() if k not in ('early','earlycluster','_named_disk')+pure_names},rows=rows[:base_sizes[0]],supports=supports[:base_sizes[1]],
                 braids=braids[:base_sizes[2]],split=len(route['thirty_factors']),overview_summary=overview_summary)
    encoded=json.dumps(display,separators=(',',':'));version=sha256(encoded.encode()).hexdigest()[:16]
    (out/'display.json').write_text(encoded,encoding='utf-8')
    (out/'certificate.json').write_text(json.dumps(dict(source_sha256=sha256(source).hexdigest(),source_phase='positive_sphere_expansion',
        source=records,route=route,thirty_boundary=thirty,working_seed_bridge=working,compact_boundary_chart=compact,half_lantern_transport=transport,f6_alignment=alignment,f9_unwinding=unwinding,f11_rounding=rounding,early_boundary=early,early_positive_cluster=earlycluster,early_alternative_lantern=dict(alternative,applied_to_public_replay=True),early_alternative_transport=dict(alttransport,applied_to_public_replay=True),early_alternative_exterior=dict(altexterior,applied_to_public_replay=True),early_alternative_closure=dict(altclosed,applied_to_public_replay=True),early_purification=purification,pure_cluster_contractions=dict(pure_contractions,applied_to_public_replay=True),early_exterior_lantern=dict(exterior,applied_to_public_replay=True),exterior_residual_lantern=residual,second_residual_cluster=dict(second,applied_to_public_replay=True),second_exterior_lanterns=dict(outer_two,applied_to_public_replay=True),round_four_point_reconstruction=dict(rebuilt,applied_to_public_replay=True),named_boundary_closure=dict(closed,applied_to_public_replay=True),named_full_route=dict(stages=named_raw,summary=named_summary),named_disk_frame_shortening={k:v for k,v in named_disk.items() if k not in ('stages','factors')},named_cyclic_start_shortening={k:v for k,v in named_current.items() if k not in ('stages','factors')},named_unaligned_daisy_shortening={k:v for k,v in named_latest.items() if k not in ('stages','factors')},named_expanded_loan_shortening={k:v for k,v in named_expanded.items() if k not in ('stages','factors')},named_upward_daisy_shortening={k:v for k,v in named_upward.items() if k not in ('stages','factors')},named_positive_frame_shortening={k:v for k,v in named_positive.items() if k not in ('stages','factors')},named_repeated_petal_shortening={k:v for k,v in named_final.items() if k not in ('stages','factors')},
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
    (out/'index.html').write_text((ROOT/'examples/fifty_twenty_extraction.html').read_text(encoding='utf-8').replace('EARLYVERSION',early_version).replace('PUREVERSION',pure_version).replace('VERSION',version),encoding='utf-8')
    build_exterior_target(pure_contractions['next_exterior_lantern'],out,version)
    print('Saved',out,'states',{name:len(states) for name,states in display_routes.items()},'supports',len(supports),'braids',len(braids),'bytes',len(encoded.encode()),'version',version)
    return out


if __name__=='__main__':build()
