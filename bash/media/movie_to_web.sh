#!/usr/bin/env bash
set -euo pipefail

# 
#   DIY Transcoding to web formats (MP4 and WebM)
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#
#   Usage: movie_to_web.sh <path to file>
# 

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/media_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: movie_to_web.sh <path to file>

DIY Transcoding to web formats (MP4 and WebM)

Arguments:
    path_to_file   Path to input movie file

Options:
    -h, --help     Show this help message and exit

Features:
    - Converts to web-optimized MP4 format
    - Converts to WebM format for better web compatibility
    - Optimizes file size and quality for web delivery
    - Preserves original aspect ratio

Examples:
    movie_to_web.sh input.mov
    movie_to_web.sh ~/Movies/myvideo.avi

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

# Validate required commands
validate_command "ffmpeg" "FFmpeg"

# Parse filename components using shared function
declare -A file_parts
parse_filename "$fullpath" file_parts

# Generate output filenames
mp4_output="$(generate_output_filename "$fullpath" "web" "mp4")"
webm_output="$(generate_output_filename "$fullpath" "web" "webm")"

echo "Input: ${file_parts[fullpath]}"
echo "MP4 Output: $mp4_output"
echo "WebM Output: $webm_output"
echo "Target resolution: 720p"

# Set up codec parameters for web formats
mp4_vcodec="-vcodec libx264 -pix_fmt yuv420p -vf scale='trunc(oh/a/2)*2:720' -g 30 -crf 15 -vprofile high -bf 0"
mp4_acodec="$(setup_audio_codec "aac" "160k" "2")"

webm_vcodec="-pix_fmt yuv420p -vcodec libvpx -vf scale='trunc(oh/a/2)*2:720' -g 30 -b:v 7000k -quality realtime -cpu-used 0 -qmin 10 -qmax 42"
webm_acodec="$(setup_audio_codec "vorbis" "160k" "2")"

# Encode MP4
echo "Starting MP4 encoding for web..."
mp4_cmd="ffmpeg -i \"$fullpath\" $mp4_acodec $mp4_vcodec -f mp4 \"$mp4_output\""
echo "Executing: $mp4_cmd"

if eval "$mp4_cmd"; then
    echo "✓ MP4 encoding completed successfully!"
    
    # Show MP4 file size
    if is_macos; then
        mp4_size="$(stat -f%z "$mp4_output" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    else
        mp4_size="$(stat -c%s "$mp4_output" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    fi
    echo "MP4 file size: $mp4_size"
else
    echo "✗ Error: MP4 encoding failed" >&2
    exit 1
fi

# Encode WebM
echo "Starting WebM encoding for web..."
webm_cmd="ffmpeg -i \"$fullpath\" $webm_acodec $webm_vcodec -f webm \"$webm_output\""
echo "Executing: $webm_cmd"

if eval "$webm_cmd"; then
    echo "✓ WebM encoding completed successfully!"
    
    # Show WebM file size
    if is_macos; then
        webm_size="$(stat -f%z "$webm_output" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    else
        webm_size="$(stat -c%s "$webm_output" 2>/dev/null | awk '{print int($1/1024/1024)} " MB"' || echo "unknown")"
    fi
    echo "WebM file size: $webm_size"
    
    echo ""
    echo "✓ Web format conversion completed successfully!"
    echo "Created files:"
    echo "  MP4: $mp4_output ($mp4_size)"
    echo "  WebM: $webm_output ($webm_size)"
    
    exit 0
else
    echo "✗ Error: WebM encoding failed" >&2
    exit 1
fi