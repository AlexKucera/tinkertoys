#!/bin/bash

LOG="/Users/alex/Documents/scripts/mount_unmount_bootable.log"
LOGSIZE=$( wc -c "$LOG" | awk '{print $1}' )
echo $LOGSIZE
MAXSIZE=128 # Maximum Log Size in KiloBytes
let "MAXSIZE=1024*$MAXSIZE" # Get the size in bytes


if [ $LOGSIZE -gt $MAXSIZE ]; 
then
   echo "Larger"
else
   echo "Smaller"
fi