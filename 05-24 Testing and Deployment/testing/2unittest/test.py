import unittest
from moretest import Tests as Tests2
from avg import avg

class Tests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(avg([3, 5]), 4)
        self.assertEqual(avg([-1, 1]), 0)
    
    def test_2(self):
        self.assertEqual(avg([1, 2, 3, 4, 5]), 3)
        self.assertEqual(avg([1, 2]), 1.5)
    
    def test_3(self):
        self.assertGreater(avg([4, 5, 6]), avg([1, 2, 3]))

    def test_4(self):
        self.assertEqual(avg(range(1000001)), 500000)
    
    def test_5(self):
        self.assertEqual(avg([4]), 4)
    
    def test_6(self):
        self.assertRaises(ZeroDivisionError, avg, [])

unittest.main()
