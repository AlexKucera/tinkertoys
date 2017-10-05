#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
${PROJECT_NAME} - ${NAME}

Release Notes:

V0.1 Initial Release - ${YEAR}-${MONTH}-${DAY}

"""

import argparse
import traceback


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
import sys

import os


def main(infile):
    newpath = "U:\\BabylonDreams\\010_0010_v08\\imported_images\\"
    paths = ["/Volumes/ProjectsRaid/WorkingProjects/peri/peri-2016_001-ACS/img/textures/",
             "/Volumes/ProjectsRaid/WorkingProjects/peri/peri-2014_000-sharedspace/img/textures/",
             "/Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/modo/content/Kits/vizpak_products_vray_octane-1.0.0/VizPak_Products/Images/Metal/",
             "/Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/modo/content/Kits/vizpak_products_vray_octane-1.0.0/VizPak_Products/Images/Wood/"]

    with open(infile) as readfile:
        file_str = readfile.read()

    outstr = []

    for line in file_str.splitlines(True):

        for path in paths:
            if path in line:
                replace = line.replace(path, newpath)
                print("{} → {}".format(line, replace))
                line = replace

        outstr.append(line)

    file_str = ''.join(outstr)

    outfile = os.path.splitext(infile)[0] + "_volker" + os.path.splitext(infile)[1]

    with open(outfile, "w") as f:
            f.write(file_str)





# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':

    # Set up optional arguments
    parser = argparse.ArgumentParser(description="Switches out paths of a provided vrscene file.")
    parser.add_argument("input", help="input file")

    # Parse arguments
    try:
        args = parser.parse_args()
        # Assign or use argument values

        if not args.input:
            print("\nNo input file specified\n\n")
            parser.print_help()
        else:
            infile = args.input

            try:
                main(infile)
            except:
                print traceback.format_exc()

    except:

        sys.exit(0)