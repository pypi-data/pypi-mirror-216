# type: ignore

"""The setup script."""


import codecs
import os
import os.path

from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")


# please keep this lean and mean. Add dev requirements to .devcontainer/requirments.txt
requirements = ["click", "pymap3d", "pynmea2", "websockets", "asyncio-mqtt", "pydantic"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="ROX Autmation",
    author_email="dev@roxautomation.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
    description="KISS robootics framework",
    install_requires=requirements,
    include_package_data=True,
    keywords="",
    name="roxbot",
    package_dir={"": "src"},
    packages=find_packages("src"),
    test_suite="tests",
    tests_require=test_requirements,
    url="",
    version=get_version("src/roxbot/__init__.py"),
    zip_safe=False,
    package_data={"roxbot": ["py.typed"]},
    entry_points={"console_scripts": ["roxbot=roxbot.cli:cli"]},
)
