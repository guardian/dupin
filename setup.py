#! /usr/bin/python

from setuptools import setup

setup(name="Dupin",
      description="Search for secrets in an Organisation's Github repositories",
      version='0.0.1',
      packages=['dupin'],
      entry_points={
          'console_scripts': [
              'dupin = dupin.dupin:main'
          ]
      }
)
