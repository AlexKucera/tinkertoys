#!/usr/bin/env bash
# Media processing utility functions
# Created by Alexander Kucera / babylondreams.de

# Source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# Function to validate video/image file
validate_media_file() {
    local file="$1"
    local supported_exts=("jpg" "jpeg" "png" "tiff" "tif" "tga" "bmp" "exr" "mov" "mp4" "avi" "mkv" "webm")
    
    if ! validate_file "$file" "media file"; then
        return 1
    fi
    
    # Extract extension
    local ext="${file##*.}"
    ext="${ext,,}" # Convert to lowercase
    
    # Check if extension is supported
    local supported=false
    for supported_ext in "${supported_exts[@]}"; do
        if [[ "$ext" == "$supported_ext" ]]; then
            supported=true
            break
        fi
    done
    
    if [[ "$supported" == false ]]; then
        echo "Warning: File extension '$ext' may not be supported" >&2
    fi
    
    return 0
}

# Function to parse sequence filename
parse_sequence_filename() {
    local fullpath="$1"
    local -n seq_result="$2"
    
    # Get basic filename components
    parse_filename "$fullpath" seq_result
    
    # Parse sequence-specific components
    local filename="${seq_result[filename]}"
    local base_temp="${filename%[._][0-9]*.*}"
    
    if [[ "$base_temp" != "$filename" ]]; then
        # This appears to be a sequence file
        seq_result[sequence_base]="$base_temp"
        local counter_ext="${filename#$base_temp}"
        seq_result[counter_separator]="${counter_ext:0:1}"
        counter_ext="${counter_ext:1}"
        seq_result[counter]="${counter_ext%.*}"
        seq_result[is_sequence]="true"
        
        # Build sequence pattern
        local counter_length="${#seq_result[counter]}"
        seq_result[sequence_pattern]="${seq_result[dir]}${seq_result[sequence_base]}${seq_result[counter_separator]}%0${counter_length}d.${seq_result[ext]}"
    else
        seq_result[is_sequence]="false"
        seq_result[sequence_base]="${seq_result[base]}"
        seq_result[counter_separator]=""
        seq_result[counter]=""
        seq_result[sequence_pattern]=""
    fi
}

# Function to setup ffmpeg video codec parameters
setup_h264_codec() {
    local resolution="$1"
    local fps="$2"
    local quality="$3"
    local max_bitrate="${4:-5000}"
    
    local double_bitrate=$((max_bitrate * 2))
    
    echo "-vcodec libx264 -preset veryslow -pix_fmt yuv420p -vf scale='${resolution}:trunc(ow/a/2)*2' -g ${fps} -crf ${quality} -maxrate ${max_bitrate}k -bufsize ${double_bitrate}k -vprofile high -level 4.0 -bf 0"
}

# Function to setup ffmpeg ProRes codec parameters
setup_prores_codec() {
    local resolution="$1"
    local fps="$2"
    local quality="$3"
    local format="${4:-4}"
    
    echo "-c:v prores_ks -profile:v ${format} -pix_fmt yuv444p10le -vendor ap10 -vf scale='${resolution}:trunc(ow/a/2)*2' -g ${fps} -qscale:v ${quality}"
}

# Function to setup ffmpeg audio codec parameters
setup_audio_codec() {
    local codec_type="${1:-aac}"
    local bitrate="${2:-160k}"
    local channels="${3:-2}"
    
    case "$codec_type" in
        "aac")
            echo "-c:a libfdk_aac -b:a ${bitrate} -ac ${channels}"
            ;;
        "alac")
            echo "-acodec alac"
            ;;
        "vorbis")
            echo "-acodec libvorbis -aq 60 -ac ${channels}"
            ;;
        *)
            echo "Error: Unsupported audio codec: $codec_type" >&2
            return 1
            ;;
    esac
}

# Function to validate and setup Nuke environment
setup_nuke_environment() {
    local -n nuke_result="$1"
    
    if [[ -z "${NUKEPATH:-}" ]]; then
        nuke_result[available]=false
        nuke_result[path]=""
        nuke_result[error]="NUKEPATH environment variable not set"
        return 1
    fi
    
    if [[ ! -x "$NUKEPATH" ]]; then
        nuke_result[available]=false
        nuke_result[path]="$NUKEPATH"
        nuke_result[error]="Nuke executable not found or not executable: $NUKEPATH"
        return 1
    fi
    
    nuke_result[available]=true
    nuke_result[path]="$NUKEPATH"
    nuke_result[error]=""
    return 0
}

# Function to convert images to JPG using Nuke
convert_to_jpg_with_nuke() {
    local input_file="$1"
    local nuke_path="$2"
    local output_dir="$3"
    
    if [[ ! -x "$nuke_path" ]]; then
        echo "Error: Nuke executable not found: $nuke_path" >&2
        return 1
    fi
    
    if [[ ! -f "$input_file" ]]; then
        echo "Error: Input file not found: $input_file" >&2
        return 1
    fi
    
    echo "Converting to JPG using Nuke..."
    "$nuke_path" -t /Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/Nuke/plugins/bd_convertToJPG.py "$input_file"
    
    if [[ $? -eq 0 ]]; then
        echo "Nuke conversion completed successfully"
        return 0
    else
        echo "Error: Nuke conversion failed" >&2
        return 1
    fi
}

# Function to validate media processing parameters
validate_media_params() {
    local resolution="$1"
    local fps="$2"
    local quality="$3"
    
    # Validate resolution
    if [[ ! "$resolution" =~ ^[0-9]+$ ]] || [[ "$resolution" -lt 240 ]] || [[ "$resolution" -gt 7680 ]]; then
        echo "Error: Invalid resolution '$resolution'. Must be between 240 and 7680." >&2
        return 1
    fi
    
    # Validate FPS
    if [[ ! "$fps" =~ ^[0-9]+(\.[0-9]+)?$ ]] || (( $(echo "$fps < 1" | bc -l) )) || (( $(echo "$fps > 120" | bc -l) )); then
        echo "Error: Invalid frame rate '$fps'. Must be between 1 and 120." >&2
        return 1
    fi
    
    # Validate quality (CRF values)
    if [[ ! "$quality" =~ ^[0-9]+$ ]] || [[ "$quality" -lt 0 ]] || [[ "$quality" -gt 51 ]]; then
        echo "Error: Invalid quality '$quality'. Must be between 0 and 51." >&2
        return 1
    fi
    
    return 0
}

# Function to estimate encoding time
estimate_encoding_time() {
    local input_file="$1"
    local complexity="${2:-medium}" # low, medium, high
    
    # This is a very rough estimation
    local file_size_mb
    if is_macos; then
        file_size_mb=$(stat -f%z "$input_file" 2>/dev/null | awk '{print int($1/1024/1024)}')
    else
        file_size_mb=$(stat -c%s "$input_file" 2>/dev/null | awk '{print int($1/1024/1024)}')
    fi
    
    local multiplier
    case "$complexity" in
        "low") multiplier=0.1 ;;
        "medium") multiplier=0.5 ;;
        "high") multiplier=2.0 ;;
        *) multiplier=0.5 ;;
    esac
    
    local estimated_seconds=$(echo "$file_size_mb * $multiplier" | bc -l 2>/dev/null || echo "60")
    printf "Estimated encoding time: %.0f seconds\n" "$estimated_seconds"
}

# Function to generate output filename
generate_output_filename() {
    local input_file="$1"
    local suffix="$2"
    local extension="$3"
    
    declare -A file_parts
    parse_filename "$input_file" file_parts
    
    echo "${file_parts[dir]}${file_parts[base]}_${suffix}.${extension}"
}