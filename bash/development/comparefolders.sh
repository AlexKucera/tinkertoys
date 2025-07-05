#!/usr/bin/env bash
set -euo pipefail

# 
#   Compare two folders for any file differences
# 
#   Created by Alexander Kucera on 2012-11-30.
#   Copyright (c) 2012 BabylonDreams. All rights reserved.
#

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

# Help function
show_help() {
    cat << EOF
Usage: comparefolders.sh <path1> <path2>

Compares two directories for file differences

Arguments:
    path1          Path to first directory to compare
    path2          Path to second directory to compare

Options:
    -h, --help     Show this help message and exit

Features:
    - Recursive comparison of all files
    - Excludes .DS_Store and Thumbs files
    - Outputs differences to ~/compare.txt
    - Reports number of differences found

Examples:
    comparefolders.sh /path/to/folder1 /path/to/folder2
    comparefolders.sh ~/Documents/old ~/Documents/new

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
        echo "Error: Missing required arguments" >&2
        echo "Use -h or --help for usage information" >&2
        exit 1
        ;;
esac

# Input validation
if [[ -z "${1:-}" ]] || [[ -z "${2:-}" ]]; then
	echo "Error: Missing required arguments - need both path1 and path2" >&2
	echo "Use -h or --help for usage information" >&2
	exit 1
fi

path1="$1"
path2="$2"

# Validate directories using shared functions
if ! validate_directory "$path1" "first directory"; then
	exit 1
fi

if ! validate_directory "$path2" "second directory"; then
	exit 1
fi

# Set up output file
output_file="$HOME/compare.txt"
echo "Comparing directories..."
echo "Path 1: $path1"
echo "Path 2: $path2"
echo "Output: $output_file"

# Perform comparison
if diff -qr "$path1" "$path2" | grep -v -e 'DS_Store' -e 'Thumbs' > "$output_file"; then
	if [[ -s "$output_file" ]]; then
		echo "✓ Differences found and written to $output_file"
		echo "Number of differences: $(wc -l < "$output_file")"
	else
		echo "✓ No differences found between directories"
		echo "Directories are identical (excluding .DS_Store and Thumbs files)"
	fi
	exit 0
else
	echo "✗ Error occurred during comparison" >&2
	exit 1
fi

