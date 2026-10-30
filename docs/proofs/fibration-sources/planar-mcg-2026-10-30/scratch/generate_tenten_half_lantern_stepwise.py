from __future__ import annotations

from pathlib import Path

from planar_mcg import (
    CutIntersectionLoop,
    Factorization,
    PlanarArc,
    PlanarMappingClass,
    SurfaceSpec,
    format_simplified_thurston,
    render_factorization_svg,
    tentenembedded_factorization,
    tentenhalf_lantern_factorization,
    tentenhalf_lantern_standard_left_factorization,
    tentenhalf_lantern_standard_right_factorization,
    write_svg,
)
from planar_mcg.rendering import _factor_curve

from generate_tenten_half_lantern_figures import (
    CURVE_STYLE,
    OUTPUT,
    embed_svg,
    page_start,
)


FORWARD_WORD = (-3, 4, 5, 5, 4, 3, 1, 2)
INVERSE_WORD = tuple(-generator for generator in reversed(FORWARD_WORD))

# Exact, smoothly drawable representatives of the transported middle arc.
ALPHA_ROUTES = (
    ((3, 4), (6,), False),
    ((2, 4), (6,), False),
    ((1, 4), (6,), False),
    ((1, 3), (2, 3, 6, 0), True),
    ((1, 3), (5, 0, 6, 5), True),
    ((1, 3), (5,), False),
    ((1, 3), (3, 4, 6), False),
    ((1, 3), (2, 6, 5, 3, 6, 3, 6), False),
    ((1, 4), (3, 4, 6, 2, 3, 6), False),
)


def generator_label(generator: int) -> str:
    suffix = "^-1" if generator < 0 else ""
    return f"sigma_{abs(generator)}{suffix}"


def horizontal_arrow(
    x1: float,
    x2: float,
    y: float,
    label: str,
) -> str:
    points = (
        f"{x2},{y} {x2 - 7},{y - 4} {x2 - 7},{y + 4}"
        if x2 > x1
        else f"{x2},{y} {x2 + 7},{y - 4} {x2 + 7},{y + 4}"
    )
    return (
        f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
        'stroke="#8f8f8f" stroke-width="1.35"/>'
        f'<polygon points="{points}" fill="#8f8f8f"/>'
        f'<text x="{(x1 + x2) / 2}" y="{y - 8}" text-anchor="middle" '
        'font-size="10" font-family="Georgia, serif" fill="#5f6670">'
        f"{label}</text>"
    )


def vertical_arrow(
    x: float,
    y1: float,
    y2: float,
    label: str,
) -> str:
    return (
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" '
        'stroke="#a46038" stroke-width="1.8"/>'
        f'<polygon points="{x},{y2} {x - 5},{y2 - 9} {x + 5},{y2 - 9}" '
        'fill="#a46038"/>'
        f'<text x="{x - 10}" y="{(y1 + y2) / 2}" text-anchor="end" '
        'font-size="12" font-family="Georgia, serif" fill="#92512e">'
        f"{label}</text>"
    )


def factorization_states(
    initial: Factorization,
    word: tuple[int, ...],
) -> tuple[Factorization, ...]:
    states = [initial]
    current = initial
    for generator in word:
        current = current.global_conjugate(
            PlanarMappingClass.from_artin_word(
                current.surface,
                (generator,),
            )
        )
        states.append(current)
    return tuple(states)


def alpha_arc(
    surface: SurfaceSpec,
    route: tuple[tuple[int, int], tuple[int, ...], bool],
) -> PlanarArc:
    endpoints, cuts, start_above = route
    return PlanarArc(
        surface,
        endpoints[0],
        endpoints[1],
        cut_intersections=cuts,
        start_above=start_above,
    )


def coordinate_labels(factorization: Factorization) -> tuple[str, ...]:
    return tuple(
        format_simplified_thurston(_factor_curve(factor)[0])
        for factor in factorization.factors
    )


