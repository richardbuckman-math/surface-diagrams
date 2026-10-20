"""Reconcile Mabry's pictured 16 with the complete four-unit net catalog.

Parsing/summarizing uses the standard library. The optional PDF CLI imports
pypdf. No source PDF is bundled or sent to any external service.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re

CATALOG_URL = 'https://lsusmath.rickmabry.org/rmabry/dodec/delta/commonNets-fiveDeltahedra-catalog1.pdf'
PICTURED_IDS = (6,12,13,23,28,97,105,155,164,216,309,323,342,374,376,447)
HEADER = re.compile(r'd\s*=\s*(\d+),\s*dels\s*=\s*\{([^}]+)\},\s*total\s*=\s*(\d+),\s*subtotals\s*=\s*\{([^}]+)\}')
PAIR = re.compile(r'\(\s*del\s*=\s*(\d+),\s*net\s*=\s*(\d+)\s*\)')


def parse_catalog(text):
    headers = list(HEADER.finditer(text))
    if not headers:
        raise ValueError('No catalog records found')
    result = []
    for i, match in enumerate(headers):
        d, members, total, subtotals = match.groups()
        members = sorted(map(int, members.split(',')))
        subtotals = list(map(int, subtotals.split(',')))
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        pairs = [tuple(map(int, pair)) for pair in PAIR.findall(text[match.end():end])]
        if len(subtotals) != 5 or any(n < 0 for n in subtotals):
            raise ValueError('Invalid five-surface subtotals')
        if sum(subtotals) != int(total) or len(pairs) != int(total):
            raise ValueError('Catalog totals do not match its net records')
        if members != [j + 1 for j, n in enumerate(subtotals) if n]:
            raise ValueError('Membership does not match subtotals')
        counts = Counter(f for f, net in pairs)
        if [counts[j] for j in range(1, 6)] != subtotals:
            raise ValueError('Per-surface records do not match subtotals')
        result.append(dict(d=int(d), members=members, subtotals=subtotals, pairs=pairs))
    if len({entry['d'] for entry in result}) != len(result):
        raise ValueError('Duplicate outline ID')
    return result


def summarize(entries):
    common = [e for e in entries if {1,2,3} <= set(e['members'])]
    exclusive = [e for e in common if e['members'] == [1,2,3] and e['subtotals'][:3] == [1,1,1]]
    if any(len(set(e['subtotals'][:3])) != 1 for e in common):
        raise ValueError('Common outline has unequal variant counts; inspect cuts explicitly')
    totals = [sum(e['subtotals'][j] for e in entries) for j in range(5)]
    # Every numbered per-surface net must occur once in the outline catalog.
    for surface in range(1, 6):
        ids = [net for e in entries for f, net in e['pairs'] if f == surface]
        if sorted(ids) != list(range(1, totals[surface - 1] + 1)):
            raise ValueError('Per-surface net IDs are not a complete unique inventory')
    counts = Counter(e['subtotals'][0] for e in common)
    return dict(outline_records=len(entries), per_surface_totals=totals,
                common_outline_ids=[e['d'] for e in common], common_outlines=len(common),
                pictured_exclusive_ids=[e['d'] for e in exclusive],
                pictured_exclusive_count=len(exclusive),
                common_variant_histogram=dict(sorted(counts.items())),
                six_variant_outline_ids=[e['d'] for e in common if e['subtotals'][0] == 6],
                common_fixed_cut_variant_count=sum(e['subtotals'][0] for e in common),
                common_records=[dict(d=e['d'],members=e['members'],subtotals=e['subtotals']) for e in common])


def run(pdf, destination, audit_path=None):
    from pypdf import PdfReader
    reader = PdfReader(pdf)
    entries = parse_catalog('\n'.join(page.extract_text() for page in reader.pages))
    result = summarize(entries)
    assert result['outline_records'] == 448
    assert result['per_surface_totals'] == [452,280,203,98,242]
    assert tuple(result['pictured_exclusive_ids']) == PICTURED_IDS
    assert result['common_outlines'] == 37
    assert result['common_fixed_cut_variant_count'] == 47
    result.update(source_url=CATALOG_URL, source_sha256=sha256(pdf.read_bytes()).hexdigest(),
                  pictured_ids_transcribed_from='fiveDeltahedra-commonNets-threeTet4linge-deciamonds.png',
                  explanation='The pictured 16 exclude outlines that also fold into the other two deltahedra and exclude the two six-cut-variant outlines. The complete catalog has 37 shared outlines; 35 single variants plus 2*6 variants give 47, agreeing with both local folding implementations.')
    if audit_path:
        audit = json.loads(audit_path.read_text())
        apply_comparison(audit['4'], result)
        audit_path.write_text(json.dumps(audit, separators=(',', ':')))
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('common_records','common_outline_ids','explanation')}))
    return result


def apply_comparison(row, comparison):
    checks = [row['common_footprints'] == comparison['common_outlines'],
              row['common_net_count'] == comparison['common_fixed_cut_variant_count'],
              sorted(row['single_surface_inventory_counts']) == sorted(comparison['per_surface_totals'][:3]),
              tuple(comparison['pictured_exclusive_ids']) == PICTURED_IDS]
    if not all(checks):
        raise ValueError('Local audit and published catalog do not agree')
    row.pop('published_common_net_count', None)
    row.update(common_count_discrepancy_resolved=True,
               published_picture_count=comparison['pictured_exclusive_count'],
               catalog_comparison=comparison)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--audit', type=Path)
    args = parser.parse_args()
    run(args.pdf, args.destination, args.audit)
