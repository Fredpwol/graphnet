import numpy as np

class Graph:

    def __init__(self, max_node=float("inf"), max_edge=float("inf"), graph_type="scalar", ref="value" ):
        self.max_node = max_node
        self.max_edge = max_edge
        self.graph_type = graph_type
        self.ref = ref
        self.edges = []
        self.__adj_matrix = np.array()
