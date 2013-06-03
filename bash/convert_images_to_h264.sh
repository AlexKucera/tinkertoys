#!/usr/bin/env bash

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

vcodec="-vcodec libx264 -pix_fmt yuv420p -vf scale='960:trunc(ow/a/2)*2' -g 30 -crf 15 -vprofile high -bf 0"
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