#!/usr/bin/env bash
set -euo pipefail

# 
#   DIY Movie Transcoding to H.264
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: convert_movie_to_h264.sh <path to file> [options]
# 

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/media_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: convert_movie_to_h264.sh <path to file> [resolution] [quality] [max_bitrate]

DIY Movie Transcoding to H.264

Arguments:
    path_to_file   Path to input movie file
    resolution     Optional resolution (default: 1920x1080)
    quality        Optional quality setting (default: 20)
    max_bitrate    Optional maximum bitrate in kbps (default: 10000)

Options:
    -h, --help     Show this help message and exit

Bitrate Guidelines:
    SD: 2,000 – 5,000
    720p: 5,000 – 10,000
    1080p: 10,000 – 20,000
    2K: 20,000 – 30,000
    4K: 30,000 – 60,000

Examples:
    convert_movie_to_h264.sh input.mov
    convert_movie_to_h264.sh input.mov 1920x1080 20 15000
    convert_movie_to_h264.sh input.avi 1280x720 18 8000

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
resolution="${2:-960}"
quality="${3:-15}"
max_bitrate="${4:-5000}"

# Validate parameters using shared function
if ! validate_media_params "$resolution" "25" "$quality"; then
    exit 1
fi

# Validate required commands
validate_command "ffmpeg" "FFmpeg"

# Parse filename components using shared function
declare -A file_parts
parse_filename "$fullpath" file_parts

# Generate output filename using shared function
output_file="$(generate_output_filename "$fullpath" "h264" "mp4")"

echo "Input: ${file_parts[fullpath]}"
echo "Output: $output_file"
echo "Resolution: ${resolution}p"
echo "Quality: $quality"
echo "Max bitrate: ${max_bitrate}k"

# Set up codec parameters using shared functions
video_codec="$(setup_h264_codec "$resolution" "25" "$quality" "$max_bitrate")"
audio_codec="$(setup_audio_codec "aac" "160k" "2")"

# Start encoding
echo "Starting H.264 movie encoding..."

# Execute ffmpeg with error handling
ffmpeg_cmd="ffmpeg -i \"$fullpath\" $audio_codec $video_codec -f mp4 \"$output_file\""
echo "Executing: $ffmpeg_cmd"

if eval "$ffmpeg_cmd"; then
    echo "✓ H.264 movie encoding completed successfully!"
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
    echo "✗ Error: H.264 movie encoding failed" >&2
    exit 1
fi