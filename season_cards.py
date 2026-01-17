import os
from dataclasses import dataclass
from typing import Callable

from utils import *

CARDS_DIR = "images/season_cards"


class Season(Enum):
    AIR = "air"
    SPRING = "wood"
    SUMMER = "fire"
    AUTUMN = "metal"
    WINTER = "water"
    EARTH = "earth"


SEASON_COLORS: dict[Season, Color] = {
    Season.AIR: Color.CREAM,
    Season.SPRING: Color.SPRING_GREEN,
    Season.SUMMER: Color.SUMMER_GOLD,
    Season.AUTUMN: Color.AUTUMN_RED,
    Season.WINTER: Color.WINTER_BLUE,
    Season.EARTH: Color.BLACK,
}

LIGHT_COLORS = (Color.CREAM, Color.SPRING_GREEN, Color.SUMMER_GOLD)


def earth_path(cx, cy, radius, color):
    factor = (math.sqrt(2)-1)/(3*math.sqrt(2))
    inner_radius = radius*(1-2*factor)
    avg_radius = (radius+inner_radius)/2
    line_thickness = radius*factor

    return f"""
    <circle cx="{cx}" cy="{cy}" r="{avg_radius}" stroke="{color.value}" stroke-width="{radius - inner_radius}" fill="none"/>
    {rectangle_template(cx - line_thickness, cy - avg_radius, 2*line_thickness, 2*avg_radius, color.value)}
    {rectangle_template(cx - avg_radius, cy - line_thickness, 2*avg_radius, 2*line_thickness, color.value)}
    """


def moon_path(cx, cy, radius, color):
    return crescent_moon_template(cx + .2*radius, cy - .2*radius, radius, color.value, -math.pi/4, .25)


SUN_VALLEY = .625


def sun_path(cx, cy, radius, color):
    return path_template(
        polygon_path(
            star_vertices(
                points=8,
                center=(cx, cy),
                peak_radius=radius,
                valley_radius=radius*SUN_VALLEY,
                askew=math.pi/8,
            )
        ),
        color=color.value,
    )


def sun_area(radius):
    width = 2*radius*math.cos(math.pi/8)
    square_area = width*width

    corner_length = radius*(math.cos(math.pi/8) - math.sin(math.pi/8))
    corner_area = corner_length**2/2
    octagon_area = square_area - 4*corner_area

    indent_base = 2*radius*math.sin(math.pi/8)
    indent_height = (width/2) - SUN_VALLEY*radius
    indent_area = indent_base*indent_height/2
    sun_area = octagon_area - 8*indent_area

    return sun_area


STAR_VALLEY = .4


def star_path(cx, cy, radius, color):
    return path_template(
        polygon_path(
            star_vertices(
                points=4,
                center=(cx, cy),
                peak_radius=radius,
                valley_radius=radius * STAR_VALLEY,
                askew=0,
            )
        ),
        color=color.value,
    )


def star_area(radius):
    width = radius*math.sqrt(2)
    diamond_area = width*width
    indent_height = (width/2) - radius*STAR_VALLEY
    indent_area = width*indent_height/2
    star_area = diamond_area - 4*indent_area
    return star_area


SHAPES = {
    "sun": sun_path,
    "moon": moon_path,
    "star": star_path,
    "earth": earth_path,
}

EM = 50  # 15
SIDE_LENGTH = 48 * EM
BORDER_WIDTH = 4 * EM
CORNER_RADIUS = BORDER_WIDTH*.75
INNER_LENGTH = SIDE_LENGTH - BORDER_WIDTH*2


@dataclass
class NumberInfo:
    radius: int
    centers: list[tuple[int, int]]

LARGE = SIDE_LENGTH//6
SMALL = SIDE_LENGTH//12

QUARTER = SIDE_LENGTH//4
HALF = SIDE_LENGTH//2
THREE_QUARTER = 3*SIDE_LENGTH//4

