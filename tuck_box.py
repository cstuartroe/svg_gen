import cairosvg
from PIL import Image, ImageFont, ImageDraw
from utils import Color, svg_template, rectangle_template, path_template, polygon_path
from season_cards import sun_path, moon_path, star_path, earth_path, solar_system_paths, NUMBERS, HALF, EM

MULTIPLE = 10

WIDTH = 650*MULTIPLE
HEIGHT = 498*MULTIPLE

LEFT_OFFSET = round(48.5*MULTIPLE)
TOP_OFFSET = 155*MULTIPLE
BOX_WIDTH = round(190.5*MULTIPLE)
BOX_HEIGHT = round(188.5*MULTIPLE)
BOX_THICKNESS = round(106.5*MULTIPLE)

CELESTIAL_RADIUS = BOX_THICKNESS/3

FONT_PATH = "../celestial-cards/static/"

PNG_PATH = "pngs/season_cards/tuck_box.png"
TEMPLATE_PATH = "tuck_box_template.png"
TMP_SVG_PATH = "temp.svg"
TMP_PNG_PATH = "temp.png"

Domine = ImageFont.truetype("font/Domine-VariableFont_wght.ttf", 6*MULTIPLE)
OpenSans = ImageFont.truetype("font/OpenSans-VariableFont_wdth,wght.ttf", 12*MULTIPLE)

BACK_TEXT = """
Celestial cards are playing cards
with three-dimensional markings
"""

