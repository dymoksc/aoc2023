import fileinput
from collections import namedtuple

Point = namedtuple("Point", "x y z")


class Ray:
    def __init__(self, start: Point, velocity: Point):
        self.start = start
        self.velocity = velocity
        self.other_point = Point(start.x + velocity.x, start.y + velocity.y, start.z + velocity.z)

    def __str__(self):
        return "{}, {}, {} @ {}, {}, {}".format(self.start.x, self.start.y, self.start.z,
                                                self.velocity.x, self.velocity.y, self.velocity.z)


def get_intersection(l1: Ray, l2: Ray) -> Point:
    x1, y1, _ = l1.start
    x2, y2, _ = l1.other_point
    x3, y3, _ = l2.start
    x4, y4, _ = l2.other_point

    intersection = Point(
        ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) /
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)),
        ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) /
        ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)),
        0)

    if (intersection.x - l1.start.x) / l1.velocity.x < 0 or \
       (intersection.y - l1.start.y) / l1.velocity.y < 0 or \
       (intersection.x - l2.start.x) / l2.velocity.x < 0 or \
       (intersection.y - l2.start.y) / l2.velocity.y < 0:
        raise ValueError

    return intersection


assert get_intersection(Ray(Point(12, 31, 28), Point(-1, -2, -1)),
                        Ray(Point(18, 19, 22), Point(-1, -1, -2))) == Point(-6, -5, 0)

try:
    get_intersection(Ray(Point(20, 25, 34), Point(-2, -2, -4)),
                     Ray(Point(18, 19, 22), Point(-1, -1, -2)))
    assert False
except ZeroDivisionError:
    assert True

try:
    get_intersection(Ray(Point(12, 31, 28), Point(-1, -2, -1)),
                     Ray(Point(20, 19, 15), Point(1, -5, -3)))
    assert False
except ValueError:
    assert True


rays = []
with (fileinput.input(files=("input"), encoding="utf-8") as f):
    for line in f:
        p, v = ([[int(s) for s in nums.split(', ')] for nums in line.rstrip('\n').split(' @ ')])
        rays.append(Ray(Point(p[0], p[1], p[2]), Point(v[0], v[1], v[2])))

min_xy = 200000000000000
max_xy = 400000000000000

good_intersections = 0
for i in range(len(rays)):
    for j in range(i, len(rays)):
        print("Hailstone A:", rays[i])
        print("Hailstone B:", rays[j])
        try:
            intersection = get_intersection(rays[i], rays[j])
            if not min_xy <= intersection.x <= max_xy or not min_xy <= intersection.y < max_xy:
                print("outside: ", end="")
                pass
            else:
                good_intersections += 1
            print(intersection.x, intersection.y)
        except ValueError:
            print("past")
            pass
        except ZeroDivisionError:
            print("parallel")
            pass
        print()

print(good_intersections)