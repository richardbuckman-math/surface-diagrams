from __future__ import annotations

import re
from pathlib import Path

from planar_mcg import (
    ArcTwist,
    BraidSvgStyle,
    BraidWord,
    Factorization,
    PlanarArc,
    SurfaceSpec,
    SvgDiagramStyle,
    boundary_lantern_relation,
    half_lantern_relation,
    projected_half_lantern_relation,
    render_braid_blocks_svg,
    render_factorization_braid_svg,
    render_factorization_svg,
    tentenembedded_factorization,
    tentenhalf_lantern_factorization,
    tentenhalf_lantern_conversion_mapping_class,
    tentenhalf_lantern_standard_left_factorization,
    tentenhalf_lantern_standard_right_factorization,
    write_braid_svg,
    write_svg,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "scratch_figures"

CURVE_STYLE = SvgDiagramStyle(
    object_spacing=34,
    margin_x=26,
    row_height=82,
    margin_y=14,
    marked_point_radius=4.0,
    curve_width=1.8,
    marked_point_color="#0875ff",
    curve_color="#ff00ce",
    background_color="#fffdf8",
)

BRAID_STYLE = BraidSvgStyle(
    strand_spacing=26,
    crossing_height=11,
    block_padding=7,
    margin_x=18,
    margin_y=14,
    strand_width=1.25,
    crossing_gap_width=4.6,
    marker_radius=3.6,
    strand_color="#11151b",
    marker_color="#0875ff",
    background_color="#fffdf8",
)


def svg_parts(svg: str) -> tuple[str, float, float]:
    match = re.search(r'viewBox="([^"]+)"', svg)
    if match is None:
        raise ValueError("embedded SVG has no viewBox")
    _, _, width, height = map(float, match.group(1).split())
    body = svg[svg.find(">") + 1 : svg.rfind("</svg>")]
    return body, width, height


def embed_svg(
    svg: str,
    *,
    x: float,
    y: float,
    width: float | None = None,
    height: float | None = None,
) -> str:
    body, natural_width, natural_height = svg_parts(svg)
    if width is None and height is None:
        width, height = natural_width, natural_height
    elif width is None:
        width = natural_width * height / natural_height
    elif height is None:
        height = natural_height * width / natural_width
    return (
        f'<svg x="{x}" y="{y}" viewBox="0 0 {natural_width} {natural_height}" '
        f'width="{width}" height="{height}">{body}</svg>'
    )


def fitted_svg_size(
    svg: str,
    *,
    max_width: float,
    max_height: float,
) -> tuple[float, float]:
    _, natural_width, natural_height = svg_parts(svg)
    scale = min(max_width / natural_width, max_height / natural_height)
    return natural_width * scale, natural_height * scale


def arrow(x1: float, x2: float, y: float, label: str) -> str:
    return (
        f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
        'stroke="#8f8f8f" stroke-width="1.4"/>'
        f'<polygon points="{x2},{y} {x2 - 8},{y - 4} {x2 - 8},{y + 4}" '
        'fill="#8f8f8f"/>'
        f'<text x="{(x1 + x2) / 2}" y="{y - 7}" text-anchor="middle" '
        'font-size="9.5" font-family="Georgia, serif" fill="#686868">'
        f"{label}</text>"
    )


def page_start(width: float, height: float, title: str) -> list[str]:
    return [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
        ),
        '<rect width="100%" height="100%" fill="#eeebe2"/>',
        (
            f'<text x="{width / 2}" y="28" text-anchor="middle" '
            'font-size="20" font-family="Georgia, serif" fill="#20242a">'
            f"{title}</text>"
        ),
    ]


def panel_title(x: float, y: float, width: float, title: str, note: str) -> str:
    return (
        f'<text x="{x + width / 2}" y="{y}" text-anchor="middle" '
        'font-size="15" font-family="Georgia, serif" fill="#20242a">'
        f"{title}</text>"
        f'<text x="{x + width / 2}" y="{y + 15}" text-anchor="middle" '
        'font-size="9.5" font-family="Georgia, serif" fill="#59616c">'
        f"{note}</text>"
    )