WATERMARK_SATURATION: dict[Season, float] = {
    Season.AIR: .05,
    Season.SUMMER: .05,
    Season.SPRING: .075,
    Season.WINTER: .075,
    Season.AUTUMN: .1,
    Season.EARTH: .1,
}

NUMBERS = [
    NumberInfo(LARGE, [
        (HALF, HALF),
    ]),
    NumberInfo(SMALL, [
        (QUARTER, HALF),
        (THREE_QUARTER, HALF),
    ]),
    NumberInfo(SMALL, [
        (QUARTER, QUARTER),
        (HALF, HALF),
        (THREE_QUARTER, THREE_QUARTER),
    ]),
    NumberInfo(SMALL, [
        (QUARTER, HALF),
        (HALF, QUARTER),
        (THREE_QUARTER, HALF),
        (HALF, THREE_QUARTER),
    ]),
    NumberInfo(SMALL, [
        (QUARTER, QUARTER),
        (QUARTER, THREE_QUARTER),
        (HALF, HALF),
        (THREE_QUARTER, QUARTER),
        (THREE_QUARTER, THREE_QUARTER),
    ]),
]


@dataclass
class SeasonWatermark:
    curves: Callable[[int, int, str], list[str]]
    width: int
    height: int


WATERMARKS: dict[Season, SeasonWatermark] = {
    Season.SPRING: SeasonWatermark(
        # See comment in tessellating_clover_paths. There's some constraint that I failed to figure out, so I
        # arrived at these numbers by some trial and error.
        curves=lambda x, y, color: [
            f'<path d="{path}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>'
            for path in tessellating_clover_paths(x, y, math.pi * .6, math.pi * .1205, 2.4*EM, 1.2*EM)
        ] + [
            f'<path d="{path}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>'
            for path in tessellating_clover_paths(x + 3*EM, y + 1.75*EM, math.pi * .6, math.pi * .1205, 2.4*EM, 1.2*EM)
        ],
        width=round(6*EM),
        height=round(3.5*EM),
    ),
    Season.SUMMER: SeasonWatermark(
        curves=lambda x, y, color: [
            f'<path d="{hexagon_path(x, y, 1.2*EM)}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>',
            f'<path d="{hexagon_path(x + 1.8*EM, y + .6*EM*math.sqrt(3), 1.2*EM)}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>',
        ],
        width=round(3.6*EM),
        height=round(1.2*EM*math.sqrt(3)),
    ),
    Season.AUTUMN: SeasonWatermark(
        curves=lambda x, y, color: [
            f'<path d="{path}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>'
            for path in (
                leaf_paths(x, y, 4*EM)
                + leaf_paths(x + 6*EM, y + 2*EM*math.sqrt(3), 4*EM)
            )
        ],
        width=round(12*EM),
        height=round(4*EM*math.sqrt(3)),
    ),
    Season.WINTER: SeasonWatermark(
        curves=lambda x, y, color: [
            f'<path d="M{x} {y}A{.8*EM} {.8*EM} 0 0 0 {x+EM} {y} {.8*EM} {.8*EM} 0 0 1 {x+2*EM} {y} {.8*EM} {.8*EM} 0 0 0 {x+EM} {y} {.8*EM} {.8*EM} 0 0 1 {x} {y}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>',
            f'<path d="M{x+EM} {y+1.6*EM}A{.8*EM} {.8*EM} 0 0 0 {x+2*EM} {y+1.6*EM} {.8*EM} {.8*EM} 0 0 1 {x+3*EM} {y+1.6*EM} {.8*EM} {.8*EM} 0 0 0 {x+2*EM} {y+1.6*EM} {.8*EM} {.8*EM} 0 0 1 {x+EM} {y+1.6*EM} " stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>',
        ],
        width=round(2*EM),
        height=round(3.2*EM),
    ),
    Season.AIR: SeasonWatermark(
        curves=lambda x, y, color: [
            f'<path d="{uniform_spiral_path(x, y, 1.8*EM, i*math.pi, 2.5*math.pi, .1*EM, 10)}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>'
            for i in range(2)
        ] + [
            f'<path d="{uniform_spiral_path(x + 1.8*EM, y + 1.8*EM*math.sqrt(3), 1.8*EM, i*math.pi, 2.5*math.pi, .1*EM, 10)}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>'
            for i in range(2)
        ],
        width=round(3.6*EM),
        height=round(3.6*EM*math.sqrt(3))
    ),
    Season.EARTH: SeasonWatermark(
        curves=lambda x, y, color: [
            f'<path d="{path}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>'
            for path in (
                cube_paths(x, y, 2*EM)
                + cube_paths(x + 1*EM*math.sqrt(3), y + 3*EM, 2*EM)
            )
        ],
        width=round(2*EM*math.sqrt(3)),
        height=round(6*EM),
    ),
}


