# !/usr/bin/python2
# coding: utf-8


""" Config data for GAME models """

import os

THREADS_COUNT = 7
PROCESSES_COUNT = 1
GAMES_FOLDER = os.path.join(
    os.getenv("HOME"), "Work", "sns", "game", "code", "gamecourse", "uploads"
)
OUTPUT_FOLDER = os.path.join(
    os.getenv("HOME"), "Work", "sns", "game", "code", "gamecourse", "outputs"
)
SEC_BETWEEN_RUNS = 10
MAX_PARALLEL_GAMES = 30
