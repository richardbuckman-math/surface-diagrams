"""Exact post-half outer contraction and the separate45 comparison."""
from dataclasses import asdict,replace
from hashlib import sha256
from pathlib import Path
import json
from examples.analyze_fixed_half_gather import equality,matrix
from surface_diagrams.braid_actions import inverse_word,reduce_word
from surface_diagrams.clarity_derivation import factor_from_data
from surface_diagrams.early_boundary_pure import _score
from surface_diagrams.factorization_explorer import Factor
from surface_diagrams.posthalf_outer import contract_posthalf_daisy,reconstruct_posthalf_145
from surface_diagrams.six_seven_structure import research_hurwitz_move
ROOT=Path(__file__).resolve().parents[1]


def report():
    path=ROOT/'docs/proofs/six-seven-posthalf-spare.json';old=json.loads(path.read_text(encoding='utf-8'));source=tuple(factor_from_data(f) for f in old['route']['factors']);target=old['new_round45_donor_target'];parent=factor_from_data(target['original145_parent']);outputs=tuple(factor_from_data(f) for f in target['original145_source_outputs'])
    selected=contract_posthalf_daisy(source);alternative=reconstruct_posthalf_145(source,parent,outputs)
    q45=Factor('round45',(),4,2);spare=next(f for f in source if f.id=='posthalf.output.1');w=next(f for f in source if f.id=='posthalf.supply.0')
    preliminary=tuple(dict(sign=s,candidate=replace(spare,conjugator=reduce_word((q45.word if s==1 else inverse_word(q45.word))+spare.conjugator)),comparison=equality(replace(spare,conjugator=reduce_word((q45.word if s==1 else inverse_word(q45.word))+spare.conjugator)).word,w.word),applied=False) for s in (-1,1))
    fs=alternative['factors'];rejected=[]
    for a,b in ((12,11),(11,12)):
        raw=research_hurwitz_move(fs,a,b);score=_score(raw['factors'])
        if score['max_support_word']<=20:raise ValueError('The saved over-bound next carry changed')
        rejected.append(dict(source=a,target=b,raw_move=raw,score=score,applied=False))
    before,after,other=(matrix(fs) for fs in (source,selected['factors'],alternative['factors']))
    by={f.id:f for f in selected['factors']};new15=by['outer.loan.1'];old15=tuple(f for f in source if f.id in ('posthalf.supply.0','posthalf.output.1'))
    new15_matches=tuple(dict(old=f,comparison=equality(new15.word,f.word)) for f in old15)
    if any(x['comparison']['equal'] for x in new15_matches):raise ValueError('The new target must use a genuinely different15 class')
    shared=tuple(f.id for f in source if any(g.id==f.id for g in selected['factors']))
    if any(next(f for f in source if f.id==name)!=next(f for f in selected['factors'] if f.id==name) for name in shared):raise ValueError('Every shared actual record stays literal')
    return dict(source_file=path.name,source_sha256=sha256(path.read_bytes()).hexdigest(),source_ref='route.factors',route=selected,round45_comparison=alternative,preliminary_spare_matches=preliminary,rejected_next_comparison_carries=tuple(rejected),before_closed_matrix=before,after_closed_matrix=after,comparison_closed_matrix=other,shared_actual_records_unchanged=shared,next_new15_triangle_target=dict(actual_inputs=(by['alternative.P13'],by['alternative.return.2'],new15),new15_comparisons=new15_matches,applied=False,necessary_ordered_relation_checked=False,scope='The new125-loan15 is different from BOTH old15 records,so the old unchanged-triangle exclusions do not cover this candidate. No joint135 rose,ordered centrality test,gather or contraction is claimed. First check an exact necessary ordered relation; only then seek a useful common chart involving newO1245 and actual round234.'),posthalf_combined_operations=old['posthalf_combined_operations']+4,posthalf_combined_adjacent_checks=old['posthalf_combined_adjacent_checks']+1,research_prefix_operation_count_at_checkpoint=63,preferred_moves=101,preferred_steps=71,public_replay_changed=False,
        scope='Selected4-move route has14 records rather than15 and a named four-point outer. Endpoint support15/85,braid200,CLOSED524/34 versus source15/103,232,700/34. Inventories differ, so totals are descriptive,not an entrywise dominance or whole-proof complexity claim. The12 loan remains consumed in the outer; two125 donor petals remain. The3-move45 alternative restores145 using a matching OTHERW copy and retains originalW; it is not selected. Preferred complete101/71 stays solved and unchanged; no useful complete suffix join is reached.')


if __name__=='__main__':
    r=report();p=ROOT/'docs/proofs/six-seven-posthalf-outer.json'
    with p.open('w',encoding='utf-8',newline='\n') as f:json.dump(r,f,default=asdict,separators=(',',':'))
    print('Selected',r['route']['graphical_operations'],len(r['route']['factors']),r['route']['after_score'],'CLOSED',r['after_closed_matrix']['total'],p.stat().st_size)
