# !/usr/bin/python2
# coding: utf-8


""" Example of run """

from gamer.config import GAMES_FOLDER, SEC_BETWEEN_RUNS
from gamer.models.core import Gamer

if __name__ == "__main__":
    gamer = Gamer(GAMES_FOLDER, SEC_BETWEEN_RUNS)
    gamer.run()
