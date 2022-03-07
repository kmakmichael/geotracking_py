import math
import nodemap
import gps


tol = 8e-6  # should probably be on a node-to-node basis via road width?


def distance(x, y):
    return math.sqrt(x*x + y*y)


def navigate(m, route):
    print(f'navigating route:\n{route}')
    record = [(), ()]
    for target in m:
        print(f'heading towards "{target}"')
        pos = (0, 0)
        while distance(pos, nodemap.node_pos(m, target)) > tol:
            pos = gps.get_coords()
            record[0].append(pos[0])
            record[1].append(pos[1])
            print(f'too far')
