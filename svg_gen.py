import random
import colorsys
import math

from utils import *


def create_rasta_flower():
    width, height = 1000, 1000
    center = width//2, height//2

    stars = list(map(lambda x: path_template(
        flower_path(
            *flat_armed_star_peaks_valleys(
                6,
                center,
                x[0],
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
                stars,
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
                stars,
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
                [path],
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
                [path],
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
        Color.MEDIUM_BLUE,
        Color.MEDIUM_BLUE,
        Color.MEDIUM_BLUE,
        Color.MEDIUM_BLUE,
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
    band_thickness = height*.035
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
                [
                    *tris,
                    horizontal_stripe,
                    vertical_stripe,
                    diagonal_stripe1,
                        diagonal_stripe2,
                    star_outer,
                    *stars,
                    # text,
                    circle,
                ],
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
                rects,
            )
        )


def percent_to_hex(p: float):
    return hex(round(p*255))[2:].rjust(2, '0')


def hsv_to_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h/360, s, v)
    return f"#{percent_to_hex(r)}{percent_to_hex(g)}{percent_to_hex(b)}"


def create_color_scheme():
    side_length = 600
    distance_from_center = 200
    radius = 50
    circle_size = 6

    s1 = .5  # 1.0
    v1 = .8  # random.random()
    s2 = .4  # random.random()/2 + .5
    v2 = 1.0  # random.random()
    h_start = 260  # random.randrange(360)

    paths = []
    for i in range(circle_size):
        if i % 2 == 0:
            s, v = s1, v1
        else:
            s, v = s2, v2
        h = (h_start - i*(360//circle_size)) % 360
        # print(hsv_to_hex(h, s, v))
        paths.append(
            circle_template(
                side_length//2 + math.cos(math.pi*i*2/circle_size)*distance_from_center,
                side_length//2 + math.sin(math.pi*i*2/circle_size)*distance_from_center,
                radius,
                hsv_to_hex(h, s, v),
            )
        )

    with open("images/color_scheme.svg", "w") as fh:
        fh.write(
            svg_template(
                side_length,
                side_length,
                paths,
                background_color="black",
            )
        )


def create_jaobon_flag(wavy=False):
    paths = []
    h1 = 260  # random.randrange(360)
    s1 = .5  # random.random()
    v1 = .8  # random.random()
    h2 = (h1 - 60) % 360
    s2 = .4  # random.random()
    v2 = 1.0  # random.random()
    h3 = (h1 - 120) % 360
    colors = [
        hsv_to_hex(h1, s1, v1),
        hsv_to_hex(h2, s2, v2),
        hsv_to_hex(h3, s1, v1),
    ]

    width = 3
    height = 2
    side_length = 1200 if max(width, height) <= 3 else 240

    for i in range(width):
        for j in range(height):
            paths.append(rectangle_template(side_length*i, side_length*j, side_length, side_length, color=colors[(i+j) % 3]))

    for i in range(width*2 + 1):
        for j in range(height*2 + 1):
            if ((i + j) % 2 == 0) and not wavy:
                continue

            r = side_length//4 if wavy else side_length//6
            paths.append(circle_template(i*side_length//2, j*side_length//2, r, colors[(-i + j + 1) % 3]))

    with open(f"images/jaobon_flag_{colors[0][1:]}_{'wavy' if wavy else 'puzzle'}_{width}x{height}.svg", "w") as fh:
        fh.write(
            svg_template(
                side_length*width,
                side_length*height,
                paths,
                background_color="white",
            ),
        )


if __name__ == "__main__":
    create_rasta_flower()
    create_trippy_lotus()
    create_black_lotus()
    create_rub_el_hizb_black_solid()
    create_lauvinko_flag()
    create_lauvinko_tricolor()
    create_jaobon_flag()
    create_color_scheme()
