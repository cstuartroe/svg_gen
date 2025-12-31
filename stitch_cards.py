import os
import re
from PIL import Image
from tqdm import tqdm

from season_cards import SIDE_LENGTH

WIDTH = 10
HEIGHT = 12
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

for i in tqdm(range(WIDTH)):
    for j in range(HEIGHT):
        card_filename = card_fronts[i + WIDTH*j]
        card_image = Image.open(os.path.join(PNG_DIR, card_filename))

        left = i * SIDE_LENGTH
        top = j * SIDE_LENGTH

        for x in range(SIDE_LENGTH):
            for y in range(SIDE_LENGTH):
                stitched_image.putpixel(
                    (left+x, top+y),
                    card_image.getpixel((x, y))
                )

stitched_image.save(os.path.join(PNG_DIR, "stitched_fronts.png"))
