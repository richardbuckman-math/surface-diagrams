"""Build the algebraic fiber-sum certificate for the imported (10,10)."""

from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

from surface_diagrams.braid_actions import inverse_word, reduce_word
from surface_diagrams.factorization_explorer import Factor, product
from surface_diagrams.hyperelliptic_homology import IDENTITY, homology_action
from surface_diagrams.mapping_classes import exact_action, supported_class
from surface_diagrams.point_pushing import point_push_braid, point_push_generator
from surface_diagrams.six_seven_structure import research_hurwitz_move
from surface_diagrams.small_fibration_derivations import action_match, transport
from surface_diagrams.sphere_actions import sphere_chain_certificate
from surface_diagrams.sphere_linking import sphere_linking_character


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "docs/proofs/fibration-derivations/10-10.json"
SOURCE_PIN = "2fd554824c44c1db0e2c570c61e91562677338796ad7f5f559f8d485e8a7c06e"
TARGET = "docs/proofs/ten-ten-short-four-three-target.json"
TARGET_PIN = "bc349407881635661a5435a5c59f00377e8bf56484855b9830ec8dc10b827a4b"
OUTPUT = "docs/proofs/ten-ten-algebraic-fiber-sum.json"
STRANDS = 6


def _pinned_factors(root, path, pin, key):
    data = (root / path).read_bytes()
    if sha256(data).hexdigest() != pin:
        raise ValueError("The algebraic certificate requires the exact pinned input")
    return tuple(
        Factor(**dict(record, conjugator=tuple(record["conjugator"])))
        for record in json.loads(data)[key]
    )


def _sphere_and_lift(word):
    lift = homology_action(word)
    if lift != IDENTITY:
        raise ValueError("The chosen lift must be +I")
    character = sphere_linking_character(word)
    if character["nonidentity_sphere_proved"]:
        raise ValueError("The marked-sphere linking character must vanish")
    sphere = sphere_chain_certificate(word, max_letters=50000)
    if not sphere["certified"]:
        raise ValueError("The complete five-arc sphere action must be the identity")
    return dict(word=word, chosen_lift=lift, character=character, sphere=sphere)


def _block_identity(state, first, middle, last, backwards):
    """Evaluate a block Hurwitz identity without moving any diagram factors."""
    left = state[first:middle]
    right = state[middle:last]
    if backwards:
        local = right + transport(left, inverse_word(product(right)))
        indices = tuple(
            (i, i - 1)
            for start in range(middle, last)
            for i in range(start, start - len(left), -1)
        )
    else:
        local = transport(right, product(left)) + left
        indices = tuple(
            (i, i + 1)
            for start in range(middle - 1, first - 1, -1)
            for i in range(start, start + len(right))
        )
    after = state[:first] + local + state[last:]
    discrepancy = reduce_word(product(state) + inverse_word(product(after)))
    assert not discrepancy and len(indices) == len(left) * len(right)
    assert sorted(f.id for f in after) == sorted(f.id for f in state)
    assert all(f.power > 0 for f in after)
    return dict(
        input_factors=state, output_factors=after, block=(first, middle, last),
        inverse=backwards, formal_adjacent_indices=indices,
        full_raw_discrepancy=discrepancy, diagram_applied=False,
    )


def _representative(position):
    return tuple(-i for i in range(STRANDS - 1, position - 1, -1))


def _push(meridian):
    word = point_push_generator(STRANDS, abs(meridian))
    return word if meridian > 0 else inverse_word(word)


def _factored_disk_split(word, edge_proofs):
    """Collect the full nonabelian kernel without expanding long free words."""
    position = STRANDS
    shadow = ()
    edges = []
    expansion = []
    raw_edges = []
    kernel_terms = []
    kernel_braid = []
    for crossing in word:
        index = abs(crossing)
        end = index + 1 if position == index else index if position == index + 1 else position
        base = position if crossing > 0 else end
        sign = 1 if crossing > 0 else -1
        if index == base:
            kind, generator, edge_word = "identity", 0, ()
        elif index == base - 1:
            kind, generator = "push", sign * index
            edge_word = _push(generator)
        else:
            kind, generator = "shadow", sign * (index - int(index > base))
            edge_word = (generator,)
        literal_edge = reduce_word(
            _representative(position) + (crossing,) + inverse_word(_representative(end))
        )
        key = (position, crossing, end)
        if key not in edge_proofs:
            edge_proofs[key] = action_match(literal_edge, edge_word, STRANDS)
        edges.append(dict(
            position=position, crossing=crossing, next_position=end,
            kind=kind, generator=generator, edge_word=edge_word,
        ))
        raw_edges.extend(literal_edge)
        expansion.extend(edge_word)
        if kind == "shadow":
            shadow = reduce_word(shadow + edge_word)
        elif kind == "push":
            kernel_terms.append(dict(shadow_prefix=shadow, signed_meridian=generator))
            kernel_braid.extend(shadow + edge_word + inverse_word(shadow))
        position = end
    assert position == STRANDS and reduce_word(raw_edges) == reduce_word(word)
    kernel_braid = reduce_word(kernel_braid)
    reconstructed = reduce_word(kernel_braid + shadow)
    assert reconstructed == reduce_word(expansion)
    return dict(
        strands=STRANDS, source_word=word, edges=edges, shadow_word=shadow,
        kernel_free_loop_terms=tuple(reversed(kernel_terms)),
        kernel_loop_rule="Apply each recorded shadow Artin action to its signed meridian, "
        "then concatenate in the retained order.",
        kernel_braid_word=kernel_braid, reconstructed_word=reconstructed,
        exact_reconstruction_by_faithful_edge_equalities=True,
        collection_discrepancy=(), expanded_free_loop_computed=False,
    )


