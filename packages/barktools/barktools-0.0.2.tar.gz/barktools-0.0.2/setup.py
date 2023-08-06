import sys
import setuptools
from setuptools.command.test import test as TestCommand

with open("README.md", "r") as file:
    long_description = file.read()

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setuptools.setup(
    name="barktools",
    version="0.0.2",
    entry_points={
        "console_scripts": [
            "index_files = scripts.index_files:main"
            ]
    },
    author="Oscar Bark",
    author_email="kurshid.ognianov@protonmail.com",
    description="Package containing various useful python modules and scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BarkenBark/python-tools",
    packages=['barktools', 'scripts'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],
    python_requires=">=3.6",
    tests_require=['pytest'],
    cmdclass={'test': PyTest}
)