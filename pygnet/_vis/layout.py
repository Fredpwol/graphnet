from matplotlib.patches import ConnectionPatch
import matplotlib.pyplot as plt 
import numpy as np


def plot_graph_directed(graph, n, ref, weighted):
    _, ax1 = plt.subplots(1 ,figsize=(20, 15))
    space = np.linspace(0,1,n+1)
    scale = 100 // n
    size = scale + 10
    x = []
    for i in range(0, len(space)-1):
        point = (space[i]+space[i+1]) / 2
        x.append(point)
    y = [np.random.random() for _ in range(n)]
    points = dict()
    for i, node in enumerate(graph):
        points[node] = (x[i], y[i])
    coordsA = "data"
    coordsB = "data"
    for node in graph:
        x_i, y_i = points[node]
        for adj_node in node.adjacent_nodes:
            x_prime, y_prime = points[adj_node]
            con = ConnectionPatch((x_i, y_i), (x_prime, y_prime), coordsA, coordsB,
                        arrowstyle="-|>", shrinkA=30, shrinkB=30,
                        mutation_scale=scale, fc="k")
            if weighted:
                x_mid , y_mid = (x_prime+x_i) / 2, (y_prime+y_i) / 2
                _from = eval('node.%s'%ref)
                _to = eval('adj_node.%s'%ref)
                weight = graph.connections[_from][_to].weight
                ax1.text(x_mid, y_mid, weight, fontsize=12)
            ax1.add_artist(con)
    ax1.plot(x, y, "o",markersize=size)

    for node in points:
        x, y = points[node]
        value = eval('node.%s'%ref)
        ax1.annotate(value, (x, y))
