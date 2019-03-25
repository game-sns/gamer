# !/usr/bin/python2
# coding: utf-8

""" GAME models """

import datetime
import json
import os
import shutil
import time
from multiprocessing import Process

import psutil
from game.errors import GameException
from game.models import Game, FilesConfig, LabelsConfig

from gamer.config import OUTPUT_FOLDER, MAX_PARALLEL_GAMES, \
    SAFETY_CORES
from gamer.emails.mailer import notify_user_of_start, notify_user_of_end
from gamer.models.logs import Logger
from gamer.utils.files import get_folders, name_of_folder


def get_available_cores(sample_time=3, min_cpu=75):
    """
    :param sample_time: measure CPU % this number of seconds
    :param min_cpu: min CPU % for a core to be unavailable
    """

    cores_percent = psutil.cpu_percent(interval=sample_time, percpu=True)
    available_cores = [
        core
        for core in cores_percent
        if core < min_cpu
    ]
    n_available = len(available_cores) - SAFETY_CORES

    return max(0, n_available)  # if less than 0, return 0


class Runner(Logger):
    """ Runs GAME models """

    def __init__(self, features, inputs_file, errors_file,
                 labels_file,
                 output_folder, optional_files, n_repetitions,
                 n_estimators, email,
                 verbose=True):
        Logger.__init__(self, verbose)

        self.output_folder = output_folder
        self.output_extra_filename = None
        self.labels = features

        files = FilesConfig(
            inputs_file,
            errors_file,
            labels_file,
            output_folder,
            optional_files
        )
        labels = LabelsConfig(
            features
        )

        self.driver = Game(
            files,
            get_available_cores(),  # count cores available
            n_repetitions,
            n_estimators,
            labels
        )
        self.email = email
        self.successful_run = False

    def start(self):
        self.successful_run = notify_user_of_start(self.email)

    def run(self):
        self.start()

        try:
            self.log("Starting GAME driver:")
            self.log("labels:", self.driver.labels_config.output)
            self.log("input file:", self.driver.filename_config.filename_int)
            self.log("errors file:", self.driver.filename_config.filename_err)
            self.log("labels file:",
                     self.driver.filename_config.filename_library)
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
            self.output_folder,
            self.output_extra_filename
        )


class GameConfig(Logger):
    """ Config files for GAME models """

    EXCEPTION_FILES_FORMAT = 'Cannot parse {}'
    DATE_TIME_FORMAT = '%Y-%d-%m %H:%M:%S'

    def __init__(self, config_folder):
        """
        :param config_folder: str
            Path to config file
        """

        Logger.__init__(self, True)

        self.folder = config_folder
        self.file = os.path.join(config_folder, "data.json") or None
        self.raw_data = None

        self._parse()
        self.creation_time = datetime.datetime.strptime(self.raw_data['time'],
                                                        self.DATE_TIME_FORMAT)

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

            if label.lower() == 'av':
                yield 'Av'

            if label.lower() == 'fesc':
                yield 'fesc'

    def _parse(self):
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
            except:
                exception = GameException.build_files_exception(
                    self.EXCEPTION_FILES_FORMAT.format(self.file)
                )
                raise exception

        self.raw_data['labels'] = list(self.get_labels())
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
               self.get_arg("InputFile"), \
               self.get_arg("ErrorFile"), \
               self.get_arg("LabelsFile"), \
               self.get_arg("UploadFolder"), \
               self.get_arg('OptionalFiles'), \
               self.get_arg('nRepetitions'), \
               self.get_arg('nEstimators'), \
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
        ]
        self.configs = sorted(self.configs, key=lambda x: x.creation_time)
        self.configs = self.configs[:MAX_PARALLEL_GAMES]
        self.create_gamers()
        self.log("Found", len(self.configs), "config")

    def create_gamers(self):
        self.runners = [
            Runner(
                *config.get_args()
            ) for config in self.configs
        ]
        self.slaves = [
            Process(target=runner.run)
            for runner in self.runners
        ]

    def launch_models(self):
        for slave in self.slaves:  # start
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
            shutil.move(config.folder, output_folder)
            self.log("Written output to", output_folder)

    def run(self):
        while True:
            self.parse_configs()
            self.launch_models()
            time.sleep(self.sleep_time)
