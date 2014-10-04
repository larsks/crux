#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='crux',
    version='7',
    description='A tool for manipulating Keystone',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    url='http://github.com/larsks/crux',
    install_requires=open('requirements.txt').readlines(),
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'crux=crux.main:main',
        ],
    }
)
