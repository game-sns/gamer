# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" GAME models """

import json
from threading import Thread

from utils import get_files, threaded_function


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
        self.parse()

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

    def get_args(self):
        """
        :return: tuple (...)
            Args written in config file
        """

        return 10 ** 3, 2, 1


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

    def parse_configs(self):
        """
        :return: void
            Scans config folder and finds config files
        """

        self.configs = get_files(self.config_folder, ending="json")
        self.configs = [
            GameConfig(config) for config in self.configs
        ]

    def run(self):
        threads = [
            Thread(
                target=threaded_function,
                args=config.get_args()
            ) for config in self.configs
        ]

        for thread in threads:  # start
            thread.start()

        for thread in threads:  # wait until all are done
            thread.join()
