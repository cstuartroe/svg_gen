import math
import re

import utils
import season_cards

# 20 is standard Scryfall size
EM = 40

CARD_WIDTH = round(24.4*EM)
CARD_HEIGHT = round(34*EM)

CARD_RADIUS = EM
BORDER_THICKNESS = round(EM*1.25)
INTERNAL_BORDER_WIDTH = .25*EM
BADGE_HEIGHT = 2*EM
BADGE_CURVE_RADIUS = BADGE_HEIGHT
MANA_SYMBOL_HEIGHT = round(.75*BADGE_HEIGHT)


LIGHT_GRAY = utils.mix_hex_colors(utils.Color.EARTH_BROWN.value, utils.Color.CREAM.value, .4)


SEASON_LETTERS = {
    season_cards.Season.AIR: "W",
    season_cards.Season.EARTH: "B",
    season_cards.Season.SPRING: "G",
    season_cards.Season.SUMMER: "Y",
    season_cards.Season.AUTUMN: "R",
    season_cards.Season.WINTER: "U",
}


def badge_path(height: float) -> str:
    return utils.path_template(
        vertex_string=(
            f"M{2*BORDER_THICKNESS} {height} "
            f"L {CARD_WIDTH - 2*BORDER_THICKNESS} {height} "
            f"A {BADGE_CURVE_RADIUS} {BADGE_CURVE_RADIUS} 0 0 1 {CARD_WIDTH - 2*BORDER_THICKNESS} {height + BADGE_HEIGHT} "
            f"L {2*BORDER_THICKNESS} {height + BADGE_HEIGHT} "
            f"A {BADGE_CURVE_RADIUS} {BADGE_CURVE_RADIUS} 0 0 1 {2*BORDER_THICKNESS} {height} Z"
        ),
        color=utils.Color.CREAM.value,
        border_color=utils.Color.EARTH_BROWN.value,
        border_width=INTERNAL_BORDER_WIDTH,
    )


def make_mtg_frame(season: season_cards.Season, letter: str):
    color = season_cards.SEASON_COLORS[season]
    contrast_color = utils.Color.EARTH_BROWN if color is utils.Color.CREAM else utils.Color.CREAM
    watermark = season_cards.WATERMARKS[season](.375*EM, .075*EM)

    pattern_paths = []
    watermark_color = utils.mix_hex_colors(contrast_color.value, color.value, season_cards.WATERMARK_SATURATION[season])
    for x in range(-watermark.width, CARD_WIDTH, watermark.width):
        for y in range(-watermark.height, CARD_HEIGHT, watermark.height):
            pattern_paths += watermark.curves(x, y, watermark_color)

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
                color=color.value,
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
                CARD_HEIGHT - 6*BORDER_THICKNESS,
                color=utils.Color.CREAM.value,
                border_color=utils.Color.EARTH_BROWN.value,
                border_width=INTERNAL_BORDER_WIDTH,
            ),
            badge_path(2*BORDER_THICKNESS),
            badge_path(CARD_HEIGHT*.535),
        ],
    )

    with open(f"images/mtg/frame_{letter}.svg", "w") as fh:
        fh.write(template)


