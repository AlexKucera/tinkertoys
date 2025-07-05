#!/usr/bin/env bash
set -euo pipefail

# 
#   DIY Movie Transcoding to ProRes
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: convert_movie_to_prores.sh <path to file> [options]
# 

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/media_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: convert_movie_to_prores.sh <path to file> [resolution] [framerate] [quality] [format]

DIY Movie Transcoding to ProRes

Arguments:
    path_to_file   Path to input movie file
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
    convert_movie_to_prores.sh input.mov
    convert_movie_to_prores.sh input.mov 1920x1080 25 20 3
    convert_movie_to_prores.sh input.avi 1280x720 30 18 2

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

# Parse filename components using shared function
declare -A file_parts
parse_filename "$fullpath" file_parts

# Generate output filename using shared function
output_file="$(generate_output_filename "$fullpath" "prores" "mov")"

echo "Input: ${file_parts[fullpath]}"
echo "Output: $output_file"
echo "Resolution: ${resolution}p"
echo "Frame rate: ${fps} fps"
echo "Quality: $quality"
echo "ProRes format: $format"

# Set up codec parameters using shared functions
video_codec="$(setup_prores_codec "$resolution" "$fps" "$quality" "$format")"
audio_codec="$(setup_audio_codec "aac" "160k" "2")"

# Start encoding
echo "Starting ProRes movie encoding..."

# Build ffmpeg command with frame rate option if specified
fps_option=""
if [[ "$fps" != "25" ]]; then
    fps_option="-r $fps"
fi

ffmpeg_cmd="ffmpeg -y $fps_option -i \"$fullpath\" $audio_codec $video_codec -f mov \"$output_file\""
echo "Executing: $ffmpeg_cmd"

# Execute encoding
if eval "$ffmpeg_cmd"; then
    echo "✓ ProRes movie encoding completed successfully!"
    echo "Output file: $output_file"
    
    # Show file size
    if is_macos; then
        file_size="$(stat -f%z "$output_file" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    else
        file_size="$(stat -c%s "$output_file" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    fi
    echo "File size: $file_size"
    
    exit 0
else
    echo "✗ Error: ProRes movie encoding failed" >&2
    exit 1
fi