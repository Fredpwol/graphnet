from matplotlib.patches import ConnectionPatch
import matplotlib.pyplot as plt 
import numpy as np
from .decorators import preproccess_plot


COORDSA = "data"
COORDSB = "data"




@preproccess_plot
def plot_graph_directed(graph, ax, n, weighted):
    for node in graph.get_nodes:
        x_i, y_i = plot_graph_directed.points[node]
        for adj_node in node.adjacent_nodes:
            x_prime, y_prime = plot_graph_directed.points[adj_node]
            con = ConnectionPatch((x_i, y_i), (x_prime, y_prime), COORDSA, COORDSB,
                        arrowstyle="-|>", shrinkA=30, shrinkB=30,
                        mutation_scale=plot_graph_directed.scale, fc="k")
            if weighted:
                x_mid , y_mid = (x_prime+x_i) / 2, (y_prime+y_i) / 2
                _from = graph.get_node_id(node)
                _to = graph.get_node_id(adj_node)
                weight = graph.connections[_from][_to].weight
                ax.text(x_mid, y_mid, str(weight), fontsize=12)
            ax.add_artist(con)




@preproccess_plot
def plot_graph_undirected(graph, ax, n, weighted):
    for node in graph.get_nodes:
        x_i, y_i = plot_graph_undirected.points[node]
        for adj_node in node.adjacent_nodes:
            x_prime, y_prime = plot_graph_undirected.points[adj_node]
            con = ConnectionPatch((x_i, y_i), (x_prime, y_prime), COORDSA, COORDSB,
                        arrowstyle="-", shrinkA=1, shrinkB=1,
                        mutation_scale=plot_graph_undirected.scale, fc="k")
            if weighted:
                x_mid , y_mid = (x_prime+x_i) / 2, (y_prime+y_i) / 2
                _from = graph.get_node_id(node)
                _to = graph.get_node_id(adj_node)
                weight = graph.connections[_from][_to].weight
                ax.text(x_mid, y_mid, weight, fontsize=12)
            ax.add_artist(con)





