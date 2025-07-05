#!/bin/bash
set -euo pipefail

# Mail notification for completed renders
# Requires sendemail: http://caspian.dotconf.net/menu/Software/SendEmail/
# Created by Alexander Kucera / babylondreams.de

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/system_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: mail_send.sh

Mail notification for completed renders

Options:
    -h, --help     Show this help message and exit

Features:
    - Sends email notification when render completes
    - Tracks render start and end times
    - Calculates total render duration
    - Includes machine hostname in notification
    - Requires sendemail utility to be installed

Configuration:
    - Edit config/mail_send.conf for email settings
    - Set MAIL_PASSWORD environment variable for security

Examples:
    mail_send.sh                    # Send notification for completed render
    export MAIL_PASSWORD='pass' && mail_send.sh

Requirements:
    - sendemail: http://caspian.dotconf.net/menu/Software/SendEmail/

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

# Load mail configuration
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
SUBJECT="modo render completed"
declare -A sys_info
get_system_info sys_info
MACHINE="${sys_info[hostname]}"

# Record timing
START="$(date +%s)"
STARTDATE="$(get_timestamp)"

echo "Render started at: $STARTDATE"
echo "Machine: $MACHINE"

# Simulate work (in real use, this would be where actual work happens)
# For this script, we just record start and end times

END="$(date +%s)"
ENDDATE="$(get_timestamp)"
DURATION="$(calculate_duration "$START" "$END")"

BODY="${MACHINE} just finished rendering a shot. It started at ${STARTDATE} and ended at ${ENDDATE} taking ${DURATION} overall."

echo "Sending notification email..."
echo "Duration: $DURATION"

# Send notification email
if sendemail -f "${FROM_ADDRESS}" -t "${TO_ADDRESS}" -m "${BODY}" -u "${SUBJECT}" -s "${SERVER}" -xu "${USER}" -xp "${PASS}"; then
    echo "✓ Notification email sent successfully"
    exit 0
else
    echo "✗ Failed to send notification email" >&2
    exit 1
fi