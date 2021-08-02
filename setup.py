import setuptools

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
)