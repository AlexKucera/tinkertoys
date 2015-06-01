#!/usr/bin/env bash

# 
#   DIY Transcoding to h264
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: convert_movie_to_h264.sh <path to file> <optional: output resolution (720, 1080, etc.)>
# 

echo "
Usage: convert_images_to_h264.sh <path to file> 
<optional: output resolution width (1920, 1280, etc.; defaults to 960)> 
<optional: quality (20 is great, 30 is lousy); defaults to 15> 
<optional: maximum bitrate (average) e.g: 1500 or 2000; defaults to 5000>

"

if [[ ! $1 ]]; then
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
	res="960"
fi

if [[ $3 ]]; then
	quality=${3}
else
	quality="15"
fi

if [[ $4 ]]; then
	let double=$4*2
	rate="-maxrate ${4}k -bufsize ${double}k"
else
	rate="-maxrate 5000k -bufsize 10000k"
fi

dest_file_mp4="${dir}${base}_h264.mp4"
mp4_vcodec="-vcodec libx264 -preset veryslow -pix_fmt yuv420p -vf scale='$res:trunc(ow/a/2)*2' -g $fps -crf $quality $rate -vprofile high -level 4.0 -bf 0"
mp4_acodec="-c:a libfdk_aac -b:a 160k -cutoff 20000 -ac 2"
echo $mp4_vcodec
echo $mp4_acodec
ffmpeg -i "$fullpath" $mp4_acodec $mp4_vcodec -f mp4 "$dest_file_mp4"