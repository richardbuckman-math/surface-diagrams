"""Cyclic starts are conjugations, with disk centrality checked separately."""
from tempfile import TemporaryDirectory
from pathlib import Path
import json
import runpy
import unittest

from surface_diagrams.braid_actions import inverse_word
from surface_diagrams.cyclic_factorizations import rotate_factors
from surface_diagrams.factorization_explorer import Factor, initial_factors, product, export_factors
from surface_diagrams.factorization_lab import LabServer, validated_session_document
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action
from surface_diagrams.sphere_actions import sphere_chain_certificate


class CyclicFactorizationTests(unittest.TestCase):
    def test_all_block_sizes_preserve_factors_and_certify_the_conjugated_product(self):
        fs=initial_factors()
        for offset in (*range(1,len(fs)),*range(1-len(fs),0)):
            with self.subTest(offset=offset):
                r=rotate_factors(fs,offset);g=r['frame']
                cut=offset%len(fs)
                self.assertEqual(r['factors'],fs[cut:]+fs[:cut])
                self.assertEqual(r['word_certificate'],())
                self.assertEqual(r['scope'],'explicit_global_conjugation')
                self.assertFalse(r['sphere_move'])
                if offset in (3,-2):
                    self.assertEqual(exact_action(product(r['factors'])),
                                     exact_action(g+product(fs)+inverse_word(g)))
                self.assertEqual(rotate_factors(r['factors'],-offset)['factors'],fs)

    def test_noncentral_disk_product_is_never_mislabelled_as_disk_equality(self):
        fs=(Factor('a',(),1,2,half=True),Factor('b',(),2,2,half=True))
        r=rotate_factors(fs,1)
        self.assertNotEqual(exact_action(product(fs)),exact_action(product(r['factors'])))
        self.assertEqual(r['frame'],(-1,))
        self.assertNotEqual(r['disk_discrepancy'],())
        # For a central full twist, changing the start really is a disk equality.
        rose=tuple(Factor(str(i),(),i,2,half=True) for i in (1,2)*3)
        self.assertEqual(exact_action(product(rose)),
                         exact_action(product(rotate_factors(rose,1)['factors'])))

    def test_six_seven_rotation_discrepancy_is_sphere_trivial_and_lifts_to_plus_i(self):
        r=rotate_factors(initial_factors(),3)
        self.assertNotEqual(exact_action(product(initial_factors())),
                            exact_action(product(r['factors'])))
        self.assertTrue(sphere_chain_certificate(r['disk_discrepancy'])['certified'])
        self.assertEqual(homology_action(r['disk_discrepancy']),IDENTITY)

    def test_invalid_rotations_are_rejected(self):
        fs=initial_factors()
        for value in (None,True,0,13,-13,1.5,'2'):
            with self.assertRaises(ValueError):rotate_factors(fs,value)
        with self.assertRaises(ValueError):rotate_factors((),1)
        with self.assertRaises(ValueError):rotate_factors(fs[:1],1)

    def test_lab_rotation_composes_frames_and_survives_undo_export_and_reopen(self):
        with TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as folder:
            path=Path(folder)/'cyclic.json'
            server=LabServer(session_path=path)
            try:
                server.mutate(dict(op='conjugate',word=[5,-3],revision=0))
                before=server.history[server.position]
                server.mutate(dict(op='rotate',offset=3,revision=1))
                after=server.history[server.position];frame=server.frames[server.position]
                self.assertEqual(after,before[3:]+before[:3])
                self.assertEqual(server.operations[-1],'Cyclic basepoint: 3 factors top to bottom')
                self.assertIn('globally conjugate',server.message)
                exported=json.loads(json.dumps(dict(export_factors(after),global_conjugator=frame)))
                server.mutate(dict(op='undo',revision=2))
                self.assertEqual(server.history[server.position],before)
                server.mutate(dict(op='redo',revision=3))
                self.assertEqual(server.frames[server.position],frame)
                server.mutate(dict(op='import',document=exported,revision=4))
                self.assertEqual(server.history[server.position],after)
                saved=json.loads(json.dumps(server.session_document()))
                restored=validated_session_document(saved)
                self.assertEqual(restored[0][-1],after)
                self.assertEqual(restored[1][-1],frame)
                previous=(server.history,server.frames,server.revision)
                with self.assertRaises(ValueError):server.mutate(dict(op='rotate',offset=13,revision=5))
                self.assertEqual((server.history,server.frames,server.revision),previous)
            finally:server.server_close()
            reopened=LabServer(session_path=path)
            try:self.assertEqual(reopened.history[reopened.position],after)
            finally:reopened.server_close()

    def test_public_browser_backend_uses_the_same_rotation(self):
        root=Path(__file__).resolve().parents[1]
        api=runpy.run_path(str(root/'src/surface_diagrams/lab_assets/public-lab-backend.py'))
        dispatch=api['dispatch']
        response=json.loads(dispatch('/api/action','POST',json.dumps(dict(op='rotate',offset=-2,revision=0))))
        self.assertEqual(response['status'],200)
        body=json.loads(response['body'])
        self.assertEqual([f['id'] for f in body['factors'][:2]],['F12','F13'])
        reopened=runpy.run_path(str(root/'src/surface_diagrams/lab_assets/public-lab-backend.py'))
        reopened['restore_browser_session'](json.dumps(response['session']))
        restored=json.loads(json.loads(reopened['dispatch']('/api/state','GET',''))['body'])
        self.assertEqual(restored['frame'],body['frame'])
        self.assertEqual(restored['factors'],body['factors'])


if __name__=='__main__':unittest.main()
