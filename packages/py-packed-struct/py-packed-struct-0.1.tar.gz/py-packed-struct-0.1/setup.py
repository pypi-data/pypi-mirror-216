#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


required_packages = ["bitstruct"]
setup(
    name="py-packed-struct",
    version=0.1,
    author="Luca Macavero",
    author_email="luca.macavero@gmail.com",
    maintainer="Luca Macavero",
    maintainer_email="luca.macavero@gmail.com",
    url="https://github.com/lu-maca/py-packed-struct",
    description="An implementation of C-like packed structures in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    packages=find_packages(),
    setup_requires=["wheel"] + required_packages,
    install_requires=required_packages,
    include_package_data=True,
)
