import os

from setuptools import find_packages, setup

base_dir = os.path.dirname(__file__)
__author__ = "Kay Hau"
__email__ = "virtualda@gmail.com"
__title__ = "helper"
__version__ = "0.1.0.dev0"
__summary__ = "This package includes some simple scripts for setting up local development environment."
__uri__ = "https://github.com/kyhau/aws-tools/"

__requirements__ = [
    "boto3==1.28.44",
    "click==8.1.7",
    "docker==6.1.3",
    "InquirerPy==0.3.4",
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

__long_description__ = ""
try:
    # Reformat description as PyPi use ReStructuredText rather than Markdown
    import pypandoc
    __long_description__ = pypandoc.convert_file(os.path.join(base_dir, "README.md"), "rst")
except (ImportError, IOError, OSError) as e:
    print("long_description conversion failure, fallback to using raw contents")
    import io
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        __long_description__ = f.read()

CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3 :: Only",
]

setup(
    author=__author__,
    author_email=__email__,
    classifiers=CLASSIFIERS,
    # data_files parameter is only required for files outside the packages, used in conjunction with the MANIFEST.in
    data_files=[("", ["ReleaseNotes.md"]),],
    description=__summary__,
    entry_points=__entry_points__,
    install_requires=__requirements__,
    long_description=__long_description__,
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
