import colorsys
from dataclasses import dataclass
from enum import Enum
import math


def percent_to_hex(p: float):
    return hex(round(p*255))[2:].rjust(2, '0')


def hsv_to_hex(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h/360, s, v)
    return f"#{percent_to_hex(r)}{percent_to_hex(g)}{percent_to_hex(b)}"


def hex_to_rgb(h: str):
    return tuple(int(h[i:i+2], 16) for i in range(1, 7, 2))


def rgb_to_hex(c):
    r, g, b = c
    return f"#{r:02x}{g:02x}{b:02x}"


def mix(n1, n2, percent: float):
    assert 0 <= percent
    assert percent <= 1

    return n1*percent + n2*(1-percent)


def mix_rgb_colors(c1, c2, percent: float):
    r1, g1, b1 = c1
    r2, g2, b2 = c2

    return round(mix(r1, r2, percent)), round(mix(g1, g2, percent)), round(mix(b1, b2, percent))


def mix_hex_colors(hex1: str, hex2: str, percent: float):
    return rgb_to_hex(mix_rgb_colors(hex_to_rgb(hex1), hex_to_rgb(hex2), percent))


def star_peaks_valleys(points, center, peak_radius, valley_radius, askew):
    peaks, valleys = [], []

    for i in range(points):
        peak_theta = math.pi*(2*i/points + 3/2 + (1/points if askew else 0))
        valley_theta = peak_theta + math.pi/points
        center_x, center_y = center

        peaks.append((
            center_x + round(peak_radius * math.cos(peak_theta)),
            center_y + round(peak_radius * math.sin(peak_theta)),
        ))

        valleys.append((
            center_x + round(valley_radius * math.cos(valley_theta)),
            center_y + round(valley_radius * math.sin(valley_theta))
        ))

    return peaks, valleys


def star_vertices(points, center, peak_radius, valley_radius, askew):
    peaks, valleys = star_peaks_valleys(points, center, peak_radius, valley_radius, askew)
    out = []
    for i in range(len(peaks)):
        out += peaks[i], valleys[i]
    return out


def flat_arm_valley_radius(points, peak_radius):
    return peak_radius * math.cos(2 * math.pi / points) / math.cos(math.pi / points)


def flat_armed_star_peaks_valleys(points, center, peak_radius, askew):
    return star_peaks_valleys(points, center, peak_radius, flat_arm_valley_radius(points, peak_radius), askew)


def flat_armed_star_vertices(points, center, peak_radius, askew):
    return star_vertices(points, center, peak_radius, flat_arm_valley_radius(points, peak_radius), askew)


def polygon_path(vertices):
    vertex_string = ""
    for i, (x, y) in enumerate(vertices):
        vertex_string += "M " if (i == 0) else "L "
        vertex_string += f"{x} {y} "

    return vertex_string + "Z"


def flower_control_points(center, peak, valley, curviness):
    center_x, center_y = center
    peak_x, peak_y = peak
    valley_x, valley_y = valley

    direction_vector = (
        (center_x + valley_x)/2 - peak_x,
        (center_y + valley_y)/2 - peak_y,
    )

    outer_control = (
        peak_x + round(direction_vector[0]*curviness),
        peak_y + round(direction_vector[1]*curviness),
    )

    inner_control = (
        valley_x - round(direction_vector[0]*curviness),
        valley_y - round(direction_vector[1]*curviness),
    )

    return outer_control, inner_control


def flower_path(peaks, valleys, center, curviness=1/6):
    vertex_string = f"M {peaks[0][0]} {peaks[0][1]} "

    for i in range(len(peaks)):
        source_peak, valley, dest_peak = peaks[i], valleys[i], peaks[(i+1) % len(peaks)]

        (control1_x, control1_y), (control2_x, control2_y) = flower_control_points(center, source_peak, valley, curviness)
        vertex_string += f"C {control1_x} {control1_y}, {control2_x} {control2_y}, {valley[0]} {valley[1]} "

        (control2_x, control2_y), (control1_x, control1_y) = flower_control_points(center, dest_peak, valley, curviness)
        vertex_string += f"C {control1_x} {control1_y}, {control2_x} {control2_y}, {dest_peak[0]} {dest_peak[1]} "

    return vertex_string + "Z"


def rectangle_path(x, y, width, height):
    return polygon_path([
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height),
    ])


def hexagon_path(x, y, side_length):
    short_side = side_length/2
    half_height = side_length*math.sqrt(3)/2

    return polygon_path([
        (x, y),
        (x + side_length, y),
        (x + side_length + short_side, y + half_height),
        (x + side_length, y + 2*half_height),
        (x, y + 2*half_height),
        (x - short_side, y + half_height),
    ])


