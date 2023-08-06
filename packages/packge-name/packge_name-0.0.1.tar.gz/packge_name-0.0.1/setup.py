from setuptools import setup
from setuptools import find_packages

with open("README.md", 'r') as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requiriments = f.read().splitlines()

setup(
    name = 'packge_name',
    version = '0.0.1',
    author='Peter Douglas',
    description='Image Processing Package using Skimage',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url="https://github.com/petersousa/image-processing-package.git",
    package_dir={"": "image_processing"},
    packages=find_packages(where='image_processing'),
    install_requires=requiriments,
    python_requires='>=3.8'
)