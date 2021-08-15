import sys, os, unittest
import numpy as np
from numpy.testing import assert_array_equal
from scipy.spatial.distance import pdist

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyminimax import minimax, _minimax_brute_force


class TestMinimax(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        np.random.seed(0)
        X = np.random.rand(20, 2)
        dists = pdist(X)

        cls.Z1_w_proto = minimax(dists, return_prototype=True)
        cls.Z1         = minimax(dists, return_prototype=False)
        
        cls.Z2_w_proto = _minimax_brute_force(dists, return_prototype=True)
        cls.Z2         = _minimax_brute_force(dists, return_prototype=False)
        
    def test_minimax(self):
        assert_array_equal(self.Z1_w_proto, self.Z2_w_proto)
        assert_array_equal(self.Z1, self.Z2)
        
    def test_return_size(self):
        self.assertEqual(self.Z1_w_proto.shape[1], 5)
        self.assertEqual(self.Z1.shape[1], 4)
        
        
if __name__ == '__main__':
    unittest.main()