def generate_relation_check_sheet() -> Path:
    surface_three = SurfaceSpec(0, 3)
    hurwitz_left = Factorization(
        surface_three,
        (ArcTwist(surface_three, 1, 2), ArcTwist(surface_three, 2, 3)),
    )
    relations = [
        (
            "Sign convention",
            render_braid_blocks_svg([BraidWord(2, (1,))], style=BRAID_STYLE),
            render_braid_blocks_svg([BraidWord(2, (-1,))], style=BRAID_STYLE),
            "positive: upper-left over to lower-right",
        ),
        (
            "Artin braid relation",
            render_braid_blocks_svg(
                [BraidWord(3, (1,)), BraidWord(3, (2,)), BraidWord(3, (1,))],
                style=BRAID_STYLE,
            ),
            render_braid_blocks_svg(
                [BraidWord(3, (2,)), BraidWord(3, (1,)), BraidWord(3, (2,))],
                style=BRAID_STYLE,
            ),
            "sigma_1 sigma_2 sigma_1 = sigma_2 sigma_1 sigma_2",
        ),
        (
            "Commuting generators",
            render_braid_blocks_svg(
                [BraidWord(4, (1,)), BraidWord(4, (3,))],
                style=BRAID_STYLE,
            ),
            render_braid_blocks_svg(
                [BraidWord(4, (3,)), BraidWord(4, (1,))],
                style=BRAID_STYLE,
            ),
            "sigma_1 sigma_3 = sigma_3 sigma_1",
        ),
        (
            "Hurwitz move",
            render_factorization_braid_svg(hurwitz_left, style=BRAID_STYLE),
            render_factorization_braid_svg(
                hurwitz_left.hurwitz_left(0),
                style=BRAID_STYLE,
            ),
            "(a,b) -> (b,b^-1 a b)",
        ),
        (
            "Projected half lantern",
            render_factorization_braid_svg(
                projected_half_lantern_relation(surface_three)[0],
                style=BRAID_STYLE,
            ),
            render_factorization_braid_svg(
                projected_half_lantern_relation(surface_three)[1],
                style=BRAID_STYLE,
            ),
            "checked exact equality",
        ),
        (
            "Lifted half lantern",
            render_factorization_braid_svg(
                half_lantern_relation(SurfaceSpec(1, 2))[0],
                style=BRAID_STYLE,
            ),
            render_factorization_braid_svg(
                half_lantern_relation(SurfaceSpec(1, 2))[1],
                style=BRAID_STYLE,
            ),
            "checked exact equality with one boundary",
        ),
        (
            "Boundary lantern",
            render_factorization_braid_svg(
                boundary_lantern_relation(SurfaceSpec(3, 0))[0],
                style=BRAID_STYLE,
            ),
            render_factorization_braid_svg(
                boundary_lantern_relation(SurfaceSpec(3, 0))[1],
                style=BRAID_STYLE,
            ),
            "checked exact equality",
        ),
    ]

    width = 760
    fitted_relations = []
    for name, left, right, note in relations:
        left_width, left_height = fitted_svg_size(
            left,
            max_width=230,
            max_height=530,
        )
        right_width, right_height = fitted_svg_size(
            right,
            max_width=230,
            max_height=530,
        )
        row_height = 86 + max(left_height, right_height)
        fitted_relations.append(
            (
                name,
                left,
                right,
                note,
                left_width,
                left_height,
                right_width,
                right_height,
                row_height,
            )
        )

    height = 52 + sum(item[-1] for item in fitted_relations)
    fragments = page_start(width, height, "Braid convention and relation checks")
    top = 52
    for (
        name,
        left,
        right,
        note,
        left_width,
        left_height,
        right_width,
        right_height,
        row_height,
    ) in fitted_relations:
        fragments.append(
            f'<rect x="18" y="{top}" width="{width - 36}" height="{row_height - 16}" '
            'rx="10" fill="#fffdf8" stroke="#d7d0c2"/>'
        )
        fragments.append(panel_title(24, top + 25, width - 48, name, note))
        content_top = top + 52
        content_height = row_height - 76
        left_x = 190 - left_width / 2
        left_y = content_top + (content_height - left_height) / 2
        right_x = 570 - right_width / 2
        right_y = content_top + (content_height - right_height) / 2
        fragments.append(
            embed_svg(
                left,
                x=left_x,
                y=left_y,
                width=left_width,
                height=left_height,
            )
        )
        fragments.append(
            f'<text x="{width / 2}" y="{content_top + content_height / 2}" '
            'dominant-baseline="middle" text-anchor="middle" '
            'font-size="24" font-family="Georgia, serif" fill="#777">=</text>'
        )
        fragments.append(
            embed_svg(
                right,
                x=right_x,
                y=right_y,
                width=right_width,
                height=right_height,
            )
        )
        top += row_height
    fragments.append("</svg>")
    return write_braid_svg(
        "".join(fragments),
        OUTPUT / "braid_relation_checks.svg",
    )


