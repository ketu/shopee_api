from setuptools import setup, find_packages
from codecs import open
from os import path

current_path = path.abspath(path.dirname(__file__))

with open(path.join(current_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='flash_validator',
    version='1.0.0',
    description='simple python data validation',
    long_description=long_description,
    url='https://github.com/ketu/flash_validator',
    author='ketu.lai',
    author_email='ketu.lai@gmail.com',
    license='MIT',
    keywords='python data validation',
    packages= find_packages(),
    install_requires=[],
    tests_require=[],
)