def make_season_cards():
    os.makedirs("images/season_cards", exist_ok=True)

    i = 0
    for season in Season:
        season_color = SEASON_COLORS[season]
        contrast_color = Color.BLACK if season_color in LIGHT_COLORS else Color.CREAM

        for shape_name, shape_function in SHAPES.items():
            for number_info in NUMBERS:
                count = len(number_info.centers)

                i += 1
                file_name = f"{i:03d}_{season.value}_{count}_{shape_name}s.svg"
                filepath = f"{CARDS_DIR}/{file_name}"

                paths = []
                paths.append(
                    rectangle_template(
                        0, 0, SIDE_LENGTH, SIDE_LENGTH,
                        radius=0,
                        color=contrast_color.value,
                    )
                )
                paths.append(
                    rectangle_template(
                        BORDER_WIDTH,
                        BORDER_WIDTH,
                        SIDE_LENGTH - 2*BORDER_WIDTH,
                        SIDE_LENGTH - 2*BORDER_WIDTH,
                        radius=CORNER_RADIUS,
                        color=season_color.value,
                    )
                )

                if season in WATERMARKS:
                    mask = f"""
                        <mask id="bodymask">
                            {rectangle_template(
                                0,
                                0,
                                SIDE_LENGTH,
                                SIDE_LENGTH,
                                radius=0,
                                color="black",
                            )}
                            {rectangle_template(
                                BORDER_WIDTH,
                                BORDER_WIDTH,
                                SIDE_LENGTH - 2*BORDER_WIDTH,
                                SIDE_LENGTH - 2*BORDER_WIDTH,
                                radius=CORNER_RADIUS,
                                color="white",
                            )}
                        </mask>
                    """
                    paths.append(mask)

                    watermark = WATERMARKS[season]
                    watermark_color = mix_hex_colors(contrast_color.value, season_color.value, WATERMARK_SATURATION[season])
                    for x in range(0, SIDE_LENGTH, watermark.width):
                        for y in range(0, SIDE_LENGTH, watermark.height):
                            paths += watermark.curves(x, y, watermark_color)

                for cx, cy in number_info.centers:
                    paths.append(
                        shape_function(cx, cy, number_info.radius, contrast_color)
                    )

                with open(filepath, "w") as fh:
                    fh.write(
                        svg_template(
                            SIDE_LENGTH,
                            SIDE_LENGTH,
                            paths,
                        )
                    )


