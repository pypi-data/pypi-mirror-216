#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 10:32:16 2023

@author: mariohevia
"""

from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'OcamlEC plots'
LONG_DESCRIPTION = 'Package to plot and get statistics from OcamlEC files'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="ocamlec_plt", 
        version=VERSION,
        author="Mario Hevia Fajardo",
        author_email="<m.heviafajardo@bham.ac.uk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["pandas","numpy","seaborn","matplotlib","PyPDF2",
                          "networkx","os","statistics","io","itertools"],
        # add any additional packages that 
        # needs to be installed along with your package.
        
        keywords=['python', 'ocamlec'],
        classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Science/Research",
            "License :: Free for non-commercial use",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ]
)