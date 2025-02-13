# -*- coding: utf-8 -*-
"""
Created on Fri May  5 12:50:11 2023

@author: rohit.trivedi
"""

from setuptools import setup, find_packages

setup(
    name='StoreNet',
    version='1.0',
    description='Software to download, process and plot data',
    maintainer='Rohit Trivedi',
    maintainer_email='rohit.trivedi@ierc.ie',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'pandas==1.2.4',
        'numpy==1.20.1',
        'h5py==2.10.0',
        'matplotlib==3.3.4',
        'pytz==2021.1',
        'plotly==5.12.0'
    ]
)
