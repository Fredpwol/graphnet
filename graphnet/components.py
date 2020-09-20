
class Node:
    """
    The Node class is used for initializing a node in a graph

    Parameters
    ----------

    value:int, str or object 
        This is the value of a node object. In graph it is used for identifying
        every node in it.
    color:str,default=None
        This specifies the color of the node instance to be displayed in a graph
        display method

    Attributes
    ----------
    value:int, str or object
    adjacent_nodes : List(Node)
        This is a list of all adjacent node object connected to the node.
    radius: int, float default:0
        The radius of the node when visualization value must be between -1 and 1.
    """

    def __init__(self, value=None, color=None):
        self.value = value
        self.adjacent_nodes = []
        self.color = "blue"
        self.__node_radius = 0

    @property
    def radius(self):
        return self.__node_radius
    
    @radius.setter
    def radius(self, value):
        if value < -1 or value > 1:
            raise ValueError("radius must be a float between -1 and 1.")
        else:
            self.__node_radius = value


    def add_node(self, node):
        """
        adds connected node in a graph to the adjacent_nodes list of the Node object.

        Parameters
        ----------
        node : Node
            node to be added to the list.
        """
        self.adjacent_nodes.append(node)

    def __eq__(self, other):
        if type(other) == type(self):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return "Node(%s)"%str(self.value)

    

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
    color:str
        This specifies the color of the node instance to be displayed in a graph
        display method
    
    Attributes
    ----------
    _from:Node
    _to:Node
    weight:str, int, float, default=None
    color:str, optional
    fontsize:int default=0
        The fontsize of the weight.
    linewidth:None, float, default=None
        Width of the line connecting nodes together.

    """

    def __init__ (self, _from, _to, weight=None, color=None):
        self.weight = weight
        self._from = _from
        self._to = _to
        self.color = "k"
        self.__fontsize = 0
        self.__linewidth = None
    
    @property
    def linewidth(self):
        return self.__linewidth
    
    @linewidth.setter
    def linewidth(self, value):
        if value < 0 or value > 1:
            raise ValueError("linewidth must be a float between 0 and 1")
        else:
            self.__linewidth = value
    
    @property
    def fontsize(self):
        return self.__fontsize
    
    @fontsize.setter
    def fontsize(self, value):
        if value < -1 or value > 1:
            raise ValueError("fontsize must be a float between -1 and 1")
        else:
            self.__fontsize = value

    
    def __repr__(self):
        return "Edge(src=%s, dest=%s, weight=%s)"%(self._from, self._to, self.weight)
