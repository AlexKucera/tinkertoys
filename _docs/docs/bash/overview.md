# Bash Scripts Overview

The bash scripts collection provides comprehensive automation tools for development, media processing, system administration, and rendering workflows. All scripts have been modernized with proper error handling, security best practices, and shared library integration.

## Script Categories

### 🔧 Development Tools
Development utilities for app creation, version management, and project maintenance.

| Script | Purpose | Key Features |
|--------|---------|--------------|
| [appifiy.sh](development/appifiy.md) | Convert shell scripts to macOS apps | Creates .app bundles, custom naming |
| [comparefolders.sh](development/comparefolders.md) | Compare two directories | Recursive comparison, difference reporting |
| [fixImgExt.sh](development/fixImgExt.md) | Fix image file extensions | Content-based detection, batch processing |
| [version_up.sh](development/version_up.md) | Increment version numbers | Semantic versioning, history tracking |

### 🎥 Media Processing
Professional-grade media conversion and processing tools with optimized settings.

| Script | Purpose | Key Features |
|--------|---------|--------------|
| [convert_images_to_h264.sh](media/convert_images_to_h264.md) | Convert image sequences to H.264 | Configurable quality, bitrate guidelines |
| [convert_images_to_prores.sh](media/convert_images_to_prores.md) | Convert image sequences to ProRes | Multiple ProRes formats, high quality |
| [convert_movie_to_h264.sh](media/convert_movie_to_h264.md) | Convert movies to H.264 | Optimized compression, format flexibility |
| [convert_movie_to_prores.sh](media/convert_movie_to_prores.md) | Convert movies to ProRes | Professional codecs, configurable quality |
| [movie_to_web.sh](media/movie_to_web.md) | Convert movies for web | MP4 + WebM output, web optimization |
| [split_stereo_to_mono.sh](media/split_stereo_to_mono.md) | Split stereo audio to mono | Apple Lossless output, channel separation |

### ⚙️ System Administration
Tools for system monitoring, application management, and maintenance automation.

| Script | Purpose | Key Features |
|--------|---------|--------------|
| [application_list_updater.sh](system/application_list_updater.md) | Track installed applications | Homebrew integration, backup lists |
| [checkLogSize.sh](system/checkLogSize.md) | Monitor log file sizes | Configurable limits, automation-ready |
| [getDiskDevice.sh](system/getDiskDevice.md) | Find disk devices by label | Label-based lookup, device identification |
| [purgeLoop.sh](system/purgeLoop.md) | Automated memory purging | Intelligent thresholds, continuous monitoring |
| [log_collector.sh](system/log_collector.md) | Advanced log collection | Category filtering, time-based queries |

### 🎬 Rendering Tools
Automation and notification tools for rendering workflows.

| Script | Purpose | Key Features |
|--------|---------|--------------|
| [mail_send.sh](rendering/mail_send.md) | Email notifications for renders | Timing tracking, completion alerts |
| [nukerender_bash.sh](rendering/nukerender_bash.md) | Automated Nuke rendering | Interactive setup, email integration |

### 📚 Shared Libraries
Reusable function libraries that provide common functionality across all scripts.

| Library | Purpose | Key Functions |
|---------|---------|---------------|
| [common.sh](lib/common.md) | Core utility functions | Validation, timestamps, logging |
| [media_functions.sh](lib/media_functions.md) | Media processing utilities | Codec setup, format validation |
| [system_functions.sh](lib/system_functions.md) | System information functions | Memory info, platform detection |
| [writeToLogAndEcho.sh](lib/writeToLogAndEcho.md) | Logging utilities | Console + file output, message handling |

## Common Features

### Security & Safety
- **Input Validation**: All user inputs are validated and sanitized
- **Path Protection**: Protection against path traversal attacks
- **No Hardcoded Secrets**: All credentials use environment variables
- **Error Handling**: Comprehensive error handling with `set -euo pipefail`

### User Experience
- **Standardized Help**: All scripts support `-h` and `--help` flags
- **Consistent Interface**: Unified argument and option patterns
- **Progress Feedback**: Clear status messages and progress indicators
- **Error Messages**: Helpful error messages with troubleshooting guidance

### Quality Assurance
- **Syntax Validation**: All scripts validated for correct bash syntax
- **Shared Libraries**: Common functionality extracted to reusable modules
- **Testing**: Comprehensive test suite validates all functionality
- **Documentation**: Complete documentation following MkDocs standards

## Usage Patterns

### Getting Help
Every script provides comprehensive help:
```bash
script_name.sh --help
```

### Common Options
Most scripts support these standard patterns:
- `-h, --help`: Show help information
- Input validation with clear error messages
- Configuration via environment variables where appropriate
- Progress feedback and status reporting

### Environment Variables
Scripts use environment variables for configuration:
- `MAIL_PASSWORD`: Email notification password
- `NUKEPATH`: Path to Nuke executable
- `LOG_FILE`: Custom log file location (for logging utilities)

## Integration

### Shared Libraries
Scripts automatically source required shared libraries:
```bash
source "${SCRIPT_DIR}/../lib/common.sh"
source "${SCRIPT_DIR}/../lib/media_functions.sh"  # Media scripts
source "${SCRIPT_DIR}/../lib/system_functions.sh" # System scripts
```

### Configuration Files
Centralized configuration in `config/` directory:
- `mail_send.conf`: Email notification settings
- `log_sources.conf`: Log collection source definitions

### Testing
Comprehensive test suite available:
```bash
# Run all tests
./test_all_scripts.sh

# Quick validation
./quick_test.sh

# Full validation with logging
./final_validation.sh
```

## Architecture

The bash scripts follow a consistent architecture pattern:

1. **Header & Metadata**: Script purpose, author, requirements
2. **Library Integration**: Source shared libraries as needed
3. **Help System**: Standardized help function and argument parsing
4. **Input Validation**: Validate all arguments and file paths
5. **Main Logic**: Core functionality with error handling
6. **Output & Cleanup**: Status reporting and temporary file cleanup

This organization ensures maintainability, security, and consistent user experience across all scripts.