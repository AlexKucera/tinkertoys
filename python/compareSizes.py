#!/usr/bin/env python
# encoding: utf-8
"""
compareSizes.py

Created by Alexander Kucera on 2013-05-22.
Copyright (c) 2013 BabylonDreams. All rights reserved.
"""

import os, sys
from query_yes_no import query_yes_no
from hash_for_file import hash_for_file

def main(argv=None):
	
	filterstring = raw_input('Filter for this file type (please type the file extension, e.g. ".mov" or leave empty to work on all files): ')
	hashing = query_yes_no("Do you want to use the much more time intensive, but accurate checksum approach? (WARNING: Not feasible for anything beyond a couple of GB!!)", default="no")

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
	
	if not hashing:
		print "\n\nPlease be patient. This might take a while. (About 1.5 minutes for 1TB of data over ethernet.)"
	else:
		print "\n\nPlease be patient. This might take a while. (About 1.5 days (!!) for 1TB of data over ethernet.)"
	
	print "\nCaching first path's items…"
	for root, dirs, files in os.walk(inputleft):
		for name in files:
			if filterstring in name:
				nameleft.append(name)
				pathleft.append(os.path.join(root, name))
				countleft += 1
	
	print "Caching second path's items…\n"
	for root, dirs, files in os.walk(inputright):
		for name in files:
			if filterstring in name:
				nameright.append(name)
				pathright.append(os.path.join(root, name))
				countright += 1

	leftset = set(nameleft)
	matches = leftset.intersection(nameright)
	
	copyagain = None
	copyrecord = ""
	exists = 0
	mismatch = 0
	i = 1
	
	for match in matches:
		leftindex = nameleft.index(match)
		rightindex = nameright.index(match)
		if hashing:
			print "Comparing file " + str(i) + " of " + str(len(matches))
			i += 1
			sizeleft=hash_for_file(pathleft[leftindex])
			sizeright=hash_for_file(pathright[rightindex])
		else:
			sizeleft = os.stat(pathleft[leftindex]).st_size
			sizeright = os.stat(pathright[rightindex]).st_size
		if (sizeleft != sizeright):
			mismatch = 1
			if (copyagain == None):
				copyagain = query_yes_no("\n\nThere have been mismatches in size. Do you want to mark the specified files for later processing?")
			if (copyagain == True):
				copyrecord = inputright + "/copyagain.py"
				if exists:
					file = open(copyrecord, 'a')
					file.write("copyFile(\"" + pathleft[leftindex] + "\", \"" + pathright[rightindex] + "\")\n")
					file.close()
				else:
					file = open(copyrecord, 'w')
					file.write("#!/usr/bin/env python\n# encoding: utf-8\nfrom copyFile import copyFile\n\ncopyFile(\"" + pathleft[leftindex] + "\", \"" + pathright[rightindex] + "\")\n")
					file.close()
					exists = 1
			print "\n\n" + match + " has a size mismatch\n"
	if exists and os.path.exists(copyrecord):
		os.chmod(copyrecord, 0755)
		print "\n\nA file with all data to be copied has been written to your destination directory.\n\n" + copyrecord + "\n\nRefine it as you see fit or simply run it to get a new copy of the mismatched files.\n"
	if not mismatch:
		print "There has been no size mismatch!"


if __name__ == "__main__":
	sys.exit(main())
