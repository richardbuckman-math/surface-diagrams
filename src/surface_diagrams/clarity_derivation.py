"""Clarity-first view: sphere redraws, disk substitutions, and parallel rounds.

The79-operation source remains unchanged. A framing ledger is separate from
all main factor diagrams and is part of the represented word, never omitted.
"""
from dataclasses import dataclass,replace
from itertools import combinations
from .braid_actions import inverse_word,reduce_word
from .factorization_explorer import Factor,product
from .mapping_classes import exact_action,supported_class
from .hyperelliptic_homology import homology_action,IDENTITY
from .sphere_actions import sphere_supported_class,sphere_curve_action,sphere_chain_certificate
from .six_seven_structure import SignedResearchFactor
from .point_pushing import split_fixed_last_strand
from .framed_boundary_relations import enclosed_boundaries

BOUNDARY=(1,2,3,4)*5

@dataclass(frozen=True)
class PeripheralFactor:
    id: str
    conjugator: tuple=()
    first: int=6
    points: int=1
    power: int=2
    half: bool=False
    peripheral: bool=True
    def __post_init__(self):
        if self.conjugator or self.first!=6 or self.points!=1 or self.half or type(self.power) is not int or self.power<2 or self.power%2 or self.peripheral is not True:
            raise ValueError('Only the checked even peripheral powers are used here')
    @property
    def mapping_class(self):return self
    @property
    def core(self):return ()
    @property
    def word(self):return ()


def factor_from_data(f):
    if f.get('peripheral'):return PeripheralFactor(**dict(f,conjugator=tuple(f['conjugator'])))
    cls=SignedResearchFactor if 'sign' in f else Factor
    return cls(**dict(f,conjugator=tuple(f['conjugator'])))


def curve_class(f):
    return sphere_curve_action((),(6,)) if isinstance(f,PeripheralFactor) else sphere_supported_class(f.mapping_class)


def word(state):return (() if state.get('ledger') is None else state['ledger'].word)+product(state['factors'])


def _ledger(power):return None if not power else Factor('framing.ledger',(),1,5,power)


def _interval(before,after):
    p=0
    while p<min(len(before),len(after)) and before[p]==after[p]:p+=1
    q=0
    while q<min(len(before),len(after))-p and before[-1-q]==after[-1-q]:q+=1
    return before[p:len(before)-q if q else len(before)],after[p:len(after)-q if q else len(after)]


def apply_edit(state,edit):
    """Apply one already-certified local edit by literal factor identity."""
    fs=state['factors'];a,b=edit['edit_before'],edit['edit_after']
    if not a:raise ValueError('An independent edit needs a nonempty input interval')
    i=next((i for i in range(len(fs)-len(a)+1) if fs[i:i+len(a)]==a),None)
    if i is None:raise ValueError('The independent local input is not present')
    ledger=state.get('ledger');increment=edit.get('framing_increment',0)
    if increment:ledger=_ledger((0 if ledger is None else ledger.power)+increment)
    return dict(factors=fs[:i]+b+fs[i+len(a):],ledger=ledger)


