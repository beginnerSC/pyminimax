import sys, os, unittest
import numpy as np
from numpy import dtype
from numpy.testing import assert_array_equal
from scipy.spatial.distance import pdist

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyminimax import minimax, _minimax_brute_force, fcluster_prototype


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
        
    def test_fcluster_prototype(self):
        clust_proto = fcluster_prototype(self.Z1_w_proto, t=0.3, criterion='distance')
        self.assertEqual(clust_proto.dtype, dtype('int32'))
        assert_array_equal(clust_proto, 
                           [[2, 11], [3,  1], [3, 1], [2, 11], [1, 19], [3,  1], [2, 11], [5, 7], [4, 8], [1, 19], 
                            [1, 19], [2, 11], [4, 8], [4,  8], [3,  1], [2, 11], [3,  1], [4, 8], [3, 1], [1, 19]])
        
        clust_proto = fcluster_prototype(self.Z1_w_proto, t=0.7, criterion='distance')
        self.assertEqual(clust_proto.dtype, dtype('int32'))
        assert_array_equal(clust_proto, 
                           [[2, 11], [3,  1], [3, 1], [2, 11], [1, 19], [3,  1], [2, 11], [5, 7], [4, 8], [1, 19], 
                            [1, 19], [2, 11], [4, 8], [4,  8], [3,  1], [2, 11], [3,  1], [4, 8], [3, 1], [1, 19]])


if __name__ == '__main__':
    unittest.main()