def make_pt_badge():
    template = utils.svg_template(
        8*BORDER_THICKNESS,
        BADGE_HEIGHT + INTERNAL_BORDER_WIDTH,
        paths=[
            utils.path_template(
                vertex_string=(
                    f"M{2 * BORDER_THICKNESS} {INTERNAL_BORDER_WIDTH/2} "
                    f"L {6 * BORDER_THICKNESS} {INTERNAL_BORDER_WIDTH/2} "
                    f"A {BADGE_CURVE_RADIUS} {BADGE_CURVE_RADIUS} 0 0 1 {6 * BORDER_THICKNESS} {BADGE_HEIGHT + INTERNAL_BORDER_WIDTH/2} "
                    f"L {2 * BORDER_THICKNESS} {BADGE_HEIGHT + INTERNAL_BORDER_WIDTH/2} "
                    f"A {BADGE_CURVE_RADIUS} {BADGE_CURVE_RADIUS} 0 0 1 {2 * BORDER_THICKNESS} {INTERNAL_BORDER_WIDTH/2} Z"
                ),
                color=utils.Color.CREAM.value,
                border_color=utils.Color.EARTH_BROWN.value,
                border_width=INTERNAL_BORDER_WIDTH,
            ),
        ],
    )

    with open(f"images/mtg/badge_pt.svg", "w") as fh:
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
                color=LIGHT_GRAY,
            ),
            utils.path_template(
                utils.centered_hexagon_path(
                    cx=MANA_SYMBOL_HEIGHT/2,
                    cy=MANA_SYMBOL_HEIGHT/2,
                    side_length=.94*MANA_SYMBOL_HEIGHT/2,
                    vert=True,
                ),
                color=utils.Color.CREAM.value,
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
            color=LIGHT_GRAY,
        ),
        utils.circle_template(
            cx=cx,
            cy=cy,
            radius=cy,
            color=utils.Color.CREAM.value,
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


LEAF_PATH_PATTERN = '(<path d="M [0-9.]+ [0-9.]+ L [0-9.]+ [0-9.]+ L [0-9.]+ [0-9.]+ L [0-9.]+ [0-9.]+ L [0-9.]+ [0-9.]+ L [0-9.]+ [0-9.]+ )L [0-9.]+ [0-9.]+ L [0-9.]+ [0-9.]+ (" stroke="#[0-9a-f]+" stroke-width="[0-9.]+" fill="none" mask="url\\(#bodymask\\)"/>)'


def make_mana_symbols():
    for season, letter in SEASON_LETTERS.items():
        color = season_cards.SEASON_COLORS[season]
        watermark = season_cards.WATERMARKS[season]
        watermark_color = LIGHT_GRAY if color is utils.Color.CREAM else utils.Color.CREAM.value

        cx = MANA_SYMBOL_HEIGHT / 2
        cy = MANA_SYMBOL_HEIGHT / 2
        stroke_width = .05*EM

        if letter == "B":
            earth_paths = watermark(.375*EM, stroke_width).curves(cx, cy, watermark_color)
            pattern_paths = earth_paths[1:4]
        elif letter == "G":
            scaled_watermark = watermark(.2*EM, stroke_width)
            pattern_paths = scaled_watermark.curves(cx, cy, watermark_color)[:1]
        elif letter == "R":
            scaled_watermark = watermark(.15*EM, stroke_width)
            hex_paths = scaled_watermark.curves(cx - scaled_watermark.width/2, cy - scaled_watermark.height/6, watermark_color)[:6]

            pattern_paths = []
            for path in hex_paths:
                m = re.match(LEAF_PATH_PATTERN, path)
                pattern_paths.append(m.group(1) + m.group(2))

        elif letter == "U":
            scaled_watermark = watermark(.25*EM, stroke_width)
            wave_paths = []
            for y in [-1, 0]:
                for x in [-1, 0]:
                    wave_paths += scaled_watermark.curves(cx + x*scaled_watermark.width, cy + y*scaled_watermark.height, watermark_color)
            pattern_paths = [wave_paths[1], *wave_paths[4:7]]
        elif letter == "W":
            scaled_watermark = watermark(.275 * EM, stroke_width)
            pattern_paths = scaled_watermark.curves(cx, cy, watermark_color)[:2]
        elif letter == "Y":
            side_length = .4*cx

            pattern_paths = [
                utils.path_template(
                    utils.centered_hexagon_path(cx, cy, side_length, vert=True),
                    border_color=watermark_color,
                    border_width=stroke_width,
                )
            ]

            spoke_length = .8
            for i in range(6):
                corner_x = cx + math.sin(i*math.pi/3)*side_length
                corner_y = cx + math.cos(i*math.pi/3)*side_length
                tip_x = cx + math.sin(i*math.pi/3)*side_length*(1+spoke_length)
                tip_y = cx + math.cos(i*math.pi/3)*side_length*(1+spoke_length)

                pattern_paths.append(
                    utils.path_template(
                        utils.polygon_path([(corner_x, corner_y), (tip_x, tip_y)]),
                        border_color=watermark_color,
                        border_width=stroke_width,
                    ),
                )

        else:
            raise ValueError

        template = utils.svg_template(
            MANA_SYMBOL_HEIGHT,
            MANA_SYMBOL_HEIGHT,
            paths=[
                utils.path_template(
                    utils.centered_hexagon_path(
                        cx,
                        cy,
                        side_length=cy,
                        vert=True,
                    ),
                    color=color.value,
                ),
                # utils.circle_template(
                #     cx,
                #     cy,
                #     radius=cy,
                #     color=color.value,
                # ),
                utils.mask_template(
                    name=season_cards.PATTERN_MASK_ID,
                    paths=[
                        # utils.circle_template(
                        #     cx,
                        #     cy,
                        #     radius=cy,
                        #     color="white",
                        # ),
                        utils.path_template(
                            utils.centered_hexagon_path(
                                cx,
                                cy,
                                side_length=cy,
                                vert=True,
                            ),
                            color="white",
                        ),
                    ],
                ),
                *pattern_paths,
            ],
        )

        with open(f"images/mtg/mana_{letter}.svg", "w") as fh:
            fh.write(template)


if __name__ == "__main__":
    for season, letter in SEASON_LETTERS.items():
        make_mtg_frame(season, letter)

    make_pt_badge()
    make_mana_badge()
    make_mana_symbols()
    make_tap_symbol()


