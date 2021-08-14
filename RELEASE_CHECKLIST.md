# Release Checklist

* Tags in the below files need to be updated
    * ./docs/source/conf.py:30:release = '0.0.3'
    * ./pyminimax/\__init\__.py:1:\__version\__= '0.0.3'
    * ./setup.py:17:    version="0.0.3",
    * All download badges: 
        * ./docs/source/index.rst:32:   :target: https://pepy.tech/project/pyminimax?versions=0.0.3&versions=0.0.1
        * ./README.md:8:[![Downloads](https://pepy.tech/badge/pyminimax)](https://pepy.tech/project/pyminimax?versions=0.0.3&versions=0.0.1)
        * ./README.md:9:[![Downloads](https://pepy.tech/badge/pyminimax/month)](https://pepy.tech/project/pyminimax?versions=0.0.3&versions=0.0.1)