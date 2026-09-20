import math
import re

from . import utils
from . import season_cards

# 20 is standard Scryfall size
EM = 40

CARD_WIDTH = round(24.4*EM)
CARD_HEIGHT = round(34*EM)

CARD_RADIUS = EM
BORDER_THICKNESS = round(EM*1.25)
INTERNAL_BORDER_WIDTH = .25*EM
BADGE_HEIGHT = 2*EM
BADGE_CURVE_RADIUS = BADGE_HEIGHT
MANA_SYMBOL_HEIGHT = round(.5*BADGE_HEIGHT)
TITLE_BADGE_HEIGHT = 2*BORDER_THICKNESS
TYPE_BADGE_HEIGHT = CARD_HEIGHT*.535
SIDE_PADDING = 2 * BORDER_THICKNESS
BOTTOM_PADDING = 2.5*BORDER_THICKNESS


LIGHT_GRAY = utils.mix_hex_colors(utils.Color.EARTH_BROWN.value, utils.Color.CREAM.value, .1)
SEMILIGHT_GRAY = utils.mix_hex_colors(utils.Color.EARTH_BROWN.value, utils.Color.CREAM.value, .18)
MEDIUM_GRAY = utils.mix_hex_colors(utils.Color.EARTH_BROWN.value, utils.Color.CREAM.value, .4)


SEASON_LETTERS = {
    "W": season_cards.Season.AIR,
    "B": season_cards.Season.EARTH,
    "G": season_cards.Season.SPRING,
    "Y": season_cards.Season.SUMMER,
    "R": season_cards.Season.AUTUMN,
    "U": season_cards.Season.WINTER,
}

LAND_NAMES = {
    "W": "steppe",
    "B": "floodplain",
    "G": "forest",
    "Y": "desert",
    "R": "mountain",
    "U": "island",
}


MANA_PAIRS = [
    "UG",
    "GY",
    "YR",
    "RU",

    "WU",
    "UY",
    "YW",

    "BG",
    "GR",
    "RB",

    "GW",
    "WR",

    "UB",
    "BY",

    "WB",
]


def badge_path(height: float, color: str) -> str:
    return utils.path_template(
        vertex_string=(
            f"M{SIDE_PADDING} {height} "
            f"L {CARD_WIDTH - SIDE_PADDING} {height} "
            f"A {BADGE_CURVE_RADIUS} {BADGE_CURVE_RADIUS} 0 0 1 {CARD_WIDTH - SIDE_PADDING} {height + BADGE_HEIGHT} "
            f"L {SIDE_PADDING} {height + BADGE_HEIGHT} "
            f"A {BADGE_CURVE_RADIUS} {BADGE_CURVE_RADIUS} 0 0 1 {SIDE_PADDING} {height} Z"
        ),
        color=color,
        border_color=utils.Color.EARTH_BROWN.value,
        border_width=INTERNAL_BORDER_WIDTH,
    )


