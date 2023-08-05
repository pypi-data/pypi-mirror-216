#!/usr/bin/env python
# Copyright (C) 2022, NG:ITL
import versioneer
from setuptools import find_packages, setup


setup(
    name="data_aggregator",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Simple data aggregator framework to simplify data processing",
    long_description="Simple data aggregator framework to simplify data processing",
    author="NG:ITL",
    license="GPLv3",
    author_email="torsten.wylegala@volkswagen.de",
    url="https://github.com/vw-wob-it-edu-ngitl/data_aggregator/",
    packages=find_packages("."),
    install_requires=[
        "ngitl-common-py~=0.4.3",
        "openpyxl~=3.0.10",
        "watchdog~=3.0.0",
        "PySide6~=6.5.1",
        "pywin32==306",
        "requests~=2.31.0",
        "chardet~=5.1.0",
    ],
    include_package_data=True,
)
