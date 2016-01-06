#!/bin/bash

# Requires http://caspian.dotconf.net/menu/Software/SendEmail/

source /Volumes/ProjectsRaid/x_Pipeline/Scripting/tinkertoys/bash/mail_send.conf
SUBJECT="modo render completed"
MACHINE=$(hostname -s)


START=$(date +%s)
STARTDATE=$(date -j -f "%s" "`date +%s`" "+%A, %d.%m.%Y %T")






END=$(date +%s)
ENDDATE=$(date -j -f "%s" "`date +%s`" "+%A, %d.%m.%Y %T")
secs=$((END-START))
DURATION=$(printf '%dh:%02dm:%02ds\n' $(($secs/3600)) $(($secs%3600/60)) $(($secs%60)))

BODY="${MACHINE} just finished rendering a shot. It started at ${STARTDATE} and ended at ${ENDDATE} taking ${DURATION} overall."

sendemail -f ${FROM_ADDRESS} -t ${TO_ADDRESS} -m ${BODY} -u ${SUBJECT} -s ${SERVER} -xu ${USER} -xp ${PASS}