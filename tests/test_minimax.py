import sys, os, unittest
import numpy as np
from numpy import dtype
from numpy.testing import assert_array_equal
from scipy.spatial.distance import pdist

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyminimax import minimax, _minimax_brute_force, fcluster_prototype, condensed_index


class TestMinimax(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n = 20
        
        np.random.seed(0)
        X = np.random.rand(cls.n, 2)
        
        cls.dist = pdist(X)
        cls.Z1_w_proto = minimax(cls.dist, return_prototype=True)
        cls.Z1         = minimax(cls.dist, return_prototype=False)
        
        cls.Z2_w_proto = _minimax_brute_force(cls.dist, return_prototype=True)
        cls.Z2         = _minimax_brute_force(cls.dist, return_prototype=False)
        
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
        
        clust_proto = fcluster_prototype(self.Z1_w_proto, t=0.7, criterion='distance')    # single cluster
        self.assertEqual(clust_proto.dtype, dtype('int32'))
        assert_array_equal(clust_proto, 
                           [[1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], 
                            [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16], [1, 16]])
        
    def test_fclust_prototype_radius(self):
        '''
        Any point should always be in the circle centered at the prototype with radius equal to the cut, 
        that is, the distance between any point and the prototype of its corresponding cluster should always be less than or equal to the cut
        '''
        for cut in [0.3, 0.35]:
            cluster_proto = fcluster_prototype(self.Z1_w_proto, t=cut, criterion='distance')
            for pt, (cluster, proto) in enumerate(cluster_proto):
                if pt != proto:
                    self.assertLessEqual(self.dist[condensed_index(self.n, pt, proto)], cut)

                    
if __name__ == '__main__':
    unittest.main()