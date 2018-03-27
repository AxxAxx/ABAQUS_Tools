#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='AxPy_ODB_Reader',
    version='0.1.0',
    description="Reads ABAQUS ODB files",
    long_description=readme + '\n\n' + history,
    author="Axel Johansson",
    author_email='axel.johansson10@gmail.com',
    url='https://github.com/AxxAxx/AxPy_ODB_Reader',
    packages=[
        'AxPy_ODB_Reader',
    ],
    package_dir={'AxPy_ODB_Reader':
                 'AxPy_ODB_Reader'},
    entry_points={
        'console_scripts': [
            'AxPy_ODB_Reader=AxPy_ODB_Reader.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='AxPy_ODB_Reader',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
