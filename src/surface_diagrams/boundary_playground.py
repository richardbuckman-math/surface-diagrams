"""Exact, reusable factorization state for a marked-point boundary twist.

This is a disk-braid calculation. Inner-boundary framings, daisy and rose
relations, and changes in the number of marked points need separate encodings.
"""

from dataclasses import asdict, dataclass, replace

from .braid_actions import inverse_word, reduce_word
from .factorization_explorer import Factor
from .mapping_classes import exact_action
from .twist_simplify import simplify_twist


FORMAT = 'surface-diagrams-boundary-playground-v1'
SUPPORTED_POINTS = (3, 5)
MAX_POWER = 32
MAX_FACTORS = 80
MAX_LETTERS = 3500


def _word(factors):
    return tuple(letter for factor in factors for letter in factor.word)


def _same_action(points, before, after):
    if exact_action(_word(before), points) != exact_action(_word(after), points):
        raise ValueError('Replacement does not preserve the exact disk braid action')


def _validated_factor(factor, points):
    if not isinstance(factor, Factor):
        raise TypeError('Factors must be Factor records')
    if not isinstance(factor.id, str) or not factor.id or len(factor.id) > 250 or factor.id.splitlines() != [factor.id]:
        raise ValueError('Factor IDs must be nonempty single-line text of at most 250 characters')
    if (type(factor.first) is not int or type(factor.points) is not int or
            not 2 <= factor.points <= points or not 1 <= factor.first <= points-factor.points+1):
        raise ValueError('Factor support lies outside the marked disk')
    if type(factor.power) is not int or not 1 <= factor.power <= MAX_POWER:
        raise ValueError('Factor power must be between 1 and 32')
    if type(factor.half) is not bool or (factor.half and factor.points != 2):
        raise ValueError('Only two-point factors can be half twists')
    if (not isinstance(factor.conjugator, tuple) or len(factor.conjugator) > 1500 or
            any(type(i) is not int or not 1 <= abs(i) < points for i in factor.conjugator)):
        raise ValueError('Factor conjugator uses invalid braid generators')


