import unittest
from avg import avg

class Tests(unittest.TestCase):

    def test_1(self):
        """Test avg with an empty list"""
        self.assertEqual(avg([]), 0)

    def test_2(self):
        """Test lists with a single element"""
        self.assertEqual(avg([-3]), -3)
        self.assertEqual(avg([0]), 0)
        self.assertEqual(avg([3]), 3)
    
    def test_3(self):
        """Test lists with two elements"""
        self.assertEqual(avg([1,2]), 1.5)
        self.assertEqual(avg([-1,1]), 0)
    
    def test_4(self):
        """Test with lists containing more than two elements"""
        self.assertEqual(avg([1,2,4,8]), 3.75)
        self.assertEqual(avg([2,2,4,8]), 4)
        self.assertEqual(avg(list(range(101))), 50)
    


if __name__ == '__main__':
    unittest.main()

