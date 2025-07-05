# Common Functions Library (common.sh)

Core utility functions providing validation, timestamps, logging, and cross-platform compatibility for all bash scripts.

## Overview

The common functions library provides essential utilities used across all bash scripts, including input validation, timestamp generation, logging capabilities, and platform detection. This library ensures consistent behavior and reduces code duplication.

## Key Functions

### Validation Functions

#### `validate_file()`
```bash
validate_file "path/to/file" "description"
```
Validates that a file exists and is readable.

- **Parameters**: file_path, description
- **Returns**: 0 if valid, 1 if invalid
- **Features**: Comprehensive error reporting, path safety checks

#### `validate_directory()`
```bash
validate_directory "path/to/dir" "description"
```
Validates that a directory exists and is accessible.

- **Parameters**: directory_path, description
- **Returns**: 0 if valid, 1 if invalid
- **Features**: Permission checking, clear error messages

#### `validate_command()`
```bash
validate_command "ffmpeg" "FFmpeg"
```
Validates that a command is available in the system PATH.

- **Parameters**: command_name, display_name
- **Returns**: 0 if available, 1 if missing
- **Features**: Installation guidance, dependency checking

### Timestamp Functions

#### `get_timestamp()`
```bash
timestamp=$(get_timestamp)
```
Generates formatted timestamps for logging and reporting.

- **Returns**: Formatted timestamp string
- **Format**: "Monday, 05.07.2025 13:45:30"
- **Cross-platform**: Works on macOS and Linux

#### `calculate_duration()`
```bash
duration=$(calculate_duration "$start_time" "$end_time")
```
Calculates formatted duration between two timestamps.

- **Parameters**: start_epoch, end_epoch
- **Returns**: Formatted duration (e.g., "2h:35m:42s")
- **Features**: Human-readable format, zero-padding

### Logging Functions

#### `log_message()`
```bash
log_message "Important event occurred" "app.log"
```
Writes timestamped messages to log files.

- **Parameters**: message, log_filename
- **Features**: Automatic timestamping, safe file operations
- **Location**: Logs written to current directory

### Utility Functions

#### `get_script_dir()`
```bash
script_directory=$(get_script_dir)
```
Returns the directory containing the calling script.

- **Returns**: Absolute path to script directory
- **Use Cases**: Relative path resolution, resource location

#### `parse_filename()`
```bash
parse_filename "/path/to/file.ext" basename extension
```
Safely parses filename components.

- **Parameters**: filepath, basename_var, extension_var
- **Features**: Extension extraction, path handling

### Platform Detection

#### `is_macos()`
```bash
if is_macos; then
    echo "Running on macOS"
fi
```
Detects macOS platform for platform-specific operations.

- **Returns**: 0 if macOS, 1 if other platform
- **Use Cases**: Platform-specific command selection

#### `is_linux()`
```bash
if is_linux; then
    echo "Running on Linux"
fi
```
Detects Linux platform.

- **Returns**: 0 if Linux, 1 if other platform

## Usage Examples

### Basic Validation
```bash
#!/bin/bash
source "lib/common.sh"

# Validate input file
if ! validate_file "$1" "input video"; then
    exit 1
fi

# Validate output directory
if ! validate_directory "$OUTPUT_DIR" "output directory"; then
    exit 1
fi
```

### Logging with Timestamps
```bash
#!/bin/bash
source "lib/common.sh"

LOG_FILE="processing.log"

log_message "Processing started" "$LOG_FILE"
# ... processing work ...
log_message "Processing completed successfully" "$LOG_FILE"
```

### Duration Tracking
```bash
#!/bin/bash
source "lib/common.sh"

START_TIME="$(date +%s)"
echo "Started at: $(get_timestamp)"

# ... long running process ...

END_TIME="$(date +%s)"
DURATION="$(calculate_duration "$START_TIME" "$END_TIME")"
echo "Completed in: $DURATION"
```

### Cross-Platform Operations
```bash
#!/bin/bash
source "lib/common.sh"

if is_macos; then
    OPEN_CMD="open"
    DATE_CMD="date -j"
elif is_linux; then
    OPEN_CMD="xdg-open"
    DATE_CMD="date"
else
    echo "Unsupported platform"
    exit 1
fi
```

## Error Handling

All functions provide comprehensive error handling:

- **Input Validation**: Parameters checked before use
- **Error Reporting**: Clear, descriptive error messages
- **Safe Defaults**: Graceful handling of missing parameters
- **Return Codes**: Consistent 0/1 return codes for scripting

## Security Features

- **Path Validation**: All file paths validated for safety
- **No Arbitrary Execution**: No dynamic command construction
- **Input Sanitization**: All inputs sanitized before use
- **Safe File Operations**: Atomic file operations where possible

## Integration

### Library Loading
```bash
# Standard library loading pattern
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../lib/common.sh"
```

### Function Dependencies
Some functions depend on others:
- `log_message()` uses `get_timestamp()`
- `calculate_duration()` uses cross-platform date handling
- All validation functions use consistent error reporting

## Best Practices

### Function Usage
1. **Always Check Return Codes**: Use return codes for error handling
2. **Provide Descriptions**: Use descriptive names in validation calls
3. **Log Important Events**: Use logging for audit trails
4. **Handle Platform Differences**: Use platform detection appropriately

### Error Handling
1. **Validate Early**: Check inputs before processing
2. **Fail Fast**: Exit on validation errors
3. **Clear Messages**: Provide helpful error descriptions
4. **Consistent Patterns**: Use similar error handling across scripts

## See Also
- [Media Functions](media_functions.md) - Media-specific utilities
- [System Functions](system_functions.md) - System information functions
- [Bash Scripts Overview](../overview.md) - Integration patterns

---

*Script Location: `bash/lib/common.sh`*  
*Author: Alexander Kucera / babylondreams.de*