def make_blank_cards():
    os.makedirs("images/season_cards", exist_ok=True)

    for shape_name, shape_function in SHAPES.items():
        for number_info in NUMBERS:
            for color_name, color in (('light', Color.CREAM), ('dark', Color.BLACK)):
                count = len(number_info.centers)

                file_name = f"blank_{count}_{shape_name}s_{color_name}.svg"
                filepath = f"{CARDS_DIR}/{file_name}"

                paths = []

                for cx, cy in number_info.centers:
                    paths.append(
                        shape_function(cx, cy, number_info.radius, color)
                    )

                with open(filepath, "w") as fh:
                    fh.write(
                        svg_template(
                            SIDE_LENGTH,
                            SIDE_LENGTH,
                            paths,
                        )
                    )

    for season in Season:
        contrast_color = Color.BLACK if SEASON_COLORS[season] in LIGHT_COLORS else Color.CREAM
        file_name = f"blank_{season.value}.svg"
        filepath = f"{CARDS_DIR}/{file_name}"

        paths = []
        paths.append(
            rectangle_template(
                0,0, SIDE_LENGTH*3, SIDE_LENGTH*3,
                radius=0,
                color=SEASON_COLORS[season].value,
            )
        )

        if season in WATERMARKS:
            watermark = WATERMARKS[season]
            watermark_color = mix_hex_colors(contrast_color.value, SEASON_COLORS[season].value, WATERMARK_SATURATION[season])
            for x in range(-watermark.width, SIDE_LENGTH*3 + watermark.width, watermark.width):
                for y in range(-watermark.height, SIDE_LENGTH*3 + watermark.height, watermark.height):
                    paths += watermark.curves(x, y, watermark_color)

        with open(filepath, "w") as fh:
            fh.write(
                svg_template(
                    SIDE_LENGTH*3,
                    SIDE_LENGTH*3,
                    paths,
                )
            )


# starts on the top and goes clockwise
def diamond_corners(center: tuple[int, int], radius: int):
    x, y = center
    return [
        (x, y - radius),
        (x + radius, y),
        (x, y + radius),
        (x - radius, y),
    ]


# starts on the top right and goes clockwise
def square_corners(center: tuple[int, int], radius: int):
    x, y = center
    return [
        (x + radius, y - radius),
        (x + radius, y + radius),
        (x - radius, y + radius),
        (x - radius, y - radius),
    ]


def rotate_list(l: list, r: int):
    r = r % len(l)
    return l[r:] + l[:r]


