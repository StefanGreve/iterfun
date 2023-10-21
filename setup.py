#!/usr/bin/env python3

import glob
import os
from typing import List, Optional

from setuptools import Extension, find_packages, setup

#region helper functions

def read_file(path: str, split: Optional[bool]=False) -> str | List[str]:
    with open(path, mode="r", encoding="utf-8") as file_handler:
        return file_handler.readlines() if split else file_handler.read()

sources = glob.glob("src/*.c")
optimization_flags = "/O2" if os.name == "nt" else "-O3"

#endregion

setup(
    author="StefanGreve",
    author_email="greve.stefan@outlook.jp",
    name="iterfun",
    version="0.1.0",
    description="Implements an eager iterator class reminiscent of Elixir's Enum structure.",
    license="MIT",
    url="https://github.com/StefanGreve/iterfun",
    project_urls={
        "Documentation": "https://github.com/StefanGreve/iterfun/blob/master/README.md",
        "Source Code": "https://github.com/StefanGreve/iterfun",
        "Bug Reports": "https://github.com/StefanGreve/iterfun/issues",
    },
    python_requires=">=3.12",
    install_requires=read_file("requirements/release.txt", split=True),
    extras_require={
        "dev": read_file("requirements/development.txt", split=True)[1:],
    },
    ext_modules = [
        Extension("iterfun", sources=sources, extra_compile_args={optimization_flags})
    ],
    include_package_data=True,
    package_dir={
        "": "src"
    },
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: C",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    keywords="utils, functional programming, functools, itertools, extension",
)
