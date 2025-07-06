#!/usr/bin/env bash
set -euo pipefail

#
# Duplicate Folder Structure Script
# Creates a duplicate of a directory tree structure without copying files.
# Only creates directories, preserving the exact folder hierarchy.
#
# Author: Alexander Kucera
# Contact: babylondreams.de
#
# Usage:
#   duplicate_folder_structure.sh SOURCE DESTINATION [OPTIONS]
#   duplicate_folder_structure.sh /path/to/source /path/to/destination
#   duplicate_folder_structure.sh /project --suffix "_backup"
#

# Load common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$(cd "${SCRIPT_DIR}/../lib" && pwd)"

# Source common library
if [[ -f "${LIB_DIR}/common.sh" ]]; then
    # shellcheck source=../lib/common.sh
    source "${LIB_DIR}/common.sh"
else
    echo "Error: Could not find common.sh library" >&2
    exit 1
fi

# Script metadata
SCRIPT_NAME="duplicate_folder_structure.sh"
SCRIPT_DESCRIPTION="Duplicate directory structure without copying files"

# Global variables
SOURCE_DIR=""
DESTINATION_DIR=""
DRY_RUN=false
VERBOSE=false
FORCE=false
DIRS_CREATED=0
DIRS_SKIPPED=0
ERRORS=0

# Function to show help
show_script_help() {
    local usage="$SCRIPT_NAME SOURCE [DESTINATION] [OPTIONS]"
    local options="  -s, --suffix SUFFIX     Add suffix to source directory name for destination
  -p, --prefix PREFIX     Add prefix to source directory name for destination
  -d, --dry-run          Show what would be done without making changes
  -v, --verbose          Show detailed output
  -f, --force            Skip confirmation prompts
  -h, --help             Show this help message"
    
    local examples="  $SCRIPT_NAME /project/source /backup/structure
  $SCRIPT_NAME /project --suffix \"_folders\"
  $SCRIPT_NAME /data --prefix \"structure_\" --verbose
  $SCRIPT_NAME /source /dest --dry-run --verbose"
    
    show_help "$SCRIPT_NAME" "$SCRIPT_DESCRIPTION" "$usage" "$options" "$examples"
    echo ""
    echo "DESCRIPTION:"
    echo "  This tool creates an exact copy of a directory tree structure without"
    echo "  copying any files. Only directories are created, preserving the exact"
    echo "  folder hierarchy from the source."
    echo ""
    echo "  If DESTINATION is not provided, you must use --suffix or --prefix to"
    echo "  generate the destination path automatically."
}

