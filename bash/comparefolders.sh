#!/usr/bin/env bash

# 
#   Compare two folders for any file differences
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: comparefolders.sh <path 1> <path 2>
# 

if [[ ! $1 ]]; then
	echo "Usage: comparefolders.sh <path 1> <path 2>"
	exit
	if [[ ! $2 ]]; then
		echo "Usage: comparefolders.sh <path 1> <path 2>"
		exit
	fi
fi

diff -qr "$1" "$2"| grep -v -e 'DS_Store' -e 'Thumbs' > ~/compare.txt

if [ "$?" == "0" ]; then
	echo "Encode Successful!"
	exit 0
fi

