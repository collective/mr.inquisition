from setuptools import setup, find_packages
import codecs
import os

version = '0.1'


class UltraMagicString(object):
    """ Catch-22:
    - if I return Unicode, python setup.py --long-description as well
      as python setup.py upload fail with a UnicodeEncodeError
    - if I return UTF-8 string, python setup.py sdist register
       fails with an UnicodeDecodeError

    Taken from zest.releaser.
    Adapted from http://stackoverflow.com/questions/1162338
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value.decode('utf-8')

    def __add__(self, other):
        return UltraMagicString(self.value + str(other))

    def split(self, *args, **kw):
        return self.value.split(*args, **kw)


def read(filename):
    return unicode(codecs.open(filename, encoding='utf-8').read())


long_description = u'\n\n'.join([read('README.txt'),
                                 read(os.path.join("docs", "CREDITS.txt")),
                                 read(os.path.join("docs", "HISTORY.txt")),
                                 read(os.path.join("docs", "TODO.txt")),
                                 ])


setup(name='mr.inquisition',
      version=version,
      description="A package to help with exploring a Plone site.",
      long_description=long_description,
      classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Plone",
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