@dataclass(frozen=True)
class BoundaryProject:
    """An ordered positive factorization of one selected boundary twist power.

    Factor order is the braid-word order used by ``exact_action``. Every
    construction and mutation verifies the complete product in B_points.
    """

    points: int
    power: int
    factors: tuple

    def __post_init__(self):
        if type(self.points) is not int or self.points not in SUPPORTED_POINTS:
            raise ValueError('Choose 3 or 5 marked points')
        if type(self.power) is not int or not 1 <= self.power <= MAX_POWER:
            raise ValueError('Choose a boundary-twist power between 1 and 32')
        object.__setattr__(self, 'factors', tuple(self.factors))
        if not 1 <= len(self.factors) <= MAX_FACTORS:
            raise ValueError('A project needs 1 to 80 factors')
        for factor in self.factors:
            _validated_factor(factor, self.points)
        if len({factor.id for factor in self.factors}) != len(self.factors):
            raise ValueError('Factor IDs must be distinct')
        if sum(len(factor.word) for factor in self.factors) > MAX_LETTERS:
            raise ValueError('The factorization exceeds 3500 braid letters')
        if exact_action(self.word, self.points) != exact_action(self.target_word, self.points):
            raise ValueError('Factorization does not equal the selected boundary twist power')

    @property
    def target_word(self):
        return tuple(range(1, self.points)) * (self.points * self.power)

    @property
    def word(self):
        return _word(self.factors)

    def _replace(self, factors):
        return BoundaryProject(self.points, self.power, factors)

    def move(self, source, target):
        """Drag one unchanged factor through checked adjacent Hurwitz moves."""
        factors = list(self.factors)
        if (type(source) is not int or type(target) is not int or
                not 0 <= source < len(factors) or not 0 <= target < len(factors)):
            raise ValueError('Choose two valid factor positions')
        while source < target:
            u, v = factors[source:source+2]
            twist = replace(v, conjugator=reduce_word(u.word + v.conjugator)).mapping_class
            simplified = simplify_twist(twist, strands=self.points)
            changed = replace(v, conjugator=simplified.conjugator, first=simplified.first)
            _same_action(self.points, (u, v), (changed, u))
            factors[source:source+2] = (changed, u)
            source += 1
        while source > target:
            v, u = factors[source-1:source+1]
            twist = replace(v, conjugator=reduce_word(inverse_word(u.word) + v.conjugator)).mapping_class
            simplified = simplify_twist(twist, strands=self.points)
            changed = replace(v, conjugator=simplified.conjugator, first=simplified.first)
            _same_action(self.points, (v, u), (u, changed))
            factors[source-1:source+1] = (u, changed)
            source -= 1
        return self._replace(factors)

    def split(self, index, kind):
        if type(index) is not int or not 0 <= index < len(self.factors):
            raise ValueError('Choose a valid factor position')
        factor = self.factors[index]
        if kind == 'powers' and factor.power > 1:
            replacement = tuple(replace(factor, id=f'{factor.id}.{i+1}', power=1)
                                for i in range(factor.power))
        elif kind == 'halves' and not factor.half and factor.points == 2:
            replacement = tuple(replace(factor, id=f'{factor.id}.h{i+1}', half=True, power=1)
                                for i in range(2 * factor.power))
        elif kind == 'lantern' and not factor.half and factor.points == 3:
            i = factor.first
            replacement = tuple(
                Factor(f'{factor.id}.L{repeat+1}.{j+1}', reduce_word(factor.conjugator + g), a, 2)
                for repeat in range(factor.power)
                for j, (g, a) in enumerate((((), i), ((i+1,), i), ((), i+1)))
            )
        else:
            raise ValueError('That split is not available for this factor')
        _same_action(self.points, (factor,), replacement)
        return self._replace(self.factors[:index] + replacement + self.factors[index+1:])

    def combine(self, index):
        if type(index) is not int or not 0 <= index < len(self.factors)-1:
            raise ValueError('Select a factor with a following neighbor')
        a, b = self.factors[index:index+2]
        same_type = (a.first, a.points, a.half) == (b.first, b.points, b.half)
        if same_type and exact_action(replace(a, power=1).word, self.points) == exact_action(replace(b, power=1).word, self.points):
            count = 2
            total = a.power + b.power
            combined = replace(a, id=f'{a.id}+{b.id}', power=total)
            if a.half and total % 2 == 0:
                combined = replace(combined, half=False, power=total//2)
        else:
            triple = self.factors[index:index+3]
            if (len(triple) != 3 or a.first+2 > self.points or
                    any(f.half or f.points != 2 or f.power != 1 for f in triple)):
                raise ValueError('Combine needs equal neighboring powers or a verified three-factor marked-point lantern')
            combined = Factor('+'.join(f.id for f in triple), a.conjugator, a.first, 3)
            _same_action(self.points, triple, (combined,))
            count = 3
        _same_action(self.points, self.factors[index:index+count], (combined,))
        return self._replace(self.factors[:index] + (combined,) + self.factors[index+count:])

    def to_dict(self):
        return {
            'format': FORMAT,
            'points': self.points,
            'power': self.power,
            'factors': [dict(asdict(f), conjugator=list(f.conjugator), word=list(f.word))
                        for f in self.factors],
        }


def new_project(points, power=1):
    return BoundaryProject(points, power, (Factor('T', (), 1, points, power),))


def import_project(document):
    """Load only exact factorizations of their declared target braid."""
    if not isinstance(document, dict) or document.get('format') != FORMAT:
        raise ValueError('Choose a boundary playground JSON file')
    points, power, rows = document.get('points'), document.get('power'), document.get('factors')
    if type(points) is not int or points not in SUPPORTED_POINTS:
        raise ValueError('Choose 3 or 5 marked points')
    if type(power) is not int or not 1 <= power <= MAX_POWER:
        raise ValueError('Choose a boundary-twist power between 1 and 32')
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_FACTORS:
        raise ValueError('Expected 1 to 80 factor records')
    factors = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('conjugator'), list):
            raise ValueError('Invalid factor record')
        factor = Factor(row.get('id'), tuple(row['conjugator']), row.get('first'),
                        row.get('points'), row.get('power'), row.get('half'))
        _validated_factor(factor, points)
        if row.get('word') != list(factor.word):
            raise ValueError('Saved braid word disagrees with its factor record')
        factors.append(factor)
    return BoundaryProject(points, power, tuple(factors))
