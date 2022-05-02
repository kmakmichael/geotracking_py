import networkx
import nodemap
#import trip
import gps
from threading import Thread, Timer, Event, Lock
from enum import IntEnum
from btcomms import BTComms


class GPSStatus(IntEnum):
    STOP = 0
    GO = 1
    TURN = 2
status_lock = Lock()
status_changed = Event()
current_status = 0



def distance(a,b):
    return math.sqrt(abs(b[0]-a[0])**2 + abs(b[1]-a[1])**2)


def navigate(m, route, s):
    print(f'[navigation] navigating from {route[0]} to {route[-1]}')
    # record = ([], [])
    pos = gps.get_coords()
    for target in route:
        # print(f'[navigation] heading towards {target}')
        while distance(pos, nodemap.nose_pos(m, target)) > tol:
            pos = gps.get_coords()
            #record[0].append(pos[0])
            #record[1].append(pos[1])
    with status_lock:
        s = GPSStatus.STOP
    status_changed.set()
    # return record

def status_update(com, s):
    print(f'[navigation] sending update: {s}')
    with status_lock:
        if s == 1:
            com.send('G')
        else:
            com.send('S')
    ouroboros = Timer(2, status_update, args=[com, s])
    ouroboros.start()



if __name__ == '__main__':
    print('loading nodemap...')
    # load the node map
    campus_map = networkx.Graph()
    nodemap.load_nodes(campus_map, "mapdata/nodes.csv")
    nodemap.load_edges(campus_map, "mapdata/edges.csv")
    print('successfully loaded map')

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
    status_update(com, current_status)
    # start navigating
    #   in actuality, the first thing we need to do is find where we are and then get to point A
    #   so we'd need a function to do that, and then trip.navigate() a path here to A
    trip = Thread(target=navigate, args=[campus_map, route, current_status])
    trip.start()
    while True:
        status_changed.wait()
        with status_lock:
            if current_status == 1:
                com.send('G')
            else:
                com.send('S')
        status_changed.clear()
