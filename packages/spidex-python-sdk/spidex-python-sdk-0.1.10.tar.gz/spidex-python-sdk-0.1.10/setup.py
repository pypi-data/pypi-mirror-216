import os
from setuptools import setup, find_packages

with open(
    os.path.join(os.path.dirname(__file__), "requirements.txt"), "r"
) as fh:
    requirements = fh.readlines()

name = "spidex-python-sdk"
description = "This is a lightweight library for Spidex API."
url = "https://github.com/hellosoldier/spidex-api"
author_email = "404260423@qq.com"
author = "spx"
license="MIT"

version = "0.1.10"

about = {}

# with open("REST_API.md", "r") as fh:
#     about["long_description"] = fh.read()

root = os.path.abspath(os.path.dirname(__file__))

setup(
    name=name,
    version=version,
    license="MIT",
    description=description,
    long_description_content_type="text/markdown",
    AUTHOR=author,
    url=url,
    keywords=["Spidex API"],
    include_package_data=True,
    install_requires=[req for req in requirements],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)


# python setup.py bdist_wheel