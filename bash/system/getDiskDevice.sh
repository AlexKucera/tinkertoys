#!/bin/bash
set -euo pipefail

# Get Disk Device by Label
# Finds disk device identifier by searching for a label
# Created by Alexander Kucera / babylondreams.de

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/system_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: getDiskDevice.sh [label]

Finds disk device identifier by searching for a label

Arguments:
    label          Disk label to search for (default: BackupSystem)

Options:
    -h, --help     Show this help message and exit

Features:
    - Searches for mounted disks by volume label
    - Returns disk device identifier (e.g., /dev/disk2s1)
    - Works on macOS using diskutil
    - Validates disk exists before returning

Exit Codes:
    0: Disk found successfully
    1: Disk not found or error occurred

Examples:
    getDiskDevice.sh                        # Search for default "BackupSystem"
    getDiskDevice.sh "My External Drive"    # Search for custom label
    getDiskDevice.sh TimeMachine           # Search for Time Machine disk

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
DEFAULT_LABEL="BackupSystem"
SEARCH_LABEL="${1:-$DEFAULT_LABEL}"

# Input validation
if [[ -z "$SEARCH_LABEL" ]]; then
    echo "Error: No label specified" >&2
    echo "Use -h or --help for usage information" >&2
    exit 1
fi

echo "Searching for disk with label: $SEARCH_LABEL"

# Use shared function to find disk by label
if is_macos; then
    disk_device="$(find_disk_by_label "$SEARCH_LABEL")"
    
    if [[ -n "$disk_device" ]]; then
        echo "Found disk device: $disk_device"
        echo "$disk_device"
        exit 0
    else
        echo "No disk found with label: $SEARCH_LABEL" >&2
        exit 1
    fi
else
    echo "Error: This script currently only supports macOS" >&2
    exit 1
fi