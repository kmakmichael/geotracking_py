import networkx
from math import sqrt
import nodemap
import gps
import time
from threading import Thread, Event, Lock
from enum import IntEnum
from btcomms import BTComms

cdir = '/home/bt/budgetTesla/macronav/geotracking_py'

class GPSStatus(IntEnum):
    STOP = 0
    GO = 1
    TURN = 2

status_changed = Event()
status_lock = Lock()
shmem = {
        "status": 0
        }

tol = 8e-5


def distance(a,b):
    return sqrt(abs(b[0]-a[0])**2 + abs(b[1]-a[1])**2)


def navigate(m, route, shmem):
    print(f'[navigation] navigating from {route[0]} to {route[-1]}')
    # record = ([], [])
    # print('[navigation] setting status to GO')
    with status_lock:
        shmem["status"] = 1 # int(GPSStatus.GO)
        # com.send('G')
        status_changed.set()
    pos = gps.get_coords()
    for target in route:
        print(f'[navigation] heading towards {target}')
        while distance(pos, nodemap.node_pos(m, target)) > tol:
            pos = gps.get_coords()
            #record[0].append(pos[0])
            #record[1].append(pos[1])
    with status_lock:
        shmem["status"] = GPSStatus.STOP
        # com.send('S')
        status_changed.set()
    # return record



if __name__ == '__main__':
    # load the node map
    print('[navigation] loading nodemap...')
    campus_map = networkx.Graph()
    nodemap.load_nodes(campus_map, f'{cdir}/mapdata/courtyard_improved_nodes.csv')
    nodemap.load_edges(campus_map, f'{cdir}/mapdata/courtyard_improved_edges.csv')
    print('[navigation] successfully loaded map')


    # set these on-the-fly
    pt_a = '2636064209' # in front of Khoury
    pt_b = '2674334939' # in front of Anderson corner
    route = networkx.shortest_path(campus_map, pt_a, pt_b)
    # nodemap.route_graph(campus_map, route)

    # wait for a fix before we begin
    print('[navigation] waiting for a fix')
    gps.fix()
    print('[navigation] sending confirmation')
    com = BTComms('N')
    com.confirm()
    print('[navigation] recieved ACK')
    # start update timer
    # update = Thread(target=status_update, args=[com, shmem])
    # update.start()

    # start navigating
    #   in actuality, the first thing we need to do is find where we are and then get to point A
    #   so we'd need a function to do that, and then trip.navigate() a path here to A
    navi = Thread(target=navigate, args=[campus_map, route, shmem])
    navi.start()
    print('[navigation] sending initial GO')
    com.send('G')
    while True:
        status_changed.wait()
        print(f'[navigation] status changed: {shmem["status"]}')
        with status_lock:
            if shmem["status"] == 1:
                com.send('G')
            else:
                com.send('S')
            status_changed.clear()
