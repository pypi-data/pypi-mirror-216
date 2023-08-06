#!/usr/bin/env python3
"""Description:

Setup script for Peak-based Enhancement Analysis Pipeline for MeRIP-Seq

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file LICENSE included with
the distribution).
"""

import sys
import os
import re
from setuptools import setup, Extension
import subprocess
import sysconfig

# get PEALS version
exec(open("PEALS/io/constant.py").read())

# classifiers
classifiers =[\
              'Environment :: Console',
              'Intended Audience :: Developers',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: BSD License',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Topic :: Scientific/Engineering :: Bio-Informatics',
              'Programming Language :: Python :: 3.8', ]

installRequires = [ "numpy>=1.21.2",
                     "pandas>=1.1.4",
                     "scipy>=1.7.1",
                     "pysam>=0.16.0.1",
                     "psutil>=5.9.4",
                     "pyBigWig>=0.3.18",
                     "tqdm>=4.64.1",
                     "rpy2>=3.4.5",
                     "mpmath>=1.1.0",
                     "findpeaks>=2.4.6",
                     "csaps>=1.1.0",
                     "bottleneck>=1.3.2",
                     "scikit-learn>=0.24.2",
                     "networkx>=2.5.1",
                     "fisher>=0.1.10",
                     "setuptools>=45.2.0",
                     "pytest>=5.4.1"
                    ]

testsRequires = [ 'pytest' ]


def main():
    if sys.version_info < (3,8):
        sys.stderr.write("CRITICAL: Python version must >= 3.8!\n")
        sys.exit(1)

    with open("README.md", "r") as fh:
        longDescription = fh.read()

    setup( name = "PEALS",
           version = VERSION,
           description = "Peak-based Enhancement Analysis Pipeline for MeRIP-Seq",
           long_description = longDescription,
           long_description_content_type = "text/markdown",
           include_package_data=True,
           author = 'Keren Zhou',
           author_email = 'zhoukr062@gmail.com',
           url = 'http://github.com/kerenzhou062/PEALS/',
           package_dir = {'PEALS' : 'PEALS'},
           packages = ['PEALS', 'PEALS.io', 'PEALS.collection', 'PEALS.peak', 'PEALS.stats', 'PEALS.subcmd'],
           package_data = {'PEALS.stats':['*.R']},
           scripts = ['bin/peals', ],
           classifiers = classifiers,
           install_requires = installRequires,
           setup_requires = installRequires,
           tests_require = testsRequires,
           python_requires = '>=3.8' )

if __name__ == '__main__':
    main()
