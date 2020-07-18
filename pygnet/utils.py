import random
import copy


def check_cycle(source, visited, rec_stack):
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
    temp = copy.deepcopy(graph)
    graph = temp if not inplace else graph
    for node in graph.get_nodes:
        for neigh in node.adjacent_nodes:
            graph.remove_edge(graph.get_node_id(neigh), graph.get_node_id(node))
    if not inplace:
        return graph






class GraphPriorityQueue:

    def __init__(self, graph, type="min", state=False):
        if type == 'min' or type == 'max':
            self.type = type
        else:
            raise TypeError("type attribute most be 'min' or 'max'")
        self.graph = graph
        self._top = float('inf') if self.type == 'min' else -float('inf')       
        self.queue = dict()
        self.__state = state
        for node in self.graph:
            self.queue[node] = float('inf')
        if self.__state:
            self.status = dict()
            for node in self.graph:
                self.status[node] = False
        

    def __repr__(self):
        return str(list(self.queue.values()))



    def get(self):
        if self.__state:
            if all(self.status.values()):
                return None
        if len(self.queue) != 0:
            sign = "<=" if self.type == "min" else ">=" if self.type == "max" else ''
            state = '' if not self.__state else 'and (not self.status[node])'
            for node in self.queue:
                if eval("(self.queue[node] %s self._top %s)"%(sign, state)):
                    self._top = self.queue[node]
                    res = node
            del self.queue[res]
            if self.__state:
                del self.status[res]
            self._top = float('inf') if self.type == 'min' else -float('inf')
            return res
        return None
        
    def set_state(self, node, value):
        assert (value == True or value == False) and (self.__state)
        self.status[node] = value
    

    def enqueue(self, node , value=0):
        self.queue[node] = value

    def is_empty(self):
        if len(self.queue) !=0:
            return False
        return True




    