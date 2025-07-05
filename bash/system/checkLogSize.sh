#!/bin/bash
set -euo pipefail

# Log Size Checker
# Checks if a log file exceeds a specified size limit
# Created by Alexander Kucera / babylondreams.de

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/system_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: checkLogSize.sh [log_file] [max_size_kb]

Checks if a log file exceeds a specified size limit

Arguments:
    log_file       Path to log file to check (default: ~/Documents/scripts/mount_unmount_bootable.log)
    max_size_kb    Maximum size in KB (default: 128)

Options:
    -h, --help     Show this help message and exit

Features:
    - Validates log file exists and is readable
    - Compares file size against specified limit
    - Returns appropriate exit codes for scripting
    - Uses shared functions for consistent validation

Exit Codes:
    0: File size is within limits
    1: File size exceeds limit or error occurred

Examples:
    checkLogSize.sh                                    # Use defaults
    checkLogSize.sh /var/log/my.log 256               # Check custom log with 256KB limit
    checkLogSize.sh ~/logs/debug.log 1024             # Check with 1MB limit

Created by Alexander Kucera / babylondreams.de
EOF
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
esac

# Configuration
DEFAULT_LOG="/Users/alex/Documents/scripts/mount_unmount_bootable.log"
DEFAULT_MAX_SIZE_KB=128

# Get parameters
LOG_FILE="${1:-$DEFAULT_LOG}"
MAX_SIZE_KB="${2:-$DEFAULT_MAX_SIZE_KB}"

# Input validation
if [[ -z "$LOG_FILE" ]]; then
    echo "Error: No log file specified" >&2
    echo "Use -h or --help for usage information" >&2
    exit 1
fi

# Check log file using shared function
if check_log_size "$LOG_FILE" "$MAX_SIZE_KB"; then
    echo "✓ Log file is within size limits"
    exit 0
else
    echo "⚠ Log file exceeds size limits"
    exit 1
fi