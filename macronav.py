import networkx

import nodemap
import trip
import gps
from btcomms import BTComms

if __name__ == '__main__':
    print('[navigation] creating UDS')
    com = BTComms('N')
    print('[navigation] loading nodemap...')
    # load the node map
    campus_map = networkx.Graph()
    nodemap.load_nodes(campus_map, "mapdata/nodes.csv")
    nodemap.load_edges(campus_map, "mapdata/edges.csv")
    print('[navigation] successfully loaded map')

    print('[navigation] sending READY signal')
    com.send('READY')

    pt_a = 'library' # replace /w whatever IPC we'll use. sys.argv[1], perhaps?
    pt_b = 'uc_fountain'
    route = networkx.shortest_path(campus_map, pt_a, pt_b)
    # nodemap.route_graph(campus_map, route)
    # wait for a fix before we begin
    gps.fix()
    com.send('READY')
    # TODO com.close()
    # start navigating
    #   in actuality, the first thing we need to do is find where we are and then get to point A
    #   so we'd need a function to do that, and then trip.navigate() a path here to A
    #nodemap.draw_graph(campus_map, pt=trip.navigate(campus_map, route))
    trip.navigate(campus_map, route)

