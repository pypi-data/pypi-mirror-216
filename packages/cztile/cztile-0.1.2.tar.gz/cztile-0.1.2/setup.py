"""Holds all relevant information for packaging and publishing to PyPI."""
from typing import List

import setuptools

# no external requirements of now
requirements: List[str] = []

VERSION = "0.1.2"

# pylint: disable=line-too-long
with open("README.md", "r", encoding="utf-8") as fh_read:
    long_description = fh_read.read()
setuptools.setup(
    name="cztile",
    version=VERSION,
    author="Nuno Mesquita",
    author_email="nuno.mesquita@zeiss.com",
    description="A set of tiling utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Note: Exclude test folder in MANIFEST.in to also remove from source dist
    # See https://stackoverflow.com/questions/8556996/setuptools-troubles-excluding-packages-including-data-files
    # See https://docs.python.org/3.6/distutils/sourcedist.html
    packages=setuptools.find_packages(exclude=["test", "test.*"]),
    license_files=["LICENSE.txt", "NOTICE.txt"],
    # Classifiers help users find your project by categorizing it.
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    # Make required Python version compliant with official TF docs (https://www.tensorflow.org/install)
    # It follows: We build a pure Python wheel
    # Note that Python used to build the sources specifies the Python version of the dist (relevant during build only)
    # See https://packaging.python.org/guides/distributing-packages-using-setuptools/#pure-python-wheels for more info
    # We also restrict the code to >3.6 to:
    # - fully benefit from type annotations (See https://realpython.com/python-type-checking/ for more info)
    # - having dataclasses natively supported (starting 3.7+)
    # - + see https://realpython.com/python-data-classes/
    # - + no need to include it as ext. pkg through backport in 3.6 (dev.to/hanpari/dataclasses-in-python-3-6-29id)
    python_requires=">3.6,<3.12",
    install_requires=requirements,
)
