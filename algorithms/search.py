from Pygnet.graph import Graph

import queue


def BFS(graph, source, key=None):
    assert type(graph) == Graph 
    assert source in graph

    Q = queue.Queue(0)
    visisted = {}
    level = {}
    for node in graph:
        visisted[node] = False
    Q.put(source)
    level[source] = 0

    while not Q.empty():
        node = Q.get()
        for adj_node in node.adjacent_nodes:
            if not visisted[adj_node]:
                Q.put(adj_node)
                level[adj_node] = level[node] + 1
                if adj_node == key:
                    return {adj_node: level[adj_node]}
        visisted[node] = True
    return level





    


