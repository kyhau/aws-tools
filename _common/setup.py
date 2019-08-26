from setuptools import setup, find_packages
import os

# Makes setup work inside of a virtualenv
use_system_lib = True
if os.environ.get("BUILD_LIB") == "1":
    use_system_lib = False

base_dir = os.path.dirname(__file__)

__author__ = "kyhau"
__email__ = "virtualda@gmail.com"

__title__ = "arki"
__version__ = "0.2.0.dev0"
__summary__ = "This package includes some simple scripts for setting up local development environment."
__uri__ = "https://github.com/kyhau/arki"

__requirements__ = [
    "boto3==1.9.119",
    "click==7.0",
    "docker==3.7.1",
    "pyyaml==5.1.2",
    "pypiwin32==220; sys_platform == 'win32' and python_version >= '3.6'",
    "toml==0.10.0",
    "warrant==0.6.1",
]

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

entry_points = {
    "console_scripts": [
        "arki = arki:main",
        "aws_apig_deploy = arki.aws.apig_deploy:main",
        "aws_lambda_deploy = arki.aws.lambda_deploy:main",
        "aws_lambda_permissions_to_apig = arki.aws.lambda_permissions:lambda_permissions_to_apig",
        "aws_profile = arki.aws.profiles:main",
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
