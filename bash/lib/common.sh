#!/usr/bin/env bash
# Common utility functions for bash scripts
# Created by Alexander Kucera / babylondreams.de

# Function to show standardized help output
show_help() {
    local script_name="$1"
    local description="$2"
    local usage="$3"
    local options="$4"
    local examples="$5"
    
    echo "${script_name} - ${description}"
    echo ""
    echo "USAGE:"
    echo "  ${usage}"
    echo ""
    if [[ -n "$options" ]]; then
        echo "OPTIONS:"
        echo "$options"
        echo ""
    fi
    if [[ -n "$examples" ]]; then
        echo "EXAMPLES:"
        echo "$examples"
        echo ""
    fi
    echo "AUTHOR:"
    echo "  Alexander Kucera / babylondreams.de"
}

# Function to validate file exists
validate_file() {
    local file="$1"
    local file_description="${2:-file}"
    
    if [[ ! -f "$file" ]]; then
        echo "Error: ${file_description} '$file' does not exist" >&2
        return 1
    fi
    return 0
}

# Function to validate directory exists
validate_directory() {
    local dir="$1"
    local dir_description="${2:-directory}"
    
    if [[ ! -d "$dir" ]]; then
        echo "Error: ${dir_description} '$dir' does not exist" >&2
        return 1
    fi
    return 0
}

# Function to validate command exists
validate_command() {
    local cmd="$1"
    local cmd_description="${2:-$1}"
    
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Error: ${cmd_description} command not found. Please install ${cmd}." >&2
        return 1
    fi
    return 0
}

# Function to safely remove directory
safe_remove_directory() {
    local dir="$1"
    
    # Validate path to prevent accidental deletion
    if [[ -z "$dir" ]] || [[ "$dir" == "/" ]] || [[ "$dir" == "/Users" ]] || [[ "$dir" == "/usr" ]]; then
        echo "Error: Refusing to remove critical directory: '$dir'" >&2
        return 1
    fi
    
    # Check for path traversal
    if [[ "$dir" == *".."* ]]; then
        echo "Error: Path traversal detected in directory path: '$dir'" >&2
        return 1
    fi
    
    if [[ -d "$dir" ]]; then
        rm -rf "$dir"
        echo "Removed directory: $dir"
    fi
    return 0
}

# Function to get script directory
get_script_dir() {
    echo "$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
}

# Function to parse filename components
parse_filename() {
    local fullpath="$1"
    local -n result_ref="$2"
    
    # Initialize result array
    result_ref[fullpath]="$fullpath"
    result_ref[filename]="${fullpath##*/}"
    result_ref[dir]="${fullpath%${result_ref[filename]}}"
    result_ref[base]="${result_ref[filename]%.[^.]*}"
    result_ref[ext]="${result_ref[filename]:${#result_ref[base]} + 1}"
    
    # Handle edge case where filename starts with dot
    if [[ -z "${result_ref[base]}" && -n "${result_ref[ext]}" ]]; then
        result_ref[base]=".${result_ref[ext]}"
        result_ref[ext]=""
    fi
}

# Function to calculate duration from start and end timestamps
calculate_duration() {
    local start="$1"
    local end="$2"
    
    local secs=$((end - start))
    printf '%dh:%02dm:%02ds\n' $((secs/3600)) $((secs%3600/60)) $((secs%60))
}

# Function to get timestamp in standard format
get_timestamp() {
    local format="${1:-"+%A, %d.%m.%Y %T"}"
    local seconds="${2:-$(date +%s)}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS (BSD date)
        date -j -f "%s" "$seconds" "$format"
    else
        # Linux (GNU date)
        date -d "@$seconds" "$format"
    fi
}

# Function to detect platform
detect_platform() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

# Function to log message with timestamp
log_message() {
    local message="$1"
    local log_file="${2:-}"
    local timestamp="$(date '+%Y-%m-%d %H:%M:%S')"
    
    if [[ -n "$log_file" ]]; then
        echo "[$timestamp] $message" | tee -a "$log_file"
    else
        echo "[$timestamp] $message"
    fi
}

# Function to check if running on macOS
is_macos() {
    [[ "$OSTYPE" == "darwin"* ]]
}

# Function to check if running on Linux
is_linux() {
    [[ "$OSTYPE" == "linux-gnu"* ]]
}