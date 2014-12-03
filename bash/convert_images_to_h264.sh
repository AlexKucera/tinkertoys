#!/usr/bin/env bash

# 
#   DIY Transcoding to h264
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: convert_images_to_h264.sh <path to file> <optional: output resolution width (1920, 1280, etc.; defaults to 960)>
# 

if [[ ! $1 ]]; then
	echo "Usage: convert_images_to_h264.sh <path to file> <optional: output resolution width (1920, 1280, etc.; defaults to 960)> <optional: framerate ; defaults to 25> <optional: quality (20 is great, 30 is lousy); defaults to 15>"
	exit
fi

fullpath=$1
filename="${fullpath##*/}"                      # Strip longest match of */ from start
dir="${fullpath%$filename}"
folder=`basename $dir`
folder=/${folder}/
basedir="${dir%$folder}"
base="${filename%.[^.]*.[^.]*}"                       # Strip shortest match of . plus at least one non-dot char from end
counter_ext="${filename:${#base} + 1}"                  # Substring from len of base thru end
counter="${counter_ext%.[^.]*}"
ext="${filename:${#base} + 1}"                  # Substring from len of base thru end
ext="${ext:${#counter} + 1}" 

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
	fps=${3}
else
	fps="25"
fi

if [[ $4 ]]; then
	quality=${4}
else
	quality="15"
fi

vcodec="-vcodec libx264 -pix_fmt yuv420p -vf scale='$res:trunc(ow/a/2)*2' -g 30 -crf $quality -vprofile high -bf 0"
acodec="-strict experimental -acodec aac -ab 160k -ac 2"
sequence="${dir}${base}.%0${#counter}d.jpg"
#echo $sequence
output=${basedir}/${base}.mp4
#echo $output
cmd="ffmpeg -y -f image2 -start_number $counter -r $fps -i "$sequence" $acodec $vcodec -f mp4 $output"
# >> /Volumes/ProjectsRaid/imagesequence-to-h264/convert.log
#echo $cmd
$cmd
if [ "$?" == "0" ]; then
	echo "Encode Successful!"
#	echo $dir
	# while true
	# 	do
	# 	  # (1) prompt user, and read command line argument
	# 	  read -p "Remove ${dir} now? " answer
	# 
	# 	  # (2) handle the input we were given
	# 	  case $answer in
	# 	   [yY]* ) 	rm -Rf $dir
	# 	           	echo "
	# Removed ${dir}"
	# 	           	break;;
	# 
	# 	   [nN]* ) 	echo "
	# Kept ${dir}"
	# 				exit;;
	# 
	# 	   * )     echo "Dude, just enter Y or N, please.";;
	# 	  esac
	# 	done

	exit 0
fi