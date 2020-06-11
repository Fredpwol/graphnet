from Pygnet.components import Edge

class Graph:

    def __init__(self, max_node=float("inf"), max_edge=float("inf"), graph_type="scalar", ref="value" ):
        self.max_node = max_node
        self.max_edge = max_edge
        self.graph_type = graph_type
        self.ref = ref
        self.connections = {}
        self.__nodes = []
        self.__adj_matrix = []
    
    
    def add_node(self, node):
        if node not in self.__nodes:
            self.__nodes.append(node)
            node_id = eval(f"node.{self.ref}")
            self.connections[node_id] = {}
        else:
            raise ValueError("Node instance alerady in graph network")


    def add_edge(self, _from, _to, weight=1):
        try:
            self.connections[_from][_to] = Edge(_from, _to, weight)

        except KeyError:
            print(f"Error node {_from} not in graph network")
            return None
    

    @property
    def graph_matrix(self):
        pass