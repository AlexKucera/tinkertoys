#!/usr/bin/env bash

# 
#   DIY Transcoding stereo to two mono streams
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: split_stereo_to_mono.sh <path to file>
# 

if [[ ! $1 ]]; then
	echo "Usage: split_stereo_to_mono.sh <path to file> (always outputs Apple Lossless files)"
	exit
fi

fullpath=$1

#echo $fullpath
filename="${fullpath##*/}"                      # Strip longest match of */ from start
#echo $filename
dir="${fullpath%$filename}"
#echo $dir
base="${filename%.[^.]*}"                       # Strip shortest match of . plus at least one non-dot char from end
#echo $base
ext="${filename:${#base} + 1}"                  # Substring from len of base thru end
#echo $ext
if [[ -z "$base" && -n "$ext" ]]; then          # If we have an extension and no base, it's really the base
    base=".$ext"
    ext=""
fi

dest_file_left="${dir}${base}_left.m4a"
dest_file_right="${dir}${base}_right.m4a"
ffmpeg -y -i "$fullpath" -map_channel 0.0.0 -acodec alac "$dest_file_left" -map_channel 0.0.1 -acodec alac  "$dest_file_right"