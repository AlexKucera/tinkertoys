#!/usr/bin/env bash
set -euo pipefail

# 
#   DIY Audio splitting - stereo to two mono streams
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: split_stereo_to_mono.sh <path to file>
# 

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/media_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: split_stereo_to_mono.sh <path to file>

DIY Audio splitting - stereo to two mono streams

Arguments:
    path_to_file   Path to input stereo audio file

Options:
    -h, --help     Show this help message and exit

Features:
    - Splits stereo audio into two separate mono files
    - Outputs in Apple Lossless format for quality preservation
    - Creates left and right channel files
    - Preserves original audio quality

Examples:
    split_stereo_to_mono.sh stereo_audio.wav
    split_stereo_to_mono.sh ~/Music/mysong.aiff

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
if ! validate_file "$fullpath" "audio file"; then
    exit 1
fi

# Validate required commands
validate_command "ffmpeg" "FFmpeg"

# Parse filename components using shared function
declare -A file_parts
parse_filename "$fullpath" file_parts

# Generate output filenames
left_output="${file_parts[dir]}${file_parts[base]}_left.m4a"
right_output="${file_parts[dir]}${file_parts[base]}_right.m4a"

echo "Input: ${file_parts[fullpath]}"
echo "Left channel output: $left_output"
echo "Right channel output: $right_output"
echo "Format: Apple Lossless (ALAC)"

# Set up codec parameters
alac_codec="$(setup_audio_codec "alac")"

echo "Starting stereo to mono conversion..."

# Execute ffmpeg with error handling
ffmpeg_cmd="ffmpeg -y -i \"$fullpath\" -map_channel 0.0.0 $alac_codec \"$left_output\" -map_channel 0.0.1 $alac_codec \"$right_output\""
echo "Executing: $ffmpeg_cmd"

if eval "$ffmpeg_cmd"; then
    echo "✓ Stereo to mono conversion completed successfully!"
    
    # Show file sizes
    if is_macos; then
        left_size="$(stat -f%z "$left_output" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
        right_size="$(stat -f%z "$right_output" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    else
        left_size="$(stat -c%s "$left_output" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
        right_size="$(stat -c%s "$right_output" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    fi
    
    echo ""
    echo "Created files:"
    echo "  Left channel: $left_output ($left_size)"
    echo "  Right channel: $right_output ($right_size)"
    
    exit 0
else
    echo "✗ Error: Stereo to mono conversion failed" >&2
    exit 1
fi