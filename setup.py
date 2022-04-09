# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="mailxtract",
    version="0.1.0",
    description="High-level tool tp extract data from your emails",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.joffreybvn.be/mailxtract",
    author="Joffrey Bienveni",
    author_email="joffreybvn@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(exclude=['docs', 'notebooks', 'scripts', 'tests']),
    include_package_data=False,
    install_requires=[]
)
