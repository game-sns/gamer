# !/usr/bin/python2
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Make your machine use its full potential to solve GAME models """

from datetime import datetime
from multiprocessing import Pool
from threading import Thread

import numpy as np

BIG_NUMBER = 10 ** 8
THREADS_COUNT = 4
PROC_COUNT = 16  # cpu_count() / THREADS_COUNT


def very_intensive_calc(big_num):
    for _ in range(big_num):
        _ * _


def threaded_function(thread_name):
    print datetime.now(), "->", thread_name, "START"
    pool = Pool(PROC_COUNT)
    pool.map(
        very_intensive_calc,
        (BIG_NUMBER,)
    )
    print datetime.now(), "->", thread_name, "DONE"


def main():
    print "log10(big)", np.log10(BIG_NUMBER)
    print "# threads", THREADS_COUNT
    print "# processes in use per thread", PROC_COUNT, "\n"

    threads = [
        Thread(
            target=threaded_function,
            args=(thread_num,)
        ) for thread_num in range(THREADS_COUNT)
    ]

    for thread in threads:  # start
        thread.start()

    for thread in threads:  # wait until all have finished
        thread.join()

    print "Threads finished...exiting"


if __name__ == "__main__":
    main()
