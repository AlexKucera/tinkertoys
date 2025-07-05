#!/usr/bin/env bash
# System utility functions
# Created by Alexander Kucera / babylondreams.de

# Source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# Function to get system information
get_system_info() {
    local -n sys_info="$1"
    
    sys_info[hostname]="$(hostname -s)"
    sys_info[platform]="$(detect_platform)"
    sys_info[cores]="$(getconf _NPROCESSORS_ONLN)"
    
    if is_macos; then
        sys_info[os_version]="$(sw_vers -productVersion)"
        sys_info[os_name]="macOS"
    elif is_linux; then
        sys_info[os_version]="$(lsb_release -rs 2>/dev/null || echo 'unknown')"
        sys_info[os_name]="Linux"
    else
        sys_info[os_version]="unknown"
        sys_info[os_name]="unknown"
    fi
}

# Function to get memory information (macOS specific)
get_memory_info() {
    local -n mem_info="$1"
    
    if ! is_macos; then
        echo "Error: Memory info function currently only supports macOS" >&2
        return 1
    fi
    
    # Parse vm_stat output
    local vm_stat_output
    vm_stat_output="$(vm_stat)"
    
    mem_info[free_blocks]="$(echo "$vm_stat_output" | grep 'free' | awk '{print $3}' | sed 's/\.//')"
    mem_info[inactive_blocks]="$(echo "$vm_stat_output" | grep 'inactive' | awk '{print $3}' | sed 's/\.//')"
    mem_info[speculative_blocks]="$(echo "$vm_stat_output" | grep 'speculative' | awk '{print $3}' | sed 's/\.//')"
    mem_info[active_blocks]="$(echo "$vm_stat_output" | grep 'Pages active' | awk '{print $3}' | sed 's/\.//')"
    mem_info[wired_blocks]="$(echo "$vm_stat_output" | grep 'wired' | awk '{print $4}' | sed 's/\.//')"
    
    # Calculate memory in MB (each block is 4096 bytes)
    mem_info[free_mb]=$(( (mem_info[free_blocks] + mem_info[speculative_blocks]) * 4096 / 1048576 ))
    mem_info[inactive_mb]=$(( mem_info[inactive_blocks] * 4096 / 1048576 ))
    mem_info[total_mb]=$(( (mem_info[free_blocks] + mem_info[inactive_blocks] + mem_info[speculative_blocks] + mem_info[active_blocks] + mem_info[wired_blocks]) * 4096 / 1048576 ))
}

# Function to check disk space
check_disk_space() {
    local path="$1"
    local min_space_gb="${2:-1}"
    
    if [[ ! -d "$path" ]]; then
        echo "Error: Path does not exist: $path" >&2
        return 1
    fi
    
    local available_space
    if is_macos; then
        available_space="$(df -g "$path" | tail -1 | awk '{print $4}')"
    else
        available_space="$(df -BG "$path" | tail -1 | awk '{print $4}' | sed 's/G//')"
    fi
    
    if [[ "$available_space" -lt "$min_space_gb" ]]; then
        echo "Warning: Low disk space. Available: ${available_space}GB, Minimum required: ${min_space_gb}GB" >&2
        return 1
    fi
    
    echo "Disk space check passed. Available: ${available_space}GB"
    return 0
}

# Function to find disk device by label (macOS specific)
find_disk_by_label() {
    local label="$1"
    
    if ! is_macos; then
        echo "Error: find_disk_by_label currently only supports macOS" >&2
        return 1
    fi
    
    diskutil list | grep "$label" | awk '{print $6}'
}

# Function to check if application is installed
check_application() {
    local app_name="$1"
    local check_method="${2:-command}" # command, macos_app, or path
    
    case "$check_method" in
        "command")
            if command -v "$app_name" >/dev/null 2>&1; then
                echo "✓ $app_name is available"
                return 0
            else
                echo "✗ $app_name is not available"
                return 1
            fi
            ;;
        "macos_app")
            if is_macos && [[ -d "/Applications/${app_name}.app" ]]; then
                echo "✓ $app_name is installed"
                return 0
            else
                echo "✗ $app_name is not installed"
                return 1
            fi
            ;;
        "path")
            if [[ -x "$app_name" ]]; then
                echo "✓ $app_name is available at $app_name"
                return 0
            else
                echo "✗ $app_name is not available at $app_name"
                return 1
            fi
            ;;
        *)
            echo "Error: Invalid check method: $check_method" >&2
            return 1
            ;;
    esac
}

