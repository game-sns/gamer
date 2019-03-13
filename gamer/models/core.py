# !/usr/bin/python2
# coding: utf-8

""" GAME models """

import json
import os
import shutil
import time
from multiprocessing import Process

from game.models import Game, FilesConfig, LabelsConfig

from gamer.config import OUTPUT_FOLDER, PROCESSES_COUNT, MAX_PARALLEL_GAMES
from gamer.emails.mailer import notify_user_of_start, notify_user_of_end
from gamer.models.logs import Logger
from gamer.utils.files import get_folders, name_of_folder


class Runner(Logger):
    """ Runs GAME models """

    def __init__(self, features, additional_features, inputs_file, errors_file,
                 labels_file,
                 output_folder, email, verbose=True):
        Logger.__init__(self, verbose)

        self.output_folder = output_folder
        self.output_filename = os.path.join(output_folder, "output.dat")
        self.output_extra_filename = None
        self.labels = features
        self.additional_features = additional_features

        files = FilesConfig(
            inputs_file,
            errors_file,
            labels_file,
            output_folder,
            True
        )
        labels = LabelsConfig(
            features,  # todo check format, should be ['G0', 'N' ..]
            additional_features  # todo check format, should be ['G0', 'N' ..]
        )

        self.driver = Game(
            files,
            PROCESSES_COUNT,
            10000,
            labels
        )
        self.email = email
        self.successful_run = False

    def start(self):
        self.successful_run = notify_user_of_start(self.email)

    def run(self):
        # todo add limits on files
        
        try:
            self.log("Starting GAME driver:")
            self.log("labels:", self.driver.labels_config.output)
            self.log("input file:", self.driver.filename_config.filename_int)
            self.log("errors file:", self.driver.filename_config.filename_err)
            self.log("labels file:",
                     self.driver.filename_config.filename_libraru)
            self.log("output file:", self.driver.filename_config.output_folder)

            self.driver.run()
            self.successful_run = True
        except Exception as e:
            self.successful_run = False
            self.log(self.email, "stopped GAME due to", e)

        self.end()

    def end(self):
        notify_user_of_end(
            self.email,
            self.successful_run,
            self.output_filename,
            "",  # todo debug file
            self.output_extra_filename
        )


class GameConfig(Logger):
    """ Config files for GAME models """

    def __init__(self, config_folder):
        """
        :param config_folder: str
            Path to config file
        """

        Logger.__init__(self, True)

        self.folder = config_folder
        self.file = os.path.join(config_folder, "data.json") or None
        self.raw_data = None
        self.parse()

    def get_labels(self):
        for label in self.raw_data['labels']:
            if label.lower() == 'g0':
                yield 'G0'

            if label.lower() == 'n':
                yield 'n'

            if label.lower() == 'nh':
                yield 'NH'

            if label.lower() == 'u':
                yield 'U'

            if label.lower() == 'z':
                yield 'Z'

    def get_additional_labels(self):
        for label in self.raw_data['additional labels']:
            if label.lower() == 'av':
                yield 'Av'

            if label.lower() == 'fesc':
                yield 'fesc'

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
                self.log("Cannot parse raw data of", self.file, ", due to", e)

        self.raw_data['labels'] = self.get_labels()
        self.raw_data['additional labels'] = self.get_additional_labels()

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
               self.get_arg("LabelsFile"), \
               self.get_arg("UploadFolder"), \
               self.get_arg("Email")


class Gamer(Logger):
    """ Controls GAME models """

    def __init__(self, config_folder, sec_between_runs):
        """
        :param config_folder: str
            Path to folder containing config files
        """

        Logger.__init__(self, True)

        self.config_folder = config_folder
        self.configs = []
        self.runners = []
        self.slaves = []
        self.sleep_time = float(sec_between_runs)

    def parse_configs(self):
        """
        :return: void
            Scans config folder and finds config files
        """

        self.configs = [
            GameConfig(config)
            for config in get_folders(self.config_folder)
                       ][:MAX_PARALLEL_GAMES]  # take first 30 configs at most
        self.create_gamers()
        self.log("Found", len(self.configs), "config")

    def create_gamers(self):
        self.runners = [
            Runner(
                *config.get_args()
            ) for config in self.configs
        ]
        self.slaves = [
            Process(target=runner.run) for runner in self.runners
        ]

    def launch_models(self):
        for runner in self.runners:
            runner.start()

        for slave in self.slaves:  # start
            # todo efficient memory usage must be controlled at OS-level
            slave.start()

        for slave in self.slaves:  # wait until all are done
            slave.join()

        self.end_run()

    def end_run(self):
        """
        :return: void
            Ends run and move config to output folder
        """

        for config in self.configs:
            output_folder = os.path.join(
                OUTPUT_FOLDER,
                name_of_folder(config.folder)
            )
            # todo or delete ??
            shutil.move(config.folder, output_folder)
            self.log("Written output to", output_folder)

    def run(self):
        while True:
            self.parse_configs()
            self.launch_models()
            time.sleep(self.sleep_time)
