.. PyMinimax documentation master file, created by
   sphinx-quickstart on Mon Aug  2 23:43:27 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyMinimax's documentation!
=====================================

**Package Status**

.. image:: https://readthedocs.org/projects/pyminimax/badge/?version=latest
   :target: https://pyminimax.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://github.com/beginnerSC/pyminimax/actions/workflows/test_pyminimax.yml/badge.svg
   :target: https://github.com/beginnerSC/pyminimax/actions/workflows/test_pyminimax.yml
   :alt: Continuous Integration
   

.. image:: https://codecov.io/gh/beginnerSC/pyminimax/branch/master/graph/badge.svg?token=BEE3HCNNJD
   :target: https://codecov.io/gh/beginnerSC/pyminimax
   :alt: Coverage Status


.. image:: https://img.shields.io/pypi/v/pyminimax.svg
   :target: https://pypi.python.org/pypi/pyminimax/
   :alt: PyPI


.. image:: https://static.pepy.tech/badge/pyminimax
   :target: https://pepy.tech/project/pyminimax?versions=0.1.0&versions=0.1.1&versions=0.1.2
   :alt: Downloads


.. image:: https://img.shields.io/badge/License-BSD%203--Clause-orange.svg
   :target: https://github.com/beginnerSC/pyminimax/blob/master/LICENSE
   :alt: License

----

PyMinimax is a Python implementation of Bien and Tibshirani's paper “`Hierarchical Clustering With Prototypes via Minimax Linkage
<https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4527350/>`_”[#bien2011hierarchical]_. 
This is an agglomerative hierarchical clustering algorithm available in the protoclust R package [#bien2015package]_ but not currently in SciPy nor scikit-learn. 
It has a great advantage over classical hierarchical clustering methods that in each cluster one prototype is selected from the original data. Thus the results are better interpretable. 

PyMinimax has a SciPy-compatible API. Users who are familiar with the `scipy.cluster.hierarchy <https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html>`_ module will find it easy to use. 


.. toctree::
   :maxdepth: 2
   :caption: Table of Contents
   
   quick_start
   examples
   performance
   api_ref

Reference
---------

.. [#bien2011hierarchical] \J. Bien and R. Tibshirani. Hierarchical clustering with prototypes via minimax linkage. Journal of the American Statistical Association, 106(495), 2011, 1075-1084. 
.. [#bien2015package] \J. Bien and R. Tibshirani. Package ‘protoclust’, 2015. 

