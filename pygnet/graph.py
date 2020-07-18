from collections import defaultdict
from .components import Edge, Node
from .exceptions import InvalidNodeTypeError, MaxNodeError, GraphTypeError
from .utils import check_cycle
from .algorithms.search import BFS
from ._vis.layout import plot_graph_directed, plot_graph_undirected
import matplotlib.pyplot as plt
import numpy as np



class Graph(object):

    def __init__(self, max_node=float("inf"), max_edge=float("inf"), type="scalar", ref="value" ):
        self.__max_node = max_node
        self.max_edge = max_edge
        self.type = type
        self.ref = ref
        self.edges = []
        self.connections = {}
        self.__nodes = []


    def __len__(self):
        return len(self.__nodes)


    def __iter__(self):
        self.counter = 0
        return self


    def __next__(self):
        if self.counter < self.__len__():
            res = self.__nodes[self.counter]
            self.counter += 1
            return res
        else:
            raise StopIteration


    def __getitem__(self, key):
        node = list(filter(lambda x: self.get_node_id(x) == key, self.__nodes))

        if len(node) >= 1:
            return node[0]
        else:
            raise KeyError("%s not in Graph"%(key))


    def __enter__(self):
        return self


    def __exit__(self,exc_type, exc_val, exc_tb):
        self.clear()


    def add_node(self, node):
        if self.__len__() <= self.__max_node:
            if type(node) in [str, int, float]:
                node = Node(node)
            if node not in self.__nodes:
                if type(node) == Node or issubclass(node.__class__, Node):
                    self.__nodes.append(node)
                    node_id = self.get_node_id( node)
                else:
                    raise InvalidNodeTypeError("Expected object of type str, float, int, Node or subclass of Node but %s was given."%type(node))
                self.connections[node_id] = defaultdict(int)
            else:
                raise ValueError("Node instance alerady in graph network")
        else:
            raise MaxNodeError("Graph max size exceeded, expected %d node."%(self.__max_node))


    def add_edge(self, _from, _to, weight=1):
        if len(self.connections) <= self.max_edge:
            if type(_from) == Node or issubclass(_from.__class__, Node):
                _from = self.get_node_id(_from)
            if type(_to) == Node or issubclass(_to.__class__, Node):
                _to = self.get_node_id(_to)
            node = self[_from]
            node_to = self[_to]
            edge =  Edge(node, node_to, weight)
            self.connections[_from][_to] = edge
            node.add_node(node_to)
            self.edges.append(edge)
            if self.type == 'scalar':
                edge2 = Edge(_to, _from, weight)
                self.connections[_to][_from] = edge2
                node_to.add_node(node)
                self.edges.append(edge2)
        else:
            raise  MaxNodeError("Graph max size exceeded, expected %d node."%(self.max_edge)) 


    def add_nodes_from_list(self, iterable):
        for node in iterable:
            self.add_node(node)


    @property
    def graph_matrix(self):
        nodes = self.__nodes
        self.__adj_matrix = np.zeros((self.__len__(), self.__len__()))
        for i in range(self.__len__()):
            id_i = self.get_node_id( nodes[i])
            for j in range(self.__len__()):
                id_j = self.get_node_id( nodes[j])
                edge = self.connections[id_i][id_j] if not self.connections[id_i][id_j] else self.connections[id_i][id_j].weight
                self.__adj_matrix[i, j] = edge
        return self.__adj_matrix


    @property
    def get_nodes(self):
        return self.__nodes
    

    def from_dict(self, dictonary, weights=1):
        for key in dictonary:
            node = Node(key)
            self.add_node(node)
            for edge in dictonary[key]:
                if edge in dictonary.keys():
                    self.add_edge(key, edge, weights)
                else:
                    raise KeyError("Edge %s not in dictionary."%(edge))



    def is_cyclic(self):
        if self.type != 'vector':
            raise GraphTypeError("cyclic check only works for vector type graphs")
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
        self.__nodes.clear()
        self.connections = {}
        self.edges.clear()


    def is_connected(self):
        if self.type == 'scalar':
            traverse = BFS(self)
            for node in self.__nodes:
                if not node in traverse:
                    return False
            return True
        else:
            raise GraphTypeError("Invalid graph type %s expected scalar"%(self.type))

    
    def display(self, weighted=False):
        _, ax1 = plt.subplots(1 ,figsize=(20, 15))
        if self.type == "vector":
            plot_graph_directed(self, ax1, len(self), weighted)
        else:
            plot_graph_undirected(self, ax1, len(self), weighted)


    
    def remove_edge(self, _from, _to):
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
        for vertex in self.__nodes:
            if vertex == node:
                v = node
                break
        return eval('v.%s'%self.ref)






