# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" GAME models """

import json
import os
from threading import Thread

from config import OUTPUT_FOLDER
from utils import run_game, get_folders, name_of_folder, move_folder


class GameConfig(object):
    """ Config files for GAME models """

    def __init__(self, config_folder):
        """
        :param config_folder: str
            Path to config file
        """

        object.__init__(self)

        self.folder = config_folder
        self.file = os.path.join(config_folder, "data.json") or None
        self.raw_data = None
        self.parse()

    def parse(self):
        """
        :return: void
            Parses raw data
        """

        if self.raw_data is None:
            try:
                with open(self.file, "r") as in_file:
                    self.raw_data = json.loads(
                        in_file.read()
                    )  # read and return json object
            except Exception as e:
                print str(e)
                print "Cannot parse raw data of folder", self.folder, \
                    "(should be", self.file, ")"

        return self.raw_data

    def get_arg(self, key):
        """
        :param key: str
            Key to get
        :return: obj
            Value in data
        """

        if key in self.raw_data:
            return self.raw_data[key]

        return None

    def get_args(self):
        """
        :return: tuple (...)
            Args written in config file
        """

        return self.get_arg("labels"), \
               self.get_arg("additional labels"), \
               self.get_arg("InputFile"), \
               self.get_arg("ErrorFile"), \
               self.get_arg("UploadFolder")


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

        self.configs = [
            GameConfig(config) for config in get_folders(self.config_folder)
        ]

    def run(self):
        threads = [
            Thread(
                target=run_game,
                args=config.get_args()
            ) for config in self.configs
        ]

        for thread in threads:  # start
            thread.start()

        for thread in threads:  # wait until all are done
            thread.join()

        self.end_run()

    def end_run(self):
        """
        :return: void
            Ends run and move config to output folder
        """

        output_folder = os.path.join(
            OUTPUT_FOLDER,
            name_of_folder(self.config_folder)
        )
        move_folder(self.config_folder, output_folder)
