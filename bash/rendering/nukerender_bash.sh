#!/usr/bin/env bash
set -euo pipefail

# Nuke Render Script
# Automates Nuke rendering with email notifications
# Requires http://caspian.dotconf.net/menu/Software/SendEmail/
# Created by Alexander Kucera / babylondreams.de

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/system_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: nukerender_bash.sh <nuke_script> [output_path]

Automates Nuke rendering with email notifications

Arguments:
    nuke_script    Path to Nuke script file (.nk)
    output_path    Optional output path for rendered files

Options:
    -h, --help     Show this help message and exit

Features:
    - Interactive setup for render options
    - GPU enable/disable option
    - Interactive license support for Furnace tools
    - Email notifications on completion
    - Render timing and duration tracking

Configuration:
    - Set NUKEPATH environment variable to Nuke executable
    - Edit config/mail_send.conf for email settings
    - Set MAIL_PASSWORD environment variable

Interactive Options:
    - Custom render range (e.g., -F 12-13)
    - GPU enable/disable
    - Interactive license for Furnace tools

Examples:
    nukerender_bash.sh myscript.nk
    nukerender_bash.sh myscript.nk /path/to/output

Requirements:
    - Nuke (NUKEPATH must be set)
    - sendemail for notifications

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

# Rendering on the command line
################################

# To render frame 5 of a Nuke script:
# nuke -F 5 -x myscript.nk

# To render frames 30 to 50 of a Nuke script:
# nuke -F 30-50 -x myscript.nk

# To render two frame ranges, 10-20 and 34-60, of a Nuke script:
# nuke -F 10-20 -F 34-60 -x myscript.nk

# To render every tenth frame of a 50 frame sequence of a Nuke script:
# This renders frames 1, 11, 21, 31, 41.
# nuke -F 1-50x10 -x myscript.nk

# In a script with two write nodes called WriteBlur and WriteInvert this command just renders frames 1 to 20 from the WriteBlur node:
# nuke -X WriteBlur myscript.nk 1-20

# If there are Furnace nodes in the comp, then you need to use the interactive license for rendering.

#nuke -x -i myscript.nk

# To display a list of command line flags (switches) available to you, use the following command:
# nuke -help

# Interactive configuration
echo "Please input custom render range (ex.: <-F 12-13>) or press enter to use the comps render range."
read -r RENDERRANGE

echo "Disable GPU (y/n)?"
read -r answer
if echo "$answer" | grep -iq "^y" ; then
    GPU=""
else
    GPU="--gpu"
fi

echo "Use Interactive License (i.e. if Furnace tools were used) (y/n)?"
read -r answer
if echo "$answer" | grep -iq "^y" ; then
    INTERACTIVE="-i"
else
    INTERACTIVE=""
fi

# Validate required arguments
if [[ $# -lt 1 ]]; then
    echo "Error: Missing required argument - Nuke script file" >&2
    echo "Usage: $0 <nuke_script> [output_path]" >&2
    exit 1
fi

# Validate Nuke script exists
if ! validate_file "$1" "Nuke script"; then
    exit 1
fi

# Validate NUKEPATH is set
if [[ -z "${NUKEPATH:-}" ]]; then
    echo "Error: NUKEPATH environment variable not set" >&2
    echo "Please set NUKEPATH to your Nuke executable path" >&2
    exit 1
fi

# Validate Nuke executable exists
if ! validate_file "$NUKEPATH" "Nuke executable"; then
    exit 1
fi

# Build render command
CORES="$(getconf _NPROCESSORS_ONLN)"
NUKE="$NUKEPATH"
FLAGS="-x $INTERACTIVE -m $CORES $GPU -f"
COMMAND="$NUKE $FLAGS $RENDERRANGE $1 ${2:-}"

echo "Render command: $COMMAND"
echo ""

# Mail configuration and validation
CONFIG_DIR="$(cd "${SCRIPT_DIR}/../config" && pwd)"
source "${CONFIG_DIR}/mail_send.conf"

# Validate that password is set
if [[ -z "$PASS" ]]; then
    echo "ERROR: Mail password not set. Please set MAIL_PASSWORD environment variable." >&2
    echo "Example: export MAIL_PASSWORD='your_password_here'" >&2
    exit 1
fi

# Validate sendemail command
validate_command "sendemail" "SendEmail"

# Configuration
SUBJECT="Nuke render completed"
declare -A sys_info
get_system_info sys_info
MACHINE="${sys_info[hostname]}"

# Record start time
START="$(date +%s)"
STARTDATE="$(get_timestamp)"

echo "Render started at: $STARTDATE"
echo "Machine: $MACHINE"

# Execute Nuke render command
$COMMAND

# Record end time and calculate duration
END="$(date +%s)"
ENDDATE="$(get_timestamp)"
DURATION="$(calculate_duration "$START" "$END")"

echo "Render completed at: $ENDDATE"
echo "Duration: $DURATION"

# Prepare notification email
BODY="${MACHINE} just finished rendering all assigned Nuke scripts. It started at ${STARTDATE} and ended at ${ENDDATE} taking ${DURATION} overall."

echo "Sending notification email..."

# Send notification email
if sendemail -f "${FROM_ADDRESS}" -t "${TO_ADDRESS}" -m "${BODY}" -u "${SUBJECT}" -s "${SERVER}" -xu "${USER}" -xp "${PASS}"; then
    echo "✓ Notification email sent successfully"
    exit 0
else
    echo "✗ Failed to send notification email" >&2
    exit 1
fi