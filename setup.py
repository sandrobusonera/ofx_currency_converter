#!/usr/bin/env python

from setuptools import setup

with open('setup/requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='ofx_currency_converter',
      version='0.0.1',
      author='Sandro Busonera',
      author_email='sandrobusonera@gmail.com',
      url='http://www.sandro-busonera.com',
      description='Convert all amounts of a ofx to a currency exchange rate',
      long_description=open('README.md').read(),
      install_requires=requirements,
      scripts=['ofx_currency_converter.py'],
      data_files=[('', ['templates/template.ofx', ])]
)