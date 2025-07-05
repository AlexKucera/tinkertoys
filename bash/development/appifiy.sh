#!/usr/bin/env bash
set -euo pipefail

# https://mathiasbynens.be/notes/shell-script-mac-apps

# Help function
show_help() {
    cat << EOF
Usage: appify your-shell-script.sh ['Your App Name']

Creates a macOS .app bundle from a shell script

Arguments:
    script_file    Path to the shell script to convert
    app_name       Optional name for the app (defaults to script filename)

Options:
    -h, --help     Show this help message and exit

Examples:
    appify my-script.sh
    appify my-script.sh "My Custom App"

Based on: https://mathiasbynens.be/notes/shell-script-mac-apps
EOF
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    "")
        echo "Error: Missing required argument - script file" >&2
        echo "Use -h or --help for usage information" >&2
        exit 1
        ;;
esac

# Input validation
if [[ -z "${1:-}" ]]; then
    echo "Error: Missing required argument - script file" >&2
    echo "Use -h or --help for usage information" >&2
    exit 1
fi

if [[ ! -f "$1" ]]; then
    echo "Error: Script file '$1' does not exist" >&2
    exit 1
fi

APPNAME=${2:-$(basename "${1}" '.sh')}
DIR="${APPNAME}.app/Contents/MacOS"

if [[ -e "${APPNAME}.app" ]]; then
	echo "Error: ${PWD}/${APPNAME}.app already exists" >&2
	exit 1
fi

echo "Creating app bundle: ${APPNAME}.app"
mkdir -p "${DIR}"
cp "${1}" "${DIR}/${APPNAME}"
chmod +x "${DIR}/${APPNAME}"

echo "Successfully created: ${PWD}/${APPNAME}.app"