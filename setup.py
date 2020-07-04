#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
import Packs


with open('README_PYPI.md', 'r') as f:
    ld = f.read()


setup(
    name="Packs",
    version=Packs__version__,
    long_description=ld,
    description="A package installer",
    long_description_content_type='text/markdown',
    author="Miguel Vieira Colombo",
    author_email="miguelhunter95@gmail.com",
    install_requires=['urllib3'],
    packages=['Packs', 'Packs/Utils'],
    entry_points = {
        'console_scripts': ['packs=Packs.main:main'],
    },
)