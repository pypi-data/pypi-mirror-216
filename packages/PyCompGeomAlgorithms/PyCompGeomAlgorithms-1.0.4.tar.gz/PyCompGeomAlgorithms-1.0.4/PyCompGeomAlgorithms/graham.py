from math import pi
from .core import Point


def graham(points):
    if len(points) < 3:
        yield sorted(points, key=lambda p: (p.y, -p.x))
    else:
        i = 2
        while Point.direction(points[0], points[1], points[i]) == 0:
            i += 1
        
        centroid = Point.centroid(points[0], points[1], points[i])
        yield centroid

        origin = min(points, key=lambda p: (p.y, -p.x))
        ordered_points = sort_points(points, centroid, origin)
        yield ordered_points
        yield origin

        ordered_points.append(origin)
        steps_table = []
        hull = make_hull(steps_table, ordered_points)
        ordered_points.pop()
        
        yield [row[0] for row in steps_table] # point triples
        yield [row[1] for row in steps_table] # whether angles are <pi
        yield
        yield
        yield
        
        yield hull


def sort_points(points, centroid, origin):
    min_angle = Point.polar_angle(origin, centroid)

    def angle_and_dist(p):
        p_angle = Point.polar_angle(p, centroid)
        angle = p_angle if p_angle >= min_angle else 2 * pi + p_angle
        return (angle, Point.dist(p, centroid))

    return sorted(points, key=angle_and_dist)


def make_hull(steps_table, ordered_points):
    res = ordered_points[:2]

    for point in ordered_points[2:]:
        while len(res) > 1 and Point.direction(res[-2], res[-1], point) >= 0:
            steps_table.append(steps_table_row(res, False, point))
            res.pop()

        if len(res) > 1:
            steps_table.append(steps_table_row(res, True, point))
        
        res.append(point)

    return res[:-1]


def steps_table_row(points, adding, new_point):
    """Current step: current points' triple, whether to add/delete, and point to add/delete."""
    return (points[-2], points[-1], new_point), adding
