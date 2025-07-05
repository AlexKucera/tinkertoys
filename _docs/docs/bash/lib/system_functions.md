# System Functions Library (system_functions.sh)

System information, memory management, and platform-specific utilities for system administration and monitoring scripts.

## Overview

Provides comprehensive system information gathering, memory management utilities, and cross-platform system operations. Used by system administration scripts for monitoring, maintenance, and automation tasks.

## Key Functions

### System Information

#### `get_system_info()`
```bash
declare -A sys_info
get_system_info sys_info
echo "Hostname: ${sys_info[hostname]}"
echo "OS: ${sys_info[os]}"
echo "Architecture: ${sys_info[arch]}"
```
Retrieves comprehensive system information.

- **Parameters**: associative_array (passed by reference)
- **Returns**: Populates array with system details
- **Information**: hostname, OS version, architecture, kernel

#### `get_memory_info()`
```bash
declare -A memory_info
get_memory_info memory_info
echo "Total RAM: ${memory_info[total_mb]}MB"
echo "Free RAM: ${memory_info[free_mb]}MB"
echo "Used RAM: ${memory_info[used_mb]}MB"
```
Retrieves detailed memory usage statistics.

- **Parameters**: associative_array (passed by reference)
- **Returns**: Memory statistics in MB
- **Cross-platform**: Works on macOS and Linux

### Memory Management

#### `purge_memory()`
```bash
if purge_memory 5 15; then
    echo "Memory purged successfully"
else
    echo "Memory purge not beneficial"
fi
```
Intelligently purges inactive memory when beneficial.

- **Parameters**: min_ram_percent, min_inactive_percent
- **Returns**: 0 if purged, 1 if not needed
- **Safety**: Only purges when thresholds met

#### `check_memory_pressure()`
```bash
if check_memory_pressure; then
    echo "System under memory pressure"
    # Take action
fi
```
Detects system memory pressure conditions.

- **Returns**: 0 if pressure detected, 1 if normal
- **Use Cases**: Proactive memory management

### Disk Management

#### `find_disk_by_label()`
```bash
device=$(find_disk_by_label "Time Machine")
if [[ -n "$device" ]]; then
    echo "Found disk: $device"
fi
```
Locates disk devices by volume label.

- **Parameters**: volume_label
- **Returns**: Device path (e.g., /dev/disk2s1)
- **Platform**: macOS-specific using diskutil

#### `get_disk_usage()`
```bash
declare -A disk_info
get_disk_usage "/" disk_info
echo "Available: ${disk_info[available]}GB"
echo "Used: ${disk_info[used_percent]}%"
```
Retrieves disk usage statistics.

- **Parameters**: mount_point, associative_array
- **Returns**: Usage statistics in human-readable format

### Process Management

#### `check_process_running()`
```bash
if check_process_running "ffmpeg"; then
    echo "FFmpeg is currently running"
fi
```
Checks if a process is currently running.

- **Parameters**: process_name
- **Returns**: 0 if running, 1 if not
- **Use Cases**: Prevent concurrent operations

#### `get_cpu_usage()`
```bash
cpu_percent=$(get_cpu_usage)
echo "CPU Usage: ${cpu_percent}%"
```
Retrieves current CPU usage percentage.

- **Returns**: CPU usage as percentage
- **Cross-platform**: Adapted for different OS

### Application Management

#### `list_applications()`
```bash
declare -a apps
list_applications apps
for app in "${apps[@]}"; do
    echo "Installed: $app"
done
```
Lists installed applications by category.

- **Parameters**: array (passed by reference)
- **Returns**: Array of application names
- **Sources**: /Applications, ~/Applications, Homebrew

#### `check_homebrew_packages()`
```bash
declare -a packages
check_homebrew_packages packages
echo "Homebrew packages: ${#packages[@]}"
```
Lists Homebrew packages and casks.

- **Parameters**: array (passed by reference)
- **Returns**: Array of package names
- **Types**: Both packages and casks

