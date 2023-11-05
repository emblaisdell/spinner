from solid2 import *
import math

phi = (1 + sqrt(5)) * 0.5
dR = 2 - phi
N = 250  # num time steps
dt = 0.005  # time step length

HEART = import_stl("./heart_base.stl")
AXIS_OF_ROT = [0, 1, 0]
omega = 120  # angular velocity


def scale_at(t):
    return 0.7 - 0.1 * math.sin(2.0*math.pi / (1+math.exp(-10.0*((t%2)-1))))


def scale(v, s):
    return [s * x for x in v]


def distance_at(t):
    return 0.1 + t - 0.1 * t**2  # 0.25 + 0.75 * t - 0.0625 * math.sin(8 * t)


def block_at_n(n):
    return (
        HEART.scale(0.25)
        # .rotate(scale(AXIS_OF_ROT, omega * n * dt))
        .scale(scale_at(n * dt))
        .translateX(50)
        .rotateY(-90 + 90 * distance_at(n * dt) / distance_at(1))
        .rotateZ(360.0 * dR * n)
    )


def main():
    blocks = [block_at_n(n) for n in range(N)]
    piece = union()(blocks) + sphere(r=50, _fn=100)
    piece -= cube(200, center=True).translate(0, 0, -100)
    piece -= cylinder(r=7, h=80, center=True, _fn=50)
    piece = piece.rotateX(-90)
    piece.save_as_scad()


main()
