import os
import re
from PIL import Image
from tqdm import tqdm

from season_cards import SIDE_LENGTH

WIDTH = 10
HEIGHT = 7
PNG_DIR = 'pngs/season_cards/'

card_fronts = sorted([
    filename
    for filename in os.listdir(PNG_DIR)
    if re.match(r"\d{3}", filename)
])

stitched_image = Image.new(
    mode="RGB",
    size=(WIDTH*SIDE_LENGTH, HEIGHT*SIDE_LENGTH),
)

for suffix, offset in [('_1', 0), ('_2', 60)]:
    for i in tqdm(range(WIDTH)):
        for j in range(6):
            card_filename = card_fronts[offset + i + WIDTH*j]
            card_image = Image.open(os.path.join(PNG_DIR, card_filename))

            left = i * SIDE_LENGTH
            top = j * SIDE_LENGTH

            for x in range(SIDE_LENGTH):
                for y in range(SIDE_LENGTH):
                    stitched_image.putpixel(
                        (left+x, top+y),
                        card_image.getpixel((x, y))
                    )

    dummy_front_filename = "dummy_front.png"
    dummy_front_image = Image.open(os.path.join(PNG_DIR, dummy_front_filename))

    left = 9 * SIDE_LENGTH
    top = 6 * SIDE_LENGTH

    for x in range(SIDE_LENGTH):
        for y in range(SIDE_LENGTH):
            stitched_image.putpixel(
                (left + x, top + y),
                dummy_front_image.getpixel((x, y))
            )
    
    stitched_image.save(os.path.join(PNG_DIR, f"stitched_fronts{suffix}.png"))
