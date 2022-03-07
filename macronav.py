import networkx

import nodemap
import trip
import gps

if __name__ == '__main__':
    print('loading nodemap...')
    # load the node map
    campus_map = networkx.Graph()
    nodemap.load_nodes(campus_map, "mapdata/nodes.csv")
    nodemap.load_edges(campus_map, "mapdata/edges.csv")
    print('successfully loaded map')
    # start the navigation
    gps.fix()
    #   in actuality, the first thing we need to do is find where we are and then get to point A
    #   so we'd need a function to do that, and then trip.navigate() a path here to A
    pt_a = 'library' # replace /w whatever IPC we'll use. sys.argv[1], perhaps?
    pt_b = 'engcy_khourybaun'
    route = networkx.shortest_path(campus_map, pt_a, pt_b)
    nodemap.draw_graph(campus_map, pt=trip.navigate(campus_map, route))




