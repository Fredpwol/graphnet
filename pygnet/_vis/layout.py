from matplotlib.patches import ConnectionPatch
import matplotlib.pyplot as plt
import numpy as np
from .decorators import preproccess_plot


COORDSA = "data"
COORDSB = "data"


@preproccess_plot
def plot_graph(graph, ax, n, weighted, shrinkA, shrinkB, layout, polygon_radius, attr, arrowstyle, weight_color, arrow_color):
    """
    creates a plot of nodes and edges connected by a ConnectionPatch object.
    """
    for node in plot_graph.nodes:
        x_i, y_i = plot_graph.points[node]
        for adj_node in node.adjacent_nodes:
            _from = graph.get_node_id(node)
            _to = graph.get_node_id(adj_node)
            edge = graph.connections[_from][_to]
            A_color = "k" if not arrow_color else edge.color
            A_width = edge.linewidth if not edge.linewidth else edge.linewidth * 4
            x_prime, y_prime = plot_graph.points[adj_node]
            con = ConnectionPatch((x_i, y_i), (x_prime, y_prime), COORDSA, COORDSB,
                                  arrowstyle=arrowstyle, shrinkA=shrinkA, shrinkB=shrinkB,
                                  mutation_scale=plot_graph.scale, fc=A_color, linewidth=A_width, edgecolor=A_color)
            if weighted:
                T_color = "k" if not weight_color else A_color
                x_mid, y_mid = (x_prime+x_i) * 0.5, (y_prime+y_i) * 0.5
                weight = edge.weight
                fontsize = 12 / n + 12
                ax.text(x_mid, y_mid, str(weight), fontsize=edge.fontsize*fontsize+fontsize, color=T_color)
            ax.add_artist(con)


def plot_graph_directed(graph, ax, n, weighted, weight_color, arrow_color, layout, polygon_radius, attr):
    """
    plots a directed graph with nodes as points and edges ass arrows connecting them.

    Parameters
    ---------
    graph:Graph
        The Graph to be plotted.
    ax:
        matplotlib axis
    n:int
        number of nodes
    weighted:bool, optional, default=False
        if true weights will be displayed.
    weight_color:bool, optional, default=False
        if true the weights will be colored with the edge object color attribute.
    arrow_color:bool, optional, default=True
        if true the arrow will be colored with the edge object color attribute.
    layout: optional, {random, polygon}, default=polygon
        The layout used to arrange the nodes in the plot
    polygon_radius: int, float, default=5
        if polygon layout is used this defines the radius of the polygon shape.  
    """
    plot_graph(graph, ax, n, weighted, 30, 30, layout,
               polygon_radius, attr, "-|>", weight_color, arrow_color)


def plot_graph_undirected(graph, ax, n, weighted, weight_color, arrow_color, layout, polygon_radius, attr):
    """
    plots a  undirected graph with nodes as points and edges as lines connecting them.

    Parameters
    ----------
    graph:Graph
        The Graph to be plotted.
    ax:
        matplotlib axis
    n:int
        number of nodes
    weighted:bool, optional, default=False
        if true weights will be displayed.
    weight_color:bool, optional, default=False
        if true the weights will be colored with the edge object color attribute.
    arrow_color:bool, optional, default=True
        if true the arrow will be colored with the edge object color attribute.
    layout: optional, {random, polygon}, default=polygon
        The layout used to arrange the nodes in the plot
    polygon_radius: int, float, default=5
        if polygon layout is used this defines the radius of the polygon shape.  
    """
    plot_graph(graph, ax, n, weighted, 1, 1, layout,
               polygon_radius, attr, "-", weight_color, arrow_color)
