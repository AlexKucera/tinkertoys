#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""

Release Notes:

V0.1 Initial Release

URLs of note:

http://osxdaily.com/2013/05/13/mount-unmount-drives-from-the-command-line-in-mac-os-x/
http://www.tuxation.com/setuid-on-shell-scripts.html
Use launchd for root script.

"""
import os

import traceback

__author__ = 'alex'


# FUNCTIONS -----------------------------------------------

# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():

    volume = "ProjectsRaid"
    mountpath = "/Volumes/"
    path = mountpath + volume
    faultymount = path + "-1"

    if os.path.exists(faultymount):
        print "A bad mountpoint exists! Trying to fix this now…"
        if os.path.exists(path):
            print "Exists!"


# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    try:
        main()

    except:
        print traceback.format_exc()