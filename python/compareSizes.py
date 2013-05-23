#!/usr/bin/env python
# encoding: utf-8
"""
compareSizes.py

Created by Alexander Kucera on 2013-05-22.
Copyright (c) 2013 BabylonDreams. All rights reserved.
"""

import os, sys
from query_yes_no import query_yes_no

def main(argv=None):
	
	filterstring = raw_input('Filter for this file type (please type the file extension, e.g. ".mov"): ')

	inputleft = raw_input("Enter your first path (the one copied from): ")
	if not os.path.isdir(inputleft):
		return "Error, not a valid path"
	countleft = 0
	pathleft = []
	nameleft = []
	sizeleft = []
	
	inputright = raw_input("Enter your second path (the one copied to): ")
	if not os.path.isdir(inputright):
		return "Error, not a valid path"
	countright = 0
	pathright = []
	nameright = []
	sizeright = []
	
	print "Please be patient. This might take a while. (About 1.5 minutes for 4TB of data over ethernet.)"

	for root, dirs, files in os.walk(inputleft):
		for name in files:
			if filterstring in name:
				sizeleft.append(os.stat(os.path.join(root, name)).st_size)
				nameleft.append(name)
				pathleft.append(os.path.join(root, name))
				countleft += 1

	for root, dirs, files in os.walk(inputright):
		for name in files:
			if filterstring in name:
				sizeright.append(os.stat(os.path.join(root, name)).st_size)
				nameright.append(name)
				pathright.append(os.path.join(root, name))
				countright += 1

	leftset = set(nameleft)
	matches = leftset.intersection(nameright)
	
	copyagain = None
	copyrecord = ""
	exists = 0
	mismatch = 0
	
	for match in matches:
		leftindex = nameleft.index(match)
		rightindex = nameright.index(match)
		if (sizeleft[leftindex] != sizeright[rightindex]):
			mismatch = 1
			if (copyagain == None):
				copyagain = query_yes_no("\n\nThere have been mismatches in size. Do you want to mark the specified files for later processing?")
			if (copyagain == True):
				copyrecord = inputright + "/copyagain.py"
				if exists:
					file = open(copyrecord, 'a')
					file.write("copyFile(" + pathleft[leftindex] + ", " + pathright[rightindex] + ")\n")
					file.close()
				else:
					file = open(copyrecord, 'w')
					file.write("#!/usr/bin/env python\n# encoding: utf-8\nfrom copyFile import copyFile\n\ncopyFile(\"" + pathleft[leftindex] + "\", \"" + pathright[rightindex] + "\")\n")
					file.close()
					exists = 1
			print match + " has a size mismatch"
	if exists and os.path.exists(copyrecord):
		os.chmod(copyrecord, 0755)
		print "\n\nA file with all data to be copied has been written to your destination directory.\n\n" + copyrecord + "\n\nRefine it as you see fit or simply run it to get a new copy of the mismatched files.\n"
	if not mismatch:
		print "There has been no size mismatch!"


if __name__ == "__main__":
	sys.exit(main())
