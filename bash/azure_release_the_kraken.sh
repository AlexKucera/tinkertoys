#!/usr/bin/env bash

# Script to automatically start the Azure renderfarm VMs one by one.
# https://github.com/azure/azure-xplat-cli

RUNNING=$(azure vm list | grep 'ReadyRole' | awk '{print $2}')

if [ -n "$RUNNING" ]; then
	
	if [ "$RUNNING" == "Render01" ]; then
		
		echo "Render01 is already running. Starting all the others."
		azure vm start RenderClient01
		azure vm start RenderClient02
		azure vm start RenderClient03
		azure vm start RenderClient04
		
	else
		
		echo "More then just Render01 is running. Please start the missing VMs by hand."
		echo "The following machines are already online:"
		echo $RUNNING
		
	fi
	
else
	
	echo "Starting the whole farm."
	azure vm start Render01
	azure vm start RenderClient01
	azure vm start RenderClient02
	azure vm start RenderClient03
	azure vm start RenderClient04
	
fi