from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='aniya',
    version='1.0.0rc1',
    author='cheer',
    author_email='cheerxiong0823@163.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xccx0823/aniya",
    description='aniya is a compact, simple defined parameter check package.',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
