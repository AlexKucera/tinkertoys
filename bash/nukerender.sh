#!/usr/bin/env bash

# Requires http://caspian.dotconf.net/menu/Software/SendEmail/

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

# If there are Furnace nodes in the comp, then you need to use the interactive license for rendering.

#nuke -x -i myscript.nk

# To display a list of command line flags (switches) available to you, use the following command:
# nuke -help

CORES=$(getconf _NPROCESSORS_ONLN)
NUKE=$NUKEPATH
FLAGS="-x -m $CORES --gpu -f"
COMMAND="$NUKE $1 $FLAGS"

#!/bin/bash

source /Volumes/ProjectsRaid/x_Pipeline/Scripting/tinkertoys/bash/mail_send.conf
SUBJECT="Nuke render completed"
MACHINE=$(hostname -s)


START=$(date +%s)
STARTDATE=$(date -j -f "%s" "`date +%s`" "+%A, %d.%m.%Y %T")


# basic Nuke render command line

#$COMMAND /Volumes/ProjectsRaid/WorkingProjects/peri/peri-2014_002-kopfspindel/work/nuke/kopfspindelrahmen_justieren_durchlauf_v05.nk
$COMMAND /Volumes/ProjectsRaid/WorkingProjects/peri/peri-2014_002-kopfspindel/work/nuke/kopfspindelrahmen_justieren_ohne_v04.nk
$COMMAND /Volumes/ProjectsRaid/WorkingProjects/peri/peri-2014_002-kopfspindel/work/nuke/kopfspindelrahmen_justieren_zoomout_v04.nk
$COMMAND /Volumes/ProjectsRaid/WorkingProjects/peri/peri-2014_002-kopfspindel/work/nuke/kopfspindelrahmen_justieren_zoom_v04.nk
$COMMAND /Volumes/ProjectsRaid/WorkingProjects/peri/peri-2014_002-kopfspindel/work/nuke/kopfspindelrahmen_justieren_mit_v04.nk

END=$(date +%s)
ENDDATE=$(date -j -f "%s" "`date +%s`" "+%A, %d.%m.%Y %T")
secs=$((END-START))
DURATION=$(printf '%dh:%02dm:%02ds\n' $(($secs/3600)) $(($secs%3600/60)) $(($secs%60)))

BODY="${MACHINE} just finished rendering all assigned Nuke scripts. It started at ${STARTDATE} and ended at ${ENDDATE} taking ${DURATION} overall."

sendemail -f ${FROM_ADDRESS} -t ${TO_ADDRESS} -m ${BODY} -u ${SUBJECT} -s ${SERVER} -xu ${USER} -xp ${PASS}