#!/usr/bin/env bash
OUTPUT="/Users/alex/Documents/ApplicationList.txt"
USERAPPS="/Users/alex/Applications"

echo 'time of latest update:' > $OUTPUT
date >> $OUTPUT
echo '
This file lists all the apps in ~/Applications, /Applications and /Applications/Utilities 
for future restoration purposes, because the actual apps are not being backed up.
It also list any custom binaries installed via Homebrew (https://github.com/mxcl/homebrew/wiki)

##################################################
List of '$USERAPPS'
##################################################
' >> $OUTPUT

if [[ -L "$USERAPPS" ]]; then 
	echo "$USERAPPS is a symlink" >> $OUTPUT;
else 
	cd $USERAPPS && ls >> $OUTPUT
fi
echo '



##################################################
List of /Applications/
##################################################

' >> $OUTPUT
cd /Applications/ && ls >> $OUTPUT
echo '



##################################################
List of /Applications/Utilities/
##################################################

' >> $OUTPUT
cd /Applications/Utilities/ && ls >> $OUTPUT
echo '



##################################################
List of Homebrew binaries
##################################################

' >> $OUTPUT
/usr/local/bin/brew list >> $OUTPUT

echo '



##################################################
Detailed Infos about Homebrew binaries 
can be found in Tinkertoys Brewfile
##################################################

' >> $OUTPUT

brew bundle --force --file=/Volumes/ProjectsRaid/x_Pipeline/Scripting/tinkertoys/bash/Brewfile dump