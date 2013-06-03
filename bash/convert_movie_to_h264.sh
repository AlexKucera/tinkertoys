#!/usr/bin/env bash

# 
#   DIY Transcoding to h264
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
# 

fullpath=$1

#echo $fullpath
filename="${fullpath##*/}"                      # Strip longest match of */ from start
#echo $filename
if [[ $2 ]]; then
	dir=${2}/
else
	dir="${fullpath%$filename}"
fi
#echo $dir
base="${filename%.[^.]*}"                       # Strip shortest match of . plus at least one non-dot char from end
#echo $base
ext="${filename:${#base} + 1}"                  # Substring from len of base thru end
#echo $ext
if [[ -z "$base" && -n "$ext" ]]; then          # If we have an extension and no base, it's really the base
    base=".$ext"
    ext=""
fi

dest_file_mp4="${dir}${base}_h264.mp4"
mp4_vcodec="-vcodec libx264 -pix_fmt yuv420p -vf scale='trunc(oh/a/2)*2:720' -g 30 -crf 15 -vprofile high -bf 0"
mp4_acodec="-strict experimental -acodec aac -ab 160k -ac 2"
ffmpeg -i "$fullpath" $mp4_acodec $mp4_vcodec -f mp4 "$dest_file_mp4"