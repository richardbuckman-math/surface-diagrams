"""Exact factor records and checked local rewrites for the six-point prototype."""
from dataclasses import dataclass, replace, asdict
from .braid_actions import reduce_word, inverse_word
from .mapping_classes import ConjugatedTwist,exact_action


@dataclass(frozen=True)
class Factor:
    id: str
    conjugator: tuple
    first: int
    points: int
    power: int = 1
    half: bool = False

    @property
    def mapping_class(self):
        return ConjugatedTwist(self.conjugator,self.first,self.points,self.power,self.half)

    @property
    def core(self):
        return self.mapping_class.core

    @property
    def word(self):
        return self.mapping_class.word

    @property
    def label(self):
        return ('Half twist' if self.half else f'{self.points}-point twist')+(f' × {self.power}' if self.power!=1 else '')


def initial_factors():
    # Conjugate cores extracted from the user's earlier 178-letter SVG.
    data=[((),3,3,2,False),((5,-3,-3,4),3,2,1,True),
          ((3,2),1,2,1,True),((-1,-2,-3,2,-3),4,3,2,False),
          ((),2,3,2,False),((-5,-5,-2,-3,-3,4),3,2,1,True),
          ((-5,-2,-3,4,-3),2,2,1,True),((-2,-3,4),2,3,2,False),
          ((-2,-3,4,2,-3,-2,-2),1,2,1,True),((-2,-3),4,3,2,False),
          ((-5,-5,4,3,1,-2),1,2,1,True),((-5,4,3),1,3,2,False),
          ((-5,),3,3,2,False)]
    return tuple(Factor(f'F{i+1}',*values) for i,values in enumerate(data))


def product(factors):
    return tuple(i for f in factors for i in f.word)


def validate_size(factors):
    if sum(len(f.word) for f in factors)>3500 or len(factors)>80:
        raise ValueError('This prototype limits a state to 80 factors and 3500 braid letters. Undo or simplify first.')
    if any(len(f.conjugator)>1500 or f.power>32 or len(f.id)>250 for f in factors):
        raise ValueError('Factor record exceeds the saved-workspace limit. Undo or simplify first.')
    if len({f.id for f in factors})!=len(factors):
        raise ValueError('This operation would duplicate a factor ID; rename the records in a saved file first.')


def checked(before,after):
    validate_size(after)
    if exact_action(product(before))!=exact_action(product(after)):
        raise ValueError('Exact disk action verification failed; operation was not applied')
    return tuple(after)


def parse_global_conjugator(word):
    if not isinstance(word,(list,tuple)) or len(word)>1500 or any(
            type(i) is not int or not 1<=abs(i)<=5 for i in word):
        raise ValueError('Global conjugator must contain at most 1500 signed generators 1..5')
    return reduce_word(word)


def checked_global_frame(factors,frame):
    """Check a factorization against a globally conjugated starting product."""
    frame=parse_global_conjugator(frame)
    validate_size(factors)
    expected=frame+product(initial_factors())+inverse_word(frame)
    if exact_action(product(factors))!=exact_action(expected):
        raise ValueError('Product does not match its saved global conjugation')
    return tuple(factors)


def global_conjugate_factors(factors,word):
    """Apply one simultaneous conjugation and verify its exact disk action."""
    word=parse_global_conjugator(word)
    if not word:return tuple(factors)
    result=tuple(simplify_factor(replace(f,conjugator=reduce_word(word+f.conjugator)))
                 for f in factors)
    validate_size(result)
    expected=word+product(factors)+inverse_word(word)
    if exact_action(product(result))!=exact_action(expected):
        raise ValueError('Global conjugation failed exact disk-action verification')
    return result


def move_factor(factors,source,target):
    """Dragged factor remains unchanged; it conjugates each crossed factor."""
    factors=list(factors)
    if type(source) is not int or type(target) is not int or not 0<=source<len(factors) or not 0<=target<len(factors):
        raise ValueError('Choose two valid factor positions')
    while source<target:
        u,v=factors[source:source+2]
        changed=simplify_factor(replace(v,conjugator=reduce_word(u.word+v.conjugator)))
        factors[source:source+2]=checked((u,v),(changed,u))
        source+=1
    while source>target:
        v,u=factors[source-1:source+1]
        changed=simplify_factor(replace(v,conjugator=reduce_word(inverse_word(u.word)+v.conjugator)))
        factors[source-1:source+1]=checked((v,u),(u,changed))
        source-=1
    validate_size(factors)
    return tuple(factors)