## Usage Examples

### System Monitoring
```bash
#!/bin/bash
source "lib/system_functions.sh"

# Get system information
declare -A sys_info
get_system_info sys_info

echo "System Report"
echo "============="
echo "Host: ${sys_info[hostname]}"
echo "OS: ${sys_info[os_version]}"
echo "Uptime: ${sys_info[uptime]}"

# Memory status
declare -A mem_info
get_memory_info mem_info
echo "Memory: ${mem_info[used_mb]}/${mem_info[total_mb]}MB"
```

### Automated Memory Management
```bash
#!/bin/bash
source "lib/system_functions.sh"

# Check memory pressure
if check_memory_pressure; then
    echo "Memory pressure detected"
    
    # Get current memory info
    declare -A mem_info
    get_memory_info mem_info
    
    # Purge if beneficial (5% free, 15% inactive minimum)
    if purge_memory 5 15; then
        echo "Memory purged"
        
        # Get updated info
        get_memory_info mem_info
        echo "Free memory after purge: ${mem_info[free_mb]}MB"
    else
        echo "Memory purge not beneficial"
    fi
fi
```

### Disk Space Monitoring
```bash
#!/bin/bash
source "lib/system_functions.sh"

# Check multiple mount points
for mount in "/" "/var" "/tmp"; do
    if [[ -d "$mount" ]]; then
        declare -A disk_info
        get_disk_usage "$mount" disk_info
        
        echo "$mount: ${disk_info[used_percent]}% used"
        
        if [[ "${disk_info[used_percent]%\%}" -gt 90 ]]; then
            echo "Warning: $mount is over 90% full"
        fi
    fi
done
```

### Application Inventory
```bash
#!/bin/bash
source "lib/system_functions.sh"

echo "Application Inventory"
echo "===================="

# System applications
declare -a apps
list_applications apps
echo "Applications found: ${#apps[@]}"

# Homebrew packages
declare -a packages
check_homebrew_packages packages
echo "Homebrew packages: ${#packages[@]}"
```

## Cross-Platform Support

### macOS-Specific Functions
- `find_disk_by_label()` - Uses diskutil
- `purge_memory()` - Uses macOS purge command
- `get_memory_info()` - Uses vm_stat

### Linux-Specific Functions
- Memory functions use /proc/meminfo
- Disk functions use df and lsblk
- Process functions use ps and proc filesystem

### Universal Functions
- `get_system_info()` - Adapts to platform
- `check_process_running()` - Uses ps command
- `get_cpu_usage()` - Platform-appropriate methods

## Performance Considerations

### Memory Operations
- Functions cache results when appropriate
- Expensive operations (like disk enumeration) minimized
- Memory info gathering optimized for frequent calls

### Process Monitoring
- Efficient process checking using appropriate tools
- Minimal overhead for status checks
- Batch operations when possible

## Error Handling

### Graceful Degradation
```bash
# Handle missing tools gracefully
if ! command -v diskutil >/dev/null 2>&1; then
    echo "Warning: diskutil not available (macOS only)"
    return 1
fi
```

### Platform Detection
```bash
# Adapt to platform capabilities
if is_macos; then
    # macOS-specific implementation
elif is_linux; then
    # Linux-specific implementation
else
    echo "Unsupported platform"
    return 1
fi
```

## Security Considerations

- **Safe Command Execution**: No arbitrary command construction
- **Input Validation**: All parameters validated
- **Privilege Awareness**: Functions respect user privileges
- **Path Safety**: All file operations use validated paths

## See Also
- [Common Functions](common.md) - Core utility functions
- [System Administration Scripts](../overview.md#system-administration) - Scripts using these functions
- [Memory Purge Loop](../system/purgeLoop.md) - Automated memory management

---

*Script Location: `bash/lib/system_functions.sh`*  
*Author: Alexander Kucera / babylondreams.de*