from PIL import Image, ImageDraw, ImageFont

Xiaolai = ImageFont.truetype("font/XiaolaiSC-Regular.ttf", 600)


def jaobon_logo():
    img = Image.new('RGB', (640, 640), color='#8866cc')
    draw = ImageDraw.Draw(img)
    draw.text(
        (320, 320),
        text="脚",
        fill="#ffffff",
        font=Xiaolai,
        anchor="mm",
    )
    img.save("pngs/jaobon_logo.png")


ALIA_BOX = [
    ". .   . .    ",
    "      . .    ",
    "... . . . ...",
    ". . . . . .  ",
    "....... .....",
    "             ",
    "   . .       ",
]

ALIA_COLORS = ["#00ffff", "#ff00ff", "#000000"]


def alia():
    box_height = len(ALIA_BOX) - 1
    box_width = len(ALIA_BOX[0]) + 1
    pixel_size = 64
    offset = 7
    width, height = 15, 36

    img = Image.new('RGB', (width*box_width*pixel_size, height*box_height*pixel_size), color='#ffffff')
    draw = ImageDraw.Draw(img)

    for i in range(width + 1):
        for j in range(-1, height):
            color = ALIA_COLORS[(i + (j % 2)) % 3]
            base_x = i*box_width + 1
            if j % 2 == 1:
                base_x -= offset
            base_y = j*box_height + 1

            for dy, row in enumerate(ALIA_BOX):
                for dx, c in enumerate(row):
                    if c == ".":
                        x, y = base_x + dx, base_y + dy
                        draw.rectangle(((x*pixel_size, y*pixel_size), ((x+1)*pixel_size - 1, (y+1)*pixel_size - 1)), fill=color, width=0)

    img.save("pngs/alia.png")


if __name__ == "__main__":
    jaobon_logo()
    alia()
