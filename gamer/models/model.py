# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" GAME models """

import json
import os
import shutil
import time
from multiprocessing import Process

from game.models import Game

from gamer.config import OUTPUT_FOLDER
from gamer.emails import notify_user_of_start, notify_user_of_end
from gamer.models.logs import Logger
from gamer.utils.files import get_folders, name_of_folder


class Runner(object):
    """ Runs GAME models """

    def __init__(self, labels, additional_features, input_file, errors_file,
                 labels_file,
                 output_folder, email, verbose=True):
        object.__init__(self)

        self.output_folder = output_folder
        self.output_filename = os.path.join(output_folder, "output_ml.dat")
        self.output_extra_filename = None
        self.labels = labels
        self.additional_features = additional_features

        self.driver = Game(
            labels,
            output_filename=self.output_filename,
            manual_input=False,
            verbose=True,
            inputs_file=input_file,
            errors_file=errors_file,
            labels_file=labels_file
        )
        self.email = email
        self.verbose = verbose
        self.successful_run = False

    def start(self):
        self.successful_run = notify_user_of_start(self.email)

    def run(self):
        self.run_labels()
        # todo self.run_additional_labels()

    def run_labels(self):
        try:
            if self.verbose:
                print time.time(), "starting GAME driver:"
                print "\tlabels:", self.driver.features
                print "\tinput file:", self.driver.filename_int
                print "\terrors file:", self.driver.filename_err
                print "\tlabels file:", self.driver.filename_library
                print "\toutput file:", self.driver.output_filename

            self.driver.launch_models()
        except Exception as e:
            self.successful_run = False
            print(time.time(), self.email, "stopped working due to", e)

    def run_additional_labels(self):
        if self.additional_features:
            try:
                self.output_extra_filename = os.path.join(
                    self.output_folder,
                    "output_ml_additional.dat"
                )

                if self.verbose:
                    print time.time(), "starting GAME driver (additional labels):"
                    print "\tadditional features:", self.additional_features
                    print "\toutput file:", self.output_extra_filename

                self.driver.run_additional_labels(
                    additional_features=self.additional_features,
                    output_filename=self.output_extra_filename
                )
            except Exception as e:
                self.successful_run = False
                print(
                    time.time(), self.email,
                    "(additional) stopped working due to", e
                )

    def end(self):
        notify_user_of_end(
            self.email,
            self.successful_run,
            self.output_filename,
            "",  # todo debug file
            self.output_extra_filename
        )


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
        self.raw_data = self.parse()

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
        ]
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
            slave.start()

        for slave in self.slaves:  # wait until all are done todo find better
            slave.join()

        for runner in self.runners:
            runner.end()

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