def generate_conjugation_sheet() -> Path:
    embedded = tentenembedded_factorization()
    source = Factorization(embedded.surface, embedded.factors[14:16])
    standard_left = tentenhalf_lantern_standard_left_factorization()
    standard_right = tentenhalf_lantern_standard_right_factorization()
    final = tentenhalf_lantern_factorization()
    replacement = Factorization(final.surface, final.factors[14:17])
    conversion_word = tentenhalf_lantern_conversion_mapping_class().braid.word
    conversion_label = " ".join(
        f"sigma_{abs(generator)}"
        + ("^-1" if generator < 0 else "")
        for generator in conversion_word
    )

    curve_svgs = [
        render_factorization_svg(
            source,
            style=CURVE_STYLE,
            show_factor_numbers=False,
            require_detailed=True,
        ),
        render_factorization_svg(
            standard_left,
            style=CURVE_STYLE,
            show_factor_numbers=False,
            require_detailed=True,
        ),
        render_factorization_svg(
            standard_right,
            style=CURVE_STYLE,
            show_factor_numbers=False,
            require_detailed=True,
        ),
        render_factorization_svg(
            replacement,
            style=CURVE_STYLE,
            show_factor_numbers=False,
            require_detailed=True,
        ),
    ]
    braid_svgs = [
        render_factorization_braid_svg(source, style=BRAID_STYLE),
        render_factorization_braid_svg(standard_left, style=BRAID_STYLE),
        render_factorization_braid_svg(standard_right, style=BRAID_STYLE),
        render_factorization_braid_svg(replacement, style=BRAID_STYLE),
    ]

    correction_before = PlanarArc(
        embedded.surface,
        1,
        4,
        start_above=False,
    )
    correction_after = correction_before.acted_on_by_word((4, 4))
    correction_svg = render_factorization_svg(
        Factorization(
            embedded.surface,
            (
                correction_before.half_twist(),
                correction_after.half_twist(),
            ),
        ),
        style=CURVE_STYLE,
        show_factor_numbers=False,
        require_detailed=True,
    )

    width = 1180
    height = 1040
    fragments = page_start(width, height, "10,10 half-lantern conversion and transport")
    panel_width = 238
    x_values = (20, 314, 608, 902)
    titles = (
        ("merged positions 15-16", "actual six-point curves"),
        ("standard pair", "apply c: t_(56), t_(12)"),
        (
            "half-lantern triple",
            "(curve 3 6)^2 and the two 3-to-4 half twists",
        ),
        ("final replacement", "undo the conversion by c^-1"),
    )
    for x, (title, note), curve_svg in zip(x_values, titles, curve_svgs):
        fragments.append(panel_title(x, 58, panel_width, title, note))
        fragments.append(embed_svg(curve_svg, x=x + 8, y=88, width=222))
    for left_x, right_x, label in (
        (258, 304, "apply c"),
        (552, 598, "half lantern"),
        (846, 892, "apply c^-1"),
    ):
        fragments.append(arrow(left_x, right_x, 176, label))

    fragments.append(
        '<rect x="20" y="380" width="1140" height="205" rx="10" '
        'fill="#fffdf8" stroke="#d7d0c2"/>'
    )
    fragments.append(
        '<text x="40" y="406" font-size="15" font-family="Georgia, serif" '
        'fill="#20242a">Step 3 correction</text>'
    )
    fragments.append(
        '<text x="40" y="424" font-size="10" font-family="Georgia, serif" '
        'fill="#59616c">Apply sigma_4^2 to the third curve before continuing.</text>'
    )
    fragments.append(embed_svg(correction_svg, x=322, y=392, width=222))
    fragments.append(
        '<text x="558" y="490" font-size="13" font-family="Georgia, serif" '
        'fill="#686868">top: before</text>'
        '<text x="558" y="510" font-size="13" font-family="Georgia, serif" '
        'fill="#686868">bottom: after sigma_4^2</text>'
    )

    fragments.append(
        '<text x="590" y="620" text-anchor="middle" font-size="17" '
        'font-family="Georgia, serif" fill="#20242a">'
        "Equivalent marked sub-braids</text>"
    )
    for x, braid_svg in zip(x_values, braid_svgs):
        fragments.append(embed_svg(braid_svg, x=x + 20, y=642, width=198, height=365))
    for left_x, right_x, label in (
        (258, 304, "convert"),
        (552, 598, "="),
        (846, 892, "undo"),
    ):
        fragments.append(arrow(left_x, right_x, 820, label))
    fragments.append(
        '<text x="590" y="1022" text-anchor="middle" font-size="10" '
        'font-family="Georgia, serif" fill="#59616c">'
        "Blue rows mark factor boundaries. Conversion word: "
        f"{conversion_label}. The first and last products are equal in the "
        "six-punctured sphere group."
        "</text>"
    )
    fragments.append("</svg>")
    return write_svg(
        "".join(fragments),
        OUTPUT / "tenten_half_lantern_conjugation.svg",
    )


