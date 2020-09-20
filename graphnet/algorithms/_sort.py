from ..exceptions import GraphTypeError
from graphnet import VECTOR
import queue


def topological_sort(graph):
    """
    Sorts the nodes if graph type is vector
    Parameters
    ----------
    graph:Graph

    returns
    -------
    res:List
        a list containing  all the node in the graph instance
        in a sorted form
    """
    if graph.type == VECTOR:
        if not graph.is_cyclic():
            res = []
            Q = queue.Queue()
            indegree ={}
            for node in graph:
                indegree[node] = 0
            for edge in graph.edges:
                indegree[edge._to] += 1
            for node in indegree:
                if indegree[node] == 0:
                    Q.put(node)

            while not Q.empty():
                n = Q.get()
                for adj_node in n.adjacent_nodes:
                    indegree[adj_node] -= 1
                    if indegree[adj_node] == 0:
                        Q.put(adj_node)
                res.append(n)
            return res
        else:
            raise GraphTypeError("Graph contains cycle")
    else:
        raise GraphTypeError("Invalid graph type %s expected vector"%(graph.type))