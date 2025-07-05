# Nuke Render Automation (nukerender_bash.sh)

Automated Nuke rendering with interactive configuration, email notifications, and comprehensive error handling.

## Overview

Professional Nuke rendering automation that provides interactive setup for render options, automatic email notifications, and detailed progress tracking. Designed for production environments where reliable render execution and notification are critical.

## Usage

```bash
nukerender_bash.sh <nuke_script> [output_path]
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `nuke_script` | Required | Path to Nuke script file (.nk) |
| `output_path` | Optional | Output path for rendered files |

## Interactive Configuration

The script prompts for render settings:

1. **Render Range**: Custom frame range (e.g., `-F 12-13`) or comp default
2. **GPU Usage**: Enable/disable GPU acceleration
3. **Interactive License**: Required for Furnace tools and certain plugins

## Features

### 🎬 Render Management
- **Frame Range Control**: Custom ranges or script defaults
- **GPU Acceleration**: Optional GPU rendering support
- **Interactive Licensing**: Support for Furnace and commercial plugins
- **Multi-core Utilization**: Automatic CPU core detection and usage

### 📧 Notification System
- **Email Integration**: Automatic completion notifications
- **Timing Tracking**: Detailed start/end times and duration
- **Machine Identification**: Hostname included in notifications
- **Error Reporting**: Failed renders reported via email

### 🛡️ Safety Features
- **Input Validation**: Comprehensive script and path validation
- **Environment Checks**: Validates Nuke installation and paths
- **Error Handling**: Graceful handling of render failures
- **Configuration Validation**: Checks email and system setup

## Environment Setup

### Required Environment Variables
```bash
export NUKEPATH="/Applications/Nuke/Nuke15.0v4/Nuke15.0v4"
export MAIL_PASSWORD="your_smtp_password"
```

### Configuration Files
- `config/mail_send.conf`: Email notification settings

## Examples

### Basic Rendering
```bash
# Render with interactive setup
./nukerender_bash.sh shot_001.nk

# Render to specific output location
./nukerender_bash.sh shot_001.nk /renders/shot_001/
```

### Production Workflows
```bash
#!/bin/bash
# Batch render script
for script in shots/*.nk; do
    echo "Rendering: $script"
    ./nukerender_bash.sh "$script"
    
    if [[ $? -eq 0 ]]; then
        echo "✓ $script completed successfully"
    else
        echo "✗ $script failed"
        # Continue with next script
    fi
done
```

## Render Command Examples

The script provides helpful command-line examples:

```bash
# Render specific frame
nuke -F 5 -x myscript.nk

# Render frame range
nuke -F 30-50 -x myscript.nk

# Multiple ranges
nuke -F 10-20 -F 34-60 -x myscript.nk

# Every tenth frame
nuke -F 1-50x10 -x myscript.nk

# Specific write node
nuke -X WriteBlur myscript.nk 1-20
```

## Notification Content

Email notifications include:
- **Machine Hostname**: Which system completed the render
- **Script Name**: Nuke script that was rendered
- **Start/End Times**: Complete timing information
- **Total Duration**: Formatted as hours:minutes:seconds
- **Render Settings**: GPU usage, frame range, license type

## Error Handling

### Common Issues
- **Missing Nuke Path**: Validates NUKEPATH environment variable
- **Script Validation**: Checks Nuke script exists and is readable
- **Email Configuration**: Validates mail settings before render
- **Render Failures**: Captures and reports Nuke errors

### Troubleshooting
- **Permission Issues**: Ensure script has execute permissions
- **Network Problems**: Check email server connectivity
- **Nuke Licensing**: Verify appropriate Nuke licenses available
- **Path Issues**: Use absolute paths for reliability

## Integration

### Farm Rendering
```bash
# Render farm integration
export NUKEPATH="/path/to/nuke"
export MAIL_PASSWORD="$RENDER_FARM_MAIL_PASS"

./nukerender_bash.sh "$SHOT_SCRIPT" "$RENDER_OUTPUT"
```

### CI/CD Pipelines
```bash
# Automated rendering in pipelines
if ./nukerender_bash.sh daily_comp.nk /output/; then
    echo "Daily render completed"
    deploy_to_review_system
else
    echo "Daily render failed"
    alert_team
fi
```

## Requirements

### Software Dependencies
- **Nuke**: Foundry Nuke with command-line support
- **sendemail**: For email notifications
- **Network Access**: For email delivery

### System Requirements
- **macOS/Linux**: Unix-like operating system
- **Sufficient RAM**: Based on Nuke script complexity
- **Disk Space**: For rendered output files

## See Also
- [Mail Notifications](mail_send.md) - Email notification setup
- [System Functions](../lib/system_functions.md) - System information utilities
- [Mail Configuration](../../config/mail_send.md) - Email setup details

---

*Script Location: `bash/rendering/nukerender_bash.sh`*  
*Author: Alexander Kucera / babylondreams.de*