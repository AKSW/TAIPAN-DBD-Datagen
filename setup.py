# -*- coding: utf-8 -*-
"""setup.py for the opentablebench project."""
from setuptools import find_packages, setup

setup(
    name='opentablebench',
    version="1.0",
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        "SPARQLWrapper",
        "nltk",
        "numpy",
        "palmettopy",
        "lovlabelfetcherpy"
    ],
)
