
class Node:
    """
    The Node class is used for initializing a node in a graph

    Parameters
    ----------

    value:int, str or object 
        This is the value of a node object. In graph it is used for identifying
        every node in it.

    Attributes
    ----------

    adjacent_nodes : List(Node)
        This is a list of all adjacent node object connected to the node.
    """

    def __init__(self, value, *args, **kwargs):
        self.value = value
        self.adjacent_nodes = []


    def add_node(self, node):
        """
        adds connected node in a graph to the adjecent_nodes list of the Node object.

        Parameters
        ----------
        node : Node
            node to be added to the list.
        """
        self.adjacent_nodes.append(node)


    def __repr__(self):
        return str(self.value)

    

class Edge:
    """
    Edge used for connecting two nodes together and serves as a link between them.

    Parameters
    ----------
    _from:Node, str
        The source point of the edge or the bottom of the edge.
    _to:Node, str
        The destination the edge stops.
    weight:str, int, float,optional,default=None
        This specifies the weights or label of the graph, by default is None
        which means the edge is unweighted,
        Note: to perfrom graph algorithm operations like pathfinding the weight 
        most be either of type interger or float.
    
    Attributes
    ----------
    _from
    _to
    weight

    """

    def __init__ (self, _from, _to, weight=None, *args, **kwargs):
        self.weight = weight
        self._from = _from
        self._to = _to

    
    def __repr__(self):
        return "Edge(src=%s, dest=%s, weight=%s)"%(self._from, self._to, self.weight)




