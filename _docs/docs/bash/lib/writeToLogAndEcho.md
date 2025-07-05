# Log and Echo Utilities (writeToLogAndEcho.sh)

Simple logging utilities for writing messages to both console and log files, with flexible configuration options.

## Overview

Provides convenient functions for dual output (console + log file) and log-only output. Based on proven patterns for bash logging, enhanced with modern error handling and configuration validation.

## Functions

### `log(message)`
Writes a message to the log file only.

```bash
log "Processing started at $(date)"
```

### `message(message)`  
Writes a message to both console and log file.

```bash
message "Processing completed successfully"
```

## Usage

### As Sourced Library
```bash
#!/bin/bash
source "lib/writeToLogAndEcho.sh"

# Set log file (optional - has default)
export LOG_FILE="/var/log/myapp.log"

# Log-only message
log "Background process started"

# Console and log message
message "User action completed"
```

### As Standalone Script
```bash
# Run for demonstration
./writeToLogAndEcho.sh

# Shows example usage:
# "Echoed to console only"
# "Written to log file only"
# "To console and log"
```

## Configuration

### Environment Variables

#### `LOG_FILE`
Sets the target log file location.

```bash
export LOG_FILE="/var/log/application.log"
export LOG_FILE="${HOME}/logs/debug.log"
export LOG_FILE="./processing.log"
```

**Default**: `${HOME}/script.log` if not set

### Directory Validation
The script automatically:
- Validates the log file directory exists
- Creates parent directories if needed (when possible)
- Reports errors for invalid log locations

## Examples

### Application Logging
```bash
#!/bin/bash
source "lib/writeToLogAndEcho.sh"

export LOG_FILE="/var/log/backup.log"

message "=== Backup Process Started ==="
log "Backup configuration loaded"

for file in ~/Documents/*; do
    log "Processing: $file"
    # ... backup logic ...
done

message "=== Backup Process Completed ==="
```

### Debug Logging
```bash
#!/bin/bash
source "lib/writeToLogAndEcho.sh"

export LOG_FILE="./debug_$(date +%Y%m%d).log"

message "Debug session started"

# Verbose logging for troubleshooting
log "Variable state: INPUT_DIR=$INPUT_DIR"
log "Environment: PATH=$PATH"

message "Processing step 1"
log "Step 1: Validating inputs"
# ... processing ...

message "All steps completed"
```

### Service Integration
```bash
#!/bin/bash
# Service startup script
source "lib/writeToLogAndEcho.sh"

export LOG_FILE="/var/log/service.log"

message "Service starting up..."
log "Configuration file: $CONFIG_FILE"
log "PID: $$"

# ... service logic ...

message "Service ready - listening on port 8080"
```

## Integration Patterns

### With Error Handling
```bash
#!/bin/bash
source "lib/writeToLogAndEcho.sh"

export LOG_FILE="./operation.log"

perform_operation() {
    message "Starting critical operation"
    
    if risky_command; then
        log "Operation succeeded"
        message "✓ Critical operation completed"
    else
        log "Operation failed with exit code $?"
        message "✗ Critical operation failed"
        return 1
    fi
}
```

### With Timestamped Logs
```bash
#!/bin/bash
source "lib/writeToLogAndEcho.sh"
source "lib/common.sh"  # For get_timestamp()

export LOG_FILE="./timestamped.log"

# Enhanced logging with timestamps
timestamped_log() {
    local timestamp=$(get_timestamp)
    log "[$timestamp] $1"
}

timestamped_message() {
    local timestamp=$(get_timestamp)
    message "[$timestamp] $1"
}

# Usage
timestamped_message "Process started"
timestamped_log "Configuration loaded from config.json"
```

### Batch Processing
```bash
#!/bin/bash
source "lib/writeToLogAndEcho.sh"

export LOG_FILE="./batch_$(date +%Y%m%d_%H%M%S).log"

message "=== Batch Processing Started ==="

for item in "${items[@]}"; do
    message "Processing: $item"
    log "  - Validation: $(validate_item "$item")"
    log "  - Processing: $(process_item "$item")"
    log "  - Result: Success"
done

message "=== Batch Processing Completed ==="
```

## Best Practices

### Log File Management
1. **Descriptive Names**: Use meaningful log file names
2. **Date/Time Stamps**: Include timestamps in log filenames for rotation
3. **Appropriate Locations**: Use `/var/log/` for system services, local directories for user scripts
4. **Permissions**: Ensure write access to log directories

### Message Guidelines
1. **Log vs Message**: Use `log()` for detailed info, `message()` for user-relevant updates
2. **Clear Formatting**: Use consistent formatting for different message types
3. **Context Information**: Include relevant context (timestamps, variables, etc.)
4. **Error Details**: Log error codes and conditions for troubleshooting

### Integration Tips
1. **Early Setup**: Set LOG_FILE early in scripts
2. **Combine with Common Functions**: Use with timestamp and validation functions
3. **Error Handling**: Always check log file accessibility
4. **Cleanup**: Consider log rotation for long-running processes

## Error Handling

### Missing LOG_FILE
If `LOG_FILE` is not set, the script:
- Displays a warning
- Uses default log file (`${HOME}/script.log`)
- Continues operation normally

### Invalid Log Directory
If the log directory doesn't exist or isn't writable:
- Reports clear error message
- Exits with error code 1
- Prevents further execution

### Permission Issues
For permission-denied scenarios:
- Clear error reporting
- Guidance on fixing permissions
- Graceful script termination

## Technical Details

### Dependencies
- **Common Functions**: Uses `validate_directory()` from common.sh
- **Bash Features**: Uses standard bash I/O redirection
- **File Operations**: Safe file writing with error checking

### Based On
- Reference: http://stackoverflow.com/a/18462920
- Enhanced with modern error handling and validation
- Integrated with shared library ecosystem

### Security Considerations
- **Path Validation**: Log file paths validated before use
- **Safe Operations**: No arbitrary command execution
- **Input Sanitization**: Log messages handled safely

## See Also
- [Common Functions](common.md) - Core validation and utility functions
- [System Functions](system_functions.md) - System information for enhanced logging
- [Development Tools](../overview.md#development-tools) - Scripts using logging utilities

---

*Script Location: `bash/lib/writeToLogAndEcho.sh`*  
*Based On: http://stackoverflow.com/a/18462920*  
*Enhanced by: Alexander Kucera / babylondreams.de*