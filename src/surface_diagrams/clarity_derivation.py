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
from .six_seven_structure import SignedResearchFactor,research_hurwitz_move
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
    elif len(source) in (84,86) and positions==(14,16,17,len(source)-1) and all('_source_ref' in s for s in source):first,rechart,cap,final=14,16,17,len(source)-1
    elif len(source)==80 and positions==(11,13,14,79):first,rechart,cap,final=11,13,14,79
    else:raise ValueError('Use the retained79, clearer82 or explicitly referenced83/85-operation source')
    def source_ref(i):
        if '_source_ref' in source[i]:return ((source[i]['_source_file']+':') if '_source_file' in source[i] else '')+source[i]['_source_ref']
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
        elif kind in ('global_conjugation','disk_cyclic_start','peripheral_cleanup') or s.get('parallel_barrier'):s['family']='barrier'
        else:s['family']='disk-local'
        result.append(s);return s
    for i,old in enumerate(source[1:],1):
        previous=result[-1]
        if i==first:
            g=tuple(old['local_after'][0].conjugator);outer=Factor(old['local_after'][1].id,g,1,4)
            outputs=(old['local_after'][0],outer)
            fs=outputs+previous['factors'][3:]
            c=Factor('canonical.R123',g,1,3);q=Factor('canonical.P34',g,3,2);t=Factor('canonical.R124',g+(-3,),1,3)
            parent=(c,q,t);matches=tuple(dict(actual=a,pattern=b,exact_disk_equal=exact_action(a.word,6)==exact_action(b.word,6)) for a,b in zip(previous['factors'][:3],parent)) if final in (82,83,85) else ()
            if final in (82,83,85) and not all(m['exact_disk_equal'] for m in matches):raise ValueError('The clearer PC lantern lost its individual input match')
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
            copied={k:old[k] for k in ('frame','adjacent_moves','inverse_hurwitz_transport','daisy_frame','caption','framed_balance_before_minus_after','parallel_barrier','parallel_barrier_reason') if k in old}
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


