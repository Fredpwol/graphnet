from collections import defaultdict
from .components import Edge, Node
from .exceptions import InvalidNodeTypeError, MaxNodeError, GraphTypeError
from .utils import check_cycle
from .algorithms.search import BFS
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
        else:
            raise StopIteration
        return res


    def __getitem__(self, key):
        node = list(filter(lambda x: eval(f'x.{self.ref}') == key, self.__nodes))

        if len(node) >= 1:
            return node[0]
        else:
            raise KeyError("%s not in Graph"%(key))


    def add_node(self, node):
        if self.__len__() <= self.__max_node:
            if node not in self.__nodes:
                if type(node) == Node or issubclass(node.__class__, Node):
                    self.__nodes.append(node)
                    node_id = eval(f"node.{self.ref}")
                else:
                    raise InvalidNodeTypeError(f"Expected object of type Node or subclass of Node but {type(node)} was given.")
                self.connections[node_id] = defaultdict(int)
            else:
                raise ValueError("Node instance alerady in graph network")
        else:
            raise MaxNodeError("Graph max size exceeded, expected %d node."%(self.__max_node))


    def add_edge(self, _from, _to, weight=1):
        if len(self.connections) <= self.max_edge:
            node = self[_from]
            node_to = self[_to]
            edge =  Edge(node, node_to, weight)
            self.connections[_from][_to] = edge
            node.add_node(node_to)
            if self.type == 'scalar':
                self.connections[_to][_from] = edge
                node_to.add_node(node)
            self.edges.append(edge)
        else:
            raise  MaxNodeError("Graph max size exceeded, expected %d node."%(self.max_edge))   

    @property
    def graph_matrix(self):
        nodes = self.__nodes
        self.__adj_matrix = np.zeros((self.__len__(), self.__len__()))
        for i in range(self.__len__()):
            id_i = eval(f"nodes[{i}].{self.ref}")
            for j in range(self.__len__()):
                id_j = eval(f"nodes[{j}].{self.ref}")
                edge = self.connections[id_i][id_j] if not self.connections[id_i][id_j] else self.connections[id_i][id_j].weight
                self.__adj_matrix[i, j] = edge
        return self.__adj_matrix

    
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


    def is_connected(self):
        if self.type == 'scalar':
            traverse = BFS(self)
            for node in self.__nodes:
                if not node in traverse:
                    return False
            return True
        else:
            raise GraphTypeError("Invalid graph type %s expected scalar"%(self.type))


if __name__ == "__main__":
    g = Graph(4)
    d_g = {1:[1,3],2:[0],3:[4,1],4:[2,1]}
    g.from_dict(d_g)
    print(len(g))
    print(g.graph_matrix)