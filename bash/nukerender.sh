#!/usr/bin/env bash

# Rendering on the command line
################################

# To render frame 5 of a Nuke script:
# nuke -F 5 -x myscript.nk

# To render frames 30 to 50 of a Nuke script:
# nuke -F 30-50 -x myscript.nk

# To render two frame ranges, 10-20 and 34-60, of a Nuke script:
# nuke -F 10-20 -F 34-60 -x myscript.nk

# To render every tenth frame of a 50 frame sequence of a Nuke script:
# This renders frames 1, 11, 21, 31, 41.
# nuke -F 1-50x10 -x myscript.nk

# In a script with two write nodes called WriteBlur and WriteInvert this command just renders frames 1 to 20 from the WriteBlur node:
# nuke -X WriteBlur myscript.nk 1-20

# To display a list of command line flags (switches) available to you, use the following command:
# nuke -help

NUKE="/Applications/Nuke9.0v4/NukeX9.0v4.app/NukeX9.0v4"
FLAGS="-x -m 8 --gpu -f"
COMMAND="$NUKE $FLAGS"

# basic Nuke render command line

$COMMAND -X Write3 "/Volumes/ProjectsRaid/WorkingProjects/manicgrin/manicgrin-2014_001_all-in-a-days-work/work/nuke/deadpixels_v01.nk"