from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fandanGO-core',
    version='0.1.0',
    description='Core plugin of the FandanGO application',
    long_description=long_description,
    author='CNB-CSIC, Carolina Simon, Irene Sanchez',
    author_email='carolina.simon@cnb.csic.es, isanchez@cnb.csic.es',
    packages=find_packages(),
)
