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
<optional: output resolution width (1920, 1280, etc.; defaults to 1920)> 
<optional: framerate of the input file ; defaults to same as file> 
<optional: quality (5 is great, 32 is lousy); defaults to 11>
<optional: format 0-4 (‘proxy’,‘lt’,‘standard’,‘hq’,‘4444’); defaults to 4 (ProRes 4444)>
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
	res="1920"
fi

if [[ $3 ]]; then
	fps=${3}
	ifps="-r ${3}"
else
	fps="25"
fi

if [[ $4 ]]; then
	quality=${4}
else
	quality="11"
fi

if [[ $5 ]]; then
	format=${5}
else
	format="4"
fi

dest_file_mp4="${dir}${base}_prores.mov"
mp4_vcodec="-c:v prores_ks -profile:v $format -pix_fmt yuv444p10le -vendor ap10 -vf scale='$res:trunc(ow/a/2)*2' -g $fps -qscale:v $quality"
mp4_acodec="-c:a libfdk_aac -b:a 160k -ac 2"
echo $mp4_vcodec
echo $mp4_acodec
echo $ifps
ffmpeg -y $ifps -i "$fullpath" $mp4_acodec $mp4_vcodec -f mov "$dest_file_mp4"