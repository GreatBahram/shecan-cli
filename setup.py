#!/usr/bin/env python3

from sys import version_info

from setuptools import find_packages, setup

#from src.shecan import __version__

assert version_info >= (3, 6, 1), 'shecan-cli requires Python >=3.6.1'


INSTALL_DEPS = ('requests', 'bs4', 'lxml', 'tinydb', )


setup(
    name='shecan-cli',
    #version=__version__,
    version='0.1.0',
    description='Shecan CLI',
    long_description='\n\n'.join([open('README.md').read(), open('CHANGES.md').read()]),
    long_description_content_type='text/markdown',
    author='GreatBahram',
    author_email='aghaee.bahram@gmail.com',
    license='Academic Free License, version 3',
    url='https://github.com/greatbahram/shecan-cli/',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['LICENSE']},
    install_requires=INSTALL_DEPS,
    zip_safe=False,
    entry_points={
        'console_scripts':
        ['shecan = shecan.cli:shecan_cli',]
        },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
