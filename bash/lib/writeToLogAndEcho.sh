#!/usr/bin/env bash
set -euo pipefail

# Log and Echo Functions
# Utility functions for logging and console output
# Based on: http://stackoverflow.com/a/18462920
# Enhanced by Alexander Kucera / babylondreams.de

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# Help function
show_help() {
    cat << EOF
Usage: writeToLogAndEcho.sh

Log and Echo Functions utility

Options:
    -h, --help     Show this help message and exit

Functions provided:
    log <message>       Write message to log file only
    message <message>   Write message to both console and log file

Configuration:
    - Set LOG_FILE environment variable for custom log location
    - Default log file: ~/script.log if LOG_FILE not set

Examples:
    source writeToLogAndEcho.sh
    log "This goes to log file only"
    message "This goes to both console and log"

Usage as standalone script:
    ./writeToLogAndEcho.sh         # Shows example usage

Based on: http://stackoverflow.com/a/18462920
Enhanced by Alexander Kucera / babylondreams.de
EOF
}

# Parse command line arguments (only if run directly)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    case "${1:-}" in
        -h|--help)
            show_help
            exit 0
            ;;
    esac
fi

# Check if LOG_FILE is set
if [[ -z "${LOG_FILE:-}" ]]; then
    echo "Warning: LOG_FILE not set. Using default log file." >&2
    LOG_FILE="${HOME}/script.log"
fi

# Validate log file directory
log_dir="$(dirname "$LOG_FILE")"
if ! validate_directory "$log_dir" "log directory"; then
    echo "Error: Invalid log directory: $log_dir" >&2
    exit 1
fi

# Function to write to log file only
log() {
    local message="$1"
    log_message "$message" "$(basename "$LOG_FILE")"
}

# Function to write to both console and log file
message() {
    local message="$1"
    echo "$message"
    log_message "$message" "$(basename "$LOG_FILE")"
}

# Example usage (only if script is run directly, not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Example usage:"
    echo "Echoed to console only"
    log "Written to log file only"
    message "To console and log"
fi