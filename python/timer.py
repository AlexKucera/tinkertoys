#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
tinkertoys - timer.py

Release Notes:

V0.1 Initial Release - 2017-08-23

Copyright 2017 - BabylonDreams - Alexander Kucera & Monika Kucera GbR

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

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