def refine_sphere_moves(source_stages,factor_certificates):
    source=tuple(dict(s,factors=tuple(s['factors'])) for s in source_stages)
    positions=tuple(i for i,s in enumerate(source) if s['kind']=='sphere_rewrite')
    if len(source)==83 and positions==(14,16,17,82):first,rechart,cap,final=14,16,17,82
    elif len(source)==80 and positions==(11,13,14,79):first,rechart,cap,final=11,13,14,79
    else:raise ValueError('Use the retained79 or clearer82-operation source')
    def source_ref(i):
        return ('early_boundary.stages.'+str(i) if i<=17 else 'named_full_route.stages.'+str(i-3)) if final==82 else 'named_full_route.stages.'+str(i)
    result=[dict(source[0],ledger=None,source_index=0)];curve_checks=[]
    def append(kind,title,fs,ledger=None,**extra):
        before=result[-1];s=dict(kind=kind,title=title,factors=tuple(fs),ledger=ledger,**extra)
        discrepancy=reduce_word(word(before)+inverse_word(word(s)))
        if kind in ('sphere_redraw','curve_redraw'):
            if tuple((f.id,f.power,f.half) for f in before['factors'])!=tuple((f.id,f.power,f.half) for f in s['factors']):raise ValueError('A redraw cannot insert, remove or substitute main factors')
            if 'ledger_redraw' in s:
                a,b=before['ledger'],s['ledger']
                if before['factors']!=s['factors'] or (a.id,a.power)!=(b.id,b.power) or curve_class(a)!=curve_class(b):raise ValueError('The ledger move is not a same-curve redraw')
            else:
                aa,bb=_interval(before['factors'],s['factors'])
                if len(aa)!=1 or len(bb)!=1 or curve_class(aa[0])!=curve_class(bb[0]):raise ValueError('A redraw must change exactly one drawing of the same curve')
            sphere=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
            if not sphere['certified'] or lift!=IDENTITY:raise ValueError('A corrected redraw changed its sphere action or chosen lift')
            s.update(disk_discrepancy=discrepancy,sphere_certificate=sphere,lift_homology=lift)
        elif kind not in ('global_conjugation','disk_cyclic_start'):
            if exact_action(word(before),6)!=exact_action(word(s),6):raise ValueError('A disk-only clarity move changed its disk product')
        a,b=_interval(before['factors'],s['factors'])
        s.update(edit_before=a,edit_after=b,touched_ids=tuple(sorted({f.id for f in a+b})))
        if kind in ('curve_redraw','sphere_redraw'):s['family']='redraw'
        elif kind in ('global_conjugation','disk_cyclic_start','peripheral_cleanup'):s['family']='barrier'
        else:s['family']='disk-local'
        result.append(s);return s
    for i,old in enumerate(source[1:],1):
        previous=result[-1]
        if i==first:
            g=tuple(old['local_after'][0].conjugator);outer=Factor(old['local_after'][1].id,g,1,4)
            outputs=(old['local_after'][0],outer)
            fs=outputs+previous['factors'][3:]
            c=Factor('canonical.R123',g,1,3);q=Factor('canonical.P34',g,3,2);t=Factor('canonical.R124',g+(-3,),1,3)
            parent=(c,q,t);matches=tuple(dict(actual=a,pattern=b,exact_disk_equal=exact_action(a.word,6)==exact_action(b.word,6)) for a,b in zip(previous['factors'][:3],parent)) if final==82 else ()
            if final==82 and not all(m['exact_disk_equal'] for m in matches):raise ValueError('The clearer PC lantern lost its individual input match')
            balance=tuple(sum(f.power for f in previous['factors'][:3] if j in enclosed_boundaries(f.mapping_class,6))-sum(f.power for f in outputs if j in enclosed_boundaries(f.mapping_class,6)) for j in range(1,7))
            splits=tuple(dict(factor=f,split=split_fixed_last_strand(f.word,6)) for f in previous['factors'][:3]+outputs)
            for item in splits:
                if exact_action(item['factor'].word,6)!=exact_action(item['split'].reconstructed_word,6):raise ValueError('The disk lantern lost its full kernel reconstruction')
            append('disk_lantern','Disk lantern: retain the actual four-point outer curve',fs,source_index=i,
                named_witness_ref=source_ref(i),common_chart=g,individual_named_matches=matches,canonical_parent=parent,
                framed_balance_before_minus_after=balance,complete_point_pushing=splits)
            target=old['local_after'][1];fs=(outputs[0],target)+fs[2:]
            if curve_class(outer)!=curve_class(target):raise ValueError('The lantern outer is not its complementary sphere curve')
            append('sphere_redraw','Redraw ONE outer curve from its complementary side',fs,source_index=i,
                redraws=(dict(id=outer.id,before=outer,after=target,same_sphere_curve=True),),framing_increment=0)
        elif i==rechart:
            targets=old['factors'][1:];boundary=old['factors'][0]
            if boundary.points!=5 or boundary.power!=6:raise ValueError('Keep all SIX framing corrections')
            cert_by={c['id']:c for c in factor_certificates}
            if tuple(f.id for f in targets)!=tuple(f.id for f in previous['factors']):raise ValueError('A redraw cannot change the factor list')
            for j,target in enumerate(targets):
                before=result[-1];actual=before['factors'][j];c=cert_by[actual.id];k=c['boundary_power']
                if actual.power!=target.power or actual.half!=target.half or curve_class(actual)!=curve_class(target):
                    raise ValueError('A sphere redraw must retain this factor, its power and its sphere curve')
                if actual==target and not k:continue
                corrected_local=reduce_word(actual.word+inverse_word(BOUNDARY*k+target.word))
                local=sphere_chain_certificate(corrected_local);lift=homology_action(corrected_local)
                if not local['certified'] or lift!=IDENTITY:raise ValueError('A local framing correction was dropped')
                total=(0 if before['ledger'] is None else before['ledger'].power)+k
                fs=before['factors'][:j]+(target,)+before['factors'][j+1:]
                disk_equal=exact_action(actual.word,6)==exact_action(target.word,6)
                s=append('curve_redraw' if disk_equal else 'sphere_redraw',
                    'Redraw '+actual.id+' in the five-point chart',fs,_ledger(total),source_index=i,
                    redraws=(dict(id=actual.id,before=actual,after=target,same_sphere_curve=True),),
                    framing_increment=k,corrected_local_disk_discrepancy=corrected_local,
                    corrected_local_sphere_certificate=local,corrected_local_lift=lift,
                    uncorrected_curve_lift=homology_action(reduce_word(actual.word+inverse_word(target.word))))
                curve_checks.append(s)
            if result[-1]['factors']!=targets or result[-1]['ledger'].power!=6:raise ValueError('The redraw ledger failed its literal six-correction join')
        elif i==cap:
            before=result[-1];ledger=before['ledger']
            if ledger is None or ledger.power!=6:raise ValueError('The six corrections must stay explicit')
            per=PeripheralFactor(ledger.id,power=6)
            if curve_class(ledger)!=curve_class(per):raise ValueError('The ledger curve is not peripheral on the sphere')
            append('sphere_redraw','Redraw the SIX-correction ledger curve around point6',before['factors'],per,
                source_index=i,ledger_redraw=dict(before=ledger,after=per,same_sphere_curve=True),framing_increment=0,source_unit_lift=homology_action(BOUNDARY))
            append('peripheral_cleanup','Clear the already-peripheral SIX-correction ledger',before['factors'],None,
                source_index=i,ledger_cleanup=True,chosen_lift=IDENTITY)
        elif i==final:
            before=result[-1];f=before['factors'][0]
            if len(before['factors'])!=1 or f.points!=5 or f.power!=4:raise ValueError('Keep the complete FOURTH power')
            per=PeripheralFactor(f.id,power=4)
            if curve_class(f)!=curve_class(per):raise ValueError('The terminal curve is not peripheral')
            append('sphere_redraw','Redraw the FOURTH-power exterior curve around point6',(per,),source_index=i,
                redraws=(dict(id=f.id,before=f,after=per,same_sphere_curve=True),),framing_increment=0,source_unit_lift=homology_action(BOUNDARY))
            append('peripheral_cleanup','Remove the already-peripheral FOURTH-power twist',(),source_index=i,chosen_lift=IDENTITY)
        else:
            copied={k:old[k] for k in ('frame','adjacent_moves','inverse_hurwitz_transport','daisy_frame','caption','framed_balance_before_minus_after') if k in old}
            s=append(old['kind'],old['title'],old['factors'],source_index=i,**copied)
            s['source_witness_ref']=source_ref(i)
            if old['kind'] in ('global_conjugation','disk_cyclic_start'):
                g=tuple(old['frame']);expected=g+word(previous)+inverse_word(g)
                if exact_action(expected,6)!=exact_action(word(s),6):raise ValueError('An explicit common frame changed during clarification')
            if result[-1]['factors']!=old['factors']:raise ValueError('A reused source move changed its actual factors')
    if result[-1]['factors'] or result[-1]['ledger'] is not None:raise ValueError('The clarified route did not end')
    return dict(stages=tuple(result),source_operations=len(source)-1,clarified_moves=len(result)-1,
        sphere_redraw_moves=sum(s['kind']=='sphere_redraw' for s in result),
        redraws_mix_substitutions=False,framing_corrections_retained=6,
        priority='Clear redraws and simpler geometry take precedence over operation count.')


