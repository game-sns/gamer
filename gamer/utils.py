# !/usr/bin/python2
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" GAMER utils and tools """

import os


def get_name_ext(path):
    return os.path.splitext(path)


def is_hidden(path):
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
