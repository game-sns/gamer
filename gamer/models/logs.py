# !/usr/bin/python2
# coding: utf-8

""" Log stuff """

import os
from datetime import datetime

from gamer.utils.misc import get_actual_class_name

LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def now():
    return datetime.now().strftime(LOG_TIME_FORMAT)


class Logger:
    """ Logs itself """

    OUT_FOLDER = '/opt/game/gamer/'

    def __init__(self, verbose, to_file=True):
        self.class_name = get_actual_class_name(self)
        self.verbose = bool(verbose)
        self.to_file = bool(to_file)

        self.out_file = os.path.join(self.OUT_FOLDER, now() + '.log')

    def log(self, *content):
        """
        :param content: *
            Data to print to stdout
        :return: void
            Prints log
        """

        content = " ".join([str(x) for x in content])
        msg = '{} {} >>> {}'.format(now(), self.class_name, content)

        if self.verbose:
            print msg

        with open(self.out_file, 'a') as appender:
            appender.write(msg + '\n')  # add new line