def make_mtg_frame(
        name: str,
        background_color: str,
        text_background_color: str,
        badge_color: str,
        watermark: season_cards.SeasonWatermark | None = None,
        watermark_color: str | None = None,
        mana_symbol: season_cards.WatermarkGenerator | None = None,
        mana_type: str | None = None,
        mana_symbol_color: str | None = None,
):
    pattern_paths = []
    if watermark:
        for x in range(-watermark.width, CARD_WIDTH, watermark.width):
            for y in range(-watermark.height, CARD_HEIGHT, watermark.height):
                pattern_paths += watermark.curves(x, y, watermark_color)

    mana_symbol_paths = []
    if mana_symbol:
        mana_symbol_paths += make_mana_symbol_paths(
            mana_type=mana_type,
            generator=mana_symbol,
            color=mana_symbol_color,
            scale=10*EM,
            cx=CARD_WIDTH//2,
            cy=CARD_HEIGHT*.75,
        )

    template = utils.svg_template(
        width=CARD_WIDTH,
        height=CARD_HEIGHT,
        paths=[
            utils.rectangle_template(
                0,
                0,
                CARD_WIDTH,
                CARD_HEIGHT,
                color=utils.Color.EARTH_BROWN.value,
                radius=CARD_RADIUS,
            ),
            utils.rectangle_template(
                BORDER_THICKNESS,
                BORDER_THICKNESS,
                CARD_WIDTH - 2*BORDER_THICKNESS,
                CARD_HEIGHT - 2*BORDER_THICKNESS,
                color=background_color,
                radius=0,
            ),
            utils.mask_template(
                name=season_cards.PATTERN_MASK_ID,
                paths=[
                    utils.rectangle_template(
                        BORDER_THICKNESS,
                        BORDER_THICKNESS,
                        CARD_WIDTH - 2*BORDER_THICKNESS,
                        CARD_HEIGHT - 2*BORDER_THICKNESS,
                        color="white",
                        radius=0,
                    ),
                ],
            ),
            *pattern_paths,
            utils.rectangle_template(
                2*BORDER_THICKNESS,
                3*BORDER_THICKNESS,
                CARD_WIDTH - 4*BORDER_THICKNESS,
                CARD_HEIGHT - 3*BORDER_THICKNESS - BOTTOM_PADDING,
                color=text_background_color,
                border_color=utils.Color.EARTH_BROWN.value,
                border_width=INTERNAL_BORDER_WIDTH,
            ),
            badge_path(TITLE_BADGE_HEIGHT, badge_color),
            badge_path(TYPE_BADGE_HEIGHT, badge_color),
            *mana_symbol_paths,
        ],
    )

    with open(f"images/mtg/frame_{name}.svg", "w") as fh:
        fh.write(template)


PT_BADGE_WIDTH = 7*BORDER_THICKNESS


def make_pt_badge(name: str, badge_color: str):
    template = utils.svg_template(
        PT_BADGE_WIDTH,
        BADGE_HEIGHT + INTERNAL_BORDER_WIDTH,
        paths=[
            utils.path_template(
                vertex_string=(
                    f"M{2 * BORDER_THICKNESS} {INTERNAL_BORDER_WIDTH/2} "
                    f"L {5 * BORDER_THICKNESS} {INTERNAL_BORDER_WIDTH/2} "
                    f"A {BADGE_CURVE_RADIUS} {BADGE_CURVE_RADIUS} 0 0 1 {5 * BORDER_THICKNESS} {BADGE_HEIGHT + INTERNAL_BORDER_WIDTH/2} "
                    f"L {2 * BORDER_THICKNESS} {BADGE_HEIGHT + INTERNAL_BORDER_WIDTH/2} "
                    f"A {BADGE_CURVE_RADIUS} {BADGE_CURVE_RADIUS} 0 0 1 {2 * BORDER_THICKNESS} {INTERNAL_BORDER_WIDTH/2} Z"
                ),
                color=badge_color,
                border_color=utils.Color.EARTH_BROWN.value,
                border_width=INTERNAL_BORDER_WIDTH,
            ),
        ],
    )

    with open(f"images/mtg/badge_pt_{name}.svg", "w") as fh:
        fh.write(template)


def make_mana_badge():
    template = utils.svg_template(
        MANA_SYMBOL_HEIGHT,
        MANA_SYMBOL_HEIGHT,
        paths=[
            utils.path_template(
                utils.centered_hexagon_path(
                    cx=MANA_SYMBOL_HEIGHT/2,
                    cy=MANA_SYMBOL_HEIGHT/2,
                    side_length=MANA_SYMBOL_HEIGHT/2,
                    vert=True,
                ),
                color=MEDIUM_GRAY,
            ),
        ],
    )

    with open(f"images/mtg/mana_number.svg", "w") as fh:
        fh.write(template)


def make_tap_symbol():
    cx = MANA_SYMBOL_HEIGHT / 2
    cy = MANA_SYMBOL_HEIGHT / 2

    paths = [
        utils.circle_template(
            cx=cx,
            cy=cy,
            radius=cy,
            color=MEDIUM_GRAY,
        ),
    ]

    arc_short_radius = cx/3
    arc_long_radius = cx/2
    arc_dx = arc_short_radius/2
    arc_dy = arc_short_radius*math.sqrt(3)/2

    paths.append(
        utils.path_template(
            vertex_string=f"M {cx - arc_dx} {cy + arc_dy} A {arc_long_radius} {arc_short_radius} 30 1 1 {cx + arc_dx} {cy - arc_dy} ",
            border_color=utils.Color.EARTH_BROWN.value,
            border_width=cx/5,
        ),
    )

    paths.append(
        utils.path_template(
            utils.polygon_path([(cx, cy), (cx + 2*arc_dx, cy - 2*arc_dy), (cx + 4*arc_dx, cy)]),
            color=utils.Color.EARTH_BROWN.value,
        ),
    )

    template = utils.svg_template(MANA_SYMBOL_HEIGHT, MANA_SYMBOL_HEIGHT, paths)

    with open(f"images/mtg/tap.svg", "w") as fh:
        fh.write(template)


