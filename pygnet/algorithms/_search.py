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
        uses the first node in the graph as source.
    key:int, str, float, optional
        Value of the node to stop the tranverse. if ommited the method
        stops when all  node in the graph are tranversed.
    returns
    -------
    value: list
        A list of the path traversed in order from source to key.
    """
    if key != None:
        key = graph[key]

    def dfs_traverse(node, visited, key=None):
        if key != None and key == node:
            return [node]
        
        visited[node]= True
        if len(node.adjacent_nodes) == 0:
            if key == None:
                return [node]
            else:
                return []
        res = [node]
        for adj_node in node.adjacent_nodes: 
            if visited[adj_node] == False: 
                res += dfs_traverse(adj_node, visited, key)
                if key != None:
                    if key in res:
                        break
                    else:
                        res = []
        return res
    
    visited = {node: False for node in graph}
    if source == None:
        stack = []
        for node in graph:
            if visited[node] == False: 
                res = dfs_traverse(node, visited, key)
                stack = stack + res
        return stack
    else:
        source = graph[source]
        res = dfs_traverse(source, visited, key)
        return res


            