# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = '0.2'

long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
    )

setup(name='mr.inquisition',
      version=version,
      description="A package to help with exploring a Plone site.",
      long_description=long_description,
      classifiers=[
          "Intended Audience :: Developers",
          "Framework :: Plone",
          "Framework :: Plone :: 3.3",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.4",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='information objects plone',
      author='Mark van Lent',
      author_email='mark@vlent.nl',
      url='https://github.com/collective/mr.inquisition',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mr'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target=plone
      """,
      )
