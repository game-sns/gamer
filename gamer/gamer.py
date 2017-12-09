# !/usr/bin/python2
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Make your machine use its full potential to solve GAME models """

from datetime import datetime
from multiprocessing import Process
from multiprocessing import cpu_count
from threading import Thread

import numpy as np

BIG_NUMBER = 10 ** 8
MAX_PROCESSES = cpu_count()
THREADS_COUNT = 2
PROC_COUNT = 3


def very_intensive_calc(big_num):
    print datetime.now(), "->", "calc", big_num
    for _ in range(big_num):
        _ * _


def threaded_function(thread_name):
    print "\t", datetime.now(), "->", thread_name, "START"
    print "\t", "Thread Executing!"
    print "\t", datetime.now(), "->", thread_name, "DONE"


def processed_function():
    print datetime.now(), "process START"

    threads = [
        Thread(
            target=threaded_function,
            args=(thread_num,)
        ) for thread_num in range(THREADS_COUNT)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print datetime.now(), "process END"


def main():
    print "log10(big)", np.log10(BIG_NUMBER)
    print "# threads", THREADS_COUNT
    print "# processes in use per thread", PROC_COUNT, "\n"

    processes = [
        Process(
            target=processed_function()
        ) for _ in range(PROC_COUNT)
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print "Processes finished...exiting"


if __name__ == "__main__":
    main()
