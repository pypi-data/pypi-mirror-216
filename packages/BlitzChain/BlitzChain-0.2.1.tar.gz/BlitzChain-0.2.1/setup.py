from setuptools import setup, find_packages

from pathlib import Path
from blitzchain import __version__


setup(
    name='BlitzChain',
    version=__version__,
    url='https://github.com/mr-gpt/blitzchain',
    author='Twilix',
    author_email='jacky@twilix.io',
    description='BlitzChain',
    packages=find_packages(),    
    install_requires=['requests'],
    # long_description=long_description,
)
