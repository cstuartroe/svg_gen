from dataclasses import dataclass
import math
from enum import Enum


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

    JAOBON_PURPLE = "#8866cc"
    JAOBON_GREEN = "#66cc88"
    JAOBON_BROWN = "#cc8866"


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


def svg_template(width, height, paths, background_color=None):
    if background_color:
        paths = [f'<rect width="100%" height="100%" fill="{background_color}"/>'] + paths
    return f'<svg height="{height}" width="{width}">\n' + "\n".join(paths) + '\n</svg>'
