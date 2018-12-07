# !/usr/bin/python2
# coding: utf-8


""" Config data for GAME models """

import os

THREADS_COUNT = 7
PROCESSES_COUNT = 1
GAMES_FOLDER = os.path.join(
    os.getenv("HOME"), "Coding", "Python", "game", "gamecourse", "uploads"
)
OUTPUT_FOLDER = os.path.join(
    os.getenv("HOME"), "Coding", "Python", "game", "gamecourse", "outputs"
)
SEC_BETWEEN_RUNS = 10
