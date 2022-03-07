import math
import matplotlib.pyplot as plt
import nodemap
import gps


tol = 8e-6  # should probably be on a node-to-node basis via road width?


def distance(x, y):
    return math.sqrt(x*x + y*y)


def navigate(m, route):
    print(f'navigating route:\n{route}')
    record = [(), ()]
    pos = gps.get_coords()
    plt.ion()
    fig, ax = nodemap.n_graph(m)
    rt_line, = ax.plot(pos[0], pos[1])
    img = plt.imread("mapdata/gmap.png")
    for target in m:
        print(f'heading towards "{target}"')
        while distance(pos, nodemap.node_pos(m, target)) > tol:
            pos = gps.get_coords()
            print(f'extracted coords ({pos[0]},{pos[1]})')
            record[0].append(pos[0])
            record[1].append(pos[1])
            rt_line.set_data(pos[0], pos[1])
            fig.canvas.draw()
        print(f'- - - > reached ({target}) @ ({pos[0]}, {pos[1]})')
    return record
