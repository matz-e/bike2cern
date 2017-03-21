#!/usr/bin/env python

from setuptools import setup

setup(
    name='bike2cern',
    version='0.1.1',
    description='Sync rides from Strava to CERN Sharepoint',
    author='Matthias Wolf',
    author_email='m@sushinara.net',
    url='https://github.com/matz-e/bike2cern',
    download_url='https://github.com/matz-e/bike2cern/archive/0.1.1.tar.gz',
    keywords=['strava'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
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
