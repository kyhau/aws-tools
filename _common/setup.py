import os
from setuptools import setup, find_packages


# Makes setup work inside of a virtualenv
use_system_lib = True
if os.environ.get("BUILD_LIB") == "1":
    use_system_lib = False

base_dir = os.path.dirname(__file__)

__author__ = "kyhau"
__email__ = "virtualda@gmail.com"

__title__ = "arki_common"
__version__ = "0.1.0.dev0"
__summary__ = "This package includes some simple scripts for setting up local development environment."
__uri__ = "https://github.com/kyhau/arki"

__requirements__ = [
    "boto3~=1.9",
    "click~=7.0",
    "docker~=4.0",
    "pyyaml~=5.1",
    "toml~=0.10",
]

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

entry_points = {
    "console_scripts": [
        "arki = arki:main",
        "dockerc = arki.docker:find_non_running_containers",
        "dockeri = arki.docker:find_dangling_images",
        "env_store = arki.env_variable_store:main",
    ]
}

setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=long_description,
    packages=find_packages(exclude=["tests"]),
    author=__author__,
    author_email=__email__,
    url=__uri__,
    zip_safe=False,
    install_requires=__requirements__,
    data_files=[
        ("", ["ReleaseNotes.md"]),
    ],
    # For data inside packages can use the automatic inclusion
    # include_package_data = True,
    # or the explicit inclusion, eg:
    # package_data = { "package_name": ["data.file1", "data.file2" , ...] }
    entry_points=entry_points,
)
