import unittest
from algorithms.HIT_MARKING import HIT_MARKING

class TestHitMarking(unittest.TestCase):

    def test_request(self) :

        algo = HIT_MARKING(5)

        faults = 0
        faults += algo.request(0)
        faults += algo.request(1)
        faults += algo.request(2)
        faults += algo.request(3)
        faults += algo.request(4)
        faults += algo.request(5)

        print 'faults = ', faults

        unittest.assertTrue(faults == 6)
