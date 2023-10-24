from solid2 import *

phi = (1 + sqrt(5)) * 0.5
dR = 2 - phi
N = 150  # num time steps
dt = 0.01  # time step length

BLOCK = lambda: cube(0.15, 0.25, 0.75, center=True)
AXIS_OF_ROT = [0, 1, 0]
omega = 120  # angular velocity


def posn(t):
    return [t, 0, 1 - t**2]


def scale(v, s):
    return [s * x for x in v]


def block_at_n(n):
    return (
        BLOCK()
        .rotate(scale(AXIS_OF_ROT, omega * n * dt))
        .translate(posn(n * dt))
        .rotateZ(360.0 * dR * n)
    )


def main():
    blocks = [block_at_n(n) for n in range(N)]
    piece = union()(blocks) + sphere(r=0.9, _fn=100)
    piece -= cube(4, center=True).translate(0, 0, -2)
    piece = piece.rotateX(-90)
    piece.save_as_scad()


main()
