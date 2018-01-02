import unittest
from test.graph_test import TestAddEdge
from test.hit_marking_test import TestHitMarking

if __name__ == '__main__':
    unittest.main()

    suite = TestHitMarking().suite()

    unittest.TextTestRunner().run(suite)
