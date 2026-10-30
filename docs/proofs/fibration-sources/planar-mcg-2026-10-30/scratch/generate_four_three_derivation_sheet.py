from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from planar_mcg import (
    CutIntersectionLoop,
    DehnTwist,
    Factorization,
    PlanarArc,
    PlanarMappingClass,
    SurfaceSpec,
    four_three_a_factorization,
    format_simplified_thurston,
    outer_boundary_twist,
    render_factorization_svg,
    write_svg,
)
from planar_mcg.rendering import SvgDiagramStyle, _factor_curve

from generate_tenten_half_lantern_figures import OUTPUT, embed_svg, page_start


STYLE = SvgDiagramStyle(
    object_spacing=28,
    margin_x=22,
    row_height=52,
    margin_y=10,
    marked_point_radius=3.3,
    curve_width=1.55,
    marked_point_color="#0875ff",
    curve_color="#ff00ce",
    background_color="#fffdf8",
)

DIAGRAM_WIDTH = 150


@dataclass(frozen=True)
class Panel:
    title: str
    note: str
    factors: Sequence[object] | Factorization
    surface: SurfaceSpec
    highlight: tuple[int, ...] = ()


def daisy_factorization() -> Factorization:
    surface = SurfaceSpec(0, 4)
    return Factorization(
        surface,
        (
            DehnTwist(surface, (1, 2, 3)),
            DehnTwist(surface, (1, 4)),
            DehnTwist(surface, (2, 4)),
            DehnTwist(surface, (3, 4)),
        ),
    )


def curve_from_factor(factor: object):
    return _factor_curve(factor)


def factor_label(factor: object) -> str:
    curve, power = curve_from_factor(factor)
    label = format_simplified_thurston(curve)
    if power != 1:
        label += f"^{power}"
    return label


def factor_sequence(panel: Panel) -> tuple[object, ...]:
    if isinstance(panel.factors, Factorization):
        return panel.factors.factors
    return tuple(panel.factors)


def lift_curve_to_five(curve: CutIntersectionLoop) -> CutIntersectionLoop:
    return CutIntersectionLoop(
        SurfaceSpec(0, 5),
        tuple(5 if value == 4 else value for value in curve.cut_intersections),
        start_above=curve.start_above,
    )


def lifted_daisy_square(concatenated: Factorization) -> tuple[CutIntersectionLoop, ...]:
    return tuple(
        lift_curve_to_five(curve_from_factor(factor)[0])
        for factor in concatenated.factors
    )


def arc(surface: SurfaceSpec, start: int, end: int, *cuts: int) -> object:
    return PlanarArc(
        surface,
        start,
        end,
        cut_intersections=cuts,
        start_above=False,
    ).half_twist()


def replace_equivalent_factor(
    factorization: Factorization,
    index: int,
    replacement: object,
) -> Factorization:
    if not replacement.is_equivalent_to(factorization.factors[index]):
        raise AssertionError("display replacement is not equivalent")
    factors = list(factorization.factors)
    factors[index] = replacement
    return Factorization(factorization.surface, factors)


