#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
tinkertoys - timer.py

Release Notes:

V0.1 Initial Release - 2017-08-23

"""


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
import timeit


def timer(elapsed=0.0, name=''):
    """
    Timer function for debugging.

    Example:

        start = bd_helpers.timer()

        bd_helpers.timer(start, "test")

    """
    running_timer = timeit.default_timer()
    if elapsed != 0.0:
        running_time = running_timer - elapsed
        timestring = secondsToHoursMinutesSeconds(running_time)
        if name is not '':
            name += ' '
        print('{0}Running Time: {1}'.format(name, timestring))
    return running_timer


def secondsToHoursMinutesSeconds(seconds):
    """ takes a seconds int or float and returns a string that breaks"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours != 0:
        hours = "{} hours ".format(int(hours))
    else:
        hours = ""
    if minutes != 0:
        minutes = "{} minutes ".format(int(minutes))
    else:
        minutes = ""
    seconds = "{:.2f} seconds".format(seconds)

    secondsToString = '{hours}{minutes}{seconds}'.format(hours=hours, minutes=minutes, seconds=seconds)

    return secondsToString

# END MAIN PROGRAM -----------------------------------------------