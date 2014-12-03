#!/usr/bin/env bash

# 
#   DIY Transcoding to h264
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: convert_movie_to_h264.sh <path to file> <optional: output resolution (720, 1080, etc.)>
# 

if [[ ! $1 ]]; then
	echo "Usage: convert_movie_to_h264.sh <path to file> <optional: output resolution height (720, 1080, etc.); defaults to 720)> <optional: quality (20 is great, 30 is lousy); defaults to 15>"
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

if [[ $2 ]]; then
	res=${2}
else
	res="720"
fi

if [[ $3 ]]; then
	quality=${3}
else
	quality="15"
fi

dest_file_mp4="${dir}${base}_h264.mp4"
mp4_vcodec="-vcodec libx264 -pix_fmt yuv420p -vf scale='trunc(oh*a/2)*2:$res' -g 30 -crf $quality -vprofile high -bf 0"
mp4_acodec="-strict experimental -acodec aac -ab 160k -ac 2"
ffmpeg -i "$fullpath" $mp4_acodec $mp4_vcodec -f mp4 "$dest_file_mp4"