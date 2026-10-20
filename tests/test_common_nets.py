"""Exact small-cluster counts, fold certificates, and independent tree checks."""
from copy import deepcopy
import unittest
from experiments.common_nets import engine,cubes,verify_six


class CommonNetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.polytets=engine.enumerate_polytets(5)
        cls.polycubes=cubes.enumerate_cubes(4)

    def test_exact_small_polytet_counts_and_nonoverlap(self):
        self.assertEqual([len(self.polytets[n]) for n in range(1,6)],[1,1,1,3,7])
        for n,clusters in self.polytets.items():
            for cluster in clusters:
                self.assertEqual(len(engine.surface(cluster)['faces']),2*n+2)
                for i,a in enumerate(cluster):
                    for b in cluster[i+1:]:self.assertTrue(engine.disjoint_interiors(a,b))

    def test_five_unit_common_branching_net_has_complete_certificates(self):
        surfaces=[engine.surface(c) for c in self.polytets[5]]
        search=engine.common_tree_search(surfaces,seconds=20)
        self.assertIsNotNone(search['found'])
        self.assertFalse(search['exhausted'])
        net=search['found']
        self.assertEqual(len(net['triangles']),12)
        from experiments.common_nets.audit import canonical_net,mabry_five_reference
        self.assertEqual(canonical_net(net),canonical_net(mabry_five_reference()))
        for i,surface in enumerate(surfaces):
            self.assertTrue(engine.verify_net(net,surface,net['mappings'][i]))
        corrupt=deepcopy(net['mappings'][0]);corrupt[1]=corrupt[0]
        with self.assertRaises(AssertionError):engine.verify_net(net,surfaces[0],corrupt)
        # JSON-roundtrip lists are accepted, too.
        import json
        stored=json.loads(json.dumps(net))
        self.assertTrue(engine.verify_net(stored,surfaces[0],stored['mappings'][0]))

    def test_independent_spanning_tree_enumerator_matches_kirchhoff(self):
        surface=engine.surface(self.polytets[2][0]);adj=surface['adjacency']
        unique=set();valid=0
        for edges,selected in verify_six.trees(adj):
            self.assertNotIn(selected,unique);unique.add(selected)
            net=verify_six.unfold(adj,edges,selected)
            if net:
                mapping=engine.fold_net(net,surface)
                self.assertIsNotNone(mapping);valid+=1
        self.assertEqual(len(unique),engine.spanning_tree_count(adj))
        self.assertGreater(valid,0)

    def test_cube_counts_surface_area_and_spine_certificate(self):
        self.assertEqual([len(self.polycubes[n]) for n in range(1,5)],[1,1,2,8])
        self.assertEqual(sum(map(cubes.is_tree,self.polycubes[4])),7)
        shapes=self.polycubes[3]
        patterns=[]
        for shape in shapes:
            surface=cubes.surface(shape)
            self.assertEqual(len(surface['faces']),14)
            patterns.append(set(cubes.foot_patterns(surface,3)))
        shared=set.intersection(*patterns);self.assertTrue(shared)
        net=cubes.make_net(3,min(shared))
        for shape in shapes:
            surface=cubes.surface(shape);mapping=cubes.fold_net(net,surface)
            self.assertIsNotNone(mapping);self.assertTrue(cubes.verify_net(net,surface,mapping))


    def test_complementary_spine_net_and_empty_target_set(self):
        from experiments.common_nets.complete_planar_cubes import common_spine_net
        surfaces=[cubes.surface(shape) for shape in self.polycubes[3]]
        self.assertIsNone(common_spine_net(surfaces,3,[]))
        net=common_spine_net(surfaces,3,[0,1])
        self.assertIsNotNone(net)
        self.assertEqual(net['coverage'],[0,1])
        for i,surface in enumerate(surfaces):
            self.assertTrue(cubes.verify_net(net,surface,net['mappings'][i]))

    def test_geometric_audit_reproduces_published_individual_inventories(self):
        from experiments.common_nets.audit import single_surface_inventories
        row=dict(surfaces=[engine.surface(c) for c in self.polytets[4]])
        self.assertEqual(sorted(single_surface_inventories(row)),[203,280,452])

    def test_geometric_audit_matches_folder_and_preserves_cut_pattern(self):
        from experiments.common_nets.audit import Surface,unfold,canonical_net
        surfaces=[engine.surface(c) for c in self.polytets[4]]
        checks=[Surface(s) for s in surfaces]
        for edges,selected in verify_six.trees(checks[0].adjacency):
            net=unfold(checks[0],edges,selected)
            if net is None:continue
            for surface,check in zip(surfaces,checks):
                self.assertEqual(check.folds(net),engine.fold_net(net,surface) is not None)
        example=unfold(checks[0],edges,selected)
        self.assertIsNotNone(example)
        shifted=deepcopy(example)
        shifted['triangles']=[[(100-y,50+x+y) for x,y in t] for t in example['triangles']]
        self.assertEqual(canonical_net(example),canonical_net(shifted))


if __name__=='__main__':unittest.main()
