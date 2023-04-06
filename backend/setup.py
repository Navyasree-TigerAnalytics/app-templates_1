import os
import os.path as op
from setuptools import PEP420PackageFinder
from distutils.core import setup

ROOT = op.dirname(op.abspath(__file__))
SRC = op.join(ROOT, "src")

setup(
    name="discount_app",
    version="0.1.1",
    package_dir={"": "src"},
    description="DS Templates",
    author="Tiger Analytics",
    packages=PEP420PackageFinder.find(where=str(SRC)),
)
