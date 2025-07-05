#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""

Release Notes:

Show the paths of all footage used in an AfterEffects project.

Please export a footage report via "File->Collect Files…" inside After Effects and save it to disk. Then run this script
on it with `python <path to script> <path to report file>`.

For example:

python /Volumes/Scripting/python/bd_show_used_aftereffects_footage.py /Users/alex/schnitt_43Report.txt


V0.1 Initial Release - 2016-02-23

"""

import os
import re
import sys
import finder_colors


# Child Functions

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
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
            sys.stdout.write("Please respond with 'yes' or 'no' " \
                             "(or 'y' or 'n').\n")


def list_duplicates(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set(x for x in seq if x in seen or seen_add(x))
    # turn the set into a list (as requested)
    return list(seen_twice)


def removeNonAscii(s): return "".join(i for i in s if ord(i) < 126 and ord(i) > 31)


def collectreads(script, batch=False):

    readFootage = False

    sequences = []
    singleFiles = []

    inputFile = open(script, mode='rU')
    wholePathRegEx = re.compile('/[/a-zA-Z0-9\-\_\.#]*')
    fileNameRegEx = re.compile('".*"')

    for line in inputFile:

        if "Number of missing items:" in line:
                readFootage = False

        if readFootage:
            path = wholePathRegEx.search(line)
            name = fileNameRegEx.search(line)
            if name:
                sequences.append(path.group())
            elif path:
                singleFiles.append(path.group())

        if "Collected source files" in line:
            readFootage = True

    inputFile.close()

    print("\n\n" + "#" * 37 + "\n" + "#" * 37 + "\n\n")

    if batch:
        query = "Yes"
    else:
        query = query_yes_no("Do you want to mark the used folders or files in Finder (only works on OS X)?", "no")
    if query:
        for unique_dir in sequences:
            if os.path.exists(unique_dir):
                finder_colors.set(unique_dir, "purple")
        for unique_file in singleFiles:
            if os.path.exists(unique_file):
                finder_colors.set(unique_file, "purple")

    print("\n\n" + "#" * 37 + "\n" + "#" * 37 + "\n\n")
    print("This are all the file sequences:\n\n")
    for i in sequences:
        print(i)
    print("\n\nThis are all the individual files:\n\n")
    for i in singleFiles:
        print i

    if query:
        print("\nThese directories have been colored for your convenience.")
    print("\n\n" + "#" * 37 + "\n" + "#" * 37 + "\n\n")
    return


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("\n\n" + "#" * 37 + "\n" + "#" * 37 + "\n\n")
        print('Usage: bd_show_used_aftereffects_footage.py <after_effects_xml_script>\n\n'
              'You provided only these:\n')
        for pair in sys.argv:
            print pair
        print("\n\n" + "#" * 37 + "\n" + "#" * 37 + "\n\n")
        sys.exit(-1)
    elif len(sys.argv) > 2:
        print("\n\n" + "#" * 37 + "\n" + "#" * 37 + "\n\n")
        batch = query_yes_no("You have provided several script paths at once. Do you "
                             "want to switch to batch processing? This will not list "
                             "the folder and only color them.")
        if batch == "no":
            sys.exit(0)
        else:
            scripts = sys.argv[1:]
            for script in scripts:
                collectreads(script, batch=batch)

    else:
        script = sys.argv[1]
        collectreads(script, batch=False)