def simplify_factor(factor):
    from .twist_simplify import simplify_twist
    simplified=simplify_twist(factor.mapping_class)
    return replace(factor,conjugator=simplified.conjugator,first=simplified.first)


def split_factor(factors,index,kind):
    f=factors[index]
    if kind=='powers' and f.power>1:
        replacements=tuple(replace(f,id=f'{f.id}.{i+1}',power=1) for i in range(f.power))
    elif kind=='halves' and not f.half and f.points==2:
        replacements=tuple(replace(f,id=f'{f.id}.h{i+1}',half=True,power=1) for i in range(2*f.power))
    elif kind=='lantern' and not f.half and f.points==3:
        i=f.first
        replacements=tuple(Factor(f'{f.id}.L{repeat+1}.{j+1}',reduce_word(f.conjugator+g),a,2)
            for repeat in range(f.power) for j,(g,a) in enumerate((((),i),((i+1,),i),((),i+1))))
    else:
        raise ValueError('That split is not available for this factor')
    checked((f,),replacements)
    result=tuple(factors[:index])+replacements+tuple(factors[index+1:])
    validate_size(result)
    return result


def combine_factors(factors,index):
    if not 0<=index<len(factors)-1: raise ValueError('Select a factor with a following neighbor')
    a,b=factors[index:index+2]
    unit_a=replace(a,power=1)
    unit_b=replace(b,power=1)
    same=(a.first,a.points,a.half)==(b.first,b.points,b.half)
    if same and exact_action(unit_a.word)==exact_action(unit_b.word):
        consumed=2; total=a.power+b.power
        combined=replace(a,id=f'{a.id}+{b.id}',power=total)
        if a.half and total%2==0:
            combined=replace(combined,half=False,power=total//2)
    else:
        triple=factors[index:index+3]
        if len(triple)!=3 or a.first>4 or any(f.half or f.points!=2 or f.power!=1 for f in triple):
            raise ValueError('Combine needs equal neighboring powers or a verified three-factor marked-point lantern')
        combined=Factor('+'.join(f.id for f in triple),a.conjugator,a.first,3)
        if exact_action(product(triple))!=exact_action(combined.word):
            raise ValueError('These three neighbors do not match the marked-point lantern candidate')
        consumed=3
    checked(factors[index:index+consumed],(combined,))
    result=tuple(factors[:index])+(combined,)+tuple(factors[index+consumed:])
    validate_size(result)
    return result


def export_factors(factors):
    return {'format':'surface-diagrams-factorization-v1','strands':6,
            'source':'Earlier BraidSixSeven SVG; remaining PDF support correspondence provisional',
            'factors':[dict(asdict(f),word=f.word) for f in factors]}


def parse_factors(document):
    """Validate saved records without asserting equality of their product."""
    if not isinstance(document,dict) or document.get('format')!='surface-diagrams-factorization-v1' or document.get('strands')!=6:
        raise ValueError('Choose a six-strand Factorization Lab JSON file')
    rows=document.get('factors')
    if not isinstance(rows,list) or not 1<=len(rows)<=80: raise ValueError('Expected 1 to 80 factors')
    factors=[]; ids=set()
    for row in rows:
        if not isinstance(row,dict): raise ValueError('Invalid factor record')
        identity=row.get('id'); g=row.get('conjugator'); first=row.get('first'); count=row.get('points'); power=row.get('power'); half=row.get('half')
        if not isinstance(identity,str) or not 1<=len(identity)<=250 or identity in ids: raise ValueError('Factor IDs must be distinct short strings')
        ids.add(identity)
        if not isinstance(g,list) or len(g)>1500 or any(type(i) is not int or not 1<=abs(i)<=5 for i in g): raise ValueError('Invalid conjugator')
        if type(first) is not int or type(count) is not int or not 2<=count<=6 or not 1<=first<=7-count: raise ValueError('Invalid support interval')
        if type(power) is not int or not 1<=power<=32 or type(half) is not bool or (half and count!=2): raise ValueError('Invalid twist power or type')
        f=Factor(identity,reduce_word(g),first,count,power,half)
        if 'word' in row and row['word']!=list(f.word): raise ValueError('Saved braid word disagrees with its factor record')
        factors.append(f)
    return tuple(factors)


def import_factors(document):
    # Import only an equivalent exploration of the supplied starting product.
    return checked(initial_factors(),parse_factors(document))
