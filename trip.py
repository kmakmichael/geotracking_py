import math
import nodemap


tol = 8e-6  # should probably be on a node-to-node basis via road width?


def distance(x, y):
    return 0  # math.sqrt(x*x, y*y)


def navigate(m, route):
    print(f'navigating route:\n{route}')
    for target in m:
        print(f'heading towards "{target}"')
        pos = (0, 0)  # pull this from the GPS chip
        while distance(pos, nodemap.node_pos(m, target)) > tol:
            print(f'too far')
