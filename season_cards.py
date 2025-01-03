import os
from dataclasses import dataclass
from typing import Callable

from utils import *

CARDS_DIR = "images/season_cards"


class Season(Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


SEASON_COLORS: dict[Season, Color] = {
    Season.SPRING: Color.SPRING_GREEN,
    Season.SUMMER: Color.SUMMER_GOLD,
    Season.AUTUMN: Color.AUTUMN_RED,
    Season.WINTER: Color.WINTER_BLUE,
}


def moon_path(cx, cy, radius):
    return crescent_moon_template(cx, cy, radius*.8, Color.CREAM.value, 45)


def sun_path(cx, cy, radius):
    return path_template(
        polygon_path(
            star_vertices(
                points=8,
                center=(cx, cy),
                peak_radius=radius,
                valley_radius=radius*.625,
                askew=math.pi/8,
            )
        ),
        color=Color.CREAM.value,
    )


def star_path(cx, cy, radius):
    return path_template(
        polygon_path(
            star_vertices(
                points=4,
                center=(cx, cy),
                peak_radius=radius,
                valley_radius=radius * .4,
                askew=0,
            )
        ),
        color=Color.CREAM.value,
    )


SHAPES = {
    "sun": sun_path,
    "moon": moon_path,
    "star": star_path,
}

EM = 50  # 15
SIDE_LENGTH = 48 * EM
BORDER_WIDTH = 3 * EM
CORNER_RADIUS = BORDER_WIDTH
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

WATERMARK_SATURATION = .2

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
            f'<path d="{leaf_path(x, y, 2.4*EM, .6*EM)}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>',
            # f'<line x1="{x}" y1="{y}" x2="{x+300}" y2="{y}" stroke="{color}" stroke-width="10" fill="none" mask="url(#bodymask)"/>',
            # f'<line x1="{x+150}" y1="{y+40}" x2="{x+450}" y2="{y+40}" stroke="{color}" stroke-width="10" fill="none" mask="url(#bodymask)"/>',
        ],
        width=round(4.8*EM),
        height=round(1.2*EM),
    ),
    Season.WINTER: SeasonWatermark(
        curves=lambda x, y, color: [
            f'<path d="M{x} {y}A{.8*EM} {.8*EM} 0 0 0 {x+EM} {y} {.8*EM} {.8*EM} 0 0 1 {x+2*EM} {y} {.8*EM} {.8*EM} 0 0 0 {x+EM} {y} {.8*EM} {.8*EM} 0 0 1 {x} {y}" stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>',
            f'<path d="M{x+EM} {y+1.6*EM}A{.8*EM} {.8*EM} 0 0 0 {x+2*EM} {y+1.6*EM} {.8*EM} {.8*EM} 0 0 1 {x+3*EM} {y+1.6*EM} {.8*EM} {.8*EM} 0 0 0 {x+2*EM} {y+1.6*EM} {.8*EM} {.8*EM} 0 0 1 {x+EM} {y+1.6*EM} " stroke="{color}" stroke-width="{.2*EM}" fill="none" mask="url(#bodymask)"/>',
        ],
        width=round(2*EM),
        height=round(3.2*EM),
    ),
}


def make_season_cards():
    os.makedirs("images/season_cards", exist_ok=True)

    i = 0
    for season in Season:
        for shape_name, shape_function in SHAPES.items():
            for number_info in NUMBERS:
                count = len(number_info.centers)

                i += 1
                file_name = f"{i:02d}_{season.value}_{count}_{shape_name}s.svg"
                filepath = f"{CARDS_DIR}/{file_name}"

                paths = []
                paths.append(
                    rectangle_template(
                        0, 0, SIDE_LENGTH, SIDE_LENGTH,
                        radius=0,
                        color=Color.CREAM.value,
                    )
                )
                paths.append(
                    rectangle_template(
                        BORDER_WIDTH,
                        BORDER_WIDTH,
                        SIDE_LENGTH - 2*BORDER_WIDTH,
                        SIDE_LENGTH - 2*BORDER_WIDTH,
                        radius=CORNER_RADIUS,
                        color=SEASON_COLORS[season].value,
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
                    watermark_color = mix_hex_colors(Color.CREAM.value, SEASON_COLORS[season].value, .2)
                    for x in range(0, SIDE_LENGTH, watermark.width):
                        for y in range(0, SIDE_LENGTH, watermark.height):
                            paths += watermark.curves(x, y, watermark_color)

                for cx, cy in number_info.centers:
                    paths.append(
                        shape_function(cx, cy, number_info.radius)
                    )

                with open(filepath, "w") as fh:
                    fh.write(
                        svg_template(
                            SIDE_LENGTH,
                            SIDE_LENGTH,
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


if __name__ == "__main__":
    make_season_cards()
    make_back()
