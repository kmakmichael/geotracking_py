import math
import matplotlib
import matplotlib.pyplot as plt
import nodemap
import gps


tol = 8e-6  # should probably be on a node-to-node basis via road width?


def distance(a, b):
    return math.sqrt(abs(b[0]-a[0])**2 + abs(b[1]-a[1])**2)


def distance_m(a, b):
    # convert to meters?
    d_x = (b[0]-a[0])*111139
    d_y = (b[0]-a[0])*111139
    return math.sqrt(d_x*d_x + d_y*d_y)


def navigate(m, route):
    print(f'navigating route:\n{route}')
    record = ([], [])
    pos = gps.get_coords()
    # plt.ion()
    # plt.show()
    # fig, ax = nodemap.n_graph(m)
    # rt_line, = ax.plot(pos[0], pos[1],'r')
    # img = plt.imread("mapdata/gmap.png")
    # matplotlib.use('QtAgg')
    for target in route:
        print(f'heading towards "{target}"')
        while distance(pos, nodemap.node_pos(m, target)) > tol:
            print(f'distance to node: {distance_m(pos, nodemap.node_pos(m, target))}m')
            pos = gps.get_coords()
            # print(f'extracted coords ({pos[0]},{pos[1]})')
            record[0].append(pos[0])
            record[1].append(pos[1])
            # rt_line.set_data(pos[0], pos[1])
            # fig.canvas.draw_idle()
        print(f'- - - > reached ({target}) @ ({pos[0]}, {pos[1]})')
    return record