def delayed_clarity_source(certificate):
    """Keep the last root intact until both original halves have combined.

    Nine retained disk operations replace eight early-petal operations. Every
    source witness is explicitly addressed; none of the source charts is
    silently treated as a newly normalized chart.
    """
    def converted(raw,ref):
        s=dict(raw,_source_ref=ref)
        for key in ('factors','local_before','local_after'):
            if key in s:s[key]=tuple(factor_from_data(f) for f in s[key])
        return s
    c=certificate
    baseline=tuple(converted(s,'early_boundary.stages.'+str(i)) for i,s in enumerate(c['early_boundary']['stages'][:18]))+tuple(
        converted(s,'named_full_route.stages.'+str(i)) for i,s in enumerate(c['named_full_route']['stages'][15:],15))
    raw=c['early_alternative_transport']['stages'];cyclic=c['named_cyclic_start_shortening']['replacement_interval']
    late=tuple(converted(raw[i],'early_alternative_transport.stages.'+str(i)) for i in range(20,23))+tuple(
        converted(cyclic[i],'named_cyclic_start_shortening.replacement_interval.'+str(i)) for i in range(1,len(cyclic)-1))
    if baseline[34]['factors']!=late[0]['factors'] or baseline[42]['factors']!=late[-1]['factors']:
        raise ValueError('The delayed daisy needs literal complete joins')
    checks=[];expected=exact_action(BOUNDARY*4,5)
    for i,s in enumerate(late):
        for j,a in enumerate((s,)+tuple(s.get('atomic_steps',()))):
            fs=tuple(factor_from_data(f) if isinstance(f,dict) else f for f in a['factors'])
            maximum=max(len(supported_class(f.mapping_class,5)) for f in fs)
            sphere=sphere_chain_certificate(product(fs));lift=homology_action(product(fs))
            if exact_action(product(fs),5)!=expected or maximum>20 or any(getattr(f,'sign',1)!=1 for f in fs) or not sphere['certified'] or lift!=IDENTITY:
                raise ValueError('A retained delayed state lost its positive disk/sphere/lift certificate')
            checks.append(dict(stage=i,atomic=j,faithful_disk_equal=True,positive=True,support_maximum=maximum,sphere_certificate=sphere,chosen_lift=lift))
    frames=[];halves=[]
    for i,(a,b) in enumerate(zip(late,late[1:]),1):
        before=product(a['factors']);after=product(b['factors'])
        if b['kind'] in ('disk_cyclic_start','global_conjugation'):
            g=tuple(b['frame']);before=g+before+inverse_word(g)
            if b['kind']=='disk_cyclic_start' and reduce_word(before)!=reduce_word(after):raise ValueError('Retain the raw cyclic free-word equality')
            if b['kind']=='global_conjugation':
                matches=tuple(dict(id=x.id,exact_disk_equal=x.id==y.id and exact_action(g+x.word+inverse_word(g),5)==exact_action(y.word,5)) for x,y in zip(a['factors'],b['factors']))
                if len(a['factors'])!=len(b['factors']) or not all(m['exact_disk_equal'] for m in matches):raise ValueError('The actual common-chart matches failed')
                frames.append(dict(source_ref=b['_source_ref'],matches=matches))
        if exact_action(before,5)!=exact_action(after,5):raise ValueError('A delayed ordered transition failed')
    for i in range(8):
        old={f.id:f for f in baseline[34+i]['factors'] if f.half};new={f.id:f for f in late[i]['factors'] if f.half}
        if set(old)!=set(new):raise ValueError('The actual half ancestry changed')
        for name,f in old.items():
            if exact_action(f.word,5)!=exact_action(new[name].word,5):raise ValueError('The delay changed a half-twist class')
            halves.append(dict(stage=i,id=name,early=f,delayed=new[name],exact_disk_equal=True))
    daisy=late[-1];daisy['source_title']=daisy['title'];daisy['title']='Expand the retained three-point root after the half twists combine';daisy['parallel_barrier']=True
    daisy['parallel_barrier_reason']='Presentation order: expand only after both half-twist factors are gone; no algebraic noncommutation is asserted.'
    source=daisy['source_stage']
    named=[];splits=[]
    for key in ('local_before','local_after'):
        pattern=tuple(factor_from_data(f) for f in source[key]);actual=daisy[key]
        if len(pattern)!=len(actual):raise ValueError('The daisy term count changed')
        for a,b in zip(actual,pattern):
            if exact_action(a.word,5)!=exact_action(b.word,5):raise ValueError('A delayed actual daisy input/output lost its source chart')
            named.append(dict(side=key,actual=a,source_pattern=b,exact_disk_equal=True))
            split=split_fixed_last_strand(a.word,5)
            if exact_action(split.reconstructed_word,5)!=exact_action(a.word,5):raise ValueError('Retain the full daisy kernel and shadow')
            splits.append(dict(actual=a,split=split))
    balance=tuple(sum(f.power for f in daisy['local_before'] if j in enclosed_boundaries(f.mapping_class,5))-sum(f.power for f in daisy['local_after'] if j in enclosed_boundaries(f.mapping_class,5)) for j in range(1,6))
    if balance!=tuple(daisy['framed_balance_before_minus_after']):raise ValueError('The actual signed PC balance changed')
    discrepancy=reduce_word(product(daisy['local_before'])+inverse_word(product(daisy['local_after'])))
    local_sphere=sphere_chain_certificate(discrepancy);local_lift=homology_action(discrepancy)
    if not local_sphere['certified'] or local_lift!=IDENTITY:raise ValueError('The delayed disk daisy lost its separate local sphere/lift check')
    stages=baseline[:35]+late[1:]+baseline[43:]
    return dict(stages=stages,adoption=dict(previous_source_operations=82,source_operations=len(stages)-1,
        previous_interval=(34,42),current_interval=(34,43),previous_moves=8,current_moves=9,
        literal_complete_joins=True,changed_state_checks=tuple(checks),actual_frame_matches=tuple(frames),
        actual_half_matches=tuple(halves),actual_daisy_matches=tuple(named),actual_daisy_point_pushing=tuple(splits),
        framed_balance_before_minus_after=balance,source_daisy_ref=daisy['_source_ref'],
        disk_daisy_discrepancy=discrepancy,disk_daisy_sphere_certificate=local_sphere,disk_daisy_chosen_lift=local_lift,
        scope='Delay the three-petal expansion until both half twists are gone. This reduces row clutter; the actual half classes, support-length peak and worst-pair intersections are unchanged. One MORE source operation, not a shortening.'))



