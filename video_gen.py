import math
from tqdm import tqdm
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2


MajorMono = ImageFont.truetype("font/MajorMonoDisplay-Regular.ttf", 30)
BungeeHairline = ImageFont.truetype("font/BungeeHairline-Regular.ttf", 200)


def chroma_promo():
    SIDE_LENGTH = 1000

    videodims = (SIDE_LENGTH-1,SIDE_LENGTH-1)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter("videos/chroma_promo.mp4", fourcc, 60, videodims)
    img = Image.new('RGB', videodims, color = 'black')

    def write_image(im, frames=1):
        imtemp = im.copy()
        for _ in range(frames):
            video.write(cv2.cvtColor(np.array(imtemp), cv2.COLOR_RGB2BGR))

    write_image(img, 60)

    draw = ImageDraw.Draw(img)

    text_lines = ["DVLV 9", "CHROMA"]
    horizontal_spacing = 120
    vertical_spacing = 200

    for i, line in enumerate(text_lines):
        for j, c in enumerate(line):
            x = SIDE_LENGTH/2 + (-len(line) + 1 + 2*j)*horizontal_spacing/2
            y = SIDE_LENGTH/2 + (-len(text_lines) + 1 + 2*i)*vertical_spacing/2

            draw.text(
                (x, y),
                text=c,
                fill="#ffffff",
                font=BungeeHairline,
                anchor="mm",
            )

            write_image(img, 3)

        write_image(img, 60)

    colors = (
        (255, 0, 0),
        (255, 127, 0),
        (255, 0, 255),
        (255, 255, 0),
        (0, 255, 0),
        (0, 127, 255),
    )
    light_distance_decay = 60
    light_delay = 3
    light_time_increase = .005
    light_starting_proportion = .3
    frame_resolution = 1

    for frame in tqdm(range(0, 300, frame_resolution)):
        imtemp = img.copy()

        for i, color in enumerate(colors):
            kx = (2*(i%3) + 1)*SIDE_LENGTH/6
            ky = 0 if i < 3 else SIDE_LENGTH - 2

            frames_from_switch_on = frame - light_delay*i
            if frames_from_switch_on > 0:
                kernel_brightness_fraction = (
                    light_starting_proportion + (light_time_increase * frames_from_switch_on)
                )
            else:
                kernel_brightness_fraction = 0

            for x in range(SIDE_LENGTH-1):
                for y in range(SIDE_LENGTH-1):
                    r, g, b = imtemp.getpixel((x, y))
                    distance = math.sqrt((x - kx)**2 + (y - ky)**2)
                    brightness_fraction = kernel_brightness_fraction * (2**(-distance/light_distance_decay))

                    r += round(color[0]*brightness_fraction)
                    g += round(color[1]*brightness_fraction)
                    b += round(color[2]*brightness_fraction)
                    imtemp.putpixel((x, y), (r, g, b))

        write_image(imtemp, frame_resolution)

    video.release()


if __name__ == "__main__":
    chroma_promo()
