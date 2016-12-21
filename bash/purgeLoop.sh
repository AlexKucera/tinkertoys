#!/usr/bin/env bash

# Script to automatically purge inactive memory every few minutes
# call with purgeLoop.sh <intervall in minutes>,
# for example purgeLoop.sh 15 to run the purge command every 15 minutes

# Additonally, the script has some basic smarts built in so it only triggers a purge when it is effective to do so.
# It doesn't make sense to purge inactive RAM, if only 10MB inactive RAM are available to be purged. Even if your free RAM is running low.
# If you are runnig out of RAM, but don't have any inactive RAM available, then it is time to consider a RAM upgrade, not this script.

# Config

defaultintervall=15 # in case no intervall is given at runtime this value will be used
minimum_ram_percent=5 # minimum amount of RAM, in percent of your overall RAM, before purge is triggered. 5% is a good base value. Increase to trigger purge sooner.
inactive_ram_percent=15 # minimum amount of inactive RAM, in percent of your overall RAM, that has to be present before purge is triggered. Lower this value to trigger purge sooner.

if (($1)); then
	seconds=$(($1*60))
	minutes=$(($seconds/60))
else
	seconds=$(($defaultintervall*60))
	minutes=$defaultintervall
fi


echo "Usage: purgeLoop.sh <Intervall in Minutes (defaults to 15)>"

echo "Purging RAM every $seconds seconds or $minutes minutes"

FREE_BLOCKS=$(vm_stat | grep free | awk '{ print $3 }' | sed 's/\.//')
INACTIVE_BLOCKS=$(vm_stat | grep inactive | awk '{ print $3 }' | sed 's/\.//')
SPECULATIVE_BLOCKS=$(vm_stat | grep speculative | awk '{ print $3 }' | sed 's/\.//')
ACTIVE_BLOCKS=$(vm_stat | grep 'ages active' | awk '{ print $3 }' | sed 's/\.//')
WIRED_BLOCKS=$(vm_stat | grep wired | awk '{ print $4 }' | sed 's/\.//')

installed_ram=$((($FREE_BLOCKS+$SPECULATIVE_BLOCKS+$INACTIVE_BLOCKS+$ACTIVE_BLOCKS+$WIRED_BLOCKS)*4096/1048576))
ram_limit=$(($installed_ram/(100/$minimum_ram_percent)))
inactive_limit=$(($installed_ram/(100/$inactive_ram_percent)))

echo "
RAM limit $ram_limit MB (purge if Free RAM is below this limit)"
echo "Freeing limit $inactive_limit MB (only purge if Inactive RAM is above this limit)"

while [ 1 = 1 ]
do

	FREE_BLOCKS=$(vm_stat | grep free | awk '{ print $3 }' | sed 's/\.//')
	INACTIVE_BLOCKS=$(vm_stat | grep inactive | awk '{ print $3 }' | sed 's/\.//')
	SPECULATIVE_BLOCKS=$(vm_stat | grep speculative | awk '{ print $3 }' | sed 's/\.//')

	FREE=$((($FREE_BLOCKS+SPECULATIVE_BLOCKS)*4096/1048576))
	INACTIVE=$(($INACTIVE_BLOCKS*4096/1048576))
	echo "
----------------

`date +%H:%M:%S`
	"
	echo Free:       	$FREE MB
	echo Inactive:   	$INACTIVE MB
	echo RAM limit: 	$ram_limit MB - purge if Free RAM is below this limit
	echo Freeing limit:	$inactive_limit MB - only purge if Inactive RAM is above this limit
	
	if (( $FREE <= $ram_limit )); then
		if (($INACTIVE >= $inactive_limit )); then
			purge &
			wait
			echo "
`date +%H:%M:%S` - RAM purged"
			
			FREE_BLOCKS=$(vm_stat | grep free | awk '{ print $3 }' | sed 's/\.//')
			INACTIVE_BLOCKS=$(vm_stat | grep inactive | awk '{ print $3 }' | sed 's/\.//')
			SPECULATIVE_BLOCKS=$(vm_stat | grep speculative | awk '{ print $3 }' | sed 's/\.//')
			
			FREE=$((($FREE_BLOCKS+SPECULATIVE_BLOCKS)*4096/1048576))
			INACTIVE=$(($INACTIVE_BLOCKS*4096/1048576))
			echo ""
			echo Free after Purge:       $FREE MB
			echo Inactive after Purge:   $INACTIVE MB
		else
			echo "
No purge, because you have too little inactive RAM to be worth it."
		fi
	else
		echo "
No purge, because you still have enough RAM to work a bit."
	fi
	
	sleep $seconds
	
done