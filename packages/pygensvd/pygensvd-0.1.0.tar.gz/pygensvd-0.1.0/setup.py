import os
from setuptools import setup, find_packages
from cmake_setuptools_ext import CMakeExtension, CMakeBuild

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
cmakelists = os.path.join(PROJECT_DIR, "CMakeLists.txt")

setup(
    packages=find_packages(),
    ext_modules=[CMakeExtension("pygensvd._gsvd", cmakelists)],
    cmdclass={"build_ext": CMakeBuild},
)
