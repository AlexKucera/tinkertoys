#!/usr/bin/env bash
set -euo pipefail

# 
#   DIY Transcoding to ProRes
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: convert_images_to_prores.sh <path to file> [options]
# 

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/media_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: convert_images_to_prores.sh <path to file> [resolution] [framerate] [quality] [format]

DIY Transcoding to ProRes from image sequences

Arguments:
    path_to_file   Path to input image sequence or video file
    resolution     Optional resolution (default: 1920x1080)
    framerate      Optional frame rate (default: 25)
    quality        Optional quality setting (default: 20)
    format         Optional ProRes format (default: 4)

Options:
    -h, --help     Show this help message and exit

ProRes Formats:
    0: Proxy
    1: LT
    2: Standard
    3: HQ
    4: 4444 (default)

Examples:
    convert_images_to_prores.sh sequence.%04d.jpg
    convert_images_to_prores.sh sequence.%04d.jpg 1920x1080 25 20 3
    convert_images_to_prores.sh input.mov 1280x720 30 18 2

Created by Alexander Kucera / babylondreams.de
EOF
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    "")
        echo "Error: No input file specified" >&2
        echo "Use -h or --help for usage information" >&2
        exit 1
        ;;
esac

# Input validation
if [[ -z "${1:-}" ]]; then
    echo "Error: No input file specified" >&2
    echo "Use -h or --help for usage information" >&2
    exit 1
fi

fullpath="$1"

# Validate input file using shared function
if ! validate_media_file "$fullpath"; then
    exit 1
fi

# Set up parameters with defaults
resolution="${2:-1920}"
fps="${3:-25}"
quality="${4:-11}"
format="${5:-4}"

# Validate parameters using shared function
if ! validate_media_params "$resolution" "$fps" "$quality"; then
    exit 1
fi

# Validate ProRes format
if [[ ! "$format" =~ ^[0-4]$ ]]; then
    echo "Error: Invalid ProRes format '$format'. Must be 0-4." >&2
    exit 1
fi

# Validate required commands
validate_command "ffmpeg" "FFmpeg"

# Set up Nuke environment
declare -A nuke_env
setup_nuke_environment nuke_env

# Parse filename components using shared function
declare -A file_parts
parse_sequence_filename "$fullpath" file_parts

# Generate output filename using shared function
output_file="$(generate_output_filename "$fullpath" "prores" "mov")"

echo "Input: ${file_parts[fullpath]}"
echo "Output: $output_file"
echo "Resolution: ${resolution}p"
echo "Frame rate: ${fps} fps"
echo "Quality: $quality"
echo "ProRes format: $format"

# Handle non-JPG formats with Nuke conversion if available
sequence="${file_parts[sequence_pattern]:-$fullpath}"
if [[ "${file_parts[ext]}" != "jpg" ]] && [[ "${file_parts[ext]}" != "JPG" ]] && [[ "${file_parts[ext]}" != "tga" ]] && [[ "${file_parts[ext]}" != "TGA" ]]; then
    if [[ "${nuke_env[available]}" == "true" ]]; then
        echo "Converting to JPG format using Nuke..."
        if convert_to_jpg_with_nuke "$fullpath" "${nuke_env[path]}" "${file_parts[dir]}_tmp"; then
            sequence="${file_parts[dir]}_tmp/${file_parts[sequence_base]}.%0${#file_parts[counter]}d.${file_parts[ext]}"
        else
            echo "Warning: Nuke conversion failed, using original sequence" >&2
        fi
    else
        echo "Warning: ${nuke_env[error]}, using original sequence" >&2
    fi
fi

# Set up codec parameters using shared functions
video_codec="$(setup_prores_codec "$resolution" "$fps" "$quality" "$format")"
audio_codec="$(setup_audio_codec "aac" "160k" "2")"

# Start encoding
echo "Starting ProRes encoding..."

# Build ffmpeg command
if [[ "${file_parts[is_sequence]}" == "true" ]]; then
    # For sequences, use the counter from the filename
    start_number="${file_parts[counter]}"
    ffmpeg_cmd="ffmpeg -y -f image2 -start_number $start_number -r $fps -i \"$sequence\" $video_codec -f mov \"$output_file\""
else
    # For single files
    ffmpeg_cmd="ffmpeg -y -i \"$fullpath\" $video_codec -f mov \"$output_file\""
fi

echo "Executing: $ffmpeg_cmd"

# Execute encoding
if eval "$ffmpeg_cmd"; then
    echo "✓ ProRes encoding completed successfully!"
    echo "Output file: $output_file"
    
    # Clean up temporary directory if it exists
    tmpdir="${file_parts[dir]}_tmp"
    if [[ -d "$tmpdir" ]]; then
        safe_remove_directory "$tmpdir"
    fi
    
    # Show file size using shared function
    if is_macos; then
        file_size="$(stat -f%z "$output_file" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    else
        file_size="$(stat -c%s "$output_file" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    fi
    echo "File size: $file_size"
    
    exit 0
else
    echo "✗ Error: ProRes encoding failed" >&2
    exit 1
fi