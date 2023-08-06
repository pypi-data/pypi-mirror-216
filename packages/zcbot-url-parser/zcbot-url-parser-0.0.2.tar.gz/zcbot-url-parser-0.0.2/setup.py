from distutils.core import setup
from setuptools import find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(name='zcbot-url-parser',
      version='0.0.2',
      description='zcbot url parser for zsodata',
      long_description=long_description,
      author='zsodata',
      author_email='team@zso.io',
      url='http://www.zsodata.com',
      install_requires=['requests'],
      python_requires='>=3.7',
      license='BSD License',
      packages=find_packages(),
      platforms=['all'],
      include_package_data=True
      )