def parallel_rounds(stages):
    """Group only consecutive disjoint edits with explicit two-order witnesses."""
    stages=tuple(stages);rounds=[];i=1
    while i<len(stages):
        start=i;group=[stages[i]];family=stages[i]['family'];used=set(stages[i]['touched_ids'])
        if family!='barrier' and stages[i]['edit_before']:
            while i+1<len(stages):
                nxt=stages[i+1]
                if nxt['family']!=family or not nxt['edit_before'] or used.intersection(nxt['touched_ids']):break
                group.append(nxt);used.update(nxt['touched_ids']);i+=1
        source=stages[start-1];witnesses=[]
        for a,b in combinations(group,2):
            ab=apply_edit(apply_edit(source,a),b);ba=apply_edit(apply_edit(source,b),a)
            if ab!=ba:raise ValueError('The proposed parallel edits do not commute')
            witnesses.append(dict(left=a['title'],right=b['title'],literal_two_order_equality=True))
        if len(group)>1:
            current=dict(factors=source['factors'],ledger=source.get('ledger'))
            for edit in group:current=apply_edit(current,edit)
            if current!=dict(factors=stages[i]['factors'],ledger=stages[i].get('ledger')):raise ValueError('The parallel round failed its sequential join')
        cards=[]
        for edit in group:
            after=apply_edit(source,edit) if len(group)>1 else dict(factors=edit['factors'],ledger=edit.get('ledger'))
            card=dict(move_index=stages.index(edit),before=dict(factors=source['factors'],ledger=source.get('ledger')),after=after)
            if edit['family']=='redraw':
                discrepancy=reduce_word(word(source)+inverse_word(word(after)))
                certificate=sphere_chain_certificate(discrepancy);lift=homology_action(discrepancy)
                if not certificate['certified'] or lift!=IDENTITY:raise ValueError('An independent redraw card lost its corrected lift')
                card.update(disk_discrepancy=discrepancy,sphere_certificate=certificate,lift_homology=lift)
            cards.append(card)
        rounds.append(dict(number=len(rounds)+1,first_move=start,last_move=i,move_count=len(group),family=family,
            simultaneous=len(group)>1,before=dict(factors=source['factors'],ledger=source.get('ledger')),
            after=dict(factors=stages[i]['factors'],ledger=stages[i].get('ledger')),cards=tuple(cards),
            independence_witnesses=tuple(witnesses)))
        i+=1
    return tuple(rounds)
