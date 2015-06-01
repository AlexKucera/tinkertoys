#!/usr/bin/env bash

# 
#   DIY Transcoding to web formats
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
# 

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

dest_file_mp4="${dir}${base}_web.mp4"
dest_file_webm="${dir}${base}_web.webm"
mp4_vcodec="-vcodec libx264 -pix_fmt yuv420p -vf scale='trunc(oh/a/2)*2:720' -g 30 -crf 15 -vprofile high -bf 0"
mp4_acodec="-strict experimental -acodec aac -ab 160k -ac 2"
ffmpeg -i "$fullpath" $mp4_acodec $mp4_vcodec -f mp4 "$dest_file_mp4"
webm_vcodec=" -pix_fmt yuv420p -vcodec libvpx -vf scale='trunc(oh/a/2)*2:720' -g 30 -b:v 7000k -vpre 720p -quality realtime -cpu-used 0 -qmin 10 -qmax 42"
webm_acodec="-acodec libvorbis -aq 60 -ac 2"
ffmpeg -i "$fullpath" $webm_acodec $webm_vcodec -f webm "$dest_file_webm"