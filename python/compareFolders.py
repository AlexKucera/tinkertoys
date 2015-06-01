#!/usr/bin/env python
# encoding: utf-8
"""
compareSizes.py

Created by Alexander Kucera on 2013-05-22.
Copyright (c) 2013 BabylonDreams. All rights reserved.
"""

import os, sys


def main():
    copyrecord = os.path.expanduser("~/folder-differences.txt")

    filterstring = raw_input('Filter for this file type (please type the file '
                             'extension, e.g. ".mov" or leave empty to work on all '
                             'files): ')

    inputleft = raw_input("Enter your first path (the one copied from): ")
    if not os.path.isdir(inputleft):
        return "Error, not a valid path"
    countleft = 0
    pathleft = []
    nameleft = []

    inputright = raw_input("Enter your second path (the one copied to): ")
    if not os.path.isdir(inputright):
        return "Error, not a valid path"
    countright = 0
    pathright = []
    nameright = []

    print "\n\nPlease be patient. This might take a while. (About 1.5 minutes for " \
          "1TB of data over ethernet.)\n"

    print("Caching first path's items…")
    for root, dirs, files in os.walk(inputleft):
        for name in files:
            if filterstring in name:
                nameleft.append(name)
                pathleft.append(os.path.join(root, name))
                countleft += 1

    print(str(countleft) + " items found.\n")

    print("Caching second path's items…")
    for root, dirs, files in os.walk(inputright):
        for name in files:
            if filterstring in name:
                nameright.append(name)
                pathright.append(os.path.join(root, name))
                countright += 1

    print(str(countright) + " items found.\n")

    differences = None
    differences = sorted(list(set(nameleft).symmetric_difference(set(nameright))))

    if differences is None:
        print "There has been no mismatch!"
    else:
        print("These files differ:")

        for differ in differences:
            print differ

            if os.path.exists(copyrecord):
                file = open(copyrecord, 'a')
                file.write(differ + "\n")
                file.close()
            else:
                file = open(copyrecord, 'w')
                file.write(differ + "\n")
                file.close()


if __name__ == "__main__":
    sys.exit(main())
