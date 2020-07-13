import queue


def BFS(graph, source=None, key=None):
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
    source = graph[source]


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
            visisted =[]
            dfs_traverse(node, visited=visisted)
        return visisted
    return None




    


