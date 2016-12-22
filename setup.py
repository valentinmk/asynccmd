# TBD
from setuptools import setup

install_requires = ['asyncio']

tests_require = install_requires + ['pytest']


classifiers = [
    'License :: OSI Approved ::  Apache Software License',
    'Programming Language :: Python :: 3.5',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Environment :: Console',
    'Development Status :: 1 - Beta',
    'Topic :: System',
]


setup(name='asynccmd',
      version='0.1.0',
      description=('Async implementation of cmd Python lib.'),
      long_description='Async implementation of cmd Python lib.',
      classifiers=classifiers,
      platforms=['POSIX', 'Microsoft :: Windows'],
      author='Valentin Kazakov',
      author_email='vkazakov@gmail.com',
      url='https://github.com/valentinmk/asynccmd',
      download_url='https://github.com/valentinmk/asynccmd,
      license='Apache 2',
      packages=['asynccmd'],
      install_requires=install_requires,
      extras_require=extras_require,
      include_package_data=True)
