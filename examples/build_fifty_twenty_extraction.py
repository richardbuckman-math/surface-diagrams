"""Precalculate the certified fifty -> thirty + standard-twenty extraction."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.braid_stack import braid_fragment_svg
from surface_diagrams.boundary_playground_geometry import support_svg
from surface_diagrams.factorization_geometry import number_support_points
from surface_diagrams.fifty_decomposition import extract_twenty_block,recognize_thirty_boundary,working_seed_to_legacy_chart
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
    routes=dict(extract=route,thirty=thirty_replay,working=working)
    data=json.loads((parent/'display.json').read_text());first=data['states'][0]
    candidates=tuple(SignedResearchFactor(**dict(data['rows'][i]['factor'],conjugator=tuple(data['rows'][i]['factor']['conjugator']))) for i in first['factors'])
    candidates=reframe_factors(candidates,inverse_word(first['frame']))['factors']
    pool={}
    def key(t):return t.points,t.power,t.half,sphere_supported_class(t),homology_action(t.word)
    def offer(f):
        t=simplify_twist(f.mapping_class);f=replace(f,conjugator=t.conjugator,first=t.first);k=key(t)
        if k not in pool or (len(f.conjugator),len(f.word))<(len(pool[k].conjugator),len(pool[k].word)):pool[k]=f
    extra=tuple(thirty['five_point_factors'])+(thirty['boundary'],)+tuple(
        f for stage in working['stages'] for f in stage['factors'])
    for f in candidates+extra:
        for prefix in ((),(5,5),(-5,-5)):
            offer(replace(f,conjugator=reduce_word(prefix+f.conjugator)))
        for i in range(1,8-f.points):offer(replace(f,first=i,conjugator=()))
    supports=[];braids=[];rows=[];recharts=[];support_cache={};braid_cache={};row_cache={};display_routes={}
    for name,replay in routes.items():
        states=[]
        for stage in replay['stages']:
            ids=[]
            for f in stage['factors']:
                if f not in row_cache:
                    candidate=replace(pool[key(f.mapping_class)],id=f.id)
                    check=check_support_replacement(f.mapping_class,candidate.mapping_class,max_cuts=40)
                    sk=(candidate.half,candidate.points,candidate.first,candidate.conjugator)
                    if sk not in support_cache:
                        support_cache[sk]=len(supports);supports.append(number_support_points(support_svg(candidate,6,mirror_vertical=False)))
                    if candidate.word not in braid_cache:
                        braid_cache[candidate.word]=len(braids);braids.append(braid_fragment_svg(candidate.word)['svg'])
                    row_cache[f]=len(rows)
                    rows.append(dict(id=f.id,label=('H' if f.half else 'T'+str(f.points))+('^'+str(f.power) if f.power>1 else ''),
                        units=len(f.core),word=candidate.word,height=braid_fragment_svg(candidate.word)['height'],
                        support=support_cache[sk],braid=braid_cache[candidate.word],sphere_rechart=not check['disk_equal']))
                    recharts.append(dict(source=asdict(f),displayed=asdict(candidate),certificate=check))
                ids.append(row_cache[f])
            states.append(dict(title=stage['title'],kind=stage['kind'],factors=ids,
                               disk_discrepancy=stage.get('disk_discrepancy',()),disk_equality=stage.get('disk_equality')))
        display_routes[name]=states
    display=dict(states=display_routes['extract'],routes=display_routes,rows=rows,supports=supports,braids=braids,split=len(route['thirty_factors']))
    encoded=json.dumps(display,separators=(',',':'));version=sha256(encoded.encode()).hexdigest()[:16]
    (out/'display.json').write_text(encoded,encoding='utf-8')
    (out/'certificate.json').write_text(json.dumps(dict(source_sha256=sha256(source).hexdigest(),source_phase='positive_sphere_expansion',
        source=records,route=route,thirty_boundary=thirty,working_seed_bridge=working,
        independent_sphere_identity_certificate=True,explicit_w0_w1_hurwitz_route=False,
        display_recharts=recharts),default=asdict,separators=(',',':')),encoding='utf-8')
    images=tuple(map(tuple,thirty['disk_boundary_action']))
    arcs=(based_arc_from_meridian(images[0]),)+tuple(
        arc_from_class(reduce_word(images[i]+images[i+1]),i+1,i+2) for i in range(4))
    cuts=calculate_cut_system(arcs,points=5)
    (out/'boundary-cut.svg').write_text(render_normal_cut_preview(cuts,projection='smooth',mirror_vertical=True),encoding='utf-8')
    (out/'boundary-cut-certificate.json').write_text(json.dumps(dict(points=5,arcs=[asdict(a) for a in arcs],
        owners=cuts.owners,joint_verified=True,actual_images=images,
        expected_images=thirty['stages'][-2]['disk_action_certificate']['expected']),separators=(',',':')),encoding='utf-8')
    (out/'index.html').write_text((ROOT/'examples/fifty_twenty_extraction.html').read_text(encoding='utf-8').replace('VERSION',version),encoding='utf-8')
    print('Saved',out,'states',{name:len(states) for name,states in display_routes.items()},'supports',len(supports),'braids',len(braids),'bytes',len(encoded.encode()),'version',version)
    return out


if __name__=='__main__':build()