def build_panels() -> tuple[Panel, ...]:
    four = SurfaceSpec(0, 4)
    five = SurfaceSpec(0, 5)

    daisy = daisy_factorization()
    conjugator = PlanarMappingClass.from_artin_word(
        four,
        (-1, -2, -1),
    )
    conjugated = daisy.global_conjugate(conjugator)
    variation = conjugated.cyclic_shift_left(1)
    concatenated = Factorization(
        four,
        daisy.factors + variation.factors,
    )
    if not daisy.verify_exact(outer_boundary_twist(four)):
        raise AssertionError("the reduced daisy panel is not an outer twist")
    if not concatenated.verify_exact(outer_boundary_twist(four, power=2)):
        raise AssertionError("the two daisy variants do not square the outer twist")

    lifted = lifted_daisy_square(concatenated)
    induced = (
        DehnTwist(five, (4, 5), power=-1),
        DehnTwist(five, (4, 5), power=-1),
        DehnTwist(five, (4, 5), power=-1),
        DehnTwist(five, (4, 5), power=-1),
    )
    lifted_with_induced = lifted + induced
    rotated_lifted = (lifted[-1],) + lifted[:-1]
    rotated_with_induced = rotated_lifted + induced

    curve_0135 = DehnTwist(five, (1, 4, 5))
    curve_1235 = DehnTwist(five, (2, 4, 5))
    curve_1532 = CutIntersectionLoop(five, (1, 5, 3, 2))
    curve_0531 = CutIntersectionLoop(five, (0, 5, 3, 1))
    curve_35_inverse = DehnTwist(five, (4, 5), power=-1)
    curve_35_inverse_square = DehnTwist(five, (4, 5), power=-2)

    combined_pairs = (
        DehnTwist(five, (1, 2, 3), power=2),
        curve_0135,
        curve_1235,
        DehnTwist(five, (3, 4, 5), power=2),
        curve_1532,
        curve_0531,
        curve_35_inverse,
        curve_35_inverse,
        curve_35_inverse,
        curve_35_inverse,
    )
    sandwiched = (
        DehnTwist(five, (1, 2, 3), power=2),
        curve_0135,
        curve_1235,
        DehnTwist(five, (3, 4, 5), power=2),
        curve_1532,
        curve_35_inverse_square,
        curve_0531,
        curve_35_inverse_square,
    )
    converted = Factorization(
        five,
        (
            DehnTwist(five, (1, 2, 3), power=2),
            curve_0135,
            curve_1235,
            DehnTwist(five, (3, 4, 5), power=2),
            arc(five, 2, 5),
            arc(five, 2, 5, 3),
            arc(five, 1, 5),
            arc(five, 1, 5, 3),
        ),
    )
    if not converted.verify_exact(outer_boundary_twist(five, power=2)):
        raise AssertionError("the converted half-twist stage is not Delta_5^4")

    pull_7_to_6 = converted.hurwitz_left(5)
    pull_5_to_6 = pull_7_to_6.hurwitz_right(4)
    pull_5_to_3 = pull_5_to_6.hurwitz_left(3).hurwitz_left(2)
    pull_4_to_3 = pull_5_to_3.hurwitz_left(2)
    if not pull_4_to_3.factors[1].is_equivalent_to(pull_4_to_3.factors[2]):
        raise AssertionError("the final pre-combine curves are not identical")
    short_transport_arc = arc(five, 1, 2, 2, 4, 0)
    pull_7_to_6_display = replace_equivalent_factor(
        pull_7_to_6,
        6,
        short_transport_arc,
    )
    pull_5_to_6_display = replace_equivalent_factor(
        pull_5_to_6,
        6,
        short_transport_arc,
    )
    pull_5_to_3_display = replace_equivalent_factor(
        pull_5_to_3,
        6,
        short_transport_arc,
    )
    pull_4_to_3_display = replace_equivalent_factor(
        pull_4_to_3,
        6,
        short_transport_arc,
    )

    final = four_three_a_factorization()
    if not final.verify_exact(outer_boundary_twist(five, power=2)):
        raise AssertionError("the stored 4,3 factorization is not Delta_5^4")

    return (
        Panel(
            "1. reduced daisy",
            "four marked points",
            daisy,
            four,
        ),
        Panel(
            "2. global conjugate",
            "by sigma_1^-1 sigma_2^-1 sigma_1^-1",
            conjugated,
            four,
        ),
        Panel(
            "3. rotate conjugate",
            "first factor moves to fourth",
            variation,
            four,
        ),
        Panel(
            "4. concatenate",
            "daisy followed by its variation",
            concatenated,
            four,
        ),
        Panel(
            "5. lift and glue",
            "old point 4 becomes two points; add (curve 3 5)^-4",
            lifted_with_induced,
            five,
            highlight=(9, 10, 11, 12),
        ),
        Panel(
            "6. rotate old bottom",
            "the matching pairs are now adjacent",
            rotated_with_induced,
            five,
            highlight=(1, 2, 5, 6),
        ),
        Panel(
            "7. combine pairs",
            "first pair and middle pair become squared twists",
            combined_pairs,
            five,
            highlight=(1, 4),
        ),
        Panel(
            "8. commute induced twists",
            "two inverse twists above and two below the old bottom",
            sandwiched,
            five,
            highlight=(6, 8),
        ),
        Panel(
            "9. convert two pairs",
            "each dehn/inverse-square pair becomes two half twists",
            converted,
            five,
            highlight=(5, 6, 7, 8),
        ),
        Panel(
            "10. pull 7 up to 6",
            "second-to-last arc moves up one slot",
            pull_7_to_6_display,
            five,
            highlight=(6, 7),
        ),
        Panel(
            "11. pull 5 down to 6",
            "the first arc moves down one slot",
            pull_5_to_6_display,
            five,
            highlight=(5, 6),
        ),
        Panel(
            "12. pull 5 up to 3",
            "the top half twist moves above the curve",
            pull_5_to_3_display,
            five,
            highlight=(3,),
        ),
        Panel(
            "13. pull 4 up to 3",
            "elements 2 and 3 now match",
            pull_4_to_3_display,
            five,
            highlight=(2, 3),
        ),
        Panel(
            "14. combine 2 and 3",
            "normalized 4,3 block used in the 10,10 derivation",
            final,
            five,
            highlight=(2,),
        ),
    )


