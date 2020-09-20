import random
import copy


def check_cycle(source, visited, rec_stack):
    """
    checks if a circle exists from the source node in
    the graph.
    Parameters
    ----------
    visited: list
        list of all node already visited.
    rec_stack: dict
        A dictionary of all nodes mapped with boolean
        values which is the state if a node have been
        visited in the recursion stack.
    """
    visited[source] = True
    rec_stack[source] = True
    for adj_node in source.adjacent_nodes:
        if adj_node == source:
            return True
        elif rec_stack[adj_node]:
            return True
        elif not visited[adj_node]:
            if check_cycle(adj_node, visited, rec_stack):
                return True

    rec_stack[source] = False
    return False


def remove_all_loops(graph, inplace=False):
    """
    Removes all loop edges in the graphs
    Parameters
    ----------
    graph: Graph
    inplace: boolean
        if true modifies the graph object passed in
        else returns a new graph object
    returns
    -------
    out: Graph
        A copy of the graph passed in but without loops,
        if inplace is False
    """
    temp = copy.deepcopy(graph)
    graph = temp if not inplace else graph
    for node in graph.get_nodes:
        for neigh in node.adjacent_nodes:
            graph.remove_edge(graph.get_node_id(neigh), graph.get_node_id(node))
    if not inplace:
        return graph






    