import networkx

import nodemap
import trip

if __name__ == '__main__':
    # load the node map
    campus_map = networkx.Graph()
    nodemap.load_nodes(campus_map, "mapdata/nodes.csv")
    nodemap.load_edges(campus_map, "mapdata/edges.csv")

    # start the navigation
    pt_a = 'mailroom' # sys.argv[1], perhaps?
    pt_b = 'engcy_khourybaun'
    route = networkx.shortest_path(campus_map, pt_a, pt_b)
    trip.navigate(campus_map, route)




