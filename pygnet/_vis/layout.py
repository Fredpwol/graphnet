from matplotlib.patches import ConnectionPatch
import matplotlib.pyplot as plt
import numpy as np
from .decorators import preproccess_plot


COORDSA = "data"
COORDSB = "data"


@preproccess_plot
def plot_graph(graph, ax, n, weighted, shrinkA, shrinkB, layout, polygon_radius, arrowstyle, weight_color, arrow_color):
    for node in graph.get_nodes:
        x_i, y_i = plot_graph.points[node]
        for adj_node in node.adjacent_nodes:
            A_color = "k" if not arrow_color else graph.connections[graph.get_node_id(
                node)][graph.get_node_id(adj_node)].color
            x_prime, y_prime = plot_graph.points[adj_node]
            con = ConnectionPatch((x_i, y_i), (x_prime, y_prime), COORDSA, COORDSB,
                                  arrowstyle=arrowstyle, shrinkA=shrinkA, shrinkB=shrinkB,
                                  mutation_scale=plot_graph.scale, fc=A_color)
            if weighted:
                T_color = "k" if not weight_color else graph.connections[graph.get_node_id(
                    node)][graph.get_node_id(adj_node)].color
                x_mid, y_mid = (x_prime+x_i) / 2, (y_prime+y_i) / 2
                _from = graph.get_node_id(node)
                _to = graph.get_node_id(adj_node)
                weight = graph.connections[_from][_to].weight
                ax.text(x_mid, y_mid, str(weight), fontsize=12, color=T_color)
            ax.add_artist(con)


def plot_graph_directed(graph, ax, n, weighted, weight_color, arrow_color, layout, polygon_radius):
    plot_graph(graph, ax, n, weighted, 30, 30, layout,
               polygon_radius, "-|>", weight_color, arrow_color)


def plot_graph_undirected(graph, ax, n, weighted, weight_color, arrow_color, layout, polygon_radius):
    plot_graph(graph, ax, n, weighted, 1, 1, layout,
               polygon_radius, "-", weight_color, arrow_color)
