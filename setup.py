from setuptools import setup

readme = open('README.md').read()
setup(name='HDFserver',
      version='0.1',
      author='Yohannes Libanos',
      license='MIT',
      description='REST service for HDF5 data stores',
      py_modules=['HDFserver'],
      long_description=readme,)