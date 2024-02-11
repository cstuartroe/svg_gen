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
BORDER_WIDTH = 50
CORNER_RADIUS = BORDER_WIDTH


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

    color_xys = [
        (Color.SPRING_GREEN, BORDER_WIDTH, BORDER_WIDTH),
        (Color.SUMMER_GOLD, SIDE_LENGTH//2, BORDER_WIDTH),
        (Color.AUTUMN_RED, SIDE_LENGTH//2, SIDE_LENGTH//2),
        (Color.WINTER_BLUE, BORDER_WIDTH, SIDE_LENGTH//2)
    ]

    for i, (color, x, y) in enumerate(color_xys):
        paths.append(
            rounded_rectangle_template(
                x,
                y,
                SIDE_LENGTH//2 - BORDER_WIDTH,
                SIDE_LENGTH//2 - BORDER_WIDTH,
                radius=CORNER_RADIUS,
                color=color.value,
            )
        )

        adjust = SIDE_LENGTH//2 - BORDER_WIDTH*2
        corner_xys = [
            (x, y),
            (x + adjust, y),
            (x + adjust, y + adjust),
            (x, y + adjust)
        ]

        corners = [
            rounded_rectangle_template(
                cx, cy, BORDER_WIDTH, BORDER_WIDTH,
                radius=0,
                color=color.value,
            )
            for cx, cy in corner_xys
        ]

        for j, corner in enumerate(corners):
            if i != j:
                paths.append(corner)

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
