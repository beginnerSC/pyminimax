import setuptools


# min version following scipy

numpy_minversion = '1.6.5'
scipy_minversion = '1.6.0'
python_minversion = '3.7'

req_numpy = f'numpy>={numpy_minversion}'
req_scipy = f'scipy>={scipy_minversion}'
req_python = f'>={python_minversion}'

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pyminimax",
    version="0.1.0",
    author="BeginnerSC",
    url="https://github.com/beginnerSC/pyminimax", 
    description="Python implementation of minimax-linkage hierarchical clustering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['minimax linkage', 'prototype clustering', 'protoclust', 'hierarchical clustering', 
              'data mining', 'unsupervised learning'], 
    packages=setuptools.find_packages(),
    install_requires=[req_numpy, req_scipy],
    python_requires=req_python,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries', 
        'Topic :: Scientific/Engineering',
        'Operating System :: Microsoft :: Windows', 
        'Operating System :: POSIX :: Linux', 
        'Operating System :: POSIX', 
        'Operating System :: Unix', 
        'Operating System :: MacOS', 
    ],    
)
