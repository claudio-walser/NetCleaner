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
        'NetCleaner.Analyser',
        'NetCleaner.Crawler'
    ],
    install_requires=['pyyaml', 'peewee', 'PyMySQL', 'argparse', 'argcomplete'],
    entry_points={
        'console_scripts': [
            'nc-create-database = NetCleaner.ncCreateDatabase:main',
            'nc-memorize = NetCleaner.ncMemorize:main',
            'nc-server = NetCleaner.ncServer:main',
            'nc-scanner = NetCleaner.ncScanner:main'
        ]
    }
)