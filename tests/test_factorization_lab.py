import json
import threading
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from xml.etree import ElementTree as ET
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from surface_diagrams.factorization_explorer import (Factor,initial_factors,product,exact_action,
    move_factor,split_factor,combine_factors,import_factors,export_factors)
from surface_diagrams.factorization_geometry import support_points,turn,braid_svg,row_height,deform_polyline,factorization_svg
from math import pi
from surface_diagrams.factorization_lab import LabServer


class FactorizationLabTests(unittest.TestCase):
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
        half=split_factor((Factor('P',(3,),1,2),),0,'halves')
        self.assertEqual(combine_factors(half,0)[0].word,Factor('P',(3,),1,2).word)
        with self.assertRaises(ValueError): combine_factors(initial_factors(),0)

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
    def test_continuous_braid_has_factor_separators_and_total_height(self):
        f=initial_factors(); svg=braid_svg(f)
        self.assertEqual(svg.count('stroke-dasharray'),12)
        self.assertIn(f'height="{sum(row_height(x) for x in f)}"',svg)

    def test_paired_export_preserves_missing_preview_warning(self):
        factor=Factor('<test & twist>',(),1,2)
        with patch('surface_diagrams.factorization_geometry.support_svg',side_effect=ValueError('sampling limit')):
            svg=factorization_svg((factor,))
        root=ET.fromstring(svg)
        text=' '.join(root.itertext())
        self.assertIn('Support preview unavailable',text)
        self.assertIn('sampling limit',text)
        self.assertIn('<test & twist>',text)
        self.assertIn('Numerical support previews',text)
        self.assertIn('Continuous six-strand braid',svg)

    def test_server_undo_revision_and_rejected_mutation(self):
        server=LabServer()
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            state=json.load(urlopen(server.url+'/api/state'))
            def post(data,token=state['token']):
                return urlopen(Request(server.url+'/api/action',data=json.dumps(data).encode(),
                    headers={'Content-Type':'application/json','X-Surface-Token':token}))
            with self.assertRaises(HTTPError): post({'op':'reset','revision':0},'wrong')
            split=json.load(post({'op':'split','index':0,'kind':'powers','revision':0}))
            self.assertEqual(len(split['factors']),14)
            with self.assertRaises(HTTPError): post({'op':'reset','revision':0})
            with self.assertRaises(HTTPError): post({'op':'combine','index':4,'revision':1})
            self.assertEqual(server.revision,1)
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
