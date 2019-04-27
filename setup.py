#!/usr/bin/env python

import docketapi
from setuptools import setup

setup(
    name='docketapi',
    packages=['docketapi'],
    version=docketapi.__version__,
    description='Python client API for Docket',
    license='Apache-2.0',
    url='https://github.com/vesche/docket-python-client',
    author='Austin Jackson',
    author_email='vesche@protonmail.com',
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Security"
    ]
)