def generate_final_column_sheet() -> Path:
    final = tentenhalf_lantern_factorization()
    curve_svg = render_factorization_svg(
        final,
        style=CURVE_STYLE,
        show_factor_numbers=True,
        require_detailed=True,
        title="Final 10,10 factorization after the half lantern",
    )
    compact_braid_style = BraidSvgStyle(
        strand_spacing=26,
        crossing_height=4.0,
        block_padding=5.0,
        margin_x=18,
        margin_y=14,
        strand_width=1.0,
        crossing_gap_width=3.8,
        marker_radius=3.2,
        strand_color="#11151b",
        marker_color="#0875ff",
        background_color="#fffdf8",
    )
    braid_svg = render_factorization_braid_svg(
        final,
        style=compact_braid_style,
        title="Equivalent factor braid word",
    )
    width = 620
    height = 1815
    fragments = page_start(width, height, "Final 10,10 column and equivalent braid")
    fragments.append(panel_title(26, 58, 260, "20 curve factors", "positions 15-17 are the transported half lantern"))
    fragments.append(panel_title(332, 58, 260, "20 marked sub-braids", "one blue dot per strand at every factor boundary"))
    fragments.append(embed_svg(curve_svg, x=45, y=88, height=1690))
    fragments.append(embed_svg(braid_svg, x=360, y=88, height=1690))
    fragments.append(
        '<rect x="38" y="1265" width="238" height="250" rx="8" fill="none" '
        'stroke="#b46a3c" stroke-width="1.6"/>'
    )
    fragments.append(
        '<text x="157" y="1256" text-anchor="middle" font-size="10" '
        'font-family="Georgia, serif" fill="#9a552f">half-lantern replacement</text>'
    )
    fragments.append("</svg>")
    return write_svg(
        "".join(fragments),
        OUTPUT / "tenten_final_column_and_braid.svg",
    )


if __name__ == "__main__":
    for generated in (
        generate_relation_check_sheet(),
        generate_conjugation_sheet(),
        generate_final_column_sheet(),
    ):
        print(generated)
