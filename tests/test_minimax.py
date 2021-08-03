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
    assert_array_equal(minimax(dists), _minimax_brute_force(dists))