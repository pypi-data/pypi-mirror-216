#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 10:32:16 2023

@author: mariohevia
"""

from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'OcamlEC plots'
LONG_DESCRIPTION = 'Package to plot and get statistics from OcamlEC files'

# Setting up
setup(
       # the name must match the folder name 'ocamlec_plt'
        name="ocamlec_plt", 
        version=VERSION,
        author="Mario Hevia Fajardo",
        author_email="<m.heviafajardo@bham.ac.uk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["pandas","numpy","seaborn","matplotlib","PyPDF2",
                          "networkx"],
        # add any additional packages that 
        # needs to be installed along with your package.
        
        keywords=['python', 'ocamlec'],
        classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Education",
            "License :: Free for non-commercial use",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Topic :: Scientific/Engineering :: Visualization"
        ]
)