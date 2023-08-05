from setuptools import find_packages, setup

with open("VERSION", "r") as version_file:
    version = version_file.read().strip()

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name='lib_preprocessing_REMLA23_team2',
    packages=find_packages(),
    version=version,
    description='Library for preprocessing the data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='remla23_team2',
    license='MIT',
)