# !/usr/bin/python2
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Power-up your machine to solve GAME models """


from config import CONFIG_FOLDER, SEC_BETWEEN_RUNS
from models.core import Gamer


if __name__ == "__main__":
    gamer = Gamer(CONFIG_FOLDER, SEC_BETWEEN_RUNS)
    gamer.run()
