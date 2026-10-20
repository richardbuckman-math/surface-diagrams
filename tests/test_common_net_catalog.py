"""Catalog filters, source-record validation, and the 16/37/47 reconciliation."""
import json
from pathlib import Path
import unittest
from experiments.common_nets.catalog_compare import parse_catalog,summarize,apply_comparison,PICTURED_IDS


def record(d,members,counts,pairs):
    return ('{d=%03d,dels={%s},total=%d,subtotals={%s},{%s}}' %
            (d,','.join(map(str,members)),sum(counts),','.join(map(str,counts)),
             ','.join('(del=%d,net=%d)' % pair for pair in pairs)))


class PublishedCatalogTests(unittest.TestCase):
    def sample(self):
        return '\n'.join([
            record(1,[1,2,3],[1,1,1,0,0],[(f,1) for f in (1,2,3)]),
            record(2,[1,2,3,5],[1,1,1,0,1],[(f,2) for f in (1,2,3)]+[(5,1)]),
            record(3,[1,2,3],[6,6,6,0,0],[(f,n) for f in (1,2,3) for n in range(3,9)])])

    def test_covering_a_set_differs_from_exclusive_membership_and_variant_count(self):
        result=summarize(parse_catalog(self.sample()))
        self.assertEqual(result['common_outlines'],3)
        self.assertEqual(result['pictured_exclusive_ids'],[1])
        self.assertEqual(result['common_fixed_cut_variant_count'],8)
        self.assertEqual(result['common_variant_histogram'],{1:2,6:1})

    def test_corrupt_or_duplicated_source_records_are_rejected(self):
        text=self.sample()
        with self.assertRaises(ValueError):parse_catalog(text.replace('total=3','total=4',1))
        with self.assertRaises(ValueError):parse_catalog(text+'\n'+text.splitlines()[0])
        bad=parse_catalog(text.replace('(del=1,net=1)','(del=1,net=99)',1))
        with self.assertRaises(ValueError):summarize(bad)

    def test_published_summary_matches_audit_and_picture_ids(self):
        path=Path(__file__).resolve().parents[1]/'experiments/common_nets/reference/mabry-four-comparison.json'
        comparison=json.loads(path.read_text())
        self.assertEqual(comparison['outline_records'],448)
        self.assertEqual(comparison['per_surface_totals'],[452,280,203,98,242])
        self.assertEqual(tuple(comparison['pictured_exclusive_ids']),PICTURED_IDS)
        self.assertEqual(comparison['common_variant_histogram'],{'1':35,'6':2})
        self.assertEqual(comparison['six_variant_outline_ids'],[5,405])
        row=dict(common_footprints=37,common_net_count=47,
                 single_surface_inventory_counts=[203,280,452],published_common_net_count=16)
        apply_comparison(row,comparison)
        self.assertTrue(row['common_count_discrepancy_resolved'])
        self.assertEqual(row['published_picture_count'],16)
        self.assertNotIn('published_common_net_count',row)
        row['common_footprints']=38
        with self.assertRaises(ValueError):apply_comparison(row,comparison)


if __name__=='__main__':unittest.main()