def make_back():
    filepath = f"{CARDS_DIR}/back.svg"

    paths = []
    paths.append(
        rectangle_template(
            0, 0, SIDE_LENGTH, SIDE_LENGTH,
            radius=0,
            color=Color.BLACK.value,
        )
    )

    corner_color = Color.WINTER_BLUE
    center_color = Color.SUMMER_GOLD
    color1 = Color.SPRING_GREEN
    color2 = Color.AUTUMN_RED

    paths.append(
        rectangle_template(
            BORDER_WIDTH, BORDER_WIDTH, INNER_LENGTH, INNER_LENGTH,
            radius=CORNER_RADIUS,
            color=corner_color.value,
        )
    )

    center = (SIDE_LENGTH//2, SIDE_LENGTH//2)

    paths.append(
        path_template(
            polygon_path(
                diamond_corners(center, INNER_LENGTH//4),
            ),
            color=center_color.value,
        )
    )
    for i, square_corner in enumerate(square_corners(center, INNER_LENGTH//4)):
        other_corners = rotate_list(
            diamond_corners(square_corner, INNER_LENGTH//4),
            i
        )[:2]
        paths.append(
            path_template(
                polygon_path((square_corner, *other_corners)),
                color=center_color.value,
            )
        )

    for i, square_corner in enumerate(square_corners(center, INNER_LENGTH//4)):
        other_corners = rotate_list(
            diamond_corners(square_corner, INNER_LENGTH//4),
            i+1
        )
        paths.append(
            path_template(
                polygon_path((square_corner, *other_corners[:2])),
                color=color2.value,
            )
        )
        paths.append(
            path_template(
                polygon_path((square_corner, *other_corners[2:])),
                color=color2.value,
            )
        )

    for i, diamond_corner in enumerate(diamond_corners(center, INNER_LENGTH//4)):
        other_corners = rotate_list(
            square_corners(diamond_corner, INNER_LENGTH//4),
            i + 3,
        )
    # for i, diamond_corner in enumerate(diamond_corners(center, INNER_LENGTH//2)):
    #     other_corners = rotate_list(
    #         square_corners(diamond_corner, INNER_LENGTH//4),
    #         i + 1,
    #     )

        paths.append(
            path_template(
                polygon_path((diamond_corner, *other_corners[:2])),
                color=color1.value,
            )
        )

    # for i, diamond_corner in enumerate(diamond_corners(center, INNER_LENGTH//4)):
    #     this_square_corners = rotate_list(
    #         square_corners(diamond_corner, INNER_LENGTH//4),
    #         i,
    #     )
    #     this_diamond_corners = rotate_list(
    #         diamond_corners(diamond_corner, INNER_LENGTH // 4),
    #         i,
    #     )
    #     paths.append(
    #         path_template(
    #             polygon_path((this_diamond_corners[0], this_square_corners[0], this_diamond_corners[1])),
    #             color=color2.value,
    #         )
    #     )
    #     paths.append(
    #         path_template(
    #             polygon_path((this_diamond_corners[-1], this_square_corners[-1], this_diamond_corners[0])),
    #             color=color2.value,
    #         )
    #     )

    with open(filepath, "w") as fh:
        fh.write(
            svg_template(
                SIDE_LENGTH,
                SIDE_LENGTH,
                paths,
            )
        )


def solar_system_paths(cx, cy, star_distance):
    standard_unit = star_distance/.72

    sun_radius = standard_unit * 7.5 * EM
    color_area = sun_area(sun_radius)

    earth_orbit = SIDE_LENGTH/math.sqrt(2)*(standard_unit*.39)
    earth_area = color_area/2
    earth_radius = (earth_area/math.pi)**.5

    moon_orbit = standard_unit*6.5*EM
    moon_area = color_area/16
    moon_radius = (moon_area/math.pi)**.5

    star_points = [(star_distance, 0), (star_distance, star_distance)]
    one_star_area = color_area/(4*len(star_points))
    star_radius = (one_star_area/star_area(1))**.5

    paths = []

    paths.append(
        sun_path(cx, cy, sun_radius, Color.AUTUMN_RED)
    )

    for i in range(4):
        earth_angle = i*math.pi/2 + math.pi/4
        earth_cx, earth_cy = cx + earth_orbit*math.cos(earth_angle), cy + earth_orbit*math.sin(earth_angle)

        paths.append(
            circle_template(earth_cx, earth_cy, earth_radius-.1*EM, Color.SPRING_GREEN.value)
        )
        paths.append(
            earth_path(earth_cx, earth_cy, earth_radius, Color.WINTER_BLUE)
        )

        for j in range(8):
            moon_angle = earth_angle + j*math.pi/4
            moon_cx, moon_cy = earth_cx + moon_orbit*math.cos(moon_angle), earth_cy + moon_orbit*math.sin(moon_angle)
            moon_fullness = abs(1 - j/4)
            paths.append(crescent_moon_template(moon_cx, moon_cy, moon_radius, Color.CREAM.value, earth_angle, moon_fullness))

        star_angle = i*math.pi/2
        ex, ey = cx + SIDE_LENGTH/2*math.cos(star_angle), cy + SIDE_LENGTH/2*math.sin(star_angle)
        basis = CustomBasis(cx, cy, ex, ey)
        for point in star_points:
            paths.append(star_path(*basis.convert(*point), star_radius, Color.SUMMER_GOLD))

    return paths


def make_solar_system_back():
    filepath = f"{CARDS_DIR}/solar_system_back.svg"

    cx, cy = SIDE_LENGTH / 2, SIDE_LENGTH / 2
    star_distance = .7

    paths = []
    paths.append(
        rectangle_template(
            0, 0, SIDE_LENGTH, SIDE_LENGTH,
            radius=0,
            color=Color.BLACK.value,
        )
    )
    paths += solar_system_paths(cx, cy, star_distance)

    with open(filepath, "w") as fh:
        fh.write(
            svg_template(
                SIDE_LENGTH,
                SIDE_LENGTH,
                paths,
            )
        )


if __name__ == "__main__":
    for file in os.listdir(CARDS_DIR):
        os.remove(os.path.join(CARDS_DIR, file))
    make_season_cards()
    make_blank_cards()
    make_back()
    make_solar_system_back()
