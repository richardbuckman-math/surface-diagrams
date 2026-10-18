"""Richard's twenty dictated supports, in the supplied top-to-bottom order.

This is a transcription workspace, not an identification with Nakamura's
published example. The user confirmed factor 7 is a squared three-point Dehn
twist, clarifying "half twist squared" in the original dictation.
The present product fails the sphere identity check; retain that evidence.
"""
from dataclasses import asdict
from functools import lru_cache

from .braid_actions import arc_ray_word, loop_ray_word, inverse_word, free_homotopy_key
from .curves import Arc, Loop
from .factorization_explorer import Factor, product
from .hyperelliptic_homology import homology_action, IDENTITY
from .mapping_classes import supported_class
from .sphere_actions import sphere_inner_certificate


SOURCE_ROUTES = (
    Loop((2, 4, 5, 6)),
    Loop((2, 4, 5, 6, 2, 1, 6, 2, 6, 5)),
    Arc(2, 5, direction='down'),
    Loop((1, 4)),
    Loop((1, 6, 4, 2)),
    Arc(2, 3, (6, 4), direction='up'),
    Loop((3, 6)),
    Arc(3, 5, direction='down'),
    Arc(2, 6, (4, 5, 6, 4, 3, 2, 4), direction='down'),
    Loop((2, 6, 4, 5, 6, 4)),
    Arc(2, 3, (4, 6, 5, 4, 6, 4), direction='down'),
    Arc(2, 6, (4, 6, 4), direction='down'),
    Loop((1, 4)),
    Loop((1, 6, 4, 2)),
    Loop((2, 6, 4, 2, 3, 4)),
    Arc(1, 4, (4, 3, 2, 4, 6, 2), direction='down'),
    Arc(1, 4, direction='down'),
    Loop((3, 6)),
    Arc(2, 6, (6, 4), direction='down'),
    Arc(2, 3, (6, 4, 5, 6), direction='down'),
)

SOURCE_DESCRIPTIONS = (
    'Squared Dehn twist. Up through 2, down through 4, up through 5, down through 6, back to the start (around 3, 4, and 6).',
    'Squared Dehn twist. Up through 2, down through 4, up through 5, down through 6, up through 2, down through 1, up through 6, down through 2, up through 6, down through 5, back to the start. Around 2, 5, and 6.',
    'Half twist, 2 to 5, under points 3 and 4.',
    'Squared Dehn twist. Up through 1, down through 4, back to the start.',
    'Squared Dehn twist. Up through 1, down through 6, up through 4, down through 2, back to the start.',
    'Half twist, 2 to 3. Up over points 3, 4, 5, 6, down through 6, up through 4, back down connecting to 3.',
    'Half twist squared. Up through 3, down through 6, back to the start.',
    'Half twist, 3 to 5, under point 4.',
    'Half twist, 2 to 6. Down, up through 4, down through 5, up through 6, down through 4, up through 3, down through 2, up through 4, connect to 6 on the top.',
    'Squared Dehn twist. Up through 2, down through 6, up through 4, down through 5, up through 6, down through 4, back to the start.',
    'Half twist, 2 to 3. Down, up through 4, down through 6, up through 5, down through 4, up through 6, down through 4, connect to 3 from the bottom.',
    'Half twist, 2 to 6. Down, up through 4, down through 6, up through 4, connect to 6 from the top.',
    'Squared Dehn twist. Up through 1, down through 4, back to the start.',
    'Squared Dehn twist. Up through 1, down through 6, up through 4, down through 2, back to the start.',
    'Squared Dehn twist. Up through 2, down through 6, up through 4, down through 2, up through 3, down through 4, back to the start.',
    'Half twist, 1 to 4. Down, up through 4, down through 3, up through 2, down through 4, up through 6, down through 2, connect to 4 from the bottom.',
    'Half twist, 1 to 4, under points 2 and 3.',
    'Squared Dehn twist. Up through 3, down through 6, back to the start.',
    'Half twist, 2 to 6. Down, up through 6, down through 4, connect to 6 from the bottom.',
    'Half twist, 2 to 3. Down, up through 6, down through 4, up through 5, down through 6, connect to 3 from the bottom.',
)

# Each conjugator was recovered by shortening the supplied support's exact
# boundary word. Equality of support classes below checks all winding, not
# merely the enclosed labels. No search runs in the browser.
_DATA = (
    ((-5,), 3, False),
    ((-5, -4, -3, -3, -4, 2, 3), 4, False),
    ((-4, -3), 2, True),
    ((), 2, False),
    ((-2, -3), 4, False),
    ((-3, -2, -3, -4, -5, -5, -4), 3, True),
    ((), 4, False),
    ((-4,), 3, True),
    ((5, -4, -3, -3, -3), 2, True),
    ((5, 5), 3, False),
    ((5, 5, -4, -3, -3), 2, True),
    ((5, 5, 5, -4, -3), 2, True),
    ((), 2, False),
    ((-2, -3), 4, False),
    ((-3, -3), 4, False),
    ((-3, -3, -4, -5, -2, -1, -5, -4, -3), 2, True),
    ((-3, -2), 1, True),
    ((), 4, False),
    ((-5, -5, -5, -4, -3), 2, True),
    ((-5, -5, -4, -3, -3), 2, True),
)
TEN_TEN_FACTORS = tuple(
    Factor(f'F{i}', g, first, 2 if half else 3, 1 if half else 2, half)
    for i, (g, first, half) in enumerate(_DATA, 1)
)

FACTOR_SEVEN_NOTE = ('Confirmed clarification: the user specified a squared '
                     'Dehn twist around 4, 5, 6, matching F18 and the '
                     '(10,10) count. The original wording is retained above.')
SEED_NOTE = ('Transcription workspace: twenty supplied routes in top-to-bottom '
             'order. F7 is confirmed as a squared Dehn twist. The encoded product does not close on '
             'the sphere and its genus-two homology is not +I. '
             'Edits preserve this exact starting disk product.')


def route_boundary(curve):
    """Unoriented free class of a loop or an arc's neighborhood boundary."""
    if isinstance(curve, Loop):
        return free_homotopy_key(loop_ray_word(6, curve))
    path = arc_ray_word(6, curve)
    return free_homotopy_key((curve.start,) + path + (curve.end,) + inverse_word(path))


def source_records():
    """Keep the original routes available even after factors are transformed."""
    return [dict(id=f'F{i}', description=text, route=asdict(curve),
                 itinerary=repr(curve), note=FACTOR_SEVEN_NOTE if i == 7 else '')
            for i, (text, curve) in enumerate(zip(SOURCE_DESCRIPTIONS, SOURCE_ROUTES), 1)]


@lru_cache(maxsize=1)
def transcription_certificate():
    matches = tuple(route_boundary(curve) == supported_class(f.mapping_class)
                    for curve, f in zip(SOURCE_ROUTES, TEN_TEN_FACTORS))
    word = product(TEN_TEN_FACTORS)
    sphere = sphere_inner_certificate(word)
    homology = homology_action(word)
    return dict(supports_match=matches, sphere_identity=sphere['certified'],
                disk_identity=sphere['disk_identity'], homology=homology,
                homology_identity=homology == IDENTITY,
                half_twists=10, squared_three_point_twists=10,
                provisional_factors=[], confirmed_clarifications=['F7'], braid_letters=len(word))
