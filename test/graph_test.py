import unittest
from lib.graph import Graph

class TestAddEdge(unittest.TestCase):

    def test_add_edge(self):
        g = Graph()
        g.add_edge(0,1)

        self.assertTrue((0,1) in g)
        self.assertTrue((1,0) not in g)

    def test_edge_weight(self):
        g = Graph()

        g.add_edge(0,1,5)
        self.assertTrue(g.get_edge_weight(0,1) == 5)

        g.increase_edge_weight(0,1,1)
        self.assertTrue(g.get_edge_weight(0,1) == 6)

        g.increase_edge_weight(0,2,3)
        self.assertTrue(g.get_edge_weight(0,2) == 3)

    def test_remove_node(self):
        g = Graph()
        g.add_edge(0,1)
        g.add_edge(1,2)
        g.add_edge(2,3)

        g.remove_vertex(1)

        self.assertTrue((0,1) not in g)
        self.assertTrue((1,2) not in g)
        self.assertTrue((1,2) not in g)
        self.assertTrue((2,3)  in g)


    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")



    def suite():
        suite = unittest.TestSuite()
        # suite.addTest(WidgetTestCase('add_edge'))
        #
        # suite.addTest(WidgetTestCase('edge_weight'))
        return suite
