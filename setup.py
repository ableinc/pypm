import setuptools
import os.path as path
from pypm.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as reqs:
    dependencies = reqs.readlines()

setuptools.setup(
    name="pypm",
    version=__version__,
    author="AbleInc",
    author_email="douglas.jaylen@gmail.com",
    description="Pure python package manager for Python 3 and above, similar to npm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ableinc/pypm",
    keywords=['package manager', 'dependency manager', 'manager', 'python 3', 'cli tool', 'command line tool'],
    packages=setuptools.find_packages(),
    package_data={
      'pypm': ['pypm/data/pkg.json']
    },
    data_files=[
        ('/pypm/data', [path.join('pypm/data', 'pkg.json')])
    ],
    entry_points='''
        [console_scripts]
        pypm=pypm.cli:main
    ''',
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)