#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open(os.path.join(here, 'oryxkbleds/__version__.py')) as f:
    exec(f.read(), version)


class CleanCommand(setuptools.Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./docs/_build ./.pytest_cache ./.eggs .coverage .tox')


setuptools.setup(
    name="oryxkbleds",
    version=version['__version__'],
    author="github.com/davemcphee",
    author_email="me@none.io",
    description="Keyboard LED control package for System76 Oryx laptops",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davemcphee/oryx-kb-leds",
    packages=['oryxkbleds'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv3 License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'clean': CleanCommand,
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov", "pytest-flake8", "tox"],
    entry_points={
        'console_scripts': [
            'oryxkbleds = oryxkbleds.cli:entry_point',
        ],
    },
    install_requires=[
        'colour==0.1.5',
        'psutil==5.6.3',
        'pyyaml==5.1.1'
    ]
)
