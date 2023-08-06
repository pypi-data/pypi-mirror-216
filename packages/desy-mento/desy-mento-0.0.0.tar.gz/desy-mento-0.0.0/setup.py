# SPDX-FileCopyrightText: 2021 The MENTO Authors, DESY
# SPDX-FileCopyrightText: 2021 S. Vijay Kartik <vijay.kartik@desy.de>, DESY
#
# SPDX-License-Identifier: CC0-1.0

from setuptools import find_packages, setup

name = 'desy-mento'
version = '0.1'
release = '0.1.0'

setup(
    name=name,
    author='Vijay Kartik',
    author_email='vijay.kartik@desy.de',
    url='https://gitlab.desy.de/fs-sc/mento/',

    license='GPLv3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='photon science data processing analysis',

    extras_require=dict(tests=['pytest', 'pytest-cov', 'flake8']),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='~=3.7',
)
