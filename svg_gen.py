from flower_utils import *


def path_template(vertex_string, color):
    return f'<path d="{vertex_string}" fill="{color}"/>'


def svg_template(height, width, *paths):
    return f'<svg height="{height}" width="{width}">\n' + "\n".join(paths) + '\n</svg>'


def create_rasta_flower():
    width, height = 1000, 1000
    center = width//2, height//2

    stars = list(map(lambda x: path_template(
        flower_path(
            *star_peaks_valleys(
                6,
                center,
                x[0],
                flat_arm_valley_radius(6, x[0]),
                False,
            ),
            center,
            curviness=1/3
        ),
        x[1]
    ), [
        (500, "black"),
        (400, "#007f00"),
        (300, "#ffff00"),
        (200, "#7f0000"),
    ]))

    with open("images/rasta_star.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                *stars,
            )
        )


def create_trippy_lotus():
    width, height = 1000, 1000
    center = width // 2, height // 2

    stars = list(map(lambda x: path_template(
        flower_path(
            *star_peaks_valleys(
                8,
                center,
                x[1][0],
                flat_arm_valley_radius(8, x[1][0]),
                x[0] % 2 == 1,
            ),
            center,
            curviness=1/4
        ),
        x[1][1]
    ), enumerate([
        (500, "black"),
        (383, "#007f00"),
        (292, "#ffff00"),
        (220, "#7f0000"),
        (160, "#3b0082"),
    ])))

    with open("images/trippy_lotus.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                *stars,
            )
        )


def create_black_lotus():
    width, height = 1000, 1000
    center = width // 2, height // 2

    path = path_template(
        flower_path(
            *star_peaks_valleys(
                8,
                center,
                500,
                flat_arm_valley_radius(8, 500),
                False,
            ),
            center,
        ),
        "black",
    )

    with open("images/black_lotus.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                path,
            )
        )


def create_rub_el_hizb_black_solid():
    width, height = 1000, 1000
    center = width//2, height//2
    radius = 500

    path = path_template(
        polygon_path(
            star_vertices(
                8,
                center,
                radius,
                flat_arm_valley_radius(8, radius),
                False,
            ),
        ),
        "black",
    )

    with open("images/rub_el_hizb_solid.svg", "w") as fh:
        fh.write(
            svg_template(
                width,
                height,
                path,
            )
        )


if __name__ == "__main__":
    create_rasta_flower()
    create_trippy_lotus()
    create_black_lotus()
    create_rub_el_hizb_black_solid()