def verify_states(
    forward_states: tuple[Factorization, ...],
    backward_states: tuple[Factorization, ...],
    beta_states: tuple[PlanarArc, ...],
) -> None:
    standard_left = tentenhalf_lantern_standard_left_factorization()
    if not all(
        actual.is_equivalent_to(expected)
        for actual, expected in zip(
            forward_states[-1].factors,
            standard_left.factors,
        )
    ):
        raise AssertionError("forward steps do not end at the standard pair")

    for state, route, beta in zip(
        backward_states,
        ALPHA_ROUTES,
        beta_states,
    ):
        explicit_alpha = alpha_arc(state.surface, route).half_twist()
        if not explicit_alpha.is_equivalent_to(state.factors[1]):
            raise AssertionError("an alpha route does not match its exact step")
        if not beta.half_twist().is_equivalent_to(state.factors[2]):
            raise AssertionError("a beta route does not match its exact step")

    final = tentenhalf_lantern_factorization()
    final_replacement = Factorization(final.surface, final.factors[14:17])
    if not all(
        actual.is_equivalent_to(expected)
        for actual, expected in zip(
            backward_states[-1].factors,
            final_replacement.factors,
        )
    ):
        raise AssertionError("inverse steps do not end at the final triple")


def lower_coordinate_states(
    surface: SurfaceSpec,
) -> tuple[tuple[CutIntersectionLoop, ...], tuple[PlanarArc, ...]]:
    loop = CutIntersectionLoop(surface, (3, 6), start_above=False)
    beta = PlanarArc(surface, 3, 4)
    loops = [loop]
    betas = [beta]
    for generator in INVERSE_WORD:
        loop = loop.acted_on_by_generator(generator)
        beta = beta.acted_on_by_generator(generator)
        loops.append(loop)
        betas.append(beta)
    return tuple(loops), tuple(betas)


def add_reference_lines(
    fragments: list[str],
    *,
    center_x: float,
    first_y: float,
    references: tuple[str, ...],
    font_size: float,
    first_squared: bool = False,
) -> None:
    for line_index, reference in enumerate(references):
        suffix = "^2" if first_squared and line_index == 0 else ""
        fragments.append(
            f'<text x="{center_x}" y="{first_y + line_index * 13}" '
            f'text-anchor="middle" font-size="{font_size}" '
            'font-family="Georgia, serif" fill="#65707b">'
            f"{line_index + 1}. {reference}{suffix}</text>"
        )


