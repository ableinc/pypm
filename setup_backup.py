import setuptools
import os.path as path
from pypm.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypm2",
    version=__version__,
    author="AbleInc",
    author_email="douglas.jaylen@gmail.com",
    description="Python package manager for projects running Python3.6 and above.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ableinc/pypm",
    keywords=['package manager', 'dependency manager', 'manager', 'python 3', 'cli tool', 'command line tool'],
    packages=setuptools.find_packages(),
    package_data={
      'pypm': ['pypm/data/pkg.json', 'pypm/data/pyproject.toml', 'pypm/data/setup.cfg', 'pypm/data/setup.py']
    },
    data_files=[
        ('/pypm/data', [path.join('pypm/data', 'pkg.json')]),
        ('/pypm/data', [path.join('pypm/data', 'pyproject.toml')]),
        ('/pypm/data', [path.join('pypm/data', 'setup.cfg')]),
        ('/pypm/data', [path.join('pypm/data', 'setup.py')])
    ],
    entry_points='''
        [console_scripts]
        pypm=pypm.cli:cli
    ''',
    install_requires=['Click==7.0',  'stdlib-list==0.7.0'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)