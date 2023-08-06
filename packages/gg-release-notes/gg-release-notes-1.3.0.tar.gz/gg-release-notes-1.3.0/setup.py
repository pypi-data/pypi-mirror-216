"""Python setup.py for project_name package"""
import os
from setuptools import find_packages, setup


with open('./README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

print(os.getcwd())

# What packages are required for this module to be executed?
with open("./requirements.txt") as requirements:
    REQUIRED = requirements.read().split("\n")

with open("./requirements-test.txt") as extra_requirements:
    EXTRA_REQUIRED = extra_requirements.read().split("\n")

with open("./src/gg_release_notes/__init__.py") as f:
    release_notes_version = f.read().split("=")[1].strip().strip("'")


setup(
    name="gg-release-notes",
    version=release_notes_version,
    description="Python Interface for generating release notes for Github Actions",
    url="https://github.com/DataWiz40/gg-release-notes/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="DataWiz40",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=REQUIRED,
    extras_require={"test": EXTRA_REQUIRED },
)
