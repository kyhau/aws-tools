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
__version__ = "0.1.0"
__summary__ = "This package includes some simple scripts for setting up local development environment."
__uri__ = "https://github.com/kyhau/arki"

__requirements__ = [
    "boto3==1.8.2",
    "click==6.7",
    "docker==3.4.1",
    "warrant==0.6.1",
    "pypiwin32==220; sys_platform == 'win32' and python_version >= '3.6'"
]

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

entry_points = {
    "console_scripts": [
        "arki = arki:main",
        "aws_apig_deploy = arki.aws.apig_deploy:main",
        "aws_cognito = arki.aws.cognito:main",
        "aws_ddb = arki.aws.dynamodb:main",
        "aws_ecs_list_task_definitions = arki.aws.ecs:main",
        "aws_ecs_register_task_definition = arki.aws.ecs_register_task_definition:main",
        "aws_lambda_deploy = arki.aws.lambda_deploy:main",
        "aws_lambda_permissions_to_apig = arki.aws.lambda_permissions:lambda_permissions_to_apig",
        "aws_profile = arki.aws.profiles:main",
        "dockerc = arki.docker:find_non_running_containers",
        "dockeri = arki.docker:find_dangling_images",
        #"aws_cloudwatch = arki.aws.cloudwatch:main",
        "env_store = arki.env_variable_store:main",
        "venv = arki.virtualenv:create",
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
