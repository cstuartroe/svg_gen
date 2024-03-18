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
                valley_radius=radius*.6667,
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


SIDE_LENGTH = 1200
BORDER_WIDTH = 75
CORNER_RADIUS = BORDER_WIDTH
INNER_LENGTH = SIDE_LENGTH - BORDER_WIDTH*2


@dataclass
class NumberInfo:
    radius: int
    centers: list[tuple[int, int]]


NUMBERS = [
    NumberInfo(200, [
        (600, 600),
    ]),
    NumberInfo(100, [
        (300, 600),
        (900, 600),
    ]),
    NumberInfo(100, [
        (300, 600),
        (600, 600),
        (900, 600),
    ]),
    NumberInfo(100, [
        (300, 600),
        (600, 300),
        (900, 600),
        (600, 900),
    ]),
    NumberInfo(100, [
        (300, 600),
        (600, 300),
        (600, 600),
        (900, 600),
        (600, 900),
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

    color_order = rotate_list(list(SEASON_COLORS.values()), 3)
    corner_color = color_order[0]
    # paint the corner color as background first and skip it later
    # in order to preserve rounded corners
    paths.append(
        rounded_rectangle_template(
            BORDER_WIDTH, BORDER_WIDTH, INNER_LENGTH, INNER_LENGTH,
            radius=CORNER_RADIUS,
            color=corner_color.value,
        )
    )

    center = (SIDE_LENGTH//2, SIDE_LENGTH//2)
    for i, diamond_center in enumerate(square_corners(
        center,
        INNER_LENGTH//4,
    )):
        this_color_order = rotate_list(color_order, 4-i)
        this_diamond_corners = diamond_corners(diamond_center, INNER_LENGTH//4)
        this_square_corners = square_corners(diamond_center, INNER_LENGTH//4)
        for j, color in zip(range(4), this_color_order):
            if color is corner_color:
                continue

            paths.append(
                path_template(
                    vertex_string=polygon_path([
                        this_diamond_corners[j],
                        this_square_corners[j],
                        this_diamond_corners[(j + 1) % 4]
                    ]),
                    color=color.value,
                )
            )
            paths.append(
                path_template(
                    vertex_string=polygon_path([
                        this_diamond_corners[(j + 2) % 4],
                        diamond_center,
                        this_diamond_corners[(j + 3) % 4],
                    ]),
                    color=color.value,
                )
            )

    paths.append(
        path_template(
            polygon_path(
                diamond_corners(center, INNER_LENGTH//4),
            ),
            color=color_order[2].value,
        )
    )

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
