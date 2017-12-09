# !/usr/bin/python2
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" GAME models """

import json

from utils import get_files


class GameConfig(object):
    """ Config files for GAME models """

    def __init__(self, config_file):
        """
        :param config_file: str
            Path to config file
        """

        object.__init__(self)

        self.config_file = config_file
        self.raw_data = None

    def parse(self):
        """
        :return: void
            Parses raw data
        """

        if self.raw_data is None:
            with open(self.config_file, "r") as in_file:
                self.raw_data = json.loads(
                    in_file.read()
                )  # read and return json object

        return self.raw_data


class Gamer(object):
    """ He who runs GAME models """

    def __init__(self, config_folder):
        """
        :param config_folder: str
            Path to folder containing config files
        """

        object.__init__(self)

        self.config_folder = config_folder
        self.configs = []

    def scan_folder(self):
        """
        :return: void
            Scans config folder and finds config files
        """

        configs = get_files(self.config_folder, ending="json")
        configs = [
            GameConfig(config) for config in configs
        ]
        self.configs = configs
