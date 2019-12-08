from setuptools import setup, find_packages

setup(
  name = 'gameoflife',
  version = '0.0.1',
  package_dir = {'': 'lib'},
  packages = [ 'gameoflife', 'gameoflife.scripts' ],
  install_requires=[
    'Click',
    'preconditions',
  ],
  entry_points = {'console_scripts': [
    'gameoflife=gameoflife.scripts.gameoflife:cli',
  ]}
)
