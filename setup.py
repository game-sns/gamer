# !/usr/bin/python2
# coding: utf-8


""" Install dependencies """

from setuptools import setup, find_packages

LITTLE_DESCRIPTION = "Schedule GAME models in your server"

DESCRIPTION = \
    "gamer\n\n" + LITTLE_DESCRIPTION + "\n\
    Install\n\n\
    - $ python2 setup.py install  # from source\n\
    \n\
    Questions and issues\n\n\
    The Github issue tracker is only for bug reports and feature requests.\n\
    License: Apache License Version 2.0, January 2004"

setup(
    name="gamer",
    version="1.2",
    description=LITTLE_DESCRIPTION,
    long_description=DESCRIPTION,
    keywords="game server multiprocess",
    url="https://github.com/game-sns/gamer",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        'google_api_python_client',
        'oauth2client', 'psutil'
    ],
    entry_points={
        "console_scripts": ["gamer = gamer.main:cli"]
    }
)
