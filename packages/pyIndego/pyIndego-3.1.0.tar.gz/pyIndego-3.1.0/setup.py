"""Setup for pyIndego."""
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyIndego",
    version="3.1.0",
    author="jm-73, sander1988",
    author_email="jens@myretyr.se",
    description="API for Bosch Indego mower",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jm-73/pyIndego",
    packages=find_packages("."),
    install_requires=["requests", "aiohttp", "pytz"],
    extras_require={"testing": ["pytest", "pytest-aiohttp", "pytest-cov", "mock", "pytest-asyncio"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