def leaf_control(start_x, start_y, end_x, end_y):
    mid_x = (start_x + end_x)/2
    return f"C{mid_x},{start_y} {mid_x},{end_y} {end_x},{end_y}"


def leaf_path(x, y, width, height):
    points = [(x, y), (x + width, y - height), (x + 2*width, y), (x + width, y + height), (x, y)]

    out = f"M{x},{y}"
    for i in range(4):
        (start_x, start_y), (end_x, end_y) = points[i:i+2]
        out += " " + leaf_control(start_x, start_y, end_x, end_y)

    return out + "Z"


def tessellating_clover_paths(x, y, E, F, radius, curve_radius):
    """E + F < math.pi; F < math.pi/2; curve_radius << radius"""

    # This is missing some important constraint, but I couldn't figure out what it was lol

    G = 2*math.pi/3 - E
    H = math.pi/3 - F

    circumcircle_radius = radius/math.sin(E)
    s = circumcircle_radius*math.sin(math.pi/3)
    t = circumcircle_radius*math.sin(F)
    u = circumcircle_radius*math.sin(G)
    v = circumcircle_radius*math.sin(H)

    out = []
    for i in range(3):
        angle = i*2*math.pi/3 + 7*math.pi/6
        start_x, start_y = x + u*math.cos(angle), y + u*math.sin(angle)

        left_branching_angle = angle + math.pi/2 - E - F
        left_branch_x, left_branch_y = start_x + v*math.cos(left_branching_angle), start_y + v*math.sin(left_branching_angle)

        right_branching_angle = angle + E + F - math.pi/2
        right_branch_x, right_branch_y = start_x + v*math.cos(right_branching_angle), start_y + v*math.sin(right_branching_angle)

        out.append(
            f'M{start_x}, {start_y} '
            f'A{curve_radius} {curve_radius} 0 0 0 {left_branch_x} {left_branch_y}'
            f'A{curve_radius} {curve_radius} 0 0 1 {start_x} {start_y}'
            f'A{curve_radius} {curve_radius} 0 0 1 {right_branch_x} {right_branch_y}'
            f'A{curve_radius} {curve_radius} 0 0 0 {start_x} {start_y}'
            'Z'
        )

    return out


class Color(Enum):
    BLACK = "#000000"
    WHITE = "#ffffff"
    INDIGO = "#003355"
    BP = "#3e008f"
    GOLD = "#ffbb00"
    MEDIUM_BLUE = "#114488"
    FOREST_GREEN = "#005500"
    PURPLE = "#330055"
    RED = "#661111"
    CREAM = "#ddddcc"

    SPRING_GREEN = "#478547"
    SUMMER_GOLD = "#caa02b"
    AUTUMN_RED = "#994936"
    WINTER_BLUE = "#343445"

    BLUE_GRAY = "#202027"


@dataclass
class Rotation:
    degrees: int
    cx: int
    cy: int


def path_template(vertex_string, color):
    return f'<path d="{vertex_string}" fill="{color}"/>'


def rectangle_template(x: int, y: int, width: int, height: int, color: str, radius: int = 0, rotation: Rotation | None = None):
    fields = {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "rx": radius,
        "fill": color,
    }
    if rotation:
        fields["transform"] = f"rotate({rotation.degrees}, {rotation.cx}, {rotation.cy})"

    param_strings = []
    for key, value in fields.items():
        param_strings.append(f"{key}=\"{value}\"")

    return f'<rect {" ".join(param_strings)}/>'


def circle_template(cx, cy, radius, color):
    return f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{color}"/>'


def crescent_moon_template(cx: int, cy: int, radius: int, color: str, rotation_degrees: int):
    start_radians = -math.pi*.4 - rotation_degrees*math.pi/180
    end_radians =    math.pi*.4 - rotation_degrees*math.pi/180

    arc_start_x, arc_start_y = round(cx + radius*math.cos(start_radians)), round(cy + radius*math.sin(start_radians))
    arc_end_x, arc_end_y = round(cx + radius*math.cos(end_radians)), round(cy + radius*math.sin(end_radians))

    return f'<path d="M{arc_start_x} {arc_start_y}A{radius} {radius} 0 1 0 {arc_end_x} {arc_end_y} {radius} {radius} 0 0 1 {arc_start_x} {arc_start_y}z" fill="{color}"/>'


def svg_template(width, height, paths, background_color=None):
    if background_color:
        paths = [f'<rect width="100%" height="100%" fill="{background_color}"/>'] + paths
    return f'<svg height="{height}" width="{width}">\n' + "\n".join(paths) + '\n</svg>'
