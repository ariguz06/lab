import unittest

from src import graph
from src.graph import Graph

class MyTestCase(unittest.TestCase):

    def test_star(self):
        self.graph = Graph(adjacency_dict={1: [2, 3, 5], 2: [6, 5, 3]})
        self.assertEqual(self.graph.star(self.graph.g, 1), {1: [2,3,5]})

    def test_to_list(self):
        self.test_dict: dict[int, list[int]] = {4: [3,2,0,1]}
        self.list = Graph.dict_to_list(self.test_dict)

        self.assertEqual([4,3,2,0,1], self.list)

if __name__ == '__main__':
    unittest.main()
