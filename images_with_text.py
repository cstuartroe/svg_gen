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


if __name__ == "__main__":
    jaobon_logo()