# Function to validate paths
validate_paths() {
    # Check source directory
    if ! validate_directory "$SOURCE_DIR" "source directory"; then
        return 1
    fi
    
    # Check if destination is a file
    if [[ -f "$DESTINATION_DIR" ]]; then
        echo "Error: Destination exists but is a file: $DESTINATION_DIR" >&2
        return 1
    fi
    
    # Check if source and destination are the same
    if [[ "$(realpath "$SOURCE_DIR")" == "$(realpath "$DESTINATION_DIR" 2>/dev/null || echo "$DESTINATION_DIR")" ]]; then
        echo "Error: Source and destination cannot be the same" >&2
        return 1
    fi
    
    # Check if destination is inside source (prevent infinite recursion)
    local source_real="$(realpath "$SOURCE_DIR")"
    local dest_real="$(realpath "$DESTINATION_DIR" 2>/dev/null || echo "$DESTINATION_DIR")"
    
    if [[ "$dest_real" == "$source_real"/* ]]; then
        echo "Error: Destination cannot be inside source directory" >&2
        return 1
    fi
    
    return 0
}

# Function to generate destination path with suffix or prefix
generate_destination_path() {
    local source="$1"
    local suffix="$2"
    local prefix="$3"
    
    local source_basename="$(basename "$source")"
    local source_dirname="$(dirname "$source")"
    
    if [[ -n "$suffix" ]]; then
        echo "${source_dirname}/${source_basename}${suffix}"
    elif [[ -n "$prefix" ]]; then
        echo "${source_dirname}/${prefix}${source_basename}"
    else
        echo "${source_dirname}/${source_basename}_structure"
    fi
}

# Function to ask for confirmation
ask_confirmation() {
    local question="$1"
    local default="${2:-no}"
    local response
    
    if [[ "$FORCE" == true ]]; then
        return 0
    fi
    
    if [[ "$default" == "yes" ]]; then
        printf "%s (Y/n): " "$question"
    else
        printf "%s (y/N): " "$question"
    fi
    
    read -r response
    
    if [[ -z "$response" ]]; then
        response="$default"
    fi
    
    case "$response" in
        [Yy]|[Yy][Ee][Ss]|yes)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Function to create directory structure
create_directory_structure() {
    local source="$1"
    local destination="$2"
    local dry_run="$3"
    
    if [[ "$VERBOSE" == true ]]; then
        echo "Scanning directory structure..."
    fi
    
    # Count total directories first
    local total_dirs
    total_dirs=$(find "$source" -type d | wc -l)
    total_dirs=$((total_dirs - 1))  # Exclude the source directory itself
    
    if [[ "$total_dirs" -eq 0 ]]; then
        echo "No subdirectories found to duplicate"
        return 0
    fi
    
    echo "Found $total_dirs directories to duplicate"
    
    if [[ "$dry_run" == true ]]; then
        echo ""
        echo "DRY RUN - Would create directories in: $destination"
        echo "$(printf '=%.0s' {1..50})"
    else
        echo ""
        echo "Creating directory structure in: $destination"
        echo "$(printf '=%.0s' {1..50})"
    fi
    
    # Create base destination directory
    if [[ "$dry_run" == false ]]; then
        if ! mkdir -p "$destination" 2>/dev/null; then
            echo "Error: Failed to create base directory: $destination" >&2
            return 1
        fi
        
        if [[ "$VERBOSE" == true ]]; then
            echo "Created base directory: $destination"
        fi
    fi
    
    # Process each directory using find
    local dir_count=0
    while IFS= read -r -d '' dir; do
        # Calculate relative path
        local relative_path="${dir#$source}"
        relative_path="${relative_path#/}"  # Remove leading slash
        
        # Skip empty relative path (source directory itself)
        if [[ -z "$relative_path" ]]; then
            continue
        fi
        
        local target_dir="$destination/$relative_path"
        
        if [[ "$dry_run" == true ]]; then
            if [[ "$VERBOSE" == true ]]; then
                echo "Would create: $target_dir"
            fi
            ((DIRS_CREATED++))
        else
            if [[ -d "$target_dir" ]]; then
                if [[ "$VERBOSE" == true ]]; then
                    echo "Already exists: $target_dir"
                fi
                ((DIRS_SKIPPED++))
            else
                if mkdir -p "$target_dir" 2>/dev/null; then
                    if [[ "$VERBOSE" == true ]]; then
                        echo "Created: $target_dir"
                    fi
                    ((DIRS_CREATED++))
                else
                    echo "Error: Failed to create directory: $target_dir" >&2
                    ((ERRORS++))
                fi
            fi
        fi
        
        ((dir_count++))
        
        # Show progress for large operations
        if [[ "$VERBOSE" == false && $((dir_count % 100)) -eq 0 ]]; then
            echo "Processed $dir_count/$total_dirs directories..."
        fi
        
    done < <(find "$source" -type d -print0)
    
    return 0
}

# Function to show operation summary
show_summary() {
    local dry_run="$1"
    
    echo ""
    echo "$(printf '=%.0s' {1..50})"
    
    if [[ "$dry_run" == true ]]; then
        echo "DRY RUN SUMMARY:"
        echo "Directories that would be created: $DIRS_CREATED"
    else
        echo "OPERATION SUMMARY:"
        echo "Directories created: $DIRS_CREATED"
        echo "Directories already existing: $DIRS_SKIPPED"
    fi
    
    if [[ "$ERRORS" -gt 0 ]]; then
        echo "Errors encountered: $ERRORS"
    else
        echo "No errors encountered"
    fi
    
    echo "Source: $SOURCE_DIR"
    echo "Destination: $DESTINATION_DIR"
}

# Function to parse command line arguments
parse_arguments() {
    local suffix=""
    local prefix=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_script_help
                exit 0
                ;;
            -s|--suffix)
                if [[ -n "${2:-}" ]]; then
                    suffix="$2"
                    shift 2
                else
                    echo "Error: --suffix requires a value" >&2
                    exit 1
                fi
                ;;
            -p|--prefix)
                if [[ -n "${2:-}" ]]; then
                    prefix="$2"
                    shift 2
                else
                    echo "Error: --prefix requires a value" >&2
                    exit 1
                fi
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -f|--force)
                FORCE=true
                shift
                ;;
            -*)
                echo "Error: Unknown option $1" >&2
                echo "Use --help for usage information" >&2
                exit 1
                ;;
            *)
                if [[ -z "$SOURCE_DIR" ]]; then
                    SOURCE_DIR="$1"
                elif [[ -z "$DESTINATION_DIR" ]]; then
                    DESTINATION_DIR="$1"
                else
                    echo "Error: Too many arguments" >&2
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Validate required arguments
    if [[ -z "$SOURCE_DIR" ]]; then
        echo "Error: Source directory is required" >&2
        echo "Use --help for usage information" >&2
        exit 1
    fi
    
    # Generate destination if not provided
    if [[ -z "$DESTINATION_DIR" ]]; then
        if [[ -n "$suffix" || -n "$prefix" ]]; then
            DESTINATION_DIR="$(generate_destination_path "$SOURCE_DIR" "$suffix" "$prefix")"
        else
            echo "Error: Must provide destination or use --suffix/--prefix" >&2
            exit 1
        fi
    fi
    
    # Check for conflicting options
    if [[ -n "$suffix" && -n "$prefix" ]]; then
        echo "Error: Cannot use both --suffix and --prefix" >&2
        exit 1
    fi
}

# Main function
main() {
    # Parse command line arguments
    parse_arguments "$@"
    
    # Validate paths
    if ! validate_paths; then
        exit 1
    fi
    
    # Show operation details
    echo "$SCRIPT_DESCRIPTION"
    echo ""
    echo "Source directory: $SOURCE_DIR"
    echo "Destination directory: $DESTINATION_DIR"
    
    if [[ "$DRY_RUN" == true ]]; then
        echo "Mode: DRY RUN (no changes will be made)"
    else
        echo "Mode: EXECUTE (directories will be created)"
    fi
    
    # Confirmation for non-dry-run operations
    if [[ "$DRY_RUN" == false ]]; then
        if [[ -d "$DESTINATION_DIR" ]]; then
            if ! ask_confirmation "Destination exists. Continue?" "no"; then
                echo "Operation cancelled by user"
                exit 0
            fi
        else
            if ! ask_confirmation "Proceed with directory creation?" "yes"; then
                echo "Operation cancelled by user"
                exit 0
            fi
        fi
    fi
    
    # Record start time
    local start_time
    start_time=$(date +%s)
    
    # Execute operation
    if create_directory_structure "$SOURCE_DIR" "$DESTINATION_DIR" "$DRY_RUN"; then
        show_summary "$DRY_RUN"
        
        # Show timing
        local end_time
        end_time=$(date +%s)
        local duration
        duration=$(calculate_duration "$start_time" "$end_time")
        echo "Operation completed in $duration"
        
        if [[ "$DRY_RUN" == true ]]; then
            echo ""
            echo "To execute: ${0} \"${SOURCE_DIR}\" \"${DESTINATION_DIR}\" --verbose"
        fi
        
        # Exit with error code if there were errors
        if [[ "$ERRORS" -gt 0 ]]; then
            exit 1
        fi
    else
        echo "Operation failed" >&2
        exit 1
    fi
}

# Run main function with all arguments
main "$@"