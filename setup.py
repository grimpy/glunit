#!/usr/bin/env python3
from setuptools import setup

setup(name='glunit',
      version='0.1',
      description='Gitlab Xunit lister',
      author='Jo De Boeck',
      author_email='deboeck.jo@gmail.com',
      url='http://github.com/grimpy/glunit',
      install_requires=['requests', 'flask', 'git+https://github.com/ahmedelsayed-93/junit2html'],
      packages=['glunit'],
      )
