#!/usr/bin/env python3

from setuptools import setup

setup(
    name='NetCleaner',
    version='0.0.1',
    description='Tool for cleanup infected network devices',
    author='Claudio Walser',
    author_email='claudio.walser@srf.ch',
    url='https://github.com/claudio-walser/NetCleaner',
    packages=[
        '.',
        'NetCleaner',
        'NetCleaner.Config',
        'NetCleaner.Analyser',
        'NetCleaner.Crawler'
    ],
    install_requires=['pyyaml'],
    entry_points={
        'console_scripts': [
            'netCleaner = NetCleaner.__main__:main'
        ]
    }
)