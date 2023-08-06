#!/usr/bin/env python

from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()


with open("README.md", encoding="utf8") as f:
    readme = f.read()

with open("LICENSE", encoding="utf8") as f:
    license = f.read()

setup(
    name="mongeasy",
    version="0.2.4",
    author="Joakim Wassberg",
    author_email="joakim.wassberg@arthead.se",
    description="Easy to use wrapper around pymongo for easy access to MongoDB.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/artheadsweden/mongeasy",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
    ],
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
)
