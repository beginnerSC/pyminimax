# PyMinimax

[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/beginnerSC/pyminimax)
[![Documentation Status](https://readthedocs.org/projects/pyminimax/badge/?version=latest)](https://pyminimax.readthedocs.io/en/latest/?badge=latest)
[![build](https://github.com/beginnerSC/pyminimax/actions/workflows/test_pyminimax.yml/badge.svg)](https://github.com/beginnerSC/pyminimax/actions/workflows/test_pyminimax.yml) 
[![codecov](https://codecov.io/gh/beginnerSC/pyminimax/branch/master/graph/badge.svg?token=BEE3HCNNJD)](https://codecov.io/gh/beginnerSC/pyminimax)
[![image](http://img.shields.io/pypi/v/pyminimax.svg)](https://pypi.python.org/pypi/pyminimax/)
[![Downloads](https://pepy.tech/badge/pyminimax)](https://pepy.tech/project/pyminimax)
[![Downloads](https://pepy.tech/badge/pyminimax/month)](https://pepy.tech/project/pyminimax)


PyMinimax is a python package that performs minimax linkage hierarchical clustering. 

## Installation

```bash
pip install pyminimax
```    

## Usage

```python
from pyminimax import minimax
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import complete

data = [[0, 0], [0, 1], [1, 0], [0, 4], [0, 3], [1, 4], [4, 0], [3, 0], [4, 1], [4, 4], [3, 4], [4, 3]]

dist = pdist(data)              # flattened distance matrix computed by scipy

Z_complete = complete(dist)     # complete linkage result
Z_minimax = minimax(dist)       #  minimax linkage result
```

There is only one function in PyMinimax, `pyminimax.minimax`, and its usage is exactly the same as the hierarchical clusterings in SciPy, say [scipy.cluster.hierarchy.complete](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.complete.html). See the [documentation](https://pyminimax.readthedocs.io/en/latest/) for more details and examples. 