def generate_stepwise_sheet() -> Path:
    embedded = tentenembedded_factorization()
    source = Factorization(embedded.surface, embedded.factors[14:16])
    standard_right = tentenhalf_lantern_standard_right_factorization()
    forward_states = factorization_states(source, FORWARD_WORD)
    backward_states = factorization_states(standard_right, INVERSE_WORD)
    loop_states, beta_states = lower_coordinate_states(embedded.surface)
    verify_states(forward_states, backward_states, beta_states)

    forward_svgs = tuple(
        render_factorization_svg(
            state,
            style=CURVE_STYLE,
            show_factor_numbers=False,
            require_detailed=True,
        )
        for state in forward_states
    )
    backward_displays = tuple(
        Factorization(
            state.surface,
            (
                state.factors[0],
                alpha_arc(state.surface, route).half_twist(),
                beta.half_twist(),
            ),
        )
        for state, route, beta in zip(
            backward_states,
            ALPHA_ROUTES,
            beta_states,
        )
    )
    backward_svgs = tuple(
        render_factorization_svg(
            display,
            style=CURVE_STYLE,
            show_factor_numbers=False,
            require_detailed=True,
        )
        for display in backward_displays
    )
    forward_labels = tuple(
        coordinate_labels(state)
        for state in forward_states
    )
    backward_labels = tuple(
        (
            format_simplified_thurston(loop),
            format_simplified_thurston(alpha_arc(embedded.surface, route)),
            format_simplified_thurston(beta),
        )
        for loop, route, beta in zip(
            loop_states,
            ALPHA_ROUTES,
            beta_states,
        )
    )

    cell_width = 238
    margin = 22
    width = margin * 2 + cell_width * 9
    height = 900
    panel_width = 202
    top_y = 92
    bottom_y = 472
    top_height = 174
    bottom_height = 250
    center_offsets = tuple(
        margin + index * cell_width + cell_width / 2
        for index in range(9)
    )

    fragments = page_start(
        width,
        height,
        "10,10 half-lantern conversion, one generator at a time",
    )
    fragments.append(
        '<text x="24" y="54" font-size="15" font-family="Georgia, serif" '
        'fill="#20242a">Forward: apply the reviewed word from left to right</text>'
    )
    fragments.append(
        '<text x="24" y="438" font-size="15" font-family="Georgia, serif" '
        'fill="#20242a">Backward: apply the inverse generators from right to left</text>'
    )

    for index, (center_x, state_svg, references) in enumerate(
        zip(center_offsets, forward_svgs, forward_labels)
    ):
        x = center_x - panel_width / 2
        fragments.append(
            f'<rect x="{x - 5}" y="{top_y - 7}" '
            f'width="{panel_width + 10}" height="{top_height + 14}" '
            'rx="8" fill="#fffdf8" stroke="#d8d1c4"/>'
        )
        fragments.append(
            embed_svg(
                state_svg,
                x=x,
                y=top_y,
                width=panel_width,
                height=top_height,
            )
        )
        label = (
            "start: boxed pair"
            if index == 0
            else "half-lantern left side"
            if index == 8
            else f"forward state {index}"
        )
        fragments.append(
            f'<text x="{center_x}" y="{top_y - 14}" text-anchor="middle" '
            'font-size="11" font-family="Georgia, serif" fill="#303741">'
            f"{label}</text>"
        )
        add_reference_lines(
            fragments,
            center_x=center_x,
            first_y=top_y + top_height + 17,
            references=references,
            font_size=8.2,
        )

    top_arrow_y = top_y + top_height / 2
    for index, generator in enumerate(FORWARD_WORD):
        fragments.append(
            horizontal_arrow(
                center_offsets[index] + panel_width / 2 + 7,
                center_offsets[index + 1] - panel_width / 2 - 7,
                top_arrow_y,
                generator_label(generator),
            )
        )

    for step, (state_svg, references) in enumerate(
        zip(backward_svgs, backward_labels)
    ):
        column = 8 - step
        center_x = center_offsets[column]
        x = center_x - panel_width / 2
        fragments.append(
            f'<rect x="{x - 5}" y="{bottom_y - 7}" '
            f'width="{panel_width + 10}" height="{bottom_height + 14}" '
            'rx="8" fill="#fffdf8" stroke="#d8d1c4"/>'
        )
        fragments.append(
            embed_svg(
                state_svg,
                x=x,
                y=bottom_y,
                width=panel_width,
                height=bottom_height,
            )
        )
        label = (
            "half-lantern right side"
            if step == 0
            else "final transported triple"
            if step == 8
            else f"inverse state {step}"
        )
        fragments.append(
            f'<text x="{center_x}" y="{bottom_y - 14}" text-anchor="middle" '
            'font-size="11" font-family="Georgia, serif" fill="#303741">'
            f"{label}</text>"
        )
        add_reference_lines(
            fragments,
            center_x=center_x,
            first_y=bottom_y + bottom_height + 16,
            references=references,
            font_size=7.9,
            first_squared=True,
        )

    bottom_arrow_y = bottom_y + bottom_height / 2
    for step, generator in enumerate(INVERSE_WORD):
        right_column = 8 - step
        left_column = right_column - 1
        fragments.append(
            horizontal_arrow(
                center_offsets[right_column] - panel_width / 2 - 7,
                center_offsets[left_column] + panel_width / 2 + 7,
                bottom_arrow_y,
                generator_label(generator),
            )
        )

    relation_x = center_offsets[-1]
    fragments.append(
        vertical_arrow(
            relation_x,
            top_y + top_height + 52,
            bottom_y - 28,
            "half lantern",
        )
    )
    fragments.append(
        '<text x="24" y="882" font-size="10" '
        'font-family="Georgia, serif" fill="#59616c">'
        "Each panel shows all six marked points. The two sigma_5 applications "
        "are displayed separately. Every caption is the exact simplified "
        "Thurston reference used to draw that curve; all routes are certified "
        "embedded and smoothly joined.</text>"
    )
    fragments.append("</svg>")
    return write_svg(
        "".join(fragments),
        OUTPUT / "tenten_half_lantern_step_by_step.svg",
    )


if __name__ == "__main__":
    print(generate_stepwise_sheet())
