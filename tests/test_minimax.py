import sys, os
import numpy as np
from numpy.testing import assert_array_equal
from scipy.spatial.distance import pdist

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyminimax import minimax, _minimax_brute_force

def test_minimax():
    np.random.seed(0)
    X = np.random.rand(20, 2)
    dists = pdist(X)
    
    # test return_prototype=True
    Z1 = minimax(dists, return_prototype=True)
    Z2 = _minimax_brute_force(dists, return_prototype=True)
    
    assert_array_equal(Z1, Z2)
    
    # test return_prototype=False
    Z1 = minimax(dists, return_prototype=False)
    Z2 = _minimax_brute_force(dists, return_prototype=False)
    
    assert_array_equal(Z1, Z2)
    
    
if __name__ == "__main__":
    test_minimax()