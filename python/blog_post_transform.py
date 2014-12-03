#!/usr/bin/env python
# encoding: utf-8
"""
blog_post_transform.py

Created by Alexander Kucera on 2014-10-14.
Copyright (c) 2014 BabylonDreams. All rights reserved.

Simply run the script:

python blog_post_transform.py

"""

import os
import re
import sys
from datetime import datetime, date, time

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
todaydate = now.strftime("%d.%m.%Y")
utctime = now.strftime("%Y-%m-%d-%H-%M-%S")

# where you exported your post as Markdown file.
#path = "/Users/alex/Dropbox/Apps/Ulysses/"

template  = """
----

Date: """ + todaydate + """

----

Time: """ + utctime + """

----

Link:

----

Via:

----

Text: """

### End Config ###


f = open(path)
data = f.readlines()
f.close()
# Manually grab the title of the article
firstline = data[0]
title = firstline[1:]
body = data[1:]
	
f = open(path, 'w')
f.write("Title: " + title)
f.write(template)
for line in data[1:]:
	f.write(line)
f.close()


