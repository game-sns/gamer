# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Power-up your machine to solve GAME models """


from config import CONFIG_FOLDER, SEC_BETWEEN_RUNS
from models.model import Gamer


def main():
    """
    :return: void
        Runs core algorithm
    """

    gamer = Gamer(CONFIG_FOLDER, SEC_BETWEEN_RUNS)
    gamer.run()


if __name__ == "__main__":
    main()
