#!/usr/bin/env python

# Python script to fix broken symlinks
# Monday, Sep 26, 2011 4:47 pm
# http://www.webarnes.ca/2011/09/python-script-to-fix-broken-symlinks/
#
# I recently added a new hard drive and reorganized my increasingly chaotic and whimsically named storage and backup partitions. 
# In the process, I moved a folder containing hundreds of symlinks to a different drive resulting in hundreds of broken symlinks (I should have used rsync).
# 
# This script will repair symlinks after you’ve moved a folder. Change BASEDIR to the current location of your files and OLDBASE to where they used to be. 
# For example, if you moved all your files from /mnt/Backup2 to /mnt/Backup2, then BASEDIR = ‘/mnt/Backup2′ and OLDBASE = ‘/mnt/Backup1′. 
# If you want to test (to make sure it will do what you expect) then change DEBUG to True.
# 
# This script will only fix symlinks that point to files/directories within the BASEDIR.

 
import os
 
# Configuration
 
BASEDIR = '/Volumes/ProjectsRaid/WorkingProjects'
OLDBASE = '/Volumes/Happy-SwapRAID/WorkingProjects'
DEBUG = True # I recommend a test run first
 
def relink(path):
    old_target = os.path.realpath(path)
    new_target = old_target.replace(OLDBASE,BASEDIR,1)
    if DEBUG:
        print "Relink: " + path + "\n\tfrom " + old_target + "\n\tto " + new_target
    else:
        os.remove(path)
        os.symlink(new_target,path)
 
for root, dirs, files in os.walk(BASEDIR):
    for filename in files:
        fullpath = os.path.join(root,filename)
        if os.path.islink(fullpath):
            relink(fullpath)
    for dirname in dirs:
        fullpath = os.path.join(root,dirname)
        if os.path.islink(fullpath):
            relink(fullpath)