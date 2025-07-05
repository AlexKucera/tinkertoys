#!/usr/bin/env bash
set -euo pipefail

# Memory Purge Loop
# Automatically purges inactive memory at specified intervals
# Created by Alexander Kucera / babylondreams.de

# Source shared libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/system_functions.sh"

# Help function
show_help() {
    cat << EOF
Usage: purgeLoop.sh [interval_minutes] [min_ram_percent] [inactive_percent]

Automatically purges inactive memory at specified intervals

Arguments:
    interval_minutes       Check interval in minutes (default: 15)
    min_ram_percent       Minimum free RAM percent before purge (default: 5)
    inactive_percent      Minimum inactive RAM percent required (default: 15)

Options:
    -h, --help            Show this help message and exit

Features:
    - Monitors system memory usage continuously
    - Only purges when free RAM is low AND inactive RAM is high
    - Displays memory statistics before and after purge
    - macOS-specific memory management

Safety:
    - Only purges when beneficial (high inactive memory)
    - Configurable thresholds prevent unnecessary purging
    - Ctrl+C to stop monitoring

Examples:
    purgeLoop.sh                    # Use defaults (15min, 5%, 15%)
    purgeLoop.sh 30                # Check every 30 minutes
    purgeLoop.sh 10 3 20           # 10min intervals, 3% RAM, 20% inactive

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

# Configuration defaults
DEFAULT_INTERVAL=15         # Default interval in minutes
DEFAULT_MIN_RAM_PERCENT=5   # Minimum free RAM percentage before purge
DEFAULT_INACTIVE_PERCENT=15 # Minimum inactive RAM percentage required for purge

# Input validation and setup
interval_minutes="${1:-$DEFAULT_INTERVAL}"
min_ram_percent="${2:-$DEFAULT_MIN_RAM_PERCENT}"
inactive_percent="${3:-$DEFAULT_INACTIVE_PERCENT}"

# Validate numeric inputs
if ! [[ "$interval_minutes" =~ ^[0-9]+$ ]] || [[ "$interval_minutes" -lt 1 ]]; then
    echo "Error: Invalid interval '$interval_minutes'. Must be a positive integer." >&2
    echo "Usage: purgeLoop.sh [interval_minutes] [min_ram_percent] [inactive_percent]" >&2
    exit 1
fi

if ! [[ "$min_ram_percent" =~ ^[0-9]+$ ]] || [[ "$min_ram_percent" -lt 1 ]] || [[ "$min_ram_percent" -gt 50 ]]; then
    echo "Error: Invalid min_ram_percent '$min_ram_percent'. Must be 1-50." >&2
    exit 1
fi

if ! [[ "$inactive_percent" =~ ^[0-9]+$ ]] || [[ "$inactive_percent" -lt 1 ]] || [[ "$inactive_percent" -gt 50 ]]; then
    echo "Error: Invalid inactive_percent '$inactive_percent'. Must be 1-50." >&2
    exit 1
fi

# Platform check
if ! is_macos; then
    echo "Error: This script currently only supports macOS" >&2
    exit 1
fi

# Calculate timing
interval_seconds=$((interval_minutes * 60))

echo "Memory Purge Loop Configuration:"
echo "  Interval: $interval_minutes minutes ($interval_seconds seconds)"
echo "  Minimum RAM threshold: $min_ram_percent%"
echo "  Minimum inactive RAM threshold: $inactive_percent%"
echo ""

# Get initial memory information
declare -A memory_info
if ! get_memory_info memory_info; then
    echo "Error: Failed to get memory information" >&2
    exit 1
fi

ram_limit_mb=$((memory_info[total_mb] * min_ram_percent / 100))
inactive_limit_mb=$((memory_info[total_mb] * inactive_percent / 100))

echo "System Memory Information:"
echo "  Total RAM: ${memory_info[total_mb]}MB"
echo "  RAM limit: ${ram_limit_mb}MB (purge if free RAM below this)"
echo "  Inactive limit: ${inactive_limit_mb}MB (only purge if inactive RAM above this)"
echo ""

echo "Starting memory monitoring loop..."
echo "Press Ctrl+C to stop"
echo ""

# Main monitoring loop
while true; do
    # Get current memory information
    if get_memory_info memory_info; then
        timestamp="$(date '+%H:%M:%S')"
        
        echo "[$timestamp] Memory Status:"
        echo "  Free: ${memory_info[free_mb]}MB"
        echo "  Inactive: ${memory_info[inactive_mb]}MB"
        echo "  RAM limit: ${ram_limit_mb}MB"
        echo "  Inactive limit: ${inactive_limit_mb}MB"
        
        # Check if purge is needed and beneficial
        if [[ "${memory_info[free_mb]}" -le "$ram_limit_mb" ]]; then
            if [[ "${memory_info[inactive_mb]}" -ge "$inactive_limit_mb" ]]; then
                echo "  → Purging memory..."
                
                if purge_memory "$min_ram_percent" "$inactive_percent"; then
                    # Get updated memory info after purge
                    get_memory_info memory_info
                    echo "  → Memory after purge:"
                    echo "    Free: ${memory_info[free_mb]}MB"
                    echo "    Inactive: ${memory_info[inactive_mb]}MB"
                else
                    echo "  → Memory purge completed (no change needed)"
                fi
            else
                echo "  → No purge: insufficient inactive RAM to be worthwhile"
            fi
        else
            echo "  → No purge: sufficient free RAM available"
        fi
    else
        echo "Error: Failed to get memory information" >&2
    fi
    
    echo "  → Next check in $interval_minutes minutes"
    echo ""
    
    # Sleep until next check
    sleep "$interval_seconds"
done