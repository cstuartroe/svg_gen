from enum import Enum
from flower_utils import *


class Color(Enum):
    BLACK = "#000000"
    WHITE = "#ffffff"
    INDIGO = "#003355"
    BP = "#3e008f"
    GOLD = "#ffbb00"
    FOREST_GREEN = "#005500"
    PURPLE = "#330055"
    RED = "#661111"


def path_template(vertex_string, color):
    return f'<path d="{vertex_string}" fill="{color}"/>'


def svg_template(width, height, *paths):
    return f'<svg height="{height}" width="{width}">\n' + "\n".join(paths) + '\n</svg>'


def create_rasta_flower():
    width, height = 1000, 1000
    center = width//2, height//2

    stars = list(map(lambda x: path_template(
        flower_path(
            *star_peaks_valleys(
                6,
                center,
                x[0],
                flat_arm_valley_radius(6, x[0]),
                False,
            ),
            center,
            curviness=1/3
        ),
        x[1]
    ), [
        (500, "black"),
        (400, "#007f00"),
        (300, "#ffff00"),
        (200, "#7f0000"),
    ]))

    with open("images/rasta_star.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                *stars,
            )
        )


def create_trippy_lotus():
    width, height = 1000, 1000
    center = width // 2, height // 2

    stars = list(map(lambda x: path_template(
        flower_path(
            *star_peaks_valleys(
                8,
                center,
                x[1][0],
                flat_arm_valley_radius(8, x[1][0]),
                x[0] % 2 == 1,
            ),
            center,
            curviness=1/4
        ),
        x[1][1]
    ), enumerate([
        (500, "black"),
        (383, "#007f00"),
        (292, "#ffff00"),
        (220, "#7f0000"),
        (160, "#3b0082"),
    ])))

    with open("images/trippy_lotus.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                *stars,
            )
        )


def create_black_lotus():
    width, height = 1000, 1000
    center = width // 2, height // 2

    path = path_template(
        flower_path(
            *star_peaks_valleys(
                8,
                center,
                500,
                flat_arm_valley_radius(8, 500),
                False,
            ),
            center,
        ),
        "black",
    )

    with open("images/black_lotus.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                path,
            )
        )


def create_rub_el_hizb_black_solid():
    width, height = 1000, 1000
    center = width//2, height//2
    radius = 500

    path = path_template(
        polygon_path(
            star_vertices(
                8,
                center,
                radius,
                flat_arm_valley_radius(8, radius),
                False,
            ),
        ),
        "black",
    )

    with open("images/rub_el_hizb_solid.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                path,
            )
        )


def create_lauvinko_flag():
    width, height = 1800, 1200
    center_x, center_y = width//3, height//2
    center = center_x, center_y

    corners = [
        (0, 0),
        (width, 0),
        (width, height),
        (0, height),
    ]

    intersection_points = [
        (center_x - center_y, 0),
        (center_x, 0),
        (center_x + center_y, 0),
        (width, center_y),
        (center_x + center_y, height),
        (center_x, height),
        (center_x - center_y, height),
        (0, center_y),
    ]

    stripe_color = Color.GOLD

    tris = []
    tricolors = [
        stripe_color,
        stripe_color,
        Color.BLACK,
        Color.BLACK,
        Color.INDIGO,
        Color.INDIGO,
        stripe_color,
        stripe_color,
    ]

    for i, corner in enumerate(corners):
        j = i*2

        ps = [
            (intersection_points[(j - 1) % 8], intersection_points[j]),
            (intersection_points[j], intersection_points[(j + 1) % 8]),
        ]

        for k, (p1, p2) in enumerate(ps):
            tris.append(
                path_template(
                    polygon_path([
                        center,
                        p1,
                        corner,
                        p2,
                    ]),
                    color=tricolors[j + k].value
                )
            )

    star_points = 8
    star_radius = (height//2)/(2**.5)
    band_thickness = height*.03
    star_difference = band_thickness*(2**.5)
    curviness = .12

    horizontal_stripe = path_template(
        rectangle_path(0, center_y - band_thickness//2, width, band_thickness),
        stripe_color.value,
    )

    vertical_stripe = path_template(
        rectangle_path(center_x - band_thickness//2, 0, band_thickness//2, height),
        stripe_color.value,
    )

    stripe_offset = band_thickness/(8**.5)

    diagl = max(center_x, center_y) + band_thickness

    diagonal_stripe1 = path_template(
        polygon_path([
            (center_x - diagl - stripe_offset, center_y + diagl - stripe_offset),
            (center_x - diagl + stripe_offset, center_y + diagl + stripe_offset),
            (center_x + diagl + stripe_offset, center_y - diagl + stripe_offset),
            (center_x + diagl - stripe_offset, center_y - diagl - stripe_offset),
        ]),
        color=stripe_color.value,
    )

    diagonal_stripe2 = path_template(
        polygon_path([
            (center_x - diagl - stripe_offset, center_y - diagl + stripe_offset),
            (center_x - diagl + stripe_offset, center_y - diagl - stripe_offset),
            (center_x + diagl + stripe_offset, center_y + diagl - stripe_offset),
            (center_x + diagl - stripe_offset, center_y + diagl + stripe_offset),
        ]),
        color=stripe_color.value,
    )

    star_outer = path_template(
        flower_path(
            *star_peaks_valleys(
                star_points,
                center,
                peak_radius=star_radius,
                valley_radius=flat_arm_valley_radius(star_points, star_radius),
                askew=False,
            ),
            center,
            curviness=curviness,
        ),
        color=stripe_color.value
    )

    stars = []

    ratio = ((1/(2**.5) + 1)**2 + 1/2)**.5/((2**.5) + 1)

    for i in range(3):
        r = (star_radius - star_difference)*(ratio**i)

        stars.append(
            path_template(
                flower_path(
                    *star_peaks_valleys(
                        star_points,
                        center,
                        peak_radius=r,
                        valley_radius=flat_arm_valley_radius(star_points, r),
                        askew=i % 2 == 1,
                    ),
                    center,
                    curviness=curviness,
                ),
                color=(Color.FOREST_GREEN.value if i % 2 == 0 else stripe_color.value)
            )
        )

    text = f"""
        <text 
            x="{center_x}" 
            y="{center_y}" 
            text-anchor="middle"
            style="
                font-family: Lavvinko Smooth Serif; 
                font-size: {star_radius//10}pt;
                fill: {Color.GOLD.value};
            "
        >
            laqehovinueko
        </text>
    """

    circle = f'<circle cx="{center_x}" cy="{center_y}" r="{int(star_radius*.18)}" fill="{stripe_color.value}" />'

    with open("images/lauvinko_flag.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                *tris,
                horizontal_stripe,
                vertical_stripe,
                diagonal_stripe1,
                diagonal_stripe2,
                star_outer,
                *stars,
                # text,
                circle,
            )
        )


def create_lauvinko_tricolor(width: int = 1800, height: int = 1200):
    colors = [Color.BLACK, Color.GOLD, Color.FOREST_GREEN, Color.INDIGO]

    rects = [
        path_template(
            rectangle_path(
                0,
                height*i//4,
                width,
                height//4,
            ),
            color=color.value,
        )
        for i, color in enumerate(colors)
    ]

    with open("images/lauvinko_tricolor.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                *rects,
            )
        )


if __name__ == "__main__":
    create_rasta_flower()
    create_trippy_lotus()
    create_black_lotus()
    create_rub_el_hizb_black_solid()
    create_lauvinko_flag()
    create_lauvinko_tricolor()
