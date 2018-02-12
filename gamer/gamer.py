# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Power-up your machine to solve GAME models """

import time

from config import CONFIG_FOLDER, SEC_BETWEEN_RUNS
from model import Gamer


def main():
    """
    :return: void
        Runs core algorithm
    """

    while True:
        gamer = Gamer(CONFIG_FOLDER)
        gamer.parse_configs()
        gamer.run()

        print time.time()
        time.sleep(SEC_BETWEEN_RUNS)


if __name__ == "__main__":
    main()
