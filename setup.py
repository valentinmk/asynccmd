# Copyright (c) 2016-present Valentin Kazakov
#
# This module is part of asyncpg and is released under
# the Apache 2.0 License: http://www.apache.org/licenses/LICENSE-2.0

import os
import re
from setuptools import setup

install_requires = []
tests_require = install_requires + ['pytest']
extras_require = {}

def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), 'asynccmd', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in asynccmd/__init__.py')

long_description = open('README.rst').read()

classifiers = [
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Microsoft :: Windows',
    'Environment :: Console',
    'Development Status :: 3 - Alpha',
    'Topic :: System :: Shells',
]

setup(name='asynccmd',
      version=read_version(),
      description='Asyncio implementation of Cmd Python lib.',
      long_description=long_description,
      classifiers=classifiers,
      platforms=['POSIX', 'Microsoft :: Windows'],
      author='Valentin Kazakov',
      author_email='vkazakov@gmail.com',
      url='https://github.com/valentinmk/asynccmd',
      download_url='https://github.com/valentinmk/asynccmd',
      license='Apache 2',
      packages=['asynccmd'],
      install_requires=install_requires,
      extras_require=extras_require,
)
