"""
Graph search and tranverse algorithms.
"""
import queue
import random


def BFS(graph, source, key):
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
    source = graph[source]

    Q = queue.Queue(0)
    visited = {}
    path = []
    for node in graph:
        visited[node] = False
    if source == None:
        source = list(visited.keys())[0]
    Q.put(source)

    while not Q.empty():
        node = Q.get()
        path.append(node)
        for adj_node in node.adjacent_nodes:
            if not visited[adj_node]:
                Q.put(adj_node)
                if adj_node == key:
                    return path
        visited[node] = True
    return path


def DFS(graph, source=None, key=None):
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
        A list of the path traversed in order from source to key.
    """
    if source:
        source = graph[source]
    else:
        source = random.choice(graph.get_nodes)

    def dfs_traverse(source, key=None, visited=None):
        if key:
            if source == key:
                return [source]
            for adj_node in source.adjacent_nodes:
                res = dfs_traverse(adj_node, key)
                if res:
                    res.append(source)
                    return res
            return None
        else:
            for node in source.adjacent_nodes:
                if node in visited:
                    pass
                dfs_traverse(node, visited=visited)
            visited.append(source)

    if key != None:
        assert source != None
        for adj_node in source.adjacent_nodes:
            res = dfs_traverse(adj_node, key)
            if res:
                res.append(source)
                return res
    else:
        for node in graph:
            visisted = []
            dfs_traverse(node, visited=visisted)
        return visisted
    return None
