#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for pyqode.rst
"""
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from pyqode.rst import __version__


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        if self.pytest_args:
            self.pytest_args = self.pytest_args.replace('"', '').split(' ')
        else:
            self.pytest_args = []
        print('running test command: py.test "%s"' % ' '.join(
            self.pytest_args))
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

cmdclass = {'test': PyTest}


DESCRIPTION = 'Adds RestructuredText support to pyqode.core'


def readme():
    if 'bdist_deb' in sys.argv:
        return DESCRIPTION
    return str(open('README.rst').read())


setup(
    name='pyqode.rst',
    namespace_packages=['pyqode'],
    version=__version__,
    packages=[p for p in find_packages() if 'test' not in p],
    keywords=['RestructuredText', 'editor', 'pyqode'],
    url='https://github.com/pyQode/pyqode.rst',
    license='MIT',
    author='Colin Duquesnoy',
    author_email='colin.duquesnoy@gmail.com',
    description=DESCRIPTION,
    long_description=readme(),
    install_requires=['pyqode.core', 'restructuredtext_lint', 'docutils'],
    tests_require=['pytest-cov', 'pytest-pep8', 'pytest'],
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Text Editors :: Integrated Development Environments (IDE)'])
