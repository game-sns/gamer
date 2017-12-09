# !/usr/bin/python2
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Power-up your machine to solve GAME models """

import time
from datetime import datetime
from multiprocessing import Pool
from threading import Thread

import numpy as np

from utils import get_pretty_date, write_data_to_json, very_intensive_calc

BIG_NUMBER = 3 * 10 ** 4
THREADS_COUNT = 6
PROC_COUNT = 2


def threaded_function(thread_name, big_num, processes):
    print "\t", get_pretty_date(datetime.now()), "->", thread_name, \
        "THREAD ON"
    pool = Pool(processes=processes)
    _ = pool.map(
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
    return stopwatch


def main():
    """
    :return: void
        Runs core algorithm
    """

    max_threads = 8
    max_processes = 8
    test_results = []

    for thread in range(1, max_threads + 1):
        test_result = {}
        for proc in range(1, max_processes + 1):
            stopwatch = tester(BIG_NUMBER, thread, proc)
            test_result[proc] = stopwatch
        test_result["thread"] = thread
        test_results.append(test_result)

    write_data_to_json(test_results, "out.json")


if __name__ == "__main__":
    main()
