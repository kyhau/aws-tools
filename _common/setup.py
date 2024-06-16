import os

from setuptools import find_packages, setup

base_dir = os.path.dirname(__file__)
__author__ = "Kay Hau"
__email__ = "virtualda@gmail.com"
__title__ = "helper"
__version__ = "0.1.0.dev0"
__summary__ = "This package includes some common functions for local development"
__uri__ = "https://github.com/kyhau/aws-tools/"

__requirements__ = [
    "boto3==1.34.127",
    "click==8.1.7",
    "docker==7.1.0",
    "InquirerPy==0.3.4",
    "prompt-toolkit>=3.0.13",  # required by InquirerPy, pinned by Snyk to avoid a vulnerability
    "pyyaml==6.0.1",
    "toml==0.10.2",
]

__entry_points__ = {
    "console_scripts": [
        "helper = helper:main",
        "dockerc = helper.docker:find_non_running_containers",
        "dockeri = helper.docker:find_dangling_images",
    ]
}

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3 :: Only",
]

setup(
    author=__author__,
    author_email=__email__,
    classifiers=CLASSIFIERS,
    # data_files parameter is only required for files outside the packages, used in conjunction with the MANIFEST.in
    data_files=[],
    description=__summary__,
    entry_points=__entry_points__,
    install_requires=__requirements__,
    long_description=__summary__,
    name=__title__,
    # For data inside packages can use the automatic inclusion
    #   include_package_data = True,
    # or the explicit inclusion, e.g.:
    #   package_data={ "package_name": ["data.file1", "data.file2" , ...] }
    packages=find_packages(exclude=["tests"]),
    url=__uri__,
    version=__version__,
    zip_safe=False,
)
