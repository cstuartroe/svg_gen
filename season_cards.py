from dataclasses import dataclass
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
    return circle_template(cx, cy, radius*.8, Color.CREAM.value)


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


SIDE_LENGTH = 2400 # 720
BORDER_WIDTH = 150 # 40
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

NUMBERS = [
    NumberInfo(LARGE, [
        (HALF, HALF),
    ]),
    NumberInfo(SMALL, [
        (QUARTER, HALF),
        (THREE_QUARTER, HALF),
    ]),
    NumberInfo(SMALL, [
        (QUARTER, HALF),
        (HALF, HALF),
        (THREE_QUARTER, HALF),
    ]),
    NumberInfo(SMALL, [
        (QUARTER, HALF),
        (HALF, QUARTER),
        (THREE_QUARTER, HALF),
        (HALF, THREE_QUARTER),
    ]),
    NumberInfo(SMALL, [
        (QUARTER, HALF),
        (HALF, QUARTER),
        (HALF, HALF),
        (THREE_QUARTER, HALF),
        (HALF, THREE_QUARTER),
    ]),
]


def make_season_cards():
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
                    rounded_rectangle_template(
                        0, 0, SIDE_LENGTH, SIDE_LENGTH,
                        radius=0,
                        color=Color.CREAM.value,
                    )
                )
                paths.append(
                    rounded_rectangle_template(
                        BORDER_WIDTH,
                        BORDER_WIDTH,
                        SIDE_LENGTH - 2*BORDER_WIDTH,
                        SIDE_LENGTH - 2*BORDER_WIDTH,
                        radius=CORNER_RADIUS,
                        color=SEASON_COLORS[season].value,
                    )
                )

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
        rounded_rectangle_template(
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
        rounded_rectangle_template(
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
