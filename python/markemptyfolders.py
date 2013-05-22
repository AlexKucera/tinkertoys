#!/usr/bin/env python
# encoding: utf-8
"""
markemptyfolders.py

This is a placeholder creator to keep folders trackable with Git.
Call it as follows:

	[path to script]/markemptyfolders.py <path to scan>

Created by Alexander Kucera on 2013-05-22.
Copyright (c) 2013 BabylonDreams. All rights reserved.
"""

import os, sys, getopt

help_message = '''


This is a placeholder creator to keep folders trackable with Git.

[path to script]/markemptyfolders.py <path to scan>

'''

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	empty = 0
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
		except getopt.error, msg:
			raise Usage(msg)

		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
		try:
			path = sys.argv[1]
			if os.path.isdir(path):
				# remove empty subfolders
				for root, dirs, files in os.walk(path):
					if '.git' in dirs:
					        dirs.remove('.git')
					for name in dirs:
						names = os.path.join(root, name)
						# if folder empty, mark it
						files = os.listdir(names)
						if len(files) == 0:
							keepme = names + "/keepme.md"
							file = open(keepme, 'w')
							file.write('This is a placeholder file to keep this file\'s parent folder trackable with Git for further reference, since it doesn\'t make sense to track, for example, whole software packages that are easily redownloadable again.')
							file.close()
							print "Created " + keepme
							empty += 1
				if empty == 0:
					print "No empty directories in this tree."
		except:
			raise Usage(help_message)

	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		return 2

if __name__ == "__main__":
	sys.exit(main())
