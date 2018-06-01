from setuptools import setup, find_packages
import os

# Makes setup work inside of a virtualenv
use_system_lib = True
if os.environ.get("BUILD_LIB") == "1":
    use_system_lib = False

base_dir = os.path.dirname(__file__)

__author__ = "Kay Hau"
__email__ = "virtualda@gmail.com"

__title__ = "arki"
__version__ = "0.1.0.dev0"
__summary__ = "This package creates a framework for python packages to be built."
__uri__ = "https://github.com/kyhau/arki"

__requirements__ = [
    "boto3==1.7.30",
    "click==6.7",
    "docker-py==1.10.6"
]

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

entry_points = {
    "console_scripts": [
        "arki = arki:show_all_console_scripts",
        "aws_profile = arki.aws.profiles:main",
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
