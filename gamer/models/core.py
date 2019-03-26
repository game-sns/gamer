# !/usr/bin/python2
# coding: utf-8

""" GAME models """

import datetime
import json
import math
import os
import shutil
import time
import traceback
from multiprocessing import Process

import psutil
from astraeus.core import Astraeus
from game.behaviour import GameError
from game.models import Game, FilesConfig, LabelsConfig

from gamer.config import OUTPUT_FOLDER, MAX_PARALLEL_GAMES, \
    SAFETY_CORES, DOWNLOAD_URL, DONE_FOLDER
from gamer.emails.mailer import notify_user_of_start, notify_user_of_end, \
    notify_admins
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
    n_available = max(0, n_available)  # if less than 0, return 0
    n_available = int(math.floor(n_available / MAX_PARALLEL_GAMES))
    return n_available


class Runner(Logger):
    """ Runs GAME models """

    def __init__(self, features, inputs_file, errors_file,
                 labels_file,
                 output_folder, output_archive, optional_files, n_repetitions,
                 n_estimators, email, name_surname, institution,
                 verbose=True):
        Logger.__init__(self, verbose)

        self.output_folder = output_folder
        self.output_archive = output_archive
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

        self.max_cores = get_available_cores()  # count cores available
        self.driver = Game(
            files,
            self.max_cores,
            n_repetitions,
            n_estimators,
            labels
        )
        self.email = email
        self.name_surname = name_surname
        self.institution = institution
        self.successful_run = False
        self.download_token = None

    def start(self):
        self.successful_run = notify_user_of_start(self.email,
                                                   self.name_surname)
        notify_admins(self.email, self.name_surname, self.institution,
                      self.output_folder, 'on_start')

    def run(self):
        self.start()

        try:
            self.log("Starting GAME driver with at most {} cores",
                     self.max_cores)
            self.log("output:", self.output_folder)

            game_behaviour = self.driver.run()
            if game_behaviour.is_error():
                self.successful_run = False
            else:
                self.successful_run = True
            self.successful_run = True
        except Exception as e:
            self.successful_run = False
            self.log(self.email, "stopped GAME due to", e)

        self.end()

    def _create_download_token(self):
        if not self.download_token:
            astraeus_client = Astraeus(
                port=11212,
                expire_seconds=((60 * 60) * 24) * 10  # 10 days
            )
            token = astraeus_client.save(self.output_archive)
            self.download_token = token

        return self.download_token

    def get_download_link(self):
        return DOWNLOAD_URL.format(self._create_download_token())

    def _create_archive(self):
        inner_output_folder = os.path.join(self.output_folder, 'out')
        os.makedirs(inner_output_folder)

        for f in os.listdir(self.output_folder):  # move to output folder
            complete_f = os.path.join(self.output_folder, f)
            if os.path.isfile(complete_f):
                if complete_f.endswith('.dat'):  # is output
                    shutil.move(complete_f, inner_output_folder)

        ext = 'zip'
        shutil.make_archive(self.output_archive, ext, inner_output_folder)
        self.output_archive += ('.' + ext)  # add extension

    def end(self):
        self._create_archive()

        notify_user_of_end(
            self.email,
            self.name_surname,
            self.successful_run,
            self.get_download_link()
        )

        if self.successful_run:
            notify_admins(self.email, self.name_surname, self.institution,
                          None, 'on_success')
        else:
            notify_admins(self.email, self.name_surname, self.institution,
                          self.output_folder, 'on_fail')


class GameConfig(Logger):
    """ Config files for GAME models """

    EXCEPTION_FILES_FORMAT = 'Cannot parse {}'
    DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, config_folder):
        """
        :param config_folder: str
            Path to config file
        """

        Logger.__init__(self, True)

        try:
            self.folder = config_folder
            self.file = os.path.join(config_folder, "data.json") or None
            self.raw_data = None
            self.n_reps = None

            self._parse()
            self.creation_time = datetime.datetime.strptime(
                self.raw_data['time'],
                self.DATE_TIME_FORMAT)
        except:
            notify_admins('unknown', 'unknown', 'unknown',
                          config_folder, 'on_parse_error',
                          location=config_folder)

    def get_labels(self):
        for label in self.raw_data['labels']:
            if label.lower() == 'g0':
                yield 'g0'

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
                exception = GameError.build_files_exception(
                    self.EXCEPTION_FILES_FORMAT.format(self.file)
                )
                raise exception

        self.raw_data['labels'] = list(self.get_labels())
        self.n_reps = 10000  # default
        self.n_ests = 50  # default
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

        output_archive = os.path.join(
            OUTPUT_FOLDER,
            name_of_folder(self.folder)
        )  # later on we'll add the extension

        return self.get_arg("labels"), \
               self.get_arg("InputFile"), \
               self.get_arg("ErrorFile"), \
               self.get_arg("LabelsFile"), \
               self.get_arg("OutputFolder"), \
               output_archive, \
               self.get_arg('OptionalFiles'), \
               self.n_reps, \
               self.n_ests, \
               self.get_arg("Email"), \
               self.get_arg("name_surname"), \
               self.get_arg("institution")


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
        self.log("Found", len(self.configs), "config...")
        self.configs = self.configs[:MAX_PARALLEL_GAMES]
        self.log("...selecting first", len(self.configs), "configs")
        self.create_gamers()

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
        for i, slave in enumerate(self.slaves):  # start
            self.log('started {}-th slave'.format(i))
            slave.start()

        for i, slave in enumerate(self.slaves):  # wait until all are done
            slave.join()

        self.end_run()

    def end_run(self):
        """
        :return: void
            Ends run and move config to output folder
        """

        for config in self.configs:
            output_folder = os.path.join(
                DONE_FOLDER,
                name_of_folder(config.folder)
            )

            self.log('{} -> {}'.format(config.folder, output_folder))
            shutil.move(config.folder, output_folder)

    def run(self):
        while True:
            try:
                self.parse_configs()
                self.launch_models()

                self.log('will sleep for {} seconds'.format(self.sleep_time))
            except Exception as e:
                print e
                traceback.print_exc()

            time.sleep(self.sleep_time)
