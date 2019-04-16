from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='prestashop-connector',
    version='1.0',

    description='Prestashop api connector for python',
    long_description=long_description,

    url='https://github.com/subteno-it/presta_connect',

    author='Subteno IT',
    author_email='hyacinthe.herve@subteno-it.fr',

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='prestashop api',
    py_modules=["prestashop-connector"],
    install_requires=['requests', 'xmltodict'],
)