#!/usr/bin/env python

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

setup(

    ### Metadata

    name='pyclamp',

    version='0.0.2',

    description='Time series recordings analysis in Python with UI similar to pCLAMP.',

    long_description=(HERE / "README.md").read_text(),
    long_description_content_type = "text/markdown",

    url='https://github.com/marcel-goldschen-ohm/pyCLAMP',

    download_url='',

    license='MIT',

    author='Marcel Goldschen-Ohm',
    author_email='goldschen-ohm@utexas.edu',

    maintainer='Marcel Goldschen-Ohm',
    maintainer_email='goldschen-ohm@utexas.edu',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering'
    ],

    ### Dependencies

    install_requires=[
        'PyQt6',
        'numpy',
        'scipy',
        'lmfit',
        'pyqtgraph',
        'qtawesome'
    ],

    ### Contents

    packages=find_packages()
    )
