"""Explicit capping certificates for a five-point curve on the six-point sphere."""
from .sphere_actions import sphere_chain_certificate
from .hyperelliptic_homology import homology_action, IDENTITY


def five_point_cap_certificate(power=1):
    if type(power) is not int or power < 1:
        raise ValueError('power must be a positive integer')
    word = (1, 2, 3, 4) * (5 * power)
    action = sphere_chain_certificate(word)
    lift = homology_action(word)
    expected = tuple(tuple((-1 if power % 2 else 1) * x for x in row) for row in IDENTITY)
    if not action['certified'] or lift != expected:
        raise ValueError('Five-point peripheral cap failed its independent sphere/lift checks')
    return dict(kind='sphere_rewrite', before_word=word, after_word=(),
                disk_discrepancy=word, sphere_action=action, genus_two_lift=lift,
                disk_equal=False,disk_writhe=len(word),
                lift_preserving=lift == IDENTITY, complementary_points=(6,),
                scope='marked-sphere mapping class; no spherical braid or framed boundary identity asserted',
                explanation='The complementary disk contains one marked point. Its peripheral twist is trivial on the marked sphere.')