LEAF_PATH_PATTERN = '(<path d="M [0-9.-]+ [0-9.-]+ L [0-9.-]+ [0-9.-]+ L [0-9.-]+ [0-9.-]+ L [0-9.-]+ [0-9.-]+ L [0-9.-]+ [0-9.-]+ L [0-9.-]+ [0-9.-]+ )L [0-9.-]+ [0-9.-]+ L [0-9.-]+ [0-9.-]+ (" stroke="#[0-9a-f]+" stroke-width="[0-9.]+" fill="none" mask="url\\(#bodymask\\)"/>)'



def make_mana_symbol_paths(mana_type: str, generator: season_cards.WatermarkGenerator, color: str, scale: float, cx: float, cy: float) -> list[str]:
    stroke_width = .06 * scale

    if mana_type == "B":
        earth_paths = generator(.18 * scale, stroke_width).curves(cx, cy, color)
        return earth_paths[:4]

    elif mana_type == "G":
        scaled_watermark = generator(.133 * scale, stroke_width)
        return scaled_watermark.curves(cx, cy, color)[:1]

    elif mana_type == "R":
        scaled_watermark = generator(.09 * scale, stroke_width)
        h1 = scaled_watermark.curves(cx - scaled_watermark.width / 2, cy - scaled_watermark.height / 2, color)
        h2 = scaled_watermark.curves(cx - 3 * scaled_watermark.width / 2, cy - scaled_watermark.height / 2,
                                     color)
        hex_paths = [h1[0], h1[5], h1[10], h1[9], h2[8], h2[7]]

        pattern_paths = []
        for i, path in enumerate(hex_paths):
            if i % 2 == 0:
                pattern_paths.append(path)
            else:
                m = re.match(LEAF_PATH_PATTERN, path)
                if m is None:
                    print(path)
                pattern_paths.append(m.group(1) + m.group(2))

        return pattern_paths

    elif mana_type == "U":
        scaled_watermark = generator(.15 * scale, stroke_width)
        wave_paths = []
        for y in [-1, 0]:
            for x in [-1, 0]:
                wave_paths += scaled_watermark.curves(cx + x * scaled_watermark.width, cy + y * scaled_watermark.height,
                                                      color)
        return [wave_paths[1], *wave_paths[4:7]]

    elif mana_type == "W":
        scaled_watermark = generator(.18 * scale, stroke_width)
        return scaled_watermark.curves(cx, cy, color)[:2]

    elif mana_type == "Y":
        side_length = .2 * scale

        pattern_paths = [
            utils.path_template(
                utils.centered_hexagon_path(cx, cy, side_length, vert=True),
                border_color=color,
                border_width=stroke_width,
            )
        ]

        spoke_length = .8
        for i in range(6):
            corner_x = cx + math.sin(i * math.pi / 3) * side_length
            corner_y = cy + math.cos(i * math.pi / 3) * side_length
            tip_x = cx + math.sin(i * math.pi / 3) * side_length * (1 + spoke_length)
            tip_y = cy + math.cos(i * math.pi / 3) * side_length * (1 + spoke_length)

            pattern_paths.append(
                utils.path_template(
                    utils.polygon_path([(corner_x, corner_y), (tip_x, tip_y)]),
                    border_color=color,
                    border_width=stroke_width,
                ),
            )

        return pattern_paths

    else:
        raise ValueError


