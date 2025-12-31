import colorsys
from dataclasses import dataclass
from enum import Enum
import math


def percent_to_hex(p: float):
    return hex(round(p*255))[2:].rjust(2, '0')


def hsl_to_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"#{percent_to_hex(r)}{percent_to_hex(g)}{percent_to_hex(b)}"


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


class CustomBasis:
    # transforms coordinates using a custom pair of basis vectors
    # the origin is (x1, y1)
    # the x basis vector (self.basis) is (x2, y2) - (x1, y1)
    # the y basis vector is the x basis vector rotated 90 degrees counterclockwise
    def __init__(self, x1, y1, x2, y2):
        self.ox = x1
        self.oy = y1
        self.basis = x2 - x1, y2 - y1

    def convert(self, x, y):
        return self.ox + x*self.basis[0] - y*self.basis[1], self.oy + x*self.basis[1] + y*self.basis[0]


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


def polygon_path(vertices, close=True):
    vertex_string = ""
    for i, (x, y) in enumerate(vertices):
        vertex_string += "M " if (i == 0) else "L "
        vertex_string += f"{x} {y} "

    if close:
        vertex_string += "Z"

    return vertex_string


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


# TODO: deprecate
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


def centered_hexagon_path(cx, cy, side_length, vert=False):
    points = []
    for i in range(6):
        angle = i*math.pi/3
        if vert:
            angle += math.pi/6

        points.append((cx + side_length*math.cos(angle), cy + side_length*math.sin(angle)))
    return polygon_path(points)


def cube_paths(cx, cy, side_length):
    out = []

    out.append(centered_hexagon_path(cx, cy, side_length, vert=True))

    for i in range(3):
        angle = (4*i - 1)*math.pi/6
        outer_point = cx + side_length * math.cos(angle), cy + side_length * math.sin(angle)
        basis = CustomBasis(cx, cy, *outer_point)

        points = [basis.convert(*p) for p in [(0, 0), (.75, 0)]]
        out.append(polygon_path(points, close=False))

    return out


def leaf_paths(x, y, side_length):
    half_height = side_length*math.sqrt(3)/2
    cx, cy = x + side_length/2, y + half_height

    out = []

    for i in range(6):
        points = []

        corner_angle = i * math.pi / 3
        corner_point = cx + side_length * math.cos(corner_angle), cy + side_length * math.sin(corner_angle)

        edge_angle = i * math.pi / 3 + math.pi / 6
        leading_edge_point = cx + half_height * math.cos(edge_angle), cy + half_height * math.sin(edge_angle)

        b1 = CustomBasis(cx, cy, *leading_edge_point)
        for point in [
            (0, 0),
            (.2, -.03), (.4, .06), (.6, -.09), (.8, .12),
            (1, 0),
        ]:
            points.append(b1.convert(*point))
        b2 = CustomBasis(*leading_edge_point, *corner_point)
        for point in [(.5, -.1), (1, 0)]:
            points.append(b2.convert(*point))
        # b3 = CustomBasis(*corner_point, cx, cy)
        # for point in [(.6, 0)]:
        #     points.append(b3.convert(*point))

        out.append(polygon_path(points, close=False))

    return out


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


def uniform_spiral_path(cx, cy, width, offsetr, totalr, jump, num_sections):
    start_point = (
        cx + width*math.cos(offsetr),
        cy + width*math.sin(offsetr),
    )
    out = f"M{start_point[0]}, {start_point[1]}"

    for i in range(num_sections):
        fraction = (i+1)/num_sections
        radius = jump + (width-jump)*(1-fraction)

        point = (
            cx + radius*math.cos(offsetr - fraction*totalr),
            cy + radius*math.sin(offsetr - fraction*totalr),
        )

        curve_radius = jump + (width-jump)*(1-(2*i+1)/(2*num_sections))
        out += f'A {curve_radius} {curve_radius} 0 0 0 {point[0]} {point[1]}'

    out += f"L{cx}, {cy}"
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
    SUMMER_GOLD = "#dbb448"
    AUTUMN_RED = "#994936"
    WINTER_BLUE = "#363659"

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


def crescent_moon_template(cx: int, cy: int, radius: int, color: str, rotation: float, percent: float):
    start_radians = rotation - math.pi/2
    end_radians = rotation + math.pi/2

    arc_start_x, arc_start_y = round(cx + radius*math.cos(start_radians)), round(cy + radius*math.sin(start_radians))
    arc_end_x, arc_end_y = round(cx + radius*math.cos(end_radians)), round(cy + radius*math.sin(end_radians))

    if percent < 0:
        raise ValueError
    if percent == 0:
        return ""
    if percent == .5:
        return f'<path d="M{arc_start_x} {arc_start_y}A{radius} {radius} 0 1 0 {arc_end_x} {arc_end_y} z" fill="{color}"/>'
    elif percent < .5:
        d = 1 - 2*percent
        inner_radius = radius*(d**2 + 1)/(2*d)

        return f'<path d="M{arc_start_x} {arc_start_y}A{radius} {radius} 0 1 0 {arc_end_x} {arc_end_y} {inner_radius} {inner_radius} 0 0 1 {arc_start_x} {arc_start_y}z" fill="{color}"/>'
    elif percent < 1:
        d = 2*percent - 1
        inner_radius = radius*(d**2 + 1)/(2*d)

        return f'<path d="M{arc_start_x} {arc_start_y}A{radius} {radius} 0 1 0 {arc_end_x} {arc_end_y} {inner_radius} {inner_radius} 1 0 0 {arc_start_x} {arc_start_y}z" fill="{color}"/>'
    elif percent == 1:
        return circle_template(cx, cy, radius, color)
    else:
        raise ValueError


def svg_template(width, height, paths, background_color=None):
    if background_color:
        paths = [f'<rect width="100%" height="100%" fill="{background_color}"/>'] + paths
    return f'<svg height="{height}" width="{width}">\n' + "\n".join(paths) + '\n</svg>'
