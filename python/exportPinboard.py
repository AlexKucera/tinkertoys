#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""

Release Notes:

Exports all Pinboard bookmarks as XML for further processing.

V0.1 Initial Release

"""

import traceback
import os
from datetime import datetime
import urllib2

import pytz
import shutil

__author__ = 'alex'


# FUNCTIONS -----------------------------------------------

# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():

    # Parameters.
    bookmarkdir = os.environ['HOME'] + '/Dropbox/Apps/pinboard/'
    pinboard_credentials = bookmarkdir + 'pinboard_credentials.txt'
    current = bookmarkdir + 'most_current_bookmarks.xml'

    pinboard_api = 'https://api.pinboard.in/v1/'
    yearfmt = '%Y'
    datefmt = '%m-%d'
    homeTZ = pytz.timezone('GMT')
    y = datetime.now(pytz.utc).strftime(yearfmt)
    t = datetime.now(pytz.utc).strftime(datefmt)

    daily_file = bookmarkdir + y + '/pinboard-backup.' + t + '.xml'

    # Get the user's authentication token
    with open(pinboard_credentials) as credentials:
        for line in credentials:
            me, token = line.split(':')

    if not os.path.exists(bookmarkdir + y):
        os.makedirs(bookmarkdir + y)

    # Set up a new bookmarks file
    bookmarkfile = open(daily_file, 'w')

    # Get all the posts from Pinboard
    u = urllib2.urlopen(pinboard_api + 'posts/all?auth_token=' + me + ':' + token)
    bookmarkfile.write(u.read())
    bookmarkfile.close()
    shutil.copy2(daily_file, current)


# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    try:
        main()

    except:
        print traceback.format_exc()