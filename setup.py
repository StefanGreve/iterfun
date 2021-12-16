#!/usr/bin/env python3

import re
import sys

from setuptools import find_packages, setup

print("reading meta data")

with open("src/iterfun/__init__.py", encoding='utf-8') as file_handler:
    lines = file_handler.read()
    version = re.search(r'__version__ = "(.*?)"', lines).group(1)
    package_name = re.search(r'package_name = "(.*?)"', lines).group(1)
    python_major = int(re.search(r'python_major = "(.*?)"', lines).group(1))
    python_minor = int(re.search(r'python_minor = "(.*?)"', lines).group(1))

if package_name == 'iterfun':
    print("\033[93mWARNING: You should rename the default package name.\033[0m")

try:
    assert sys.version_info >= (int(python_major), int(python_minor))
except AssertionError:
    raise RuntimeError("\033[91mWeather requires Python %s.%s+ (You have Python %s)\033[0m" % (python_major, python_minor, sys.version))

print("reading dependency file")

with open("requirements/release.txt", mode='r', encoding='utf-8') as requirements:
    packages = requirements.read().splitlines()

with open("requirements/dev.txt", mode='r', encoding='utf-8') as requirements:
    dev_packages = requirements.read().splitlines()

print("reading readme file")

with open("README.md", mode='r', encoding='utf-8') as readme:
    long_description = readme.read()

print("running %s's setup routine" % package_name)

setup(
    author='StefanGreve',
    author_email="greve.stefan@outlook.jp",
    name=package_name,
    version=version,
    description="Implements an iterator interface reminscent of languages such as Elixier of F#.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url="https://github.com/StefanGreve/iterfun",
    project_urls={
        'Documentation': "https://github.com/StefanGreve/iterfun/blob/master/README.md",    #TODO: Add proper documention
        'Source Code': "https://github.com/StefanGreve/iterfun",
        'Bug Reports': "https://github.com/StefanGreve/iterfun/issues",
        'Changelog': "https://github.com/StefanGreve/iterfun/blob/master/CHANGELOG.md"
    },
    python_requires=">=%d.%d" % (python_major, python_minor),
    install_requires=packages,
    extra_requires={
        'dev': dev_packages[1:],
        'test': ['pytest']
    },
    include_package_data=True,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
    keywords="utils, functional programming, functools, itertools, extension",
)
