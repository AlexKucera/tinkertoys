#!/bin/bash
set -euo pipefail

# Image Extension Fixer
# Fixes file extensions based on actual file content
# Original by "Ten Elite Brains" <atqueensu@gmail.com>
# Enhanced by Alexander Kucera / babylondreams.de

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

# Global variables
flag_option_found=0
v_parameter=""
s_parameter=""
r_parameter=""
checkCLData()
{
    if ((!flag_option_found)); then
        echo -e "Error! \tNo options used, Please use -h for help."
    fi
}

#-v outputs list of corrected files in ~/fixImgExt_info.txt
logEntry()
{
    if [[ -n "$v_parameter" ]]; then
        log_message "$1" "fixImgExt_info.txt"
    fi
}

showDetails()
{
    if [ ! -z "$s_parameter" ]; then
        echo -e "\t\t---------------------------------------------------------------------------------------"
        echo -e "\t\t  file path:-               $1"
        echo -e "\t\t  dir:-                     $2"
        echo -e "\t\t  file name with ext:-      $3"
        echo -e "\t\t  file name:-               $4"
        echo -e "\t\t---------------------------------------------------------------------------------------"
    fi
}

#Correcting file extenions from file, ../new
correctFile()       #$1 = return; $2=file;  
{
    local fPath="$1"
    
    # Use shared validation function
    if ! validate_file "$fPath" "image file"; then
        return 1
    fi
    local fNameWExt=$(basename "$fPath")
    local fName="${fNameWExt%.*}"
    local dir=$(dirname "$fPath")
    showDetails "$fPath" "$dir" "$fNameWExt" "$fName"                   #-s Shows details of each file in terminal

    case $(file -b "$fPath") in
        JPEG\ *)                 	e=jpeg ;;
        GIF\ *)                  	e=gif ;;
        PNG\ *)                  	e=png ;; 
        TIFF\ *)                 	e=tif ;;
        PC\ bitmap*)           		e=bmp ;;
        GIMP\ XCF\ *)            	e=xcf ;;
        Adobe\ Photoshop\ *)     	e=psd ;;
        SVG\ *)     				e=svg ;;
        WebM*)	                 	e=webm ;;
        *)                      	e= ;;
    esac

    if [ ! -z "$e" ]; then                                              #if sting is not null
        #if old> file1.jpeg == new> file1.jpeg, no correction is made. 
        if [ "$fNameWExt" == "$fName.$e" ]; then           
            echo -e "Info! \tNo change needed \t$fNameWExt"
            return 1
        fi

        # Validate directory path to prevent path traversal
        if [[ "$dir" == *".."* ]] || [[ "$fName" == *".."* ]]; then
            echo -e "Error! \tInsecure path detected: $dir/$fName.$e" >&2
            return 1
        fi
        
        #Make sure new> file.ext does not owerwrite existing old>file.ext
        if [ ! -f "$dir/$fName.$e" ]; then                              #if new> file.ext doesn't exist
            mv "$fPath" "$dir/$fName.$e"
            echo -e "Corrected! \t$fPath\t$dir/$fName.$e"                          
            logEntry "$dir/$fName$uScore$count.$e"                      #-v output corrected file
        else                                                            #if new> file.ext already exist, try file_0++.ext
            local count=0
            local uScore='_'
            while [[ -f "$dir/$fName$uScore$count.$e" ]]; do
                echo "File Exist:-  $dir/$fName$uScore$count.$e"
                count=$((count + 1));
                echo "File Inc++:-  $dir/$fName$uScore$count.$e"
            done
            mv "$fPath" "$dir/$fName$uScore$count.$e"
            echo -e "Corrected! \t$fPath\t$dir/$fName$uScore$count.$e"               
            logEntry "$dir/$fName$uScore$count.$e"                      #-v output corrected file
        fi
    else
        echo -e "Warning!\t"$(file "$fPath")        
        echo -e "Warning!\tCurrently supported formats: JPEG, GIF, PNG, TIFF, BMP, GIMP XCF, PSD, SVG, WebM"
    fi 
    return 1            #return true   
}

#Correcting file extenions from file in directory
correctDir()
{
    local dPath="$1"
    
    # Use shared validation function
    if ! validate_directory "$dPath" "input directory"; then
        return 0        
    fi

    #-r, fixes files' extenion in directory recursively
    IFS=''                                                      #file ending with space doesn't work with read unless IFS is set
    if [ ! -z "$r_parameter" ]; then
        find "$dPath" -type f | while read f; do                #return list of all the files recursively in dir
            correctFile "$f"                                    #calling function with filepath as parameter
        done
    else #-d, fixed files' extension in dir non-recursively
        find "$dPath" -maxdepth 1 -type f | while read f; do    #for f in $dPath/* ; do     #for f in *; do
            correctFile "$f"                                    #calling function with filepath as parameter
        done
    fi
    return 1                                                    #return true    
}

#------------------------------------MAIN(), program's entry point----------------------------------------
#Global variables

#get options and arguments from command line
while getopts ":f:d:rsvh" opt; do
    flag_option_found=1
    case $opt in
        f)      echo "-f was triggered, Parameter: $OPTARG" >&2
                f_parameter="$OPTARG";;
        d)      echo "-d was triggered, Parameter: $OPTARG" >&2
                d_parameter="$OPTARG";;
        r)      echo "-r was triggered" >&2
                r_parameter='true';;
        s)      echo "-s was triggered" >&2
                s_parameter='true';;
        v)      echo "-v was triggered" >&2
                v_parameter='true';;
        h)      echo -e "Usage: fixImgExt [OPTION...[+PARAMETER]]\n"
                echo -e "\t-f\t[FILE]\t\tPass a single file with file path."
                echo -e "\t  \t\t\tFile is assessed and extension of the file is corrected"
                echo -e "\t-d\t[DIRECTORY]\tPass a single directory with directory path."
                echo -e "\t  \t\t\tAll the files in the directory is assessed & extension of each file is corrected"
                echo -e "\t-r\t\t\tCan be used with -d option, corrects files in directories recursively"
                echo -e "\t-s\t\t\tShows details of each file in Command Line Interface (CLI)"
                echo -e "\t-v\t\t\tLogs the list of corrected files to fixImgExt_info.txt in currently directory"
                echo -e "\t-h\t\t\tShow help option (this) and exit";;       
        \?)     echo "Invalid option: -$OPTARG" >&2;;
        :)      echo "Option -$OPTARG requires an argument." >&2
                exit 1;;
    esac
done

#Check of any option is passed on command line
checkCLData
#-v outputs list of corrected files in ~/fixImgExt_info.txt
if [ ! -z "$v_parameter" ]; then
    logEntry "--------------------------------NEW RUN--------------------------------"          #creates a file/appends in it
fi 
#-f calling function to fix file passed as parameter
if [ ! -z "$f_parameter" ]; then
    correctFile "$f_parameter"
    return_stat=$?
fi
#-d calling function to fix file passed as parameter
if [ ! -z "$d_parameter" ]; then
    correctDir "$d_parameter"
    return_stat=$?
fi
exit 