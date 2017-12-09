# !/usr/bin/python2
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Power-up your machine to solve GAME models """

import os

from model import Gamer

BIG_NUMBER = 3 * 10 ** 4
THREADS_COUNT = 7
PROCESSES_COUNT = 1
CONFIG_FOLDER = os.path.join(
    os.getenv("HOME"),
    "tmp",
    "game"
)


def main():
    """
    :return: void
        Runs core algorithm
    """

    while True:
        gamer = Gamer(CONFIG_FOLDER)
        gamer.parse_configs()


if __name__ == "__main__":
    main()
