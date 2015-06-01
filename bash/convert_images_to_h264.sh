#!/usr/bin/env bash

# 
#   DIY Transcoding to h264
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: convert_images_to_h264.sh <path to file> <optional: output resolution width (1920, 1280, etc.; defaults to 960)>
# 

echo "
Usage: convert_images_to_h264.sh <path to file> 
<optional: output resolution width (1920, 1280, etc.; defaults to 960)> 
<optional: framerate ; defaults to 25> 
<optional: quality (20 is great, 30 is lousy); defaults to 15> 
<optional: maximum bitrate (average) e.g: 1500 or 2000; defaults to 5000>

"

if [[ ! $1 ]]; then
	exit
fi

nuke="/Applications/Nuke9.0v5/NukeX9.0v5.app/NukeX9.0v5"


fullpath=$1

if [[ -d "$fullpath" ]]
   then
       pushd "$fullpath" >/dev/null
       pwd
       popd >/dev/null
   elif [[ -e $fullpath ]]
   then
       pushd "$(dirname "$fullpath")" >/dev/null
       fullpath="$(pwd)/$(basename "$fullpath")"
       popd >/dev/null
   else
       echo "$fullpath" does not exist! >&2
       return 127
   fi

filename="${fullpath##*/}"                      # Strip longest match of */ from start
#echo $filename
dir="${fullpath%$filename}"
folder=`basename $dir`
folder=/${folder}/
basedir="${dir%$folder}"
base="${filename%[._][0-9]*.*}"                       # Strip shortest match of . or _ plus any number of numbers a dot and any number of characters from end
#echo $base
counter_ext="${filename#$base}"                  # Substring from len of base thru end
counter_ext="${counter_ext#[._]}"
#echo $counter_ext
counter="${counter_ext%.[^._]*}"
#echo $counter
ext="${filename:${#base} + 1}"                  # Substring from len of base thru end
ext="${ext:${#counter} + 1}" 
#echo $ext
counter_sep="${filename:${#base}:1}"
#echo $counter_sep

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

if [[ $5 ]]; then
	let double=$5*2
	rate="-maxrate ${5}k -bufsize ${double}k"
else
	rate="-maxrate 5000k -bufsize 10000k"
fi


vcodec="-vcodec libx264 -preset veryslow -pix_fmt yuv420p -vf scale='$res:trunc(ow/a/2)*2' -g $fps -crf $quality $rate -vprofile high -level 4.0 -bf 0"
acodec="-c:a libfdk_aac -b:a 160k -ac 2"
sequence="${dir}${base}${counter_sep}%0${#counter}d.jpg"
#echo $sequence
output=${basedir}/${base}.mp4
#echo $output

if [[ $ext != "jpg" ]]; then
	if [[ $ext != "JPG" ]]; then
		nukeconvert="$nuke -t /Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/Nuke/plugins/convertToJPG.py $fullpath"
		$nukeconvert
		sequence="${dir}_tmp/${base}.%0${#counter}d.jpg"
	fi
fi

#cmd="ffmpeg -y -f image2 -start_number $counter -r $fps -i "$sequence" $acodec $vcodec -f mp4 $output"
cmd="ffmpeg -y -f image2 -start_number $counter -r $fps -i "$sequence" $vcodec -f mp4 $output"
# >> /Volumes/ProjectsRaid/imagesequence-to-h264/convert.log
#echo $cmd
$cmd
if [ "$?" == "0" ]; then
	echo "Encode Successful!"
	tmpdir=${dir}_tmp
	rm -R -f $tmpdir
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