#! /usr/bin/python

from setuptools import setup

setup(name="Dupin",
      description="Search for secrets in an Organisation's Github repositories",
      version='0.0.1',
      packages=['dupin', 'dupin.trufflehog'],
      install_requires=[
          "GitPython==2.1.1",
          "PyGithub==1.34",
          "pyyaml==3.12",
          "PGPy==0.4.1"
      ],
      entry_points={
          'console_scripts': [
              'dupin = dupin.dupin:main'
          ]
      }
)
