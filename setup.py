from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='mr.inquisition',
      version=version,
      description="A package to help with exploring a Plone site.",
      long_description=(
          open("README.txt").read() + "\n" +
          open(os.path.join("docs", "CREDITS.txt")).read() + "\n" +
          open(os.path.join("docs", "HISTORY.txt")).read()),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Mark van Lent',
      author_email='m.van.lent@zestsoftware.nl',
      url='http://github.com/markvl/mr.inquisition',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mr'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
