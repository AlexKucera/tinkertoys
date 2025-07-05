#!/usr/bin/env bash
set -euo pipefail

# Application List Updater
# Creates a comprehensive list of installed applications for backup purposes
# Created by Alexander Kucera / babylondreams.de

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/system_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: application_list_updater.sh [output_file]

Creates a comprehensive list of installed applications for backup purposes

Arguments:
    output_file    Optional path for output file (default: ~/Documents/ApplicationList.txt)

Options:
    -h, --help     Show this help message and exit

Features:
    - Lists applications from /Applications
    - Lists user-specific applications from ~/Applications
    - Lists Homebrew packages and casks
    - Lists App Store applications
    - Organizes output by installation method
    - Includes timestamps for restoration reference

Examples:
    application_list_updater.sh
    application_list_updater.sh /path/to/my_apps.txt

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
OUTPUT="/Users/alex/Documents/ApplicationList.txt"
USER_APPS="/Users/alex/Applications"

echo "Creating application list at: $OUTPUT"

# Initialize output file with timestamp
{
    echo "Application List - Generated $(date)"
    echo "=================================================="
    echo ""
    echo "This file lists all installed applications for restoration purposes."
    echo "Note: Actual applications are not backed up, only their names."
    echo ""
} > "$OUTPUT"

# Function to add section header
add_section() {
    local title="$1"
    {
        echo ""
        echo "##################################################"
        echo "$title"
        echo "##################################################"
        echo ""
    } >> "$OUTPUT"
}

# List user applications
add_section "User Applications ($USER_APPS)"
if [[ -L "$USER_APPS" ]]; then
    echo "$USER_APPS is a symlink" >> "$OUTPUT"
elif [[ -d "$USER_APPS" ]]; then
    list_applications "$USER_APPS" "$OUTPUT"
else
    echo "Directory not found: $USER_APPS" >> "$OUTPUT"
fi

# List system applications
add_section "System Applications (/Applications)"
list_applications "/Applications" "$OUTPUT"

# List utility applications
add_section "System Utilities (/Applications/Utilities)"
list_applications "/Applications/Utilities" "$OUTPUT"

# List Homebrew packages
add_section "Homebrew Packages"
if check_application "brew" "command"; then
    if command -v brew >/dev/null 2>&1; then
        brew list >> "$OUTPUT" 2>/dev/null || echo "Failed to get brew list" >> "$OUTPUT"
    fi
else
    echo "Homebrew not installed" >> "$OUTPUT"
fi

# Add summary
add_section "Summary"
{
    declare -A sys_info
    get_system_info sys_info
    echo "Generated on: ${sys_info[hostname]} (${sys_info[os_name]} ${sys_info[os_version]})"
    echo "Date: $(date)"
    echo ""
    echo "For detailed Homebrew information, see Tinkertoys Brewfile"
} >> "$OUTPUT"

echo "✓ Application list updated successfully!"
echo "Output saved to: $OUTPUT"

# Show basic statistics
if [[ -f "$OUTPUT" ]]; then
    line_count="$(wc -l < "$OUTPUT")"
    echo "Total lines: $line_count"
fi