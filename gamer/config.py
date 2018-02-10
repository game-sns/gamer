# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Config data for GAME models """

import os

THREADS_COUNT = 7
PROCESSES_COUNT = 1
CONFIG_FOLDER = os.path.join(
    os.getenv("HOME"), "Coding", "Python", "game", "gamecourse", "uploads"
)
OUTPUT_FOLDER = os.path.join(
    os.getenv("HOME"), "Coding", "Python", "game", "gamecourse", "outputs"
)
SEC_BETWEEN_RUNS = 2
