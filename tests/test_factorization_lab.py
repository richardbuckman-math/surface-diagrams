import json
import runpy
import threading
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from itertools import product as cartesian_product
from xml.etree import ElementTree as ET
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from surface_diagrams.factorization_explorer import (Factor,initial_factors,product,exact_action,
    move_factor,split_factor,combine_factors,import_factors,export_factors,
    global_conjugate_factors,checked_global_frame,parse_global_conjugator)
from surface_diagrams.factorization_geometry import support_points,turn,braid_svg,row_height,deform_polyline,factorization_svg
from math import pi
from surface_diagrams.factorization_lab import LabServer
from surface_diagrams.factorization_audit import support_audit,audit_points,polyline_ray_word
from surface_diagrams import Arc,Loop,ConjugatedTwist,simplify_twist,support_curve,support_drawing


class FactorizationLabTests(unittest.TestCase):
    def test_public_browser_adapter_uses_checked_lab_operations(self):
        asset=Path(__file__).resolve().parents[1]/'src'/'surface_diagrams'/'lab_assets'/'public-lab-backend.py'
        dispatch=runpy.run_path(str(asset))['dispatch']
        original=json.loads(dispatch('/api/state','GET',''))
        self.assertEqual(original['status'],200)
        self.assertEqual(len(json.loads(original['body'])['factors']),13)
        moved=json.loads(dispatch('/api/action','POST',json.dumps(dict(op='move',index=0,target=1,revision=0))))
        result=json.loads(moved['body'])
        self.assertEqual(moved['status'],200)
        self.assertEqual([f['id'] for f in result['factors'][:2]],['F2','F1'])
        self.assertEqual(result['steps'][-1],'Hurwitz: F1 from 1 to 2')
        reopened=runpy.run_path(str(asset))
        reopened['restore_browser_session'](json.dumps(moved['session']))
        restored=json.loads(reopened['dispatch']('/api/state','GET',''))
        self.assertEqual(json.loads(restored['body'])['position'],1)
        self.assertEqual([f['id'] for f in json.loads(restored['body'])['factors'][:2]],['F2','F1'])
        invalid=runpy.run_path(str(asset))
        invalid['restore_browser_session']('{"format":"bad"}')
        fallback=json.loads(invalid['dispatch']('/api/state','GET',''))
        self.assertEqual(json.loads(fallback['body'])['position'],0)
        self.assertIn('Could not reopen',json.loads(fallback['body'])['message'])
        self.assertEqual(json.loads(dispatch('/api/action','POST',json.dumps(dict(op='move',index=0,target=1,revision=0))))['status'],400)
        prefix=json.loads(dispatch('/api/prefix?index=0&revision=1','GET',''))
        self.assertEqual(len(json.loads(prefix['body'])['after']),6)
        undone=json.loads(dispatch('/api/action','POST',json.dumps(dict(op='undo',revision=1))))
        self.assertEqual(json.loads(undone['body'])['position'],0)

    def test_history_labels_and_seek_survive_branching_and_legacy_reopen(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'steps.json'
            server=LabServer(session_path=path)
            try:
                server.mutate(dict(op='split',index=0,kind='powers',revision=0))
                self.assertEqual(server.operations[1],'Split F1 (powers)')
                server.mutate(dict(op='seek',position=0,revision=1))
                self.assertEqual(server.position,0)
                with self.assertRaisesRegex(ValueError,'saved history step'):
                    server.mutate(dict(op='seek',position=9,revision=2))
                server.mutate(dict(op='reset',revision=2))
                self.assertEqual(server.operations,['Original factorization','Reset to original factorization'])
                self.assertEqual(len(server.history),len(server.operations))
            finally: server.server_close()
            reopened=LabServer(session_path=path)
            try: self.assertEqual(reopened.operations[1],'Reset to original factorization')
            finally: reopened.server_close()
            saved=json.loads(path.read_text());saved.pop('operations');path.write_text(json.dumps(saved))
            legacy=LabServer(session_path=path)
            try: self.assertEqual(legacy.operations,['Earlier saved state 1','Earlier saved state 2'])
            finally: legacy.server_close()

    def test_global_conjugation_preserves_factor_types_and_checks_frame(self):
        factors=initial_factors();word=(1,-2,3)
        transformed=global_conjugate_factors(factors,word)
        self.assertEqual([f.id for f in transformed],[f.id for f in factors])
        self.assertEqual([(f.points,f.power,f.half) for f in transformed],
                         [(f.points,f.power,f.half) for f in factors])
        self.assertEqual(checked_global_frame(transformed,word),transformed)
        with self.assertRaisesRegex(ValueError,'global conjugation'):
            checked_global_frame(transformed,(-1,))
        self.assertEqual(parse_global_conjugator([1,-1,2]),(2,))
        with self.assertRaises(ValueError): parse_global_conjugator([6])

    def test_global_frame_survives_undo_and_session_reopen(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'global.json'
            server=LabServer(session_path=path)
            try:
                server.mutate(dict(op='conjugate',word=[1,-2],revision=0))
                self.assertEqual(server.frames[server.position],(1,-2))
                changed=server.history[server.position]
                server.mutate(dict(op='undo',revision=1))
                self.assertEqual(server.frames[server.position],())
                server.mutate(dict(op='redo',revision=2))
                self.assertEqual(server.history[server.position],changed)
                before=len(server.history)
                server.mutate(dict(op='conjugate',word=[3,-3],revision=3))
                self.assertEqual(len(server.history),before)
                exported=json.loads(json.dumps(dict(export_factors(changed),global_conjugator=[1,-2])))
                server.mutate(dict(op='import',document=exported,revision=4))
                self.assertEqual(server.frames[server.position],(1,-2))
            finally: server.server_close()
            reopened=LabServer(session_path=path)
            try:
                self.assertEqual(reopened.frames[reopened.position],(1,-2))
                self.assertEqual(reopened.history[reopened.position],changed)
            finally: reopened.server_close()
            saved=json.loads(path.read_text())
            saved['frames'][-1]=[4]
            path.write_text(json.dumps(saved))
            with self.assertRaisesRegex(ValueError,'global conjugation'):
                LabServer(session_path=path)

    def test_unchanged_simplification_preserves_redo_history(self):
        server=LabServer(0)
        try:
            factors=(initial_factors()[0],)
            server.history=[factors,factors]; server.position=0
            before=server.history
            server.mutate(dict(op='simplify',revision=0))
            self.assertIs(server.history,before)
            self.assertEqual(server.position,0)
            self.assertEqual(server.revision,1)
            self.assertIn('No shorter representatives',server.message)
            server.mutate(dict(op='redo',revision=1))
            self.assertEqual(server.position,1)
        finally: server.server_close()

    def test_reverse_meridian_action_retains_based_paths_and_composition(self):
        from surface_diagrams.mapping_classes import _action_by_meridian
        for word in cartesian_product((1,-1,2,-2,3,-3),repeat=3):
            self.assertEqual(_action_by_meridian(word,6),exact_action(word))
        # Central braids preserve free curve classes but are NOT identity actions.
        central=tuple(range(1,6))*6
        self.assertEqual(_action_by_meridian(central,6),exact_action(central))
        self.assertNotEqual(_action_by_meridian(central,6),exact_action(()))

    def test_session_reopens_with_explicit_limit_notice_but_rejects_mismatch(self):
        from surface_diagrams.mapping_classes import VerificationLimitError
        with TemporaryDirectory() as folder:
            path=Path(folder)/'session.json'
            path.write_text(json.dumps(dict(format='surface-diagrams-session-v1',position=0,
                history=[export_factors(initial_factors())])))
            with patch('surface_diagrams.factorization_lab.checked',side_effect=VerificationLimitError('limit')):
                server=LabServer(0,path)
            try:
                self.assertEqual(server.history[0],initial_factors())
                self.assertIn('not reverified',server.verification_notice)
                self.assertNotIn('exact products verified',server.message)
            finally: server.server_close()
            with patch('surface_diagrams.factorization_lab.checked',side_effect=ValueError('Product mismatch')):
                with self.assertRaisesRegex(ValueError,'Product mismatch'): LabServer(0,path)

    def test_supported_class_matches_full_action_without_unrelated_expansion(self):
        from surface_diagrams.mapping_classes import supported_class
        from surface_diagrams.braid_actions import free_homotopy_key
        for word in cartesian_product((1,-1,2,-2,3,-3),repeat=3):
            for first,points in ((1,2),(2,3)):
                twist=ConjugatedTwist(word,first,points)
                images=exact_action(word)
                expected=tuple(x for image in images[first-1:first+points-1] for x in image)
                self.assertEqual(supported_class(twist),free_homotopy_key(expected))
        # Exponentially growing unrelated meridians must not hide a simple curve.
        twist=ConjugatedTwist((1,-2)*20,4,2,half=True)
        self.assertEqual(supported_class(twist),free_homotopy_key((4,5)))
        with self.assertRaises(ValueError): supported_class(ConjugatedTwist((),6,2))
        support_audit.cache_clear()
        with patch('surface_diagrams.twist_supports.support_curve',side_effect=ValueError('Route unavailable')):
            audit=support_audit(initial_factors()[0])
        self.assertEqual(audit['status'],'unavailable')
        self.assertIsNone(audit['matches'])
        self.assertIsNotNone(audit['expected'])
        support_audit.cache_clear()

    def test_initial_words_and_hurwitz_inverse_preserve_product(self):
        factors=initial_factors()
        self.assertEqual([len(f.word) for f in factors],[12,9,5,22,12,13,11,18,15,16,13,18,14])
        before=exact_action(product(factors))
        moved=move_factor(factors,1,3)
        self.assertEqual(moved[3],factors[1])
        self.assertEqual(exact_action(product(moved)),before)
        self.assertEqual(move_factor(moved,3,1),factors)
        with self.assertRaises(ValueError): move_factor(factors,0,99)

    def test_square_lantern_half_splits_and_combine(self):
        f=(Factor('T',(-2,),3,3,2),)
        split=split_factor(f,0,'powers')
        self.assertEqual(exact_action(product(split)),exact_action(product(f)))
        self.assertEqual(combine_factors(split,0)[0].word,f[0].word)
        lantern=split_factor(split,0,'lantern')
        self.assertEqual(len(lantern),4)
        self.assertEqual(exact_action(product(lantern)),exact_action(product(f)))
        rejoined=combine_factors(lantern,0)
        self.assertEqual(len(rejoined),2)
        self.assertEqual(rejoined[0].word,split[0].word)
        self.assertEqual(combine_factors(rejoined,0)[0].word,f[0].word)
        wrong=(lantern[0],lantern[2],lantern[1])
        with self.assertRaises(ValueError): combine_factors(wrong,0)
        half=split_factor((Factor('P',(3,),1,2),),0,'halves')
        self.assertEqual(combine_factors(half,0)[0].word,Factor('P',(3,),1,2).word)
        with self.assertRaises(ValueError): combine_factors(initial_factors(),0)

    def test_shared_renderer_recovers_confirmed_itinerary_and_elliptic_paths(self):
        f=initial_factors()[8]
        self.assertEqual(support_curve(f.mapping_class),Arc(1,4,(4,2,1,4,5,1,2,4,2),direction='down'))
        self.assertIsInstance(support_curve(initial_factors()[0].mapping_class),Loop)
        svg=support_drawing(f.mapping_class)
        root=ET.fromstring(svg)
        arc=root.find("{http://www.w3.org/2000/svg}path[@class='arc']")
        self.assertIsNotNone(arc)
        self.assertIn('A ',arc.attrib['d'])

    def test_closed_supports_are_reconstructed_without_numerical_sampling(self):
        support_curve.cache_clear(); support_drawing.cache_clear()
        with patch('surface_diagrams.factorization_geometry.support_points',side_effect=AssertionError('No sampling')):
            for word in cartesian_product((1,-1,2,-2,3,-3),repeat=2):
                twist=ConjugatedTwist(word,2,3)
                self.assertIsInstance(support_curve(twist),Loop)
                self.assertIn('<svg',support_drawing(twist))

    def test_exact_arc_recovery_uses_no_numerical_sampling(self):
        from surface_diagrams.mapping_classes import supported_class
        from surface_diagrams.braid_actions import arc_ray_word,inverse_word,free_homotopy_key
        support_curve.cache_clear(); support_drawing.cache_clear()
        with patch('surface_diagrams.factorization_geometry.support_points',side_effect=AssertionError('No sampling')):
            for word in cartesian_product((1,-1,2,-2,3,-3),repeat=3):
                for first in (1,2,3,4):
                    twist=ConjugatedTwist(word,first,2,half=True)
                    arc=support_curve(twist); path=arc_ray_word(6,arc)
                    observed=(arc.start,)+path+(arc.end,)+inverse_word(path)
                    self.assertEqual(free_homotopy_key(observed),supported_class(twist))
                    self.assertIn('<svg',support_drawing(twist))
        with self.assertRaisesRegex(ValueError,'768'):
            support_curve(ConjugatedTwist((1,-2)*7,1,2,half=True))

    def test_dense_exact_support_expands_layout_and_keeps_geometric_checks(self):
        from surface_diagrams.svg import render_svg
        from surface_diagrams.curves import route,_conflict
        twist=ConjugatedTwist((1,-2)*6,1,2,half=True)
        curve=support_curve(twist)
        self.assertEqual(len(curve.cuts),375)
        support_drawing.cache_clear()
        with patch('surface_diagrams.twist_supports.render_svg',wraps=render_svg) as renderer:
            support_drawing(twist)
        surface=renderer.call_args.args[0]; style=renderer.call_args.kwargs['style']
        self.assertGreater(surface.width,360)
        self.assertEqual(style.curve_width,1.5)
        self.assertEqual(style.marked_point_radius,3.5)
        segments=route(surface,style)
        self.assertEqual(len(segments),376)
        for segment in segments:
            for k in range(33):
                x,y=segment.point(k/32)
                self.assertLess((2*x/surface.width)**2+(2*y/surface.height)**2,1)
        self.assertFalse(any(_conflict((a.start,a.end,a.up),(b.start,b.end,b.up))
                             for i,a in enumerate(segments) for b in segments[i+1:]))

    def test_simplification_preserves_twist_type_and_can_change_core(self):
        examples=(ConjugatedTwist((1,2),1,2,half=True),
                  ConjugatedTwist((1,2,1,-2,-1),2,2,half=True),
                  ConjugatedTwist((2,2),1,3,2))
        for twist in examples:
            reduced=simplify_twist(twist)
            self.assertEqual(exact_action(reduced.word),exact_action(twist.word))
            self.assertEqual((reduced.points,reduced.power,reduced.half),(twist.points,twist.power,twist.half))
            self.assertLess(len(reduced.conjugator),len(twist.conjugator))
        shifted=simplify_twist(examples[0])
        self.assertEqual((shifted.conjugator,shifted.first),((),2))
        factors=initial_factors(); moved=move_factor(factors,0,1)
        self.assertEqual(moved[1],factors[0])
        self.assertEqual(len(moved[0].word),11)
        self.assertEqual(exact_action(product(moved)),exact_action(product(factors)))
        # The long common conjugator need not be expanded to verify commuting
        # local rewrites; it centralizes this disjoint standard half twist.
        large=ConjugatedTwist((1,-2)*15,4,2,half=True)
        self.assertEqual(simplify_twist(large).conjugator,())
        central=tuple(range(1,6))*6
        for points,half,power in ((2,True,1),(3,False,1),(3,False,2)):
            twist=ConjugatedTwist(central,1,points,power,half)
            simplified=simplify_twist(twist,max_states=1)
            self.assertEqual(simplified.conjugator,())
            self.assertEqual(exact_action(twist.word),exact_action(simplified.word))

    def test_support_search_shortens_nonstandard_conjugates_exactly(self):
        from surface_diagrams.support_simplify import shorter_support_path
        central=tuple(range(1,6))*6
        for points,half,power in ((2,True,1),(3,False,1),(3,False,2)):
            twist=ConjugatedTwist(central+(points,),1,points,power,half)
            result=shorter_support_path(twist,max_states=16)
            self.assertEqual(len(result.conjugator),1)
            self.assertEqual((result.points,result.power,result.half),(points,power,half))
            self.assertEqual(exact_action(result.word),exact_action(twist.word))
            self.assertEqual(len(simplify_twist(twist,max_states=16).conjugator),1)

    def test_order_propagation_agrees_with_unpruned_small_route_search(self):
        from surface_diagrams.curves import route,RoutingError
        from surface_diagrams import PlanarSurface,Style
        base=PlanarSurface.row('PPPP',spacing=50,height=180,margin=50)
        def accepted(curve):
            try: route(base.with_curves(curve),Style()); return True
            except RoutingError:return False
        for cuts in cartesian_product(range(5),repeat=4):
            try:curve=Loop(cuts)
            except ValueError:continue
            optimized=accepted(curve)
            with patch('surface_diagrams.curves._forced_orders',return_value={}):
                reference=accepted(curve)
            self.assertEqual(optimized,reference,cuts)

    def test_geometric_sign_and_inverse(self):
        below=support_points(1,2,True,(-2,))
        above=support_points(1,2,True,(2,))
        self.assertAlmostEqual(below[0][0],0)
        self.assertAlmostEqual(below[-1][0],2)
        self.assertLess(min(y for x,y in below),-.1)
        self.assertGreater(max(y for x,y in above),.1)
        for point in ((.2,.3),(.6,.1),(1.4,-.3)):
            restored=turn(turn(point,1),-1)
            for a,b in zip(point,restored): self.assertAlmostEqual(a,b)

    def test_initial_and_first_drag_supports_stay_on_surface(self):
        f=initial_factors()
        for state in (f,move_factor(f,0,1)):
            for factor in state:
                pts=support_points(factor.first,factor.points,factor.half,factor.conjugator)
                self.assertTrue(all(((50+x*48-170)/164)**2+((y*48)/84)**2<1 for x,y in pts),factor.id)

    def test_save_reload_and_tamper_rejection(self):
        f=split_factor(initial_factors(),0,'powers')
        document=json.loads(json.dumps(export_factors(f)))
        self.assertEqual(import_factors(document),f)
        document['factors'][0]['word']=[1]
        with self.assertRaises(ValueError): import_factors(document)
        document=json.loads(json.dumps(export_factors(f)))
        document['factors'][0]['conjugator']=[9,-9]
        with self.assertRaises(ValueError): import_factors(document)

    def test_local_deformation_samples_crossing_chords_and_fixes_exterior(self):
        block=(0.,.55,.95,-pi)
        outside=((-1000.,2.),(1000.,2.))
        self.assertEqual(deform_polyline(outside,block),outside)
        # Both endpoints are outside, but the chord crosses the moving disk.
        crossing=deform_polyline(((-2.,0.),(2.,0.)),block)
        self.assertEqual(crossing[0],(-2.,0.))
        self.assertEqual(crossing[-1],(2.,0.))
        self.assertGreater(max(y for x,y in crossing),.2)
        self.assertLess(min(y for x,y in crossing),-.2)

    def test_factor_nine_over_seven_retains_support_preview(self):
        factors=move_factor(initial_factors(),8,6)
        for f in factors[7:9]:
            points=support_points(f.first,f.points,f.half,f.conjugator)
            self.assertGreater(len(points),2)
            self.assertTrue(all(((50+x*48-170)/164)**2+((y*48)/84)**2<1 for x,y in points))
            self.assertTrue(support_audit(f)['matches'])

    def test_support_audit_checks_drawn_class_and_detects_wrong_geometry(self):
        for f in initial_factors():
            self.assertTrue(support_audit(f)['matches'],f.id)
        f=Factor('arc',(2,),1,2,half=True)
        correct=support_points(1,2,True,(2,))
        wrong=tuple((x,-y) for x,y in correct)
        self.assertTrue(audit_points(f,correct)['matches'])
        self.assertFalse(audit_points(f,wrong)['matches'])
        self.assertEqual(audit_points(f,((0.,0.),(2.,0.)))['status'],'unavailable')
        # A ray through a polyline vertex counts once; reversing inverts the word.
        points=((-0.5,1.),(0.,1.),(.5,1.))
        self.assertEqual(polyline_ray_word(points),(1,))
        self.assertEqual(polyline_ray_word(points[::-1]),(-1,))
    def test_continuous_braid_has_factor_separators_and_total_height(self):
        f=initial_factors(); svg=braid_svg(f)
        self.assertEqual(svg.count('stroke-dasharray'),12)
        self.assertIn(f'height="{sum(row_height(x) for x in f)}"',svg)
        rows=ET.fromstring(svg).findall('{http://www.w3.org/2000/svg}rect')
        self.assertEqual(len(rows),len(f))
        self.assertEqual([int(row.get('y')) for row in rows],
                         [sum(row_height(x) for x in f[:i]) for i in range(len(f))])
        self.assertEqual([row.get('fill') for row in rows],['none']*len(f))

    def test_paired_export_preserves_missing_preview_warning(self):
        factor=Factor('<test & twist>',(),1,2)
        with patch('surface_diagrams.factorization_geometry.support_svg',side_effect=ValueError('sampling limit')):
            svg=factorization_svg((factor,))
        root=ET.fromstring(svg)
        text=' '.join(root.itertext())
        self.assertIn('Support preview unavailable',text)
        self.assertIn('sampling limit',text)
        self.assertIn('<test & twist>',text)
        self.assertIn('Shared Arc/Loop supports',text)
        self.assertIn('Continuous six-strand braid',svg)

    def test_server_undo_revision_and_rejected_mutation(self):
        server=LabServer()
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            state=json.load(urlopen(server.url+'/api/state'))
            prefix=json.load(urlopen(server.url+'/api/prefix?index=1&revision=0'))
            self.assertEqual(prefix['factor'],'F2')
            self.assertEqual(tuple(map(tuple,prefix['before'])),exact_action(product(initial_factors()[:1])))
            self.assertEqual(tuple(map(tuple,prefix['after'])),exact_action(product(initial_factors()[:2])))
            self.assertEqual(prefix['before_punctures'],[1,2,3,4,5,6])
            self.assertEqual(prefix['after_punctures'],[1,2,6,4,5,3])
            self.assertIn('<svg',prefix['before_svg'])
            self.assertIn('<svg',prefix['after_svg'])
            self.assertEqual(prefix['before_warning'],'')
            sphere=json.load(urlopen(server.url+'/api/sphere?revision=0'))
            self.assertTrue(sphere['certified'])
            self.assertFalse(sphere['disk_identity'])
            self.assertEqual(len(sphere['conjugator']),58)
            self.assertIn('<svg',sphere['chart_svg'])
            self.assertEqual(sphere['chart_warning'],'')
            def post(data,token=state['token']):
                return urlopen(Request(server.url+'/api/action',data=json.dumps(data).encode(),
                    headers={'Content-Type':'application/json','X-Surface-Token':token}))
            with self.assertRaises(HTTPError): post({'op':'reset','revision':0},'wrong')
            split=json.load(post({'op':'split','index':0,'kind':'powers','revision':0}))
            self.assertEqual(len(split['factors']),14)
            with self.assertRaises(HTTPError): post({'op':'reset','revision':0})
            with self.assertRaises(HTTPError): post({'op':'combine','index':4,'revision':1})
            self.assertEqual(server.revision,1)
            with self.assertRaises(HTTPError) as error: urlopen(server.url+'/api/prefix?index=1&revision=0')
            self.assertEqual(error.exception.code,409)
            with self.assertRaises(HTTPError) as error: urlopen(server.url+'/api/sphere?revision=0')
            self.assertEqual(error.exception.code,409)
            with self.assertRaises(HTTPError) as error: urlopen(server.url+'/api/prefix?index=99&revision=1')
            self.assertEqual(error.exception.code,400)
            undone=json.load(post({'op':'undo','revision':1}))
            self.assertEqual(len(undone['factors']),13)
            self.assertTrue(undone['redo'])
            with self.assertRaises(HTTPError) as error: urlopen(server.url+'/api/export.svg?revision=0')
            self.assertEqual(error.exception.code,409)
            export=urlopen(server.url+'/api/export.svg?revision=2').read()
            self.assertEqual(ET.fromstring(export).tag,'{http://www.w3.org/2000/svg}svg')
        finally: server.shutdown();server.server_close();thread.join()

    def test_disk_session_reopens_undo_history_and_rejects_invalid_file(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'work.json'
            server=LabServer(session_path=path)
            try:
                server.mutate(dict(op='split',index=0,kind='powers',revision=0))
                server.mutate(dict(op='undo',revision=1))
            finally: server.server_close()
            restored=LabServer(session_path=path)
            try:
                self.assertEqual(restored.position,0)
                self.assertEqual(len(restored.history),2)
                restored.mutate(dict(op='redo',revision=0))
                self.assertEqual(len(restored.history[restored.position]),14)
                before=path.read_bytes()
                with patch.object(restored,'save_session',side_effect=OSError('disk full')):
                    with self.assertRaises(OSError): restored.mutate(dict(op='reset',revision=1))
                self.assertEqual(restored.revision,1)
                self.assertEqual(len(restored.history[restored.position]),14)
                self.assertEqual(path.read_bytes(),before)
            finally: restored.server_close()
            path.write_text('{"format":"unrelated"}',encoding='utf-8')
            with self.assertRaises(ValueError): LabServer(session_path=path)
            self.assertEqual(path.read_text(),'{"format":"unrelated"}')

    def test_operations_respect_reopen_limits(self):
        with self.assertRaises(ValueError):
            combine_factors((Factor('a',(),1,2,32),Factor('b',(),1,2)),0)
        # The replacement itself fits, but the complete expanded state does not.
        factors=(Factor('T',(1,)*500,3,3),)+tuple(Factor(str(i),(),1,2,32) for i in range(16))
        with self.assertRaises(ValueError): split_factor(factors,0,'lantern')
