from Pygnet.graph import Graph

import queue


def BFS(graph, source=None, key=None):
    assert type(graph) == Graph 
    source = graph[source]

    Q = queue.Queue(0)
    visisted = {}
    path = []
    for node in graph:
        visisted[node] = False
    if source == None:
        source = list(visisted.keys())[0]
    Q.put(source)

    while not Q.empty():
        node = Q.get()
        path.append(node)
        for adj_node in node.adjacent_nodes:
            if not visisted[adj_node]:
                Q.put(adj_node)
                if adj_node == key:
                    return path
        visisted[node] = True
    return path



def DFS(graph, source=None, key=None):
    assert type(graph) == Graph 
    source = graph[source]


    def dfs_traverse(source, key=None, visisted=None):
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
                if node in visisted:
                    pass
                dfs_traverse(node, visisted=visisted)
            visisted.append(source)

    if key != None: 
        assert source != None
        for adj_node in source.adjacent_nodes:
            res = dfs_traverse(adj_node, key)
            if res:
                res.append(source)
                return res
    else:
        for node in graph:
            visisted =[]
            dfs_traverse(node, visisted=visisted)
        return visisted
    return None





    