def make_mana_symbols():
    cx = MANA_SYMBOL_HEIGHT / 2
    cy = MANA_SYMBOL_HEIGHT / 2

    for letter, season in SEASON_LETTERS.items():
        color = season_cards.SEASON_COLORS[season]
        generator = season_cards.WATERMARKS[season]
        watermark_color = MEDIUM_GRAY if color is utils.Color.CREAM else utils.Color.CREAM.value

        pattern_paths = make_mana_symbol_paths(
            mana_type=letter,
            generator=generator,
            color=watermark_color,
            scale=MANA_SYMBOL_HEIGHT,
            cx=cx,
            cy=cy,
        )

        template = utils.svg_template(
            MANA_SYMBOL_HEIGHT,
            MANA_SYMBOL_HEIGHT,
            paths=[
                utils.path_template(
                    utils.centered_hexagon_path(
                        cx=cx,
                        cy=cy,
                        side_length=cy,
                        vert=True,
                    ),
                    color=color.value,
                ),
                *pattern_paths,
            ],
        )

        with open(f"images/mtg/mana_{letter}.svg", "w") as fh:
            fh.write(template)

    dual_symbol_offset = cy*.45
    dx = dual_symbol_offset/2
    dy = dual_symbol_offset*((3/4)**.5)

    for letter_pair in MANA_PAIRS:
        l1, l2 = letter_pair

        season1 = SEASON_LETTERS[l1]
        color1 = season_cards.SEASON_COLORS[season1]
        generator1 = season_cards.WATERMARKS[season1]
        watermark_color1 = MEDIUM_GRAY if color1 is utils.Color.CREAM else utils.Color.CREAM.value

        pattern_paths1 = make_mana_symbol_paths(
            mana_type=l1,
            generator=generator1,
            color=watermark_color1,
            scale=MANA_SYMBOL_HEIGHT/2,
            cx=cx - dx,
            cy=cy - dy,
        )

        season2 = SEASON_LETTERS[l2]
        color2 = season_cards.SEASON_COLORS[season2]
        generator2 = season_cards.WATERMARKS[season2]
        watermark_color2 = MEDIUM_GRAY if color2 is utils.Color.CREAM else utils.Color.CREAM.value

        pattern_paths2 = make_mana_symbol_paths(
            mana_type=l2,
            generator=generator2,
            color=watermark_color2,
            scale=MANA_SYMBOL_HEIGHT/2,
            cx=cx + dx,
            cy=cy + dy,
        )

        hex_points = utils.centered_hexagon_points(
            cx=cx,
            cy=cy,
            side_length=cy,
            vert=True,
        )

        template = utils.svg_template(
            MANA_SYMBOL_HEIGHT,
            MANA_SYMBOL_HEIGHT,
            paths=[
                utils.path_template(
                    utils.polygon_path([
                        hex_points[2],
                        hex_points[3],
                        hex_points[4],
                        hex_points[5],
                    ]),
                    color=color1.value,
                ),
                utils.path_template(
                    utils.polygon_path([
                        hex_points[5],
                        hex_points[0],
                        hex_points[1],
                        hex_points[2],
                    ]),
                    color=color2.value,
                ),
                *pattern_paths1,
                *pattern_paths2,
            ],
        )

        with open(f"images/mtg/mana_{l1}{l2}.svg", "w") as fh:
            fh.write(template)


