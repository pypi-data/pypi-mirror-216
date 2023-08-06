from setuptools import setup, find_packages
import os

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()

def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

setup(
    name='ProkBERT base test library',
    version=get_version("prokbert/__init__.py"),
    description='A brief description of your library',
    author='gfgfgf',
    author_email='obalasz@gmail.com',
    packages=['prokbert'],
    install_requires=[],  # Add any dependencies here
)
