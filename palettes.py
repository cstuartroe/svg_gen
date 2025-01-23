from utils import *


PALETTE_SQUARE_SIZE = 100


def palette(hues: list[float], saturations: list[float], lightnesses: list[float], name: str) -> list[str]:
    out = []
    rects = []
    for x, h in enumerate(hues):
        for i, s in enumerate(saturations):
            for j, l in enumerate(lightnesses):
                hex_color = hsl_to_hex(h, s, l)
                if hex_color not in out:
                    out.append(hex_color)

                y = i*len(lightnesses) + j
                rects.append(rectangle_template(
                    x*PALETTE_SQUARE_SIZE,
                    y*PALETTE_SQUARE_SIZE,
                    PALETTE_SQUARE_SIZE,
                    PALETTE_SQUARE_SIZE,
                    hex_color,
                ))

    with open(f"images/palettes/{name}.svg", "w") as fh:
        fh.write(svg_template(
            PALETTE_SQUARE_SIZE*len(hues),
            PALETTE_SQUARE_SIZE*len(saturations)*len(lightnesses),
            rects,
        ))

    return out


if __name__ == "__main__":
    print(palette(
        [.45, .55, .65, .75, .85, .95],
        [.7],
        [.2, .45, .7],
        "Alia's Pal",
    ))
    print(palette(
        [.45, .55, .65, .75, .85, .95],
        [.6],
        [.25, .5, .75],
        "Alia's Pal 2",
    ))
