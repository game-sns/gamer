# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" GAMER utils and tools """

import os
import time

from game.models import Game

from gamer.utils.emails import notify_user_of_start, notify_user_of_end


def get_driver(labels, output_filename, input_file, errors_file, labels_file):
    return Game(
        labels,
        output_filename=output_filename,
        manual_input=False,
        verbose=True,
        inputs_file=input_file,
        errors_file=errors_file,
        labels_file=labels_file
    )


def run_driver(driver, verbose=True):
    if verbose:
        print time.time(), "starting GAME driver:"
        print "\tlabels:", driver.labels
        print "\tinput file:", driver.filename_int
        print "\terrors file:", driver.filename_err
        print "\tlabels file:", driver.filename_library
        print "\toutput file:", driver.output_filename

    driver.run()


def run_driver_additional(driver, additional_features, output_folder,
                          verbose=True):
    output_filename = os.path.join(output_folder,
                                   "output_ml_additional.dat")
    if verbose:
        print time.time(), "starting GAME driver (additional labels):"
        print "\tadditional features:", additional_features
        print "\toutput file:", output_filename

    driver.run_additional_labels(
        additional_features=additional_features,
        output_filename=output_filename
    )

    return output_filename


def run_game(labels, additional_features, input_file, errors_file, labels_file,
             output_folder, email):
    output_filename = os.path.join(output_folder, "output_ml.dat")
    driver = get_driver(
        labels, output_filename, input_file, errors_file, labels_file
    )

    output_extra_filename = None
    successful_run = notify_user_of_start(email)

    try:
        run_driver(driver)
    except Exception as e:
        successful_run = False
        print(time.time(), email, "stopped working due to", e)

    if additional_features:
        try:
            output_extra_filename = run_driver_additional(
                driver, additional_features, output_folder
            )
        except Exception as e:
            successful_run = False
            print(time.time(), email, "(additional) stopped working due to", e)

    notify_user_of_end(
        email,
        successful_run,
        output_filename,
        "",  # todo debug file
        output_extra_filename
    )
