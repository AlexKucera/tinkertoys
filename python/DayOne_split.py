#!/usr/bin/env python
# encoding: utf-8
"""
DayOne_split.py

Created by Alexander Kucera on 2013-05-16.
Copyright (c) 2013 BabylonDreams. All rights reserved.

Yesterday's discussion with http://alpha.app.net/ronnie inspired me to "rescue" all my DayOne entries into  plain text as well. This is a little script that splits a Markdown export from the DayOne desktop app into one plain text file per day with a naming of your choosing.

Simply run the script:

python DayOne_split.py

"""

import parsedatetime.parsedatetime as pdt #requires https://github.com/bear/parsedatetime
p = pdt.Calendar()

from time import mktime
from datetime import datetime

### Config ###

"""
The config below will give you a range of file
(one per day, not one per entry) that are named 
like "journal_2011-08-19_dayone-export.md"
"""

# where you exported your DayOne library as Markdown file.
# this is also the path for the newly split up entries
path = "/Users/alex/Dropbox/Apps/Day One/Export/"

#what you called the exported file
exportfile = "DayOne.md"

#if you want your new split entries to have any fixed prefix in the filename
splitfileprefix = "journal_"

#if you want to have any specific fixed suffix in the filename
splitfilesuffix = "_dayone-export"

#what extentsion should the new split up entries have?
splitfileextension = "md"

#here you can decide how to format the date that is appearing in your split up entries. 
#Fomatting accodring to http://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
splitfiledate = "%Y-%m-%d"

### End Config ###


fread = open(path+exportfile)

count = 1

# Manually grab the date of the very first entry, which we need before we enter the loop
firstline = next(fread)
entrydate = firstline[7:]

dt = p.parseDateText(str(entrydate))
dt = datetime.fromtimestamp(mktime(dt))
result = dt.strftime(splitfiledate)

fwrite = open(path + splitfileprefix + result + splitfilesuffix + "." + splitfileextension, 'w')

for line in fread:
	if "	Date:	" in line:
		entrydate = line[7:]
		dt = p.parseDateText(str(entrydate))
		dt = datetime.fromtimestamp(mktime(dt))
		newdate = dt.strftime("%Y-%m-%d")
		print "Result: " +  result
		print "Newdate: " + newdate
		if newdate != result:
			# close open file object, increment count, open new file object
			fwrite.close()
			count += 1
			result = newdate
			fwrite = open(path + splitfileprefix + result + splitfilesuffix + "." + splitfileextension, 'w')
			fwrite.write(line + "\n")
		else:
			fwrite.write(line + "\n")
	else:
		fwrite.write(line + "\n")
fwrite.close()
fread.close()

