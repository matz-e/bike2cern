#!/usr/bin/env python

from setuptools import setup

setup(
    name='bike2cern',
    version=0.1,
    description='Sync rides from Strava to CERN Sharepoint',
    author='Matthias Wolf',
    url='https://github.com/matz-e/bike2cern',
    packages=['bike2cern'],
    install_requires=[
        'keyring',
        'pyxdg',
        'sharepoint',
        'stravalib'
    ],
    entry_points={
        'console_scripts': ['bike2cern = bike2cern.sync:run']
    }
)
