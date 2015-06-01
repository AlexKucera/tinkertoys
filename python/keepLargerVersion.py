#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""

Keeps the larger of two identically named files. Doesn't care about file extensions.
If two files have the same size the older one is kept.

Release Notes:

V0.1 Initial Release

"""
import os
import traceback
import time

__author__ = 'alex'


# FUNCTIONS -----------------------------------------------

def list_duplicates(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set(x for x in seq if x in seen or seen_add(x))
    # turn the set into a list (as requested)
    return list(seen_twice)

# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():
    count = 0
    searchpath = "/Volumes/StreamingMedia/Media-Archiv/Film - TV/Serien/WatchOnce"
    filenames = []
    filepath = []

    print "\nCaching items…"
    for root, dirs, files in os.walk(searchpath):
        for name in files:
            filenames.append(os.path.splitext(name)[0])
            filepath.append(os.path.join(root, name))
            count += 1

    dupes = list_duplicates(filenames)
    reversefiles = list(reversed(filenames))
    size = len(filenames)
    print "Found " + str(size) + " items."

    if len(dupes) > 0:
        print "\nDuplicates found: \n", "\n".join(dupes), "\n"
        for dupe in dupes:

            index1 = filenames.index(dupe)
            index2 = size - reversefiles.index(dupe) - 1
            file1 = filepath[index1]
            file2 = filepath[index2]
            file1size = os.path.getsize(file1)
            file2size = os.path.getsize(file2)

            if file1size > file2size:
                print "Removing " + file2
                os.remove(file2)
            elif file2size > file1size:
                print "Removing " + file1
                os.remove(file1)
            elif file1size == file2size:
                file1create = os.path.getctime(file1)
                file2create = os.path.getctime(file2)
                if file1create < file2create:
                    print "Removing " + file2
                    os.remove(file2)
                else:
                    print "Removing " + file1
                    os.remove(file1)

        filenames = []
        for root, dirs, files in os.walk(searchpath):
            for name in files:
                filenames.append(os.path.splitext(name)[0])
                count += 1

        size = len(filenames)
        print "Found " + str(size) + " items after the cleanup."

    else:
        print "\nNo Duplicates found."


# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    try:
        main()

    except:
        print traceback.format_exc()