#!/usr/bin/env python
# encoding: utf-8
"""
blog_post_timestamp.py

Created by Alexander Kucera on 2014-10-14.
Copyright (c) 2014 BabylonDreams. All rights reserved.

Simply run the script:

python blog_post_timestamp.py <file>

Searches for the lines Date: and Time: and add the current date and time.

"""

import os
import re
import sys
from datetime import datetime

try:
    path = sys.argv[1]

except:
    print "No filepath given"
    sys.exit(0)

print path
if os.path.exists(path):
    pass
else:
    print "File does not exist."
    sys.exit(0)

### Config ###

now = datetime.now()
todaydate = now.strftime("%d.%m.%Y") # Used for the Date: slot
utctime = now.strftime("%Y-%m-%d-%H-%M-%S") # Used for the Time: slot
redate = re.compile("Date:")
retime = re.compile("Time:")

print todaydate
print utctime

### End Config ###


f = open(path, 'rU')
data = f.readlines()
f.close()

f = open(path, 'w')
for line in data:
    print line
    if redate.match(line):
        print line
        line = line.rstrip("\n")
        line = "".join([line, " ", todaydate, "\n"])
        print line
    elif retime.match(line):
        print line
        line = line.rstrip("\n")
        line = "".join([line, " ", utctime, "\n"])
        print line

    f.write(line)

f.close()


