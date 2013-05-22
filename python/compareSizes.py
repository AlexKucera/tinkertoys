#!/usr/bin/env python
# encoding: utf-8
"""
compareSizes.py

Created by Alexander Kucera on 2013-05-22.
Copyright (c) 2013 BabylonDreams. All rights reserved.
"""

import os, sys

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


def main(argv=None):
	
	filterstring = raw_input('Filter for this file type (please type the file extension, e.g. ".mov"): ')
	inputleft = raw_input("Enter your first path (the one copied from): ") #"/Volumes/WD_POKA_1/"
	countleft = 0
	pathleft = []
	nameleft = []
	sizeleft = []

	for root, dirs, files in os.walk(inputleft):
		for name in files:
			if filterstring in name:
				sizeleft.append(os.stat(os.path.join(root, name)).st_size)
				nameleft.append(name)
				pathleft.append(os.path.join(root, name))
				countleft += 1

	# print countleft
	# print sizeleft
	# print pathleft
	# print nameleft

	inputright = raw_input("Enter your second path (the one copied to): ") #"/Volumes/ProjectsRaid/WorkingProjects/jollefilm/jf-2012_001-poka/img/plates/conform"
	countright = 0
	pathright = []
	nameright = []
	sizeright = []

	for root, dirs, files in os.walk(inputright):
		for name in files:
			if filterstring in name:
				sizeright.append(os.stat(os.path.join(root, name)).st_size)
				nameright.append(name)
				pathright.append(os.path.join(root, name))
				countright += 1

	# print countright
	# print sizeright
	# print pathright
	# print nameright

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
					file.write("shutil.copy2(" + pathleft[leftindex] + ", " + pathright[rightindex] + ")\n")
					file.close()
				else:
					file = open(copyrecord, 'w')
					file.write("#!/usr/bin/env python\n# encoding: utf-8\nimport shutil\n\nshutil.copy2(" + pathleft[leftindex] + ", " + pathright[rightindex] + ")\n")
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