def _shadow_generator_proofs():
    proofs = []
    for index in range(1, STRANDS - 1):
        for letter in (index, -index):
            for meridian, loop in enumerate(exact_action((letter,), STRANDS - 1), 1):
                left = (letter,) + _push(meridian) + (-letter,)
                right = point_push_braid(loop, STRANDS)
                proofs.append(dict(
                    shadow_letter=letter, meridian=meridian, image=loop,
                    **action_match(left, right, STRANDS),
                ))
    return proofs


def _stopped_diagram_prefix(source, indices):
    state = source
    previews = []
    for start, end in indices:
        move = research_hurwitz_move(state, start, end)
        after = move["factors"]
        discrepancy = reduce_word(product(state) + inverse_word(product(after)))
        assert not discrepancy
        supports = tuple(supported_class(f.mapping_class, STRANDS) for f in after)
        maximum = max(map(len, supports))
        previews.append(dict(
            input_factors=state, raw_output_factors=after, positions=(start, end),
            raw_discrepancy=discrepancy, changed_support=supports[start],
            maximum=maximum, applied=False, rejected_before_application=maximum > 20,
        ))
        if maximum > 20:
            break
        state = after
    assert len(previews) == 2 and previews[-1]["maximum"] == 21
    assert after[start].id == "four_three_A.2"
    return previews


def report(root=ROOT):
    source = _pinned_factors(root, SOURCE, SOURCE_PIN, "factors")
    target = _pinned_factors(root, TARGET, TARGET_PIN, "target_factors")
    assert len(source) == 20 and len(target) == 7
    assert target[:4] == source[3:7] and target[5:] == source[18:20]
    P = product(source[3:7])
    d = Factor("proof.H56", (), 5, 2, half=True)
    c = transport((source[2],), inverse_word(d.word))[0]
    d_commutes_with_P = action_match(P + d.word, d.word + P, STRANDS)
    c_matches_target = action_match(inverse_word(P) + c.word + P, target[4].word, STRANDS)

    state = source
    blocks = []
    for block in (
        (10, 12, 16, False), (14, 16, 18, False), (14, 16, 17, False),
        (9, 14, 15, True), (7, 9, 10, False), (3, 7, 8, False),
        (2, 3, 4, True), (8, 18, 20, True),
    ):
        step = _block_identity(state, *block)
        blocks.append(step)
        state = step["output_factors"]
    assert not reduce_word(product(source) + inverse_word(product(state)))
    plan = tuple(move for block in blocks for move in block["formal_adjacent_indices"])
    assert len(plan) == 46
    donor = blocks[4]["output_factors"][7]
    assert donor.id == "four_three_A.6" and donor.half and donor.power == 1
    donor_match = _sphere_and_lift(reduce_word(donor.word + inverse_word(d.word)))
    donor_support = supported_class(donor.mapping_class, STRANDS)
    assert len(donor_support) == 40

    seven = state[3:10]
    thirteen = state[:3] + state[10:]
    assert seven[1:] == source[3:7] + source[18:20]
    assert seven[0].id == source[2].id
    actual_c_match = _sphere_and_lift(reduce_word(seven[0].word + inverse_word(c.word)))
    assert len(seven) == 7 and sum(f.half for f in seven) == 4
    assert len(thirteen) == 13 and sum(f.half for f in thirteen) == 6
    edge_proofs = {}
    summands = []
    for kind, factors in (((4, 3), seven), ((6, 7), thirteen)):
        word = reduce_word(product(factors))
        summands.append(dict(
            type=kind, factors=factors, closure=_sphere_and_lift(word),
            disk_split=_factored_disk_split(word, edge_proofs),
        ))

    return dict(
        source_path=SOURCE, source_sha256=SOURCE_PIN,
        target_path=TARGET, target_sha256=TARGET_PIN,
        all_twenty_source_factors=source, algebraic_blocks=blocks,
        formal_adjacent_count=len(plan), symbolic_endpoint=state,
        donor_factor=donor, donor_disk_support=donor_support, donor_matches_H56=donor_match,
        d_commutes_with_P=d_commutes_with_P, c_matches_target=c_matches_target,
        actual_B7_matches_c=actual_c_match, summands=summands,
        faithful_schreier_edges=tuple(dict(key=key, **proof) for key, proof in sorted(edge_proofs.items())),
        signed_shadow_generator_proofs=_shadow_generator_proofs(),
        gluing=dict(
            separating_circle="Enclose the contiguous seven critical values at zero-based slots 3 through 9",
            common_marking="The original genus-two fiber marking",
            boundary_monodromy="Identity",
            map_on_fiber="Identity in the common marking",
        ),
        rejected_diagram_prefix=_stopped_diagram_prefix(source, plan),
        algebraic_decomposition_proved=True, bounded_diagram_route_proved=False,
        source_diagram_moves_applied=0,
        scope="The algebraic block identities and closed positive summands certify a fiber sum. "
        "The recorded diagram plan exceeds support 20 and remains unapplied.",
    )


def certificate_bytes(root=ROOT):
    return json.dumps(report(root), default=asdict, separators=(",", ":")).encode("utf-8")


if __name__ == "__main__":
    data = certificate_bytes()
    (ROOT / OUTPUT).write_bytes(data)
    print(json.dumps(dict(bytes=len(data), sha256=sha256(data).hexdigest())))
