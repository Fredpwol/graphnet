from __future__ import absolute_import, division
from collections import defaultdict
from .components import Edge, Node
from .exceptions import InvalidNodeTypeError, MaxNodeError, GraphTypeError
from .utils import check_cycle
from .algorithms.search import BFS, DFS
from ._vis.layout import plot_graph_directed, plot_graph_undirected
from pygnet import VECTOR, SCALAR
import matplotlib.pyplot as plt
import numpy as np


class Graph(object):
    """
    Implements the Graph data structure which contains nodes or vertices linked with edges between them

    Graph helps in managing relationship between nodes in a network with their edges.
    Parameters
    ----------
    max_node:int, float, optional, default=infinity
        the maximum amount of nodes that can be added to the graph,
        default is infinty which means in theory nodes can be added
        to the graph indefinetly.
    max_edge:int, float, optional, default=infinity
        the maximum amount of edges that can be added to the graph,
        default is inifinty
    type:{'scalar'or'S', 'vector'or'V'},optional, default='scalar'
        this specifies the graph type, the are two graph types 'vector'
        which represents directional graphs and 'scalar' which represents
        undirectional graphs. the type of of graph determines the behaviour
        of the graph instance and which algorithm work with it. optionally 
        you can substutute 'scalar' with 'S' and 'vector' with 'V'.
    ref:str,optional,default="value"
        the attribute used by the graph for refrencing the node object passed in
        for identification and accessing as key value for the graph. change this
        if you are using a inherited node object to the object identifier else if
        your'e using the built in Node class directly then leave it as default.

    Attributes
    ----------
    edges:list
        This is a list of all edges in the graph instance
    connections:dict<defaultdict>
        A dictionary thats maps each node to its neighbour with an edge, a node 
        in the connection dictionary contains a default dict and in the default dict
        the adjacent node is mapped with its edge object and if there is no relationship
        with the two node 0 will be returned.
    graph_matrix: numpy.array()
        this is a adjacent matrix form of the graph, it is read only.
    get_node: list
        lits of all the node object in the graph, read only.

    """

    def __init__(self, max_node=float("inf"), max_edge=float("inf"), type=SCALAR, ref="value"):
        self.__max_node = max_node
        self.max_edge = max_edge
        self.type = type
        self.ref = ref
        self.edges = []
        self.connections = {}
        self.__nodes = []
        self.__node_map = {}

    def __len__(self):
        return len(self.__nodes)

    def __iter__(self):
        self.__counter = 0
        return self

    def __next__(self):
        if self.__counter < self.__len__():
            res = self.__nodes[self.__counter]
            self.__counter += 1
            return res
        else:
            raise StopIteration

    def __getitem__(self, key):
        return self.__node_map[key]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear()

    def add_node(self, node):
        """
        Adds an arbitrary object or Node object to the graph,
        all nodes added should be unique.
        parameters
        ----------
        node: str, int, float, Node

        """
        if self.__len__() <= self.__max_node:
            if type(node) in [str, int, float]:
                node = Node(node)
            if node not in self.__nodes:
                if type(node) == Node or issubclass(node.__class__, Node):
                    self.__nodes.append(node)
                    node_id = self.get_node_id(node)
                    self.__node_map[node_id] = node
                else:
                    raise InvalidNodeTypeError(
                        "Expected object of type str, float, int, Node or subclass of Node but %s was given." % type(node))
                self.connections[node_id] = defaultdict(int)
            else:
                raise ValueError("Node instance alerady in graph network")
        else:
            raise MaxNodeError(
                "Graph max size exceeded, expected %d node." % (self.__max_node))

    def add_edge(self, _from, _to, weight=1):
        """
        Adds a edge to the graph connecting the _from and _to nodes,
        the values passed to the parameters _from and _to must be a 
        node in the graph or a node in the graph must contain the 
        value passed in.
        if the type of the graph object is scalar an edge will be added
        from _to to _from.
        parameters
        ----------
        _from:int,str,float,Node
            this is the source from where the edge starts from
        _to:int,str,float,Node
            the destination of the edge
        weight:int, str, float, default=1
            this is the weight of the edge object connectiing the nodes
            the default value is 1.
        """
        if len(self.connections) <= self.max_edge:
            if type(_from) == Node or issubclass(_from.__class__, Node):
                _from = self.get_node_id(_from)
            if type(_to) == Node or issubclass(_to.__class__, Node):
                _to = self.get_node_id(_to)
            node = self[_from]
            node_to = self[_to]
            edge = Edge(node, node_to, weight)
            self.connections[_from][_to] = edge
            node.add_node(node_to)
            self.edges.append(edge)
            if self.type == SCALAR:
                edge2 = Edge(_to, _from, weight)
                self.connections[_to][_from] = edge2
                node_to.add_node(node)
                self.edges.append(edge2)
        else:
            raise MaxNodeError(
                "Graph max size exceded, expected %d node." % (self.max_edge))

    def add_nodes_from_iterable(self, iterable):
        """
        Adds nodes from a an iterable to the graph.
        Parameters
        ----------
        iterable:iter
            an iterable object conataining nodes to be added to the graph
        """
        for node in iterable:
            self.add_node(node)

    @property
    def graph_matrix(self):
        nodes = self.__nodes
        self.__adj_matrix = np.zeros((self.__len__(), self.__len__()))
        for i in range(self.__len__()):
            id_i = self.get_node_id(nodes[i])
            for j in range(self.__len__()):
                id_j = self.get_node_id(nodes[j])
                edge = self.connections[id_i][id_j] if not self.connections[id_i][id_j] else self.connections[id_i][id_j].weight
                self.__adj_matrix[i, j] = edge
        return self.__adj_matrix

    @property
    def get_nodes(self):
        return self.__nodes

    def from_dict(self, dictonary, weights=1):
        """
        creates and add node from a dictionary. The dictionary passed in must
        have a key with an iterable value which contains all adjacents node, and 
        node in the iterable must be in the dictionary or graph. The weight will be 
        uniform for all nodes.
        Parmeters
        ---------
        dictionary: dict
            dictonary object thats holds weights and their connections
        weights: int, str, float
            uniform weight passed to all edges.
        """
        for key in dictonary:
            node = Node(key)
            self.add_node(node)
            for edge in dictonary[key]:
                if edge in dictonary.keys() or self.__nodes:
                    self.add_edge(key, edge, weights)
                else:
                    raise KeyError("Edge %s not in dictionary." % (edge))

    def is_cyclic(self):
        """
        Checks if the graph contains a cycle, if the graph type is scalar

        returns
        -------
        bool
        """
        if self.type != VECTOR:
            raise GraphTypeError(
                "cyclic check only works for vector type graphs")
        visited = {}
        rec_stack = {}
        for node in self:
            visited[node] = False
            rec_stack[node] = False
        for source in self:
            if check_cycle(source, visited, rec_stack):
                return True

        return False

    def clear(self):
        """
        Clears all the graph content
        """
        self.__nodes.clear()
        self.connections = {}
        self.edges.clear()

    def is_connected(self):
        """
        Checks if a scalar graph is connected or not.

        returns
        -------
        bool
        """
        if self.type == SCALAR:
            traverse = self.BFS()
            for node in self.__nodes:
                if not node in traverse:
                    return False
            return True
        else:
            raise GraphTypeError(
                "Invalid graph type %s expected scalar" % (self.type))

    def display(self, weighted=False):
        """
        creates a plot of the graph.

        parameters
        ----------
        weighted:bool
            if true weights will be displayed

        """
        _, ax1 = plt.subplots(1, figsize=(20, 15))
        if self.type == VECTOR:
            plot_graph_directed(self, ax1, len(self), weighted)
        elif self.type == SCALAR:
            plot_graph_undirected(self, ax1, len(self), weighted)

    def remove_edge(self, _from, _to):
        """
        removes edge connecting to nodes if it exist.

        Parameters
        ----------
            _from:int, str, float
            _to:int, str, float
        """
        del self.connections[_from][_to]
        for i in range(len(self.edges)):
            if self.edges[i]._from == _from and self.edges[i]._to == _to:
                self.edges.pop(i)
                break

        src = self[_from]
        dest = self[_to]
        for i in range(len(src.adjacent_nodes)):
            if dest == src.adjacent_nodes[i]:
                src.adjacent_nodes.pop(i)
                break

    def get_node_id(self, node):
        """
        gets the value of the node object used in identifying 
        the node
        Parameters
        ----------
        node:Node
        returns
        -------
        value:str, int, float, object

        """
        for vertex in self.__nodes:
            if vertex == node:
                v = node
                break
        return eval('v.%s' % self.ref)

    def BFS(self, source=None, key=None):
        """
        An Impelemetaion of breath-first-search for tranversing a 
        graph of getting a node.
        Parameters
        ----------
        source:int, str, float, optional
            Value of the node to start the tranverse. if ommited the method
            uses a random node as source.
        key:int, str, float, optional
            Value of the node to stop the tranverse. if ommited the method
            stops when all  node in the graph are tranversed.
        returns
        -------
        value: list
            A list of the path tranversed in order from source to key.
        """
        return BFS(self, source, key)

    def DFS(self, source=None, key=None):
        """
        An Impelemetaion of depth-first-search for tranversing a 
        graph of getting a node.
        Parameters
        ----------
        source:int, str, float, optional
            Value of the node to start the tranverse. if ommited the method
            uses a random node as source.
        key:int, str, float, optional
            Value of the node to stop the tranverse. if ommited the method
            stops when all  node in the graph are tranversed.
        returns
        -------
        value: list
            A list of the path tranversed in order from source to key.
        """
        return DFS(self, source, key)
