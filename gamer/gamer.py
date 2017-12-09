# !/usr/bin/python2
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Make your machine use its full potential to solve GAME models """

import time
from datetime import datetime
from multiprocessing import Pool
from threading import Thread

import numpy as np

BIG_NUMBER = 3 * 10 ** 4
THREADS_COUNT = 6
PROC_COUNT = 2


def get_pretty_date(dt):
    return dt.strftime("%H:%M:%S")


def very_intensive_calc(big_num):
    for _ in range(big_num):
        _ * _
    return big_num


def threaded_function(thread_name, big_num, processes):
    print "\t", get_pretty_date(datetime.now()), "->", thread_name, \
        "THREAD ON"
    pool = Pool(processes=processes)
    results = pool.map(
        very_intensive_calc,
        range(1, big_num)
    )
    pool.close()
    pool.join()
    print "\t", get_pretty_date(datetime.now()), "->", thread_name, \
        "THREAD OFF"


def tester(big_num, threads, processes):
    print "log10(big)", np.log10(big_num)
    print "# threads", threads
    print "# processes", processes, "\n"
    print "Time now:", get_pretty_date(datetime.now())

    stopwatch = time.time()
    threads = [
        Thread(
            target=threaded_function,
            args=(thread_num, big_num, processes)
        ) for thread_num in range(threads)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    stopwatch = time.time() - stopwatch
    print "Time now:", get_pretty_date(datetime.now())
    print "Elapsed seconds:", stopwatch


def main():
    for thread in range(1, 2):
        for proc in range(1, 6):
            tester(BIG_NUMBER, thread, proc)


if __name__ == "__main__":
    main()
