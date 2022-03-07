import csv
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt


def load_nodes(g, csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            g.add_nodes_from([(row['name'], {"lat": row['lat'], "lng": row['lng']})])


def load_edges(g, csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            g.add_edge(row['a'], row['b'])


def draw_graph(g, pt=()):
    matplotlib.use('qtagg')
    # draw nodes
    fig, ax = plt.subplots()
    img = plt.imread("mapdata/gmap.png")
    ax.imshow(img, extent=[-121.3184, -121.3064, 37.9744, 37.9855])
    for n in list(g.nodes):
        plt.scatter(float(g.nodes[n]['lng']), float(g.nodes[n]['lat']), color='blue')

    # draw lines
    for e in list(g.edges):
        x = [float(g.nodes[e[0]]['lng']), float(g.nodes[e[1]]['lng'])]
        y = [float(g.nodes[e[0]]['lat']), float(g.nodes[e[1]]['lat'])]
        plt.plot(x, y, color='blue')

    if pt != ():
        plt.plot(pt[0], pt[1], color='red')

    plt.show()


