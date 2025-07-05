#!/usr/bin/env bash
set -euo pipefail

# Version Number Incrementer
# Increments version number in version.txt file
# Created by Alexander Kucera / babylondreams.de

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"

# Help function
show_help() {
    cat << EOF
Usage: version_up.sh [version_file]

Increments version number in version.txt file (or specified file)

Arguments:
    version_file   Optional path to version file (default: version.txt)

Options:
    -h, --help     Show this help message and exit

Features:
    - Automatically increments version numbers (e.g., 1.2.3 → 1.2.4)
    - Adds timestamp to version history
    - Creates new version file if none exists
    - Validates version format

Examples:
    version_up.sh                    # Use default version.txt
    version_up.sh my_version.txt     # Use custom version file

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

# Function to increment version number
increment_version() {
    local version="$1"
    declare -a part=( ${version//\./ } )
    declare new
    declare -i carry=1

    for (( CNTR=${#part[@]}-1; CNTR>=0; CNTR-=1 )); do
        len=${#part[CNTR]}
        new=$((part[CNTR]+carry))
        [ ${#new} -gt $len ] && carry=1 || carry=0
        [ $CNTR -gt 0 ] && part[CNTR]=${new: -len} || part[CNTR]=${new}
    done
    new="${part[*]}"
    echo "${new// /.}"
}

# Configuration
VERSION_FILE="${1:-version.txt}"
WORKING_DIR="$(get_script_dir)"

echo "Version incrementer working in: $WORKING_DIR"
cd "$WORKING_DIR"

# Validate version file exists
if ! validate_file "$VERSION_FILE" "version file"; then
    echo "Creating new version file with initial version 1.0.0"
    echo "1.0.0" > "$VERSION_FILE"
fi

# Read current version
current_version="$(head -n 1 "$VERSION_FILE")"
echo "Current version: $current_version"

# Validate version format
if ! [[ "$current_version" =~ ^[0-9]+(\.[0-9]+)*$ ]]; then
    echo "Error: Invalid version format in $VERSION_FILE: '$current_version'" >&2
    echo "Expected format: major.minor.patch (e.g., 1.2.3)" >&2
    exit 1
fi

# Increment version
new_version="$(increment_version "$current_version")"
date_stamp="$(date +"- %Y-%m-%d")"
version_entry="$new_version $date_stamp"

echo "New version: $new_version"
echo "Date stamp: $date_stamp"

# Update version file
if echo -e "${version_entry}\n$(cat "$VERSION_FILE")" > "$VERSION_FILE"; then
    echo "✓ Version updated successfully!"
    echo "Version file updated: $VERSION_FILE"
    
    # Show first few lines of updated file
    echo ""
    echo "Updated version history:"
    head -5 "$VERSION_FILE" | while IFS= read -r line; do
        echo "  $line"
    done
    
    exit 0
else
    echo "✗ Error: Failed to update version file" >&2
    exit 1
fi