def panel_svg(panel: Panel) -> str:
    return render_factorization_svg(
        panel.factors,
        surface=panel.surface,
        style=STYLE,
        show_factor_numbers=False,
        require_detailed=True,
    )


def panel_height(panel: Panel) -> float:
    count = len(factor_sequence(panel))
    natural_width = (
        2 * STYLE.margin_x
        + STYLE.object_spacing * max(0, panel.surface.total_strands - 1)
    )
    natural_height = count * STYLE.row_height + 2 * STYLE.margin_y
    scaled_height = natural_height * DIAGRAM_WIDTH / natural_width
    label_height = 65 + count * 15
    return max(52 + scaled_height + 24, label_height + 24)


def draw_panel(
    fragments: list[str],
    panel: Panel,
    *,
    x: float,
    y: float,
    width: float,
    height: float,
) -> None:
    label_x = x + DIAGRAM_WIDTH + 18
    fragments.append(
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        'rx="10" fill="#fffdf8" stroke="#d8d1c4"/>'
    )
    fragments.append(
        f'<text x="{x + width / 2}" y="{y + 24}" text-anchor="middle" '
        'font-size="13" font-family="Georgia, serif" fill="#20242a">'
        f"{panel.title}</text>"
    )
    fragments.append(
        f'<text x="{x + width / 2}" y="{y + 41}" text-anchor="middle" '
        'font-size="9.2" font-family="Georgia, serif" fill="#65707b">'
        f"{panel.note}</text>"
    )
    fragments.append(
        embed_svg(
            panel_svg(panel),
            x=x + 12,
            y=y + 52,
            width=DIAGRAM_WIDTH,
        )
    )
    for index, factor in enumerate(factor_sequence(panel), start=1):
        color = "#a44e20" if index in panel.highlight else "#65707b"
        weight = "600" if index in panel.highlight else "400"
        fragments.append(
            f'<text x="{label_x}" y="{y + 65 + (index - 1) * 15}" '
            f'font-size="8.4" font-family="Georgia, serif" '
            f'font-weight="{weight}" fill="{color}">'
            f"{index}. {factor_label(factor)}</text>"
        )


def generate_four_three_derivation_sheet() -> Path:
    panels = build_panels()
    rows = (
        panels[:4],
        panels[4:9],
        panels[9:],
    )
    panel_width = 390
    gap = 18
    margin = 22
    row_gap = 42
    row_heights = tuple(max(panel_height(panel) for panel in row) for row in rows)
    width = margin * 2 + 5 * panel_width + 4 * gap
    height = margin + 48 + sum(row_heights) + row_gap * (len(rows) - 1) + 34
    fragments = page_start(
        width,
        height,
        "4,3 derivation from two reduced daisy variants",
    )
    fragments.append(
        f'<text x="{width / 2}" y="54" text-anchor="middle" '
        'font-size="15" font-family="Georgia, serif" fill="#20242a">'
        "Reduced daisy variation, lift/glue correction, and Hurwitz pulls"
        "</text>"
    )
    y = margin + 64
    for row, row_height in zip(rows, row_heights):
        x = margin
        for panel in row:
            draw_panel(
                fragments,
                panel,
                x=x,
                y=y,
                width=panel_width,
                height=row_height,
            )
            x += panel_width + gap
        y += row_height + row_gap
    fragments.append(
        f'<text x="{margin}" y="{height - 18}" font-size="10" '
        'font-family="Georgia, serif" fill="#59616c">'
        "Highlighted labels mark the factors being merged, commuted, converted, "
        "or pulled in that step. Coordinates use the same cut-line convention "
        "as the 10,10 diagrams.</text>"
    )
    fragments.append("</svg>")
    return write_svg(
        "".join(fragments),
        OUTPUT / "four_three_daisy_derivation.svg",
    )


if __name__ == "__main__":
    print(generate_four_three_derivation_sheet())
