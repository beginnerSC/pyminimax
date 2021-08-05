import setuptools


# min version following scipy

np_minversion = '1.16.5'
python_minversion = '3.7'

req_np = f'numpy>={np_minversion}'
req_py = f'>={python_minversion}'

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pyminimax",
    version="0.0.1",
    author="BeginnerSC",
    description="Python implementation of minimax linkage in hierarchical clustering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[req_np],
    python_requires=req_py,    
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
