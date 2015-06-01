#!/usr/bin/env bash

# Script to automatically deallocate inactive Virtual Machines on Azure every few minutes
# call with azure_stop_idle_vm.sh <intervall in minutes>,
# for example azure_stop_idle_vm.sh 15 to run the deallocate command every 15 minutes

# Config

# defaultintervall=5 # in case no intervall is given at runtime this value will be used
# 
# if (($1)); then
# 	seconds=$(($1*60))
# 	minutes=$(($seconds/60))
# else
# 	seconds=$(($defaultintervall*60))
# 	minutes=$defaultintervall
# fi
# 
# 
# echo "Usage: azure_stop_idle_vm.sh <Intervall in Minutes (defaults to 5)>" > /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 
# echo "Deallocating VMs every $minutes minutes" >> /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 
# while [ 1 = 1 ]
# do
# 
# 	STOPPED=$(azure vm list | grep 'StoppedVM' | awk '{print $2}')
# 	
# 	echo "
# ----------------
# 
# `date +%H:%M:%S`
# " >> /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 	
# 	if [ -n "$STOPPED" ]; then
# 		
# 		echo "The following VMs are in a stopped state:
# 
# " >> /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 		echo $STOPPED >> /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 	
# 		echo "
# 	
# They will be deallocated now…" >> /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 
# 		azure vm list | grep 'StoppedVM' | awk '{system("azure vm shutdown "$2)}' >> /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 		
# 		echo "Finished deallocating." >> /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 		
# 		azure vm list >> /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 	
# 	else
# 		
# 		echo "No idle VMs at this time." >> /Users/alex/Library/Logs/azure_stopp_idle_vm.log
# 	
# 	fi
# 	
# 	sleep $seconds
# 	
# done

LOG="/Users/alex/Library/Logs/azure_stopp_idle_vm.log"

function message {
     echo "$1"
     echo "$1">>${LOG}
    }

function message_new {
     echo "$1"
     echo "$1">${LOG}
    }


LOGSIZE=$( wc -c "$LOG" | awk '{print $1}' )
#echo $LOGSIZE
MAXSIZE=128 # Maximum Log Size in KiloBytes
let "MAXSIZE=1024*$MAXSIZE" # Get the size in bytes


if [ $LOGSIZE -gt $MAXSIZE ]; 
then
	
	message_new "

Deallocating VMs…"

else
	
   	message "

Deallocating VMs…"

fi

STOPPED=$(azure vm list | grep 'StoppedVM' | awk '{print $2}')

message "
----------------

`date +%H:%M:%S`
"

if [ -n "$STOPPED" ]; then
	
	message "The following VMs are in a stopped state:

"

	message $STOPPED
	
	message "
	
They will be deallocated now…"
	
	exec 3>&1 1>>${LOG} 2>&1
	azure vm list | grep 'StoppedVM' | awk '{system("azure vm shutdown "$2)}' | tee /dev/fd/3
	
	message "Finished deallocating."
	
	azure vm list | tee /dev/fd/3
	
else
	
 	message "No idle VMs at this time."
	
fi