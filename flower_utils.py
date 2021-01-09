import math


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
    vertex_string = f"M {peaks[0][0]} {peaks[0][1]}"

    for i in range(len(peaks)):
        source_peak, valley, dest_peak = peaks[i], valleys[i], peaks[(i+1) % len(peaks)]

        (control1_x, control1_y), (control2_x, control2_y) = flower_control_points(center, source_peak, valley, curviness)
        vertex_string += f"C {control1_x} {control1_y}, {control2_x} {control2_y}, {valley[0]} {valley[1]} "

        (control2_x, control2_y), (control1_x, control1_y) = flower_control_points(center, dest_peak, valley, curviness)
        vertex_string += f"C {control1_x} {control1_y}, {control2_x} {control2_y}, {dest_peak[0]} {dest_peak[1]} "

    return vertex_string + "Z"
