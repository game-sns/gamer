# !/usr/bin/python2
# coding: utf-8

# Copyright YYYY AUTHORS
#
# YOUR COPYRIGHT HERE (IF YOU WANT IT)


""" Make your machine use its full potential to solve GAME models """

from threading import Thread
from time import sleep


def threaded_function(counter, thread_name):
    for i in range(counter):
        print thread_name, "is RUNNING counter", i
        sleep(1)  # << calculations here
        print thread_name, "has DONE counter", i


if __name__ == "__main__":
    threads = [
        Thread(
            target=threaded_function,
            args=(5, thread_num)
        ) for thread_num in range(4)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print "Threads finished...exiting"
