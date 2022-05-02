import networkx
from math import sqrt
import nodemap
#import trip
import gps
import time
from threading import Thread, Event, Lock
from enum import IntEnum
from btcomms import BTComms


class GPSStatus(IntEnum):
    STOP = 0
    GO = 1
    TURN = 2
status_lock = Lock()
status_changed = Event()
com_lock = Lock()
shmem = {
        "status": 0
        }
tol = 8e-5


def distance(a,b):
    return sqrt(abs(b[0]-a[0])**2 + abs(b[1]-a[1])**2)


def navigate(m, route, com):
    print(f'[navigation] navigating from {route[0]} to {route[-1]}')
    # record = ([], [])
    print('[navigation] setting status to GO')
    with status_lock and com_lock:
        shmem["status"] = 1 # int(GPSStatus.GO)
        com.send('G')
    status_changed.set()
    pos = gps.get_coords()
    for target in route:
        # print(f'[navigation] heading towards {target}')
        while distance(pos, nodemap.node_pos(m, target)) > tol:
            pos = gps.get_coords()
            #record[0].append(pos[0])
            #record[1].append(pos[1])
    with status_lock and com_lock:
        shmem["status"] = GPSStatus.STOP
        com.send('S')
    status_changed.set()
    # return record

def status_update(com, s):
    while True:
        time.sleep(2)
        print(f'[navigation] sending update: {s["status"]}')
        with status_lock and com_lock:
            if s["status"] == 1:
                com.send('G')
            else:
                com.send('S')


if __name__ == '__main__':
    print('[navigation] loading nodemap...')
    # load the node map
    campus_map = networkx.Graph()
    nodemap.load_nodes(campus_map, "mapdata/nodes.csv")
    nodemap.load_edges(campus_map, "mapdata/edges.csv")
    print('[navigation] successfully loaded map')

    com = BTComms('N')

    pt_a = 'library' # replace /w whatever IPC we'll use. sys.argv[1], perhaps?
    pt_b = 'uc_fountain'
    route = networkx.shortest_path(campus_map, pt_a, pt_b)
    # nodemap.route_graph(campus_map, route)
    # wait for a fix before we begin
    # gps.fix()
    print(f'[navigation] fix found')
    com.confirm()
    # start update timer
    update = Thread(target=status_update, args=[com, shmem])
    update.start()
    # start navigating
    #   in actuality, the first thing we need to do is find where we are and then get to point A
    #   so we'd need a function to do that, and then trip.navigate() a path here to A
    navigate(campus_map, route, com)
    while True:
        status_changed.wait()
        with status_lock and com_lock:
            if shmem["status"] == 1:
                com.send('G')
            else:
                com.send('S')
        status_changed.clear()
