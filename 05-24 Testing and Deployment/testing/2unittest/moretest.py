import unittest
from avg import avg

class Tests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(avg([3, 5]), 4)
        self.assertEqual(avg([-1, 1]), 0)
    
    def test_2(self):
        self.assertEqual(avg([1, 2, 3, 4, 5]), 3)
        self.assertEqual(avg([1, 2]), 1.5)
    
    
