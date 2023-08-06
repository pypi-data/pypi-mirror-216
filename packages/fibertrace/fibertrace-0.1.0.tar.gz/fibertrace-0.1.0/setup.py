from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fibertrace",
    version="0.1.0",
    author="ByteSentinel.io",
    author_email="dev@bytesentinel.io",
    description="A library for simple logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bytesentinel-io/fibertrace.py",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)