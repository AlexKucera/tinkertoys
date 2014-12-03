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
	echo "Usage: convert_shotgun.sh <path to file> <optional: output resolution height (720, 1080, etc.; defaults to 720)>"
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
	res="720"
fi

vcodec="-vcodec libx264 -pix_fmt yuv420p -vf scale='trunc(oh*a/2)*2:$res' -g 30 -crf 15 -vprofile high -bf 0"
acodec="-strict experimental -acodec aac -ab 160k -ac 2"
sequence="${dir}${base}.%0${#counter}d.jpg"
#echo $sequence
output=${basedir}/${base}.mp4
#echo $output
cmd="ffmpeg -f image2 -start_number $counter -i "$sequence" $acodec $vcodec -f mp4 $output"
# >> /Volumes/ProjectsRaid/imagesequence-to-h264/convert.log
#echo $cmd
$cmd
if [ "$?" == "0" ]; then
	echo "MP4 Encode Successful!"
	
	
	output=${basedir}/${base}.webm
	webm_vcodec="-pix_fmt yuv420p -vcodec libvpx -vf scale='trunc(oh/a/2)*2:$res' -g 30 -b:v 7000k -vpre 720p -quality realtime -cpu-used 0 -qmin 10 -qmax 42"
	webm_acodec="-acodec libvorbis -aq 60 -ac 2"
	cmd="ffmpeg -f image2 -start_number $counter -i "$sequence" $webm_acodec $webm_vcodec -f webm $output"
	#echo $cmd
	$cmd
	if [ "$?" == "0" ]; then
		echo "WebM Encode Successful!"
		exit 0
	fi
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