# Function to list applications in directory
list_applications() {
    local directory="$1"
    local output_file="${2:-}"
    
    if [[ ! -d "$directory" ]]; then
        echo "Error: Directory does not exist: $directory" >&2
        return 1
    fi
    
    local app_list
    app_list="$(ls "$directory" 2>/dev/null)"
    
    if [[ -n "$output_file" ]]; then
        echo "$app_list" >> "$output_file"
    else
        echo "$app_list"
    fi
}

# Function to check log file size
check_log_size() {
    local log_file="$1"
    local max_size_kb="${2:-128}"
    
    if [[ ! -f "$log_file" ]]; then
        echo "Error: Log file does not exist: $log_file" >&2
        return 1
    fi
    
    local file_size_bytes
    if is_macos; then
        file_size_bytes="$(stat -f%z "$log_file")"
    else
        file_size_bytes="$(stat -c%s "$log_file")"
    fi
    
    local file_size_kb=$((file_size_bytes / 1024))
    local max_size_bytes=$((max_size_kb * 1024))
    
    echo "Log file: $log_file"
    echo "Current size: ${file_size_kb}KB"
    echo "Maximum size: ${max_size_kb}KB"
    
    if [[ "$file_size_bytes" -gt "$max_size_bytes" ]]; then
        echo "Warning: Log file exceeds maximum size"
        return 1
    else
        echo "Log file size is within limits"
        return 0
    fi
}

# Function to safely purge memory (macOS specific)
purge_memory() {
    local min_ram_percent="${1:-5}"
    local min_inactive_percent="${2:-15}"
    
    if ! is_macos; then
        echo "Error: Memory purge function currently only supports macOS" >&2
        return 1
    fi
    
    declare -A memory_info
    get_memory_info memory_info
    
    local ram_limit=$((memory_info[total_mb] * min_ram_percent / 100))
    local inactive_limit=$((memory_info[total_mb] * min_inactive_percent / 100))
    
    echo "Current free memory: ${memory_info[free_mb]}MB"
    echo "Current inactive memory: ${memory_info[inactive_mb]}MB"
    echo "RAM limit: ${ram_limit}MB"
    echo "Inactive limit: ${inactive_limit}MB"
    
    if [[ "${memory_info[free_mb]}" -le "$ram_limit" ]]; then
        if [[ "${memory_info[inactive_mb]}" -ge "$inactive_limit" ]]; then
            echo "Purging memory..."
            if command -v purge >/dev/null 2>&1; then
                purge
                echo "Memory purged successfully"
                return 0
            else
                echo "Error: purge command not available" >&2
                return 1
            fi
        else
            echo "Not purging: insufficient inactive memory to make it worthwhile"
            return 1
        fi
    else
        echo "Not purging: sufficient free memory available"
        return 1
    fi
}

# Function to generate system report
generate_system_report() {
    local output_file="$1"
    
    {
        echo "System Report - $(date)"
        echo "================================"
        echo ""
        
        declare -A sys_info
        get_system_info sys_info
        
        echo "System Information:"
        echo "  Hostname: ${sys_info[hostname]}"
        echo "  Platform: ${sys_info[platform]}"
        echo "  OS: ${sys_info[os_name]} ${sys_info[os_version]}"
        echo "  CPU Cores: ${sys_info[cores]}"
        echo ""
        
        if is_macos; then
            declare -A memory_info
            if get_memory_info memory_info; then
                echo "Memory Information:"
                echo "  Total: ${memory_info[total_mb]}MB"
                echo "  Free: ${memory_info[free_mb]}MB"
                echo "  Inactive: ${memory_info[inactive_mb]}MB"
                echo ""
            fi
        fi
        
        echo "Disk Space:"
        df -h | head -1
        df -h | grep -E '^/dev/'
        echo ""
        
        echo "Available Commands:"
        for cmd in ffmpeg nuke git brew; do
            if command -v "$cmd" >/dev/null 2>&1; then
                echo "  ✓ $cmd: $(command -v "$cmd")"
            else
                echo "  ✗ $cmd: not found"
            fi
        done
        
    } | if [[ -n "$output_file" ]]; then
        tee "$output_file"
    else
        cat
    fi
}