def preferred_clarity_source(certificate,meeting_route=None):
    """Adopt the reached lower meeting when its explicit report is supplied.

    Omitting that report retains the historical83-operation delayed source.
    No archived source witness is overwritten or silently reinterpreted.
    """
    delayed=delayed_clarity_source(certificate)
    if meeting_route is None:return delayed
    old=delayed['stages'];route=meeting_route
    def factors(data):return tuple(factor_from_data(f) for f in data)
    raw=route['stages'];new=[];checks=[];expected=exact_action(BOUNDARY*4,5)
    if len(raw)!=5 or old[40]['factors']!=factors(raw[0]['factors']) or old[42]['factors']!=factors(raw[-1]['factors']):
        raise ValueError('The lower meeting needs its literal complete input/output joins')
    for i,s in enumerate(raw):
        for j,a in enumerate((s,)+tuple(s.get('atomic_steps',()))):
            fs=factors(a['factors']);maximum=max(len(supported_class(f.mapping_class,5)) for f in fs)
            sphere=sphere_chain_certificate(product(fs));lift=homology_action(product(fs))
            if maximum>20 or exact_action(product(fs),5)!=expected or not sphere['certified'] or lift!=IDENTITY or any(f.power<1 or getattr(f,'sign',1)!=1 for f in fs):
                raise ValueError('A retained meeting state lost positivity, bound or exact certificates')
            checks.append(dict(stage=i,atomic=j,support_maximum=maximum,faithful_disk_equal=True,positive=True,sphere_certificate=sphere,chosen_lift=lift))
        if i:
            item=dict(s,factors=factors(s['factors']),_source_ref='stages.'+str(i),_source_file='six-seven-fixed-half-meeting.json')
            item['adjacent_moves']=s.get('adjacent_checks',0)
            if i in (3,4):
                item['source_title']=item['title']
                item['title']=('Combine the unchanged half twists where they meet' if i==3 else 'Carry the combined full twist UP over five neighbors; the lower square stays fixed')
            new.append(item)
    adjacent=[];previous=old[40]['factors']
    for i,s in enumerate(new,1):
        state=previous
        for j,a in enumerate(s.get('atomic_steps',())):
            move=research_hurwitz_move(state,a['source'],a['target'])
            if move['factors']!=factors(a['factors']):raise ValueError('An actual adjacent route lost its ordered local match')
            state=move['factors'];adjacent.append(dict(stage=i,atomic=j,source=a['source'],target=a['target'],raw_free_discrepancy=move['disk_word_certificate']['discrepancy'],actual_factor_tuple_equal=True))
        if i in (1,2) and state!=s['factors']:raise ValueError('A fixed-half carry did not reach its actual endpoint')
        if i==3:
            k=next(k for k,f in enumerate(previous) if f.id=='F6')
            if previous[k+1].id!='F11' or exact_action(previous[k].word,5)!=exact_action(previous[k+1].word,5):raise ValueError('Combine only the adjacent equal original halves')
            target=replace(previous[k],id=s['factors'][k].id,half=False)
            if previous[:k]+(target,)+previous[k+2:]!=s['factors']:raise ValueError('The combine must retain all actual context factors')
        if i==4 and state!=factors(route['complete_join']['raw']):raise ValueError('The last actual transport must reach the checked raw join')
        previous=s['factors']
    original_halves=tuple(f for f in old[40]['factors'] if f.half)
    if any(tuple(f for f in s['factors'] if f.half)!=original_halves for s in new[:2]) or any(f.half for s in new[2:] for f in s['factors']):
        raise ValueError('Keep both original halves fixed until their separate combine')
    w=route['independent_carries']
    if w['left_then_right']!=w['right_then_left'] or factors(w['left_then_right'])!=new[1]['factors']:
        raise ValueError('The two independent carries lost their literal two-order equality')
    join=route['complete_join'];raw_join=factors(join['raw']);transport_input=factors(join['raw_transport_input'])
    if transport_input!=new[2]['factors']:raise ValueError('Use the actual post-combine input for the full-pair transport')
    raw_discrepancy=reduce_word(product(transport_input)+inverse_word(product(raw_join)))
    if raw_discrepancy:raise ValueError('Keep the full-pair transport raw equality BEFORE B5 presentations')
    matches=tuple(dict(actual=a,presentation=b,exact_disk_equal=a.id==b.id and exact_action(a.word,5)==exact_action(b.word,5)) for a,b in zip(raw_join,new[-1]['factors']))
    if len(raw_join)!=len(new[-1]['factors']) or not all(m['exact_disk_equal'] for m in matches):raise ValueError('Every actual join factor must match separately')
    kernels=[]
    for name,entries in route['neighborhood_kernel_splits'].items():
        for entry in entries:
            f=factor_from_data(entry['closed_neighborhood']);split=split_fixed_last_strand(f.word,5)
            if exact_action(f.word,5)!=exact_action(split.reconstructed_word,5):raise ValueError('Keep the full neighborhood kernel and shadow')
            kernels.append(dict(checkpoint=name,actual_half_or_twist=factor_from_data(entry['actual']),closed_neighborhood=f,split=split))
    stages=old[:41]+tuple(new)+old[43:]
    return dict(stages=stages,adoption=delayed['adoption'],meeting_adoption=dict(
        previous_source_operations=83,source_operations=len(stages)-1,previous_interval=(40,42),current_interval=(40,44),
        previous_local_moves=2,current_local_moves=4,previous_adjacent_checks=6,current_adjacent_checks=11,
        source_file='six-seven-fixed-half-meeting.json',source_refs=tuple(s['_source_ref'] for s in new),
        literal_complete_joins=True,changed_state_checks=tuple(checks),actual_adjacent_matches=tuple(adjacent),original_half_factors=original_halves,
        independent_carries=w,raw_full_pair_transport_discrepancy=raw_discrepancy,actual_join_matches=matches,
        neighborhood_point_pushing=tuple(kernels),adopted=True,
        geometry=dict(original_closed_sum=1094,current_closed_sum=936,original_closed_maximum=48,current_closed_maximum=36,
            original_support_maximum=17,current_support_maximum=18,actual_half_classes_changed=False,old_endpoint_geometry_restored_after_combine=True),
        scope='Two MORE local moves and five MORE adjacent checks. Keep the actual half arcs unchanged and combine them where closed-neighborhood coupling is lower. Carry their full twist afterward, restoring the old endpoint. This is a clarity choice, not a shorter proof or lower whole-proof tangle claim.'))
