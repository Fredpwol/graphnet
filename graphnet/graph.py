from __future__ import absolute_import, division
from collections import defaultdict
from .components import Edge, Node
from .exceptions import InvalidNodeTypeError, MaxNodeError, GraphTypeError
from .utils import check_cycle
from .algorithms._search import BFS, DFS
from .algorithms._sort import topological_sort
from ._vis.layout import plot_graph_directed, plot_graph_undirected
from graphnet import VECTOR, SCALAR
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
        default is infinity which means in theory nodes can be added
        to the graph indefinitely.
    max_edge:int, float, optional, default=infinity
        the maximum amount of edges that can be added to the graph,
        default is infinity
    type:{'scalar'or'S', 'vector'or'V'},optional, default='scalar'
        this specifies the graph type, the are two graph types 'vector'
        which represents directional graphs and 'scalar' which represents
        un-directional graphs. the type of of graph determines the behavior
        of the graph instance and which algorithm work with it. optionally 
        you can substutute 'scalar' with 'S' and 'vector' with 'V'.
    ref:str,optional,default="value"
        the attribute used by the graph for referencing the node object passed in
        for identification and accessing as key value for the graph. change this
        if you are using a inherited node object to the object identifier else if
        you're using the built in Node class directly then leave it as default.

    Attributes
    ----------
    edges:list
        This is a list of all edges in the graph instance
    connections:dict<defaultdict>
        A dictionary thats maps each node to its neighbor with an edge, a node 
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
                raise ValueError("Node instance already in graph network")
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
            this is the weight of the edge object connecting the nodes
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
                "Graph max size exceeded, expected %d node." % (self.max_edge))

    def add_nodes_from_iterable(self, iterable):
        """
        Adds nodes from a an iterable to the graph.
        Parameters
        ----------
        iterable:iter
            an iterable object containing nodes to be added to the graph
        """
        for node in iterable:
            self.add_node(node)

    def add_edges_from_iterable(self, iterable):
        """
        Adds nodes edge a an iterable to the graph.
        Parameters
        ----------
        iterable:iter
            an iterable object containing a iterable with size of 3 or 2
            where the first two values are values of nodes in the graph
            and if there's a third value it will be used as the weight of
            the edge to be added to the graph
        """
        for e in iterable:
            self.add_edge(*e)

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

    def from_dict(self, dictionary, weights=1):
        """
        creates and add node from a dictionary. The dictionary passed in must
        have a key with an iterable value which contains all adjacents node, and 
        node in the iterable must be in the dictionary or graph. The weight will be 
        uniform for all nodes.
        Parmeters
        ---------
        dictionary: dict
            dictionary object thats holds weights and their connections
        weights: int, str, float
            uniform weight passed to all edges.
        """
        self.add_nodes_from_iterable(list(dictionary.keys()))
        for key in dictionary:
            for edge in dictionary[key]:
                self.add_edge(key, edge, weights)

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

    def display(self, weighted=False, weight_color=False, arrow_color=True, layout="polygon", polygon_radius=5, attr=None, ax=None):
        """
        creates a plot of the graph.

        parameters
        ----------
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
        attr:None, str, int, object, default=None
            The attribute of the Node object to be used as label. if omitted the default value
            will be the ref attribute of the graph.
        ax:.axes.Axes, default=None
            An axis object to plot the graph, if not specified a default axis will be created.

        """
        if attr == None:
            attr = self.ref
        if not ax:
            _, ax = plt.subplots(1, figsize=(20, 20))
        if self.type == VECTOR:
            plot_graph_directed(self, ax, len(
                self), weighted, weight_color, arrow_color, layout, polygon_radius, attr)
        elif self.type == SCALAR:
            plot_graph_undirected(self, ax, len(
                self), weighted, weight_color, arrow_color, layout, polygon_radius, attr)

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

    def topological_sort(self):
        """
        Sorts the nodes if graph type is vector
        returns
        -------
        res:List
            a list containing  all the node in the graph instance
            in a sorted form
        """
        return topological_sort(self)

    def BFS(self, source=None, key=None):
        """
        An Impelemetaion of breath-first-search for tranversing a 
        graph of getting a node.
        Parameters
        ----------
        source:int, str, float, optional
            Value of the node to start the tranverse. if omitted the method
            uses a random node as source.
        key:int, str, float, optional
            Value of the node to stop the tranverse. if omitted the method
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
            Value of the node to start the tranverse. if omitted the method
            uses the first node in the graph as source.
        key:int, str, float, optional
            Value of the node to stop the tranverse. if omitted the method
            stops when all  node in the graph are tranversed.
        returns
        -------
        value: list
            A list of the path traversed in order from source to key.
        """
        return DFS(self, source, key)


class GraphPriorityQueue:
    """
    A priority queue data structure which stores node
    and get them based on priority. if state is true nodes
    will be gotten by priority and if their state value evaluate
    to true.
    Parameters
    ----------
    graph: Graph
        graph object whose node will be stored in the queue.
    type: {"min", "max"}, default="min"
        the type of priority based on how the values in the 
        graph will be retrived, if min the smallest value will
        be prioritized and if max the largest value will be prioritized.
    state: boolean, default=False
        this specifies if state will be used in the queue. If true an
        attribute status will be created to hold the states of all the 
        nodes.
    Attributes
    ---------
    type: {"min", "max"}, default="min"
    queue: dict
        this holds node and value pair, the value is what is used in 
        as priority in getting items.
    status: dict
        if state is true this will be created and hold a dictionary of
        nodes mapped with boolean.
    """

    def __init__(self, graph, type="min", state=False):
        if type == 'min' or type == 'max':
            self.type = type
        else:
            raise TypeError("type attribute most be 'min' or 'max'")
        self.__graph = graph
        self._top = float('inf') if self.type == 'min' else -float('inf')
        self.queue = dict()
        self.__state = state
        for node in self.__graph:
            self.queue[node] = float('inf')
        if self.__state:
            self.status = dict()
            for node in self.__graph:
                self.status[node] = False

    def __repr__(self):
        return str(list(self.queue.values()))

    def get(self):
        """
        gets a node based on priority if the queue isn't empty

        returns: Node
            if the queue isn't empty returns a Node object else it
            returns None.
        """
        if self.__state:
            if all(self.status.values()):
                return None
        if len(self.queue) != 0:
            sign = "<=" if self.type == "min" else ">=" if self.type == "max" else ''
            state = '' if not self.__state else 'and (not self.status[node])'
            for node in self.queue:
                if eval("(self.queue[node] %s self._top %s)" % (sign, state)):
                    self._top = self.queue[node]
                    res = node
            del self.queue[res]
            if self.__state:
                del self.status[res]
            self._top = float('inf') if self.type == 'min' else -float('inf')
            return res
        return None

    def set_status(self, node, value):
        """
        Tries to set the status of the node if state is true
        Parameters
        ----------
        node: Node
            node object to change state
        value: boolean
            value to change the node state.
        """
        assert (value == True or value == False) and (self.__state)
        self.status[node] = value

    def enqueue(self, node, value=0):
        """
        Inserts a node to the queue with the value to be used for
        prioritizing.
        Parameters
        ----------
        node: Node
            node object to insert
        value:int, float, default=0
            value to be used for prioritizing the node object.
        """
        self.queue[node] = value

    def is_empty(self):
        """
        Checks if the queue is empty
        returns
        -------
        out:boolean
            if True queue is empty else it's not.
        """
        if len(self.queue) != 0:
            return False
        return True
