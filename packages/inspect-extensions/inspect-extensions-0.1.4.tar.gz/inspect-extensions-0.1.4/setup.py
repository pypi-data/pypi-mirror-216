# python
# -*- coding: utf-8 -*-

"""Setup module for inspect extensions.

Since:
    2020/04/22

Authors:
    - Daniel Cosmo Pizetta <daniel.pizetta@usp.br>
"""

import codecs
import os
import re

from setuptools import find_packages, setup


def find_version(*file_paths):
    """Find version in a Python file, searching for the __version__."""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def read(*parts):
    """Read files."""
    # intentionally *not* adding an encoding option to open, See:
    # https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()


_long_description = read('README.rst')
_version = find_version("inspect_extensions.py")

_classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Customer Service',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Documentation',
    'Topic :: Software Development :: Bug Tracking',
    'Topic :: Software Development :: Documentation',
    'Topic :: Software Development :: Debuggers',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Testing',
    'Topic :: Terminals']

_requires = ['termcolor']
_entry_points = {"console_scripts": ["inspect-extensions=inspect_extensions:main",
                                     "insp-ext=inspect_extensions:main"]}

setup(name='inspect-extensions',
      version=_version,
      description='Extensions for Python inspect module.',
      long_description=_long_description,
      long_description_content_type='text/x-rst',
      license='MIT',
      license_file='LICENSE.rst',
      author='Daniel Cosmo Pizetta',
      author_email='daniel.pizetta@usp.br',
      maintainer='Daniel Cosmo Pizetta',
      maintainer_email='daniel.pizetta@usp.br',
      py_modules=['inspect_extensions'],
      classifiers=_classifiers,
      install_requires=_requires,
      include_package_data=True,
      entry_points=_entry_points,
      url='https://github.com/dpizetta/inspect-extensions',
      project_urls={
          "Issues": "https://github.com/dpizetta/inspect-extensions/issues",
          "Docs": "https://inspect-extensions.readthedocs.io/en/stable/index.html",
      }
      )
