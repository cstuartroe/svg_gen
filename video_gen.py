import math
from tqdm import tqdm
from pydub import AudioSegment
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2


SyneMono = ImageFont.truetype("font/SyneMono-Regular.ttf", 200)
KodeMono = ImageFont.truetype("font/KodeMono-VariableFont_wght.ttf", 200)
BungeeHairline = ImageFont.truetype("font/BungeeHairline-Regular.ttf", 200)

Keystroke = AudioSegment.from_file("audio/typewriter.wav")
Keyboard = AudioSegment.from_file("audio/mechanical-keyboard.mp3")
Click = AudioSegment.from_file("audio/click-button.mp3")
Logo = AudioSegment.from_file("audio/futuristic-logo.mp3")
Woosh = AudioSegment.from_file("audio/ethereal-woosh.wav")

SAMPLE_RATE = 44100


def chroma_promo():
    SIDE_LENGTH = 1000
    FRAMERATE = 50

    videodims = (SIDE_LENGTH-1,SIDE_LENGTH-1)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter("videos/chroma_promo.mp4", fourcc, FRAMERATE, videodims)
    audio = AudioSegment.silent(10000, frame_rate=SAMPLE_RATE)
    img = Image.new('RGB', videodims, color = 'black')

    total_frames = 0

    def write_image(im, frames=1):
        nonlocal total_frames
        imtemp = im.copy()
        for _ in range(frames):
            video.write(cv2.cvtColor(np.array(imtemp), cv2.COLOR_RGB2BGR))
        total_frames += frames

    write_image(img, 50)

    draw = ImageDraw.Draw(img)

    text_lines = ["DVLV 9", "CHROMA"]
    horizontal_spacing = 120
    vertical_spacing = 200

    for i, line in enumerate(text_lines):
        # line_start_frames = total_frames

        for j, c in enumerate(line):
            audio = audio.overlay(Click, total_frames * 1000 / FRAMERATE)

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

        # offset = [10, 80][i]
        # audio = audio.overlay(
        #     Keyboard.get_sample_slice(
        #         round(SAMPLE_RATE*offset/FRAMERATE),
        #         round(SAMPLE_RATE*(offset + total_frames - line_start_frames)/FRAMERATE),
        #     ),
        #     total_frames * 1000 / FRAMERATE,
        # )

        write_image(img, 50)

    audio = audio.overlay(Logo, total_frames*1000/FRAMERATE - 700)

    colors = [
        ((255, 0, 0), (63, 0, 0)),
        ((255, 127, 0), (63, 63, 0)),
        ((255, 0, 255), (0, 0, 127)),
        ((191, 255, 0), (63, 0, 0)),
        ((0, 255, 0), (63, 63, 0)),
        ((0, 127, 255), (0, 0, 127)),
    ]
    light_distance_decay = 60

    beat_length = 42.5
    num_beats = 4
    frame_resolution = 1

    for frame in tqdm(range(0, round(beat_length * num_beats), frame_resolution)):
        imtemp = img.copy()

        for i, color in enumerate(colors):
            kx = (2*(i%3) + 1)*SIDE_LENGTH/6
            ky = 0 if i < 3 else SIDE_LENGTH - 2

            kernel_brightness_fraction = .5 + 16*(
                (((frame % beat_length) - (beat_length / 2))/beat_length)**4
            )

            for x in range(SIDE_LENGTH-1):
                for y in range(SIDE_LENGTH-1):
                    r, g, b = imtemp.getpixel((x, y))
                    distance = math.sqrt((x - kx)**2 + (y - ky)**2)
                    lower_brightness_fraction = kernel_brightness_fraction * (2**(-distance/light_distance_decay))
                    higher_brightness_fraction = (2**(-max(0.0, distance - 120)/(2*light_distance_decay)))

                    dr, dg, db = color[0]
                    r = min(r + round(dr*lower_brightness_fraction), 255)
                    g = min(g + round(dg*lower_brightness_fraction), 255)
                    b = min(b + round(db*lower_brightness_fraction), 255)

                    dr, dg, db = color[1]
                    r = min(r + round(dr * higher_brightness_fraction), 255)
                    g = min(g + round(dg * higher_brightness_fraction), 255)
                    b = min(b + round(db * higher_brightness_fraction), 255)

                    imtemp.putpixel((x, y), (r, g, b))

        write_image(imtemp, frame_resolution)

    date_img = Image.new('RGB', videodims, color='black')
    date_draw = ImageDraw.Draw(date_img)
    date_line = "AUG 17"
    for j, c in enumerate(date_line):
        x = SIDE_LENGTH / 2 + (-len(date_line) + 1 + 2 * j) * horizontal_spacing / 2
        y = SIDE_LENGTH / 2

        date_draw.text(
            (x, y),
            text=c,
            fill="#ffffff",
            font=BungeeHairline,
            anchor="mm",
        )
    write_image(date_img, 130)

    video.release()
    audio.export("audio/chroma_promo.wav")


if __name__ == "__main__":
    chroma_promo()
