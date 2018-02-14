# !/usr/bin/python3
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" GAMER utils and tools """

import json
import os
import shutil
import time

from game.models import Game

from mailer import send_msg, get_msg


def get_pretty_date(dt):
    return dt.strftime("%H:%M:%S")


def get_name_ext(path):
    """
    :param path: str
        Path of file/folder
    :return: tuple (str, str)
        Name of file, extension of file
    """

    return os.path.splitext(path)


def is_hidden(path):
    """
    :param path: str
        Path to file/folder
    :return: bool
        True iff path is hidden (starting with a dot)
    """

    name, extension = get_name_ext(path)
    return name.startswith(".")


def ls_recurse(path, include_hidden=False):
    """
    :param path: string
        Path to directory to get list of files and folders
    :param include_hidden: bool
        Whether to include hidden files in list.
    :return: list
        List of paths in given directory recursively.
    """

    lst = []
    for f in os.listdir(path):
        hidden_file = is_hidden(f)
        if (hidden_file and include_hidden) or (not hidden_file):
            lst.append(os.path.join(path, f))
            if os.path.isdir(os.path.join(path, f)):
                lst += ls_recurse(
                    os.path.join(path, f),
                    include_hidden=include_hidden
                )  # get list of files in directory
    return lst


def get_files(path, ending):
    """
    :param path: str
        Path to folder
    :param ending: str
        Ending of files to be selected
    :return: [] of str
        List of files found (recursively) not hidden
    """

    content = ls_recurse(path)
    return [
        f for f in content
        if f.endswith(ending) and os.path.isfile(f)
    ]


def get_folders(path):
    """
    :param path: str
        Path to folder
    :param ending: str
        Ending of files to be selected
    :return: [] of str
        List of files found (recursively) not hidden
    """

    return [
        os.path.join(path, f) for f in os.listdir(path)
        if os.path.isdir(os.path.join(path, f))
    ]


def write_data_to_json(data, output_file):
    """
    :param data: list of {} or {}
        Data to write
    :param output_file: str
        Path to output file
    :return: void
        Saves output file as .json
    """

    with open(output_file, "w") as out:
        json.dump(
            data,  # data
            out,  # file handler
            indent=4, sort_keys=True  # pretty print
        )


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


def notify_user(raw_message, recipient, subject):
    """
    :param recipient: str
        Email of recipient
    :param raw_message: str
        HTML message
    :return: bool
        True iff successful notification
    """

    try:
        raw_message += "</br></br>With <3 the GAME team"
        msg = get_msg("sirfoga@protonmail.com", raw_message, subject)
        send_msg(msg)
        return True
    except Exception as e:
        print(
            "Cannot send email to",
            recipient,
            "with message\n```\n", raw_message, "\n```\nbecause of", e
        )

    return False


def notify_user_of_start(recipient):
    """
    :param recipient: str
        Email of recipient
    :return: bool
        True iff successful notification
    """

    msg = "Hi!</br>" \
          "Your GAME models are on their way!</br>" \
          "This email has been sent just to notify you that all files have" \
          "been parsed correctly and your results are coming.</br>" \
          "You will receive another email with the link to download your " \
          "results. As of now, have a nice day!" \
          "</br>" \
          "Bye!"
    return notify_user(msg, recipient, "GAME | start")


def notify_user_of_end(recipient, success, output_file,
                       debug_file, extra_output=None):
    """
    :param recipient: str
        Email of recipient
    :param output_file: str
        Path to output file
    :param extra_output: str
        Path to output file with additional labels
    :return: bool
        True iff successful notification
    """

    msg = "Hi!</br>"
    if success:
        msg += "Your GAME models have run successfully!</br>"
    else:
        msg += "Sorry, but we encountered some errors while running your " \
               "models.</br>"

    msg += "Here are your output files:</br>" \
           "<ul>" \
           "<li><a href='" + debug_file + "'>debug file</a></li>" \
                                          "<li><a href='" + output_file + "'>output file</a></li>"

    if extra_output:
        "<li><a href='" + extra_output + "'>additional output file</a></li>"

    msg += "</ul></br>"
    msg += "Make sure to download these files as soon as possible because we " \
           "they will be erased within two weeks!</br>" \
           "Hoping the results match your predictions ... see you soon!"

    return notify_user(msg, recipient, "GAME | your results")


def run_game(labels, additional_features, input_file, errors_file, labels_file,
             output_folder, email):
    output_filename = os.path.join(output_folder, "output_ml.dat")
    driver = get_driver(
        labels, output_filename, input_file, errors_file, labels_file
    )

    print time.time(), "starting GAME driver:"
    print "\tlabels:", labels
    print "\tinput file:", input_file
    print "\terrors file:", errors_file
    print "\tlabels file:", labels_file
    print "\toutput file:", output_filename

    driver.run()

    if additional_features:
        output_filename = os.path.join(output_folder,
                                       "output_ml_additional.dat")

        print time.time(), "starting GAME driver (additional labels):"
        print "\tadditional features:", additional_features
        print "\toutput file:", output_filename

        driver.run_additional_labels(
            additional_features=additional_features,
            output_filename=output_filename
        )

    print time.time(), "sending notification email:"
    print "\temail:", email


def name_of_folder(path):
    """
    :param path: str
        Path to folder
    :return: str
        Name of folder
    """

    return os.path.basename(path)


def move_folder(original_path, output_containing_folder):
    """
    :param original_path: str
        Path to folder to move
    :param output_containing_folder: str
        Path to output containing folder
    :return: void
        Moves folder tree to output folder
    """

    contents = os.listdir(original_path)
    folder_name = name_of_folder(original_path)
    out_folder = os.path.join(output_containing_folder, folder_name)
    for sub_dir in contents:
        dir_to_move = os.path.join(original_path, sub_dir)
        shutil.move(dir_to_move, out_folder)