if __name__ == "__main__":
    box_template = Image.open(TEMPLATE_PATH)

    box_overlay = Image.new("RGBA", (WIDTH, HEIGHT), Color.BLACK.value)

    draw = ImageDraw.Draw(box_overlay, "RGBA")

    def draw_svg_paths(*paths):
        with open(TMP_SVG_PATH, "w") as fh:
            fh.write(
                svg_template(WIDTH, HEIGHT, paths)
            )

        cairosvg.svg2png(url=TMP_SVG_PATH, write_to=TMP_PNG_PATH)

        shape_img = Image.open(TMP_PNG_PATH)
        box_overlay.paste(shape_img, (0, 0), shape_img)

    ss_cx = LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + BOX_WIDTH/2
    ss_cy = TOP_OFFSET + BOX_HEIGHT/2



    draw_svg_paths(
        rectangle_template(LEFT_OFFSET + BOX_WIDTH, 0, BOX_THICKNESS, HEIGHT, Color.SPRING_GREEN.value),
        rectangle_template(0, TOP_OFFSET + BOX_HEIGHT, LEFT_OFFSET + BOX_WIDTH + 2*MULTIPLE, HEIGHT - TOP_OFFSET - BOX_HEIGHT, Color.WINTER_BLUE.value),
        rectangle_template(0, 0, LEFT_OFFSET + BOX_WIDTH, TOP_OFFSET + BOX_HEIGHT, Color.CREAM.value),
        rectangle_template(LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + BOX_WIDTH, 0, WIDTH - LEFT_OFFSET - BOX_WIDTH - BOX_THICKNESS - BOX_WIDTH, HEIGHT, Color.AUTUMN_RED.value),
        rectangle_template(LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS - 2*MULTIPLE, 0, BOX_WIDTH + 4*MULTIPLE, TOP_OFFSET - 1*MULTIPLE, Color.SUMMER_GOLD.value),

        *solar_system_paths(ss_cx, ss_cy, .63),

        star_path(LEFT_OFFSET + BOX_WIDTH/2, TOP_OFFSET + BOX_HEIGHT + BOX_THICKNESS/2, CELESTIAL_RADIUS, Color.CREAM),
        earth_path(LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS/2, TOP_OFFSET + BOX_HEIGHT/2, CELESTIAL_RADIUS, Color.CREAM),
        sun_path(LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + BOX_WIDTH/2, TOP_OFFSET - BOX_THICKNESS/2, CELESTIAL_RADIUS, Color.BLACK),
        moon_path(LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + BOX_WIDTH + BOX_THICKNESS/2, TOP_OFFSET + BOX_HEIGHT/2, CELESTIAL_RADIUS, Color.BLACK),

        # triangles in the bleed zones
        path_template(
                polygon_path(
                [
                    (0, TOP_OFFSET + BOX_HEIGHT + 45*MULTIPLE),
                    (0, TOP_OFFSET + BOX_HEIGHT),
                    (LEFT_OFFSET, TOP_OFFSET + BOX_HEIGHT),
                ],
            ),
            Color.CREAM.value,
        ),
        path_template(
            polygon_path(
                [
                    (LEFT_OFFSET + BOX_WIDTH, TOP_OFFSET),
                    (LEFT_OFFSET + BOX_WIDTH, TOP_OFFSET - 50*MULTIPLE),
                    (LEFT_OFFSET + BOX_WIDTH - 50*MULTIPLE, TOP_OFFSET - 50*MULTIPLE),
                ],
            ),
            Color.SPRING_GREEN.value,
        ),
        path_template(
            polygon_path(
                [
                    (LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS, TOP_OFFSET + BOX_HEIGHT),
                    (LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS, TOP_OFFSET + BOX_HEIGHT + 50*MULTIPLE),
                    (LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + 50*MULTIPLE, TOP_OFFSET + BOX_HEIGHT + 50*MULTIPLE),
                ],
            ),
            Color.SPRING_GREEN.value,
        ),
        path_template(
            polygon_path(
                [
                    (LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + BOX_WIDTH, TOP_OFFSET + BOX_HEIGHT),
                    (LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + BOX_WIDTH, TOP_OFFSET + BOX_HEIGHT + 50*MULTIPLE),
                    (LEFT_OFFSET + BOX_WIDTH + BOX_THICKNESS + BOX_WIDTH - 50*MULTIPLE, TOP_OFFSET + BOX_HEIGHT + 50*MULTIPLE),
                ],
            ),
            Color.AUTUMN_RED.value,
        ),
    )

    cover_cx = LEFT_OFFSET + BOX_WIDTH/2
    line_spacing = 3*MULTIPLE

    draw.text(
        xy=(
            cover_cx,
            TOP_OFFSET + BOX_HEIGHT*.17,
        ),
        text=BACK_TEXT,
        align="center",
        fill=Color.BLACK.value,
        font=Domine,
        anchor='mm',
        spacing=line_spacing,
    )

    spacing = 28*MULTIPLE
    card_face_scale = .6*MULTIPLE/EM

    for i, (name, shape) in enumerate([
        ('Planet', earth_path),
        ('Sun', sun_path),
        ('Moon', moon_path),
        ('Star', star_path),
    ]):
        cx = cover_cx + (i - 1.5) * spacing
        draw_svg_paths(
            shape(cx, TOP_OFFSET + BOX_HEIGHT * .29, 7*MULTIPLE, Color.BLACK),
        )
        draw.text(
            xy=(
                cx,
                TOP_OFFSET + BOX_HEIGHT * .36,
            ),
            text=name,
            align="center",
            fill=Color.BLACK.value,
            font=Domine,
            anchor="mm",
        )

    for i, number in enumerate(["One", "Two", "Three", "Four", "Five"]):
        cx = cover_cx + (i-2)*spacing
        ni = NUMBERS[i]
        cy = TOP_OFFSET + BOX_HEIGHT*.47
        draw_svg_paths(*[
            star_path(cx + (x - HALF)*card_face_scale, cy + (y - HALF)*card_face_scale, ni.radius*card_face_scale, Color.BLACK)
            for x, y in ni.centers
        ])
        draw.text(
            xy=(
                cx,
                TOP_OFFSET + BOX_HEIGHT*.555,
            ),
            text=number,
            align="center",
            fill=Color.BLACK.value,
            font=Domine,
            anchor="mm",
        )

    for i, (color, words) in enumerate([
        (Color.CREAM, ["Air", "Void", "Beltane", "Samhain"]),
        (Color.SPRING_GREEN, ["Wood", "Jupiter", "Spring"]),
        (Color.SUMMER_GOLD, ["Fire", "Venus", "Summer"]),
        (Color.AUTUMN_RED, ["Metal", "Mars", "Autumn"]),
        (Color.WINTER_BLUE, ["Water", "Mercury", "Winter"]),
        (Color.BLACK, ["Earth", "Saturn", "Imbolc", "Lunasa"]),
    ]):
        cx = cover_cx + (i - 2.5) * spacing
        side_length = 12*MULTIPLE
        border_width = .5*MULTIPLE
        square_top = TOP_OFFSET + BOX_HEIGHT * .62
        draw_svg_paths(
            rectangle_template(
                cx - side_length/2 - border_width,
                square_top - border_width,
                side_length + 2*border_width,
                side_length + 2*border_width,
                Color.BLACK.value,
                radius=2*MULTIPLE,
            ),
            rectangle_template(
                cx - side_length/2,
                square_top,
                side_length,
                side_length,
                color.value,
                radius=2*MULTIPLE,
            )
        )

        for j, word in enumerate(words):
            draw.text(
                xy=(
                    cx,
                    TOP_OFFSET + BOX_HEIGHT * (.72 + .045*j),
                ),
                text=word,
                align="center",
                fill=Color.BLACK.value,
                font=Domine,
                anchor="mm",
            )

    draw.text(
        xy=(
            cover_cx,
            TOP_OFFSET + BOX_HEIGHT * .94,
        ),
        text="For games and more info visit\ncelestial-cards.conorstuartroe.com",
        align="center",
        fill=Color.BLACK.value,
        font=Domine,
        anchor='mm',
        spacing=line_spacing,
    )

    box_template = box_template.resize((box_template.width*MULTIPLE, box_template.height*MULTIPLE))
    Image.Image.paste(box_overlay, box_template, (0, 0), box_template)

    box_overlay.save(PNG_PATH)
