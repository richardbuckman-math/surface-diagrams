"""Import source-pinned planar construction records; not needed by package users.

Run with --source-root pointing at the separate Planar Mapping Class Groups
checkout. Only this explicit importer requires that old package. All ordinary
builders/tests use the generated native records and copied source witnesses.
"""
from pathlib import Path
from dataclasses import asdict
from hashlib import sha256
import argparse,json,sys,shutil

ROOT=Path(__file__).resolve().parents[1]

def import_sources(source_root):
    old=Path(source_root).resolve()
    sys.path.insert(0,str(old/'src'));sys.path.insert(0,str(old/'scratch'))
    from planar_mcg import ten_ten as t
    from planar_mcg.examples import six_strand_two_six_factorization
    from planar_mcg.elements import coerce_planar_element
    from planar_mcg.curves import CutIntersectionLoop
    import generate_four_three_derivation_sheet as four
    from surface_diagrams.factorization_explorer import Factor
    from surface_diagrams.braid_actions import reduce_word,inverse_word
    from surface_diagrams.mapping_classes import exact_action
    def record(v,ident,n):
        if isinstance(v,CutIntersectionLoop):
            if len(v.cut_intersections)!=2:
                return dict(source_type='CutIntersectionLoop',source_geometry=dict(cuts=v.cut_intersections,start_above=v.start_above),algebraic_encoding_provided=False)
            v=v.dehn_twist()
        raw=reduce_word(coerce_planar_element(v).capped_mapping_class.braid.word)
        signed=getattr(v,'power',1);sign=1 if signed>0 else -1;power=abs(signed)
        half='ArcTwist' in type(v).__name__
        positive=raw if sign==1 else inverse_word(raw);candidates=[]
        for points in ((2,) if half else range(2,n+1)):
            core_len=power if half else points*(points-1)*power
            if len(positive)<core_len or (len(positive)-core_len)%2:continue
            k=(len(positive)-core_len)//2;g=positive[:k]
            for first in range(1,n-points+2):
                f=Factor(ident,g,first,points,power,half)
                if f.word==positive:candidates.append(f)
        if not candidates:raise ValueError(('Cannot recover a structured source factor',type(v).__name__,raw))
        f=min(candidates,key=lambda x:(len(x.conjugator),x.first,x.points))
        assert exact_action(f.word,n)==exact_action(positive,n)
        return dict(factor=asdict(f),sign=sign,source_word=raw,source_type=type(v).__name__)
    def sequence(f,prefix):
        return dict(points=f.surface.total_strands,factors=[record(v,prefix+str(i+1),f.surface.total_strands) for i,v in enumerate(f.factors)])
    data={name:sequence(fn(),name+'.') for name,fn in [
        ('six_two',six_strand_two_six_factorization),('four_three_A',t.four_three_a_factorization),
        ('four_three_B',t.four_three_b_factorization),('four_three_C',t.four_three_c_factorization),
        ('ten_ten_reviewed_start',t.tentenstart_diagram_factorization),
        ('ten_ten_reviewed_final',t.tentenhalf_lantern_factorization),
        ('half_lantern_standard_left',t.tentenhalf_lantern_standard_left_factorization),
        ('half_lantern_standard_right',t.tentenhalf_lantern_standard_right_factorization)]}
    data['four_three_panels']=[]
    for panel in four.build_panels():
        factors=four.factor_sequence(panel)
        data['four_three_panels'].append(dict(title=panel.title,note=panel.note,points=panel.surface.total_strands,
            factors=[record(v,'P'+str(len(data['four_three_panels'])+1)+'.'+str(i+1),panel.surface.total_strands) for i,v in enumerate(factors)]))
    data['ten_ten_conversion_word']=(-3,4,5,5,4,3,1,2)
    archive=ROOT/'docs/proofs/fibration-sources/planar-mcg-2026-10-30';archive.mkdir(parents=True,exist_ok=True)
    files=['src/planar_mcg/ten_ten.py','src/planar_mcg/examples.py','src/planar_mcg/constructors.py',
           'scratch/generate_four_three_derivation_sheet.py','scratch/generate_tenten_half_lantern_figures.py',
           'scratch/generate_tenten_half_lantern_stepwise.py','docs/assets/tenten-half-lantern.png','docs/assets/four-three-daisy.png']
    pins=[]
    for name in files:
        src=old/name;dest=archive/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
        pins.append(dict(source_relative_path=name,archive_relative_path=name,bytes=dest.stat().st_size,sha256=sha256(dest.read_bytes()).hexdigest()))
    manifest=dict(source_project='Planar Mapping Class Groups',original_root=str(old),source_commit=None,
        source_git_state='master had no commits; these exact untracked source bytes are pinned',
        imported_date='2026-10-30',files=pins,
        scope='The reviewed drawing edits are imported as unadopted historical source, not assumed equal to the original exact construction. Native derivations separately verify every used word. No runtime dependency on the old project.')
    (archive/'provenance.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    text=json.dumps(data,separators=(',',':'),ensure_ascii=True)
    (archive/'factor-records.json').write_text(text,encoding='utf-8')
    generated='"""Native records imported from pinned planar sources; do not edit by hand."""\nimport json\n\nSOURCE_RECORDS = json.loads('+repr(text)+')\n'
    (ROOT/'src/surface_diagrams/_fibration_source_records.py').write_bytes(generated.encode('utf-8'))
    print(json.dumps(dict(archive=str(archive),factor_records_bytes=len(text),generated_sha256=sha256(generated.encode()).hexdigest(),sequences=list(data))))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-root',required=True)
    import_sources(parser.parse_args().source_root)