def make_city_states_logo():
    wall_rim_y = MANA_SYMBOL_HEIGHT*.5
    wall_floor_y = MANA_SYMBOL_HEIGHT*.9
    tower_top_y = 0
    parapet_depth = MANA_SYMBOL_HEIGHT*.1
    cx = MANA_SYMBOL_HEIGHT/2
    wall_radius = MANA_SYMBOL_HEIGHT*.5
    tower_bottom_radius = MANA_SYMBOL_HEIGHT*.2
    tower_top_radius = MANA_SYMBOL_HEIGHT*.15
    parapet_radius = tower_top_radius*.666
    wall_curve_radius = wall_radius*2.6
    wall_border_width = MANA_SYMBOL_HEIGHT*.02
    window_y = MANA_SYMBOL_HEIGHT*.25
    window_side_length = tower_top_radius*.45

    template = utils.svg_template(
        MANA_SYMBOL_HEIGHT,
        MANA_SYMBOL_HEIGHT,
        paths=[
            utils.path_template(
                (
                    f"M {cx - wall_radius} {wall_floor_y} "
                    f"A {wall_curve_radius} {wall_curve_radius} 0 0 0 {cx + wall_radius} {wall_floor_y} "
                    f"L {cx + wall_radius} {wall_rim_y} "
                    f"A {wall_curve_radius} {wall_curve_radius} 0 0 1 {cx - wall_radius} { wall_rim_y } Z"
                ),
                color=utils.Color.EARTH_BROWN.value,
            ),
            utils.path_template(
                (
                    f"M {cx + wall_radius} {wall_rim_y} "
                    f"A {wall_curve_radius} {wall_curve_radius} 0 0 0 {cx - wall_radius} { wall_rim_y }"
                ),
                border_color=utils.Color.EARTH_BROWN.value,
                border_width=wall_border_width,
            ),
            utils.mask_template(
                "tower",
                [
                    utils.path_template(
                        utils.rectangle_path(0, 0, MANA_SYMBOL_HEIGHT, MANA_SYMBOL_HEIGHT),
                        color="white",
                    ),
                    utils.path_template(
                        (
                            f"M {cx + wall_radius} {wall_rim_y} "
                            f"A {wall_curve_radius} {wall_curve_radius} 0 0 1 {cx - wall_radius} {wall_rim_y}"
                        ),
                        border_color="black",
                        border_width=wall_border_width,
                    ),
                    utils.path_template(
                        utils.centered_hexagon_path(cx, window_y, window_side_length, vert=True),
                        color="black",
                    ),
                ],
            ),
            utils.apply_mask(
                utils.path_template(
                    utils.polygon_path([
                        (cx - tower_bottom_radius, wall_floor_y),
                        (cx - tower_top_radius, tower_top_y),
                        (cx - tower_top_radius + parapet_radius, tower_top_y),
                        (cx - tower_top_radius + parapet_radius, tower_top_y + parapet_depth),
                        (cx + tower_top_radius - parapet_radius, tower_top_y + parapet_depth),
                        (cx + tower_top_radius - parapet_radius, tower_top_y),
                        (cx + tower_top_radius, tower_top_y),
                        (cx + tower_bottom_radius, wall_floor_y),
                    ]),
                    color=utils.Color.EARTH_BROWN.value,
                ),
                mask_name="tower",
            ),
        ],
    )

    with open(f"images/mtg/release_cts.svg", "w") as fh:
        fh.write(template)


def make_color_and_mana_frames():
    for letter, season in SEASON_LETTERS.items():
        color = season_cards.SEASON_COLORS[season]
        badge_color = utils.mix_hex_colors(color.value, utils.Color.CREAM.value, .3)

        contrast_color = utils.Color.EARTH_BROWN if color is utils.Color.CREAM else utils.Color.CREAM
        watermark = season_cards.WATERMARKS[season](.375*EM, .075*EM)
        watermark_color = utils.mix_hex_colors(contrast_color.value, color.value, season_cards.WATERMARK_SATURATION[season])

        make_mtg_frame(
            name=letter,
            background_color=color.value,
            text_background_color=utils.mix_hex_colors(color.value, utils.Color.WHITE.value, .2),
            badge_color=badge_color,
            watermark=watermark,
            watermark_color=watermark_color,
        )

        make_mtg_frame(
            name=letter + "_dual",
            background_color=color.value,
            text_background_color=utils.mix_hex_colors(color.value, utils.Color.WHITE.value, .2),
            badge_color=SEMILIGHT_GRAY,
            watermark=watermark,
            watermark_color=watermark_color,
        )

        make_pt_badge(
            name=letter,
            badge_color=badge_color,
        )

        make_mtg_frame(
            name=LAND_NAMES[letter],
            background_color=utils.Color.LAND_TAN.value,
            text_background_color=utils.mix_hex_colors(color.value, utils.Color.CREAM.value, .5),
            badge_color=badge_color,
            mana_symbol=season_cards.WATERMARKS[season],
            mana_type=letter,
            mana_symbol_color=MEDIUM_GRAY if color is utils.Color.CREAM else color.value,
        )


def make_colorless_frame():
    make_mtg_frame(
        name="C",
        background_color=MEDIUM_GRAY,
        text_background_color=LIGHT_GRAY,
        badge_color=SEMILIGHT_GRAY,
    )

    make_pt_badge(
        name="C",
        badge_color=SEMILIGHT_GRAY,
    )


if __name__ == "__main__":
    make_mana_badge()
    make_mana_symbols()
    make_tap_symbol()
    make_city_states_logo()
    make_color_and_mana_frames()
    make_colorless_frame()
