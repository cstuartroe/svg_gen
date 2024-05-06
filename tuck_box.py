import cairosvg
from PIL import Image, ImageFont, ImageDraw
from utils import Color, svg_template
from season_cards import sun_path, moon_path, star_path

WIDTH = 650
HEIGHT = 433
LEFT_OFFSET = 48
TOP_OFFSET = 97
BOX_WIDTH = 239
BOX_THICKNESS = 59

FONT_PATH = "../celestial-cards/static/"

PNG_PATH = "pngs/season_cards/tuck_box.png"
TEMPLATE_PATH = "tuck_box_template.png"
TMP_SVG_PATH = "temp.svg"
TMP_PNG_PATH = "temp.png"

Domine = ImageFont.truetype("font/Domine-VariableFont_wght.ttf", 30)
OpenSans = ImageFont.truetype("font/OpenSans-VariableFont_wdth,wght.ttf", 12)

SEASON_SIDES: list[tuple[tuple[int, int, int, int], Color, int]] = [
    (
        (
            LEFT_OFFSET,
            TOP_OFFSET + BOX_WIDTH,
            BOX_WIDTH,
            BOX_THICKNESS,
        ),
        Color.AUTUMN_RED,
        0,
    ),
    (
        (
            LEFT_OFFSET + BOX_WIDTH,
            TOP_OFFSET,
            BOX_THICKNESS,
            BOX_WIDTH,
        ),
        Color.WINTER_BLUE,
        90,
    ),
    (
        (
            LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS,
            TOP_OFFSET - BOX_THICKNESS,
            BOX_WIDTH,
            BOX_THICKNESS,
        ),
        Color.SPRING_GREEN,
        0,
    ),
    (
        (
            LEFT_OFFSET + 2 * BOX_WIDTH + BOX_THICKNESS,
            TOP_OFFSET,
            BOX_THICKNESS,
            BOX_WIDTH,
        ),
        Color.SUMMER_GOLD,
        270,
    ),
]

BACK_TEXT = """
Celestial cards are a new and
more versatile variety of
playing cards. See more
information and game rules at:
celestial-cards.conorstuartroe.com
"""

if __name__ == "__main__":
    box_template = Image.open(TEMPLATE_PATH)

    box_overlay = Image.new("RGBA", (WIDTH, HEIGHT), Color.BLUE_GRAY.value)

    draw = ImageDraw.Draw(box_overlay, "RGBA")

    def draw_svg_path(box, paths):
        x, y, width, height = box

        with open(TMP_SVG_PATH, "w") as fh:
            fh.write(
                svg_template(width, height, paths)
            )

        cairosvg.svg2png(url=TMP_SVG_PATH, write_to=TMP_PNG_PATH)

        shape_img = Image.open(TMP_PNG_PATH)
        box_overlay.paste(shape_img, (x, y), shape_img)

    def draw_celestial_body(cx, cy, radius, f):
        x = cx-radius
        y = cy-radius

        draw_svg_path(
            (x, y, radius*2, radius*2),
            [f(radius, radius, radius)],
        )

    for dim, color, rot in SEASON_SIDES:
        x, y, width, height = dim
        box = (x, y, x+width, y+height)

        txt = Image.new("RGBA", (BOX_WIDTH, BOX_THICKNESS), color.value)
        txt_draw = ImageDraw.Draw(txt)
        txt_draw.text(
            xy=(BOX_WIDTH/2, BOX_THICKNESS/2),
            text=color.name.split("_")[0].lower(),
            fill=Color.CREAM.value,
            font=Domine,
            anchor='mm',
        )
        w = txt.rotate(rot, expand=1)

        box_overlay.paste(w, box, w)

    draw_celestial_body(
        LEFT_OFFSET+BOX_WIDTH//2,
        TOP_OFFSET+3*BOX_WIDTH//4,
        30,
        sun_path,
    )

    for offset, shape in enumerate([sun_path, moon_path, star_path]):
        cx = LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + BOX_WIDTH*(offset+1)//4
        cy = TOP_OFFSET + BOX_WIDTH//3

        draw_celestial_body(cx, cy, 15, shape)
        draw.text(
            xy=(cx, cy + 20),
            text=shape.__name__.split('_')[0],
            fill=Color.CREAM.value,
            font=OpenSans,
            anchor='mm',
        )

    draw.text(
        xy=(LEFT_OFFSET+BOX_WIDTH/2, TOP_OFFSET+BOX_WIDTH/3),
        text="Celestial\nCards",
        align="center",
        fill=Color.CREAM.value,
        font=Domine,
        anchor='mm',
    )

    draw.text(
        xy=(
            LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + BOX_WIDTH//2,
            TOP_OFFSET + 3*BOX_WIDTH//4,
        ),
        text=BACK_TEXT,
        align="center",
        fill=Color.CREAM.value,
        font=OpenSans,
        anchor='mm',
    )

    # Image.Image.paste(box_template, box_overlay, (0, 0), box_overlay)
    box_overlay.save(PNG_PATH)
