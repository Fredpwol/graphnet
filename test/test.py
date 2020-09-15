if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "pygnet"


import unittest
import numpy as np
from pygnet import Graph, Node, VECTOR
from pygnet.algorithms import dijkstra

persons = [{"name":"frank", "age":19, "sex":"M"},
            {"name": "sam", "age": 22, "sex":"M"},
            {"name":"jane", "age":21, "sex":"F"},
            {"name":"sarah", "age":34, "sex":"F"}]
class Person(Node):
    def __init__(self, name, age, sex):
        Node.__init__(self)
        self.name = name
        self.age = age
        self.sex = sex
    
    def __repr__(self):
        return "Person(name=%s, age=%s, sex=%s)"%(self.name, self.age, self.sex)


class Test(unittest.TestCase):

    def setUp(self):
        self.n = [Node(1), Node(2), Node(3), Node(4)]
        self.g = Graph()
        for node in self.n :
            self.g.add_node(node)
        self.g.add_edge(1, 3)
        self.g.add_edge(2, 4)

    def test_adjecent_matrix(self):
        shape = len(self.n)
        test_res =  np.zeros((shape, shape))
        test_res[0, 2] = 1
        test_res[1, 3] = 1
        test_res[2, 0] = 1
        test_res[3, 1] = 1
        res = self.g.graph_matrix == test_res
        self.assertTrue(np.all(res))


    def test_BFS(self):
        self.assertEqual(self.g.BFS(1), [self.g[1], self.g[3]])


    def test_iscyclic(self):
        self.g = Graph(type=VECTOR)
        for i in range(5):
            self.g.add_node(Node(i))
        self.edge_list = [(0,1),(0,2),(1,4),(1,3),(2,1),(2,3),(3,0),(4,3)]
        for x, y in self.edge_list:
            self.g.add_edge(x, y)
        self.assertTrue(self.g.is_cyclic())
    

    def test_topological_sort(self):
        self.g = Graph(type=VECTOR)
        for i in range(6):
            self.g.add_node(Node(i))
        self.edge_list = [(5,2),(5,0),(4,0),(4,1),(2,3),(3,1)]
        for x, y in self.edge_list:
            self.g.add_edge(x, y)
        sort = [node.value for node in self.g.topological_sort()]
        self.assertEqual(sort , [4,5,2,0,3,1])
    
    def test_inherit_node(self):
        self.g = Graph(ref="name")
        obj = []
        for pes in persons:
            obj.append(Person(**pes))
        self.g.add_nodes_from_iterable(obj)
        self.assertAlmostEqual(obj, self.g.get_nodes)
        

if __name__ == '__main__':
    unittest.main()
