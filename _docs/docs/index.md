# Tinkertoys Documentation

Welcome to the comprehensive documentation for the Tinkertoys utility scripts collection. This repository contains a carefully curated set of automation tools, development utilities, and system administration scripts designed to streamline workflows and improve productivity.

## Overview

Tinkertoys is a collection of utility scripts and automation tools organized by programming language and purpose. The repository includes:

- **Bash Scripts**: System administration, media processing, development tools, and rendering automation
- **Python Scripts**: Data processing, media conversion, system utilities, and macOS integration
- **Configuration Files**: Centralized settings for various tools and services

## Quick Start

### Prerequisites

- **macOS**: Most scripts are designed for macOS (some may work on Linux)
- **Bash 4.0+**: Modern bash shell for script execution
- **FFmpeg**: Required for media processing scripts
- **Python 3.11+**: For Python utilities (modernized from Python 2.7)

### Installation

1. Clone or download the repository
2. Set up configuration files in the `config/` directory
3. Install required dependencies based on the scripts you plan to use
4. Make scripts executable: `chmod +x script_name.sh`

## Key Features

### 🔧 Development Tools
- **App Builder** (Bash): Convert shell scripts to macOS applications
- **Version Management** (Bash): Automated version number incrementing
- **Folder Comparison** (Bash/Python): Compare directories for differences
- **Image Extension Fixing** (Bash): Automatically correct file extensions
- **Timer Utility** (Python): Advanced timing and stopwatch functionality
- **Git Empty Folder Marker** (Python): Manage .gitkeep files in repositories

### 🎥 Media Processing
- **Video Transcoding** (Bash): Convert videos to H.264, ProRes, and web formats
- **Image Sequence Processing** (Bash): Convert image sequences to video
- **Audio Processing** (Bash): Split stereo audio to mono channels
- **PSD to EXR Converter** (Python): Convert Photoshop files to EXR format
- **Render Statistics** (Python): Analyze render times and frame sequences

### ⚙️ System Administration
- **Application Management** (Bash): Track installed applications for backup
- **Log Monitoring** (Bash): Automated log size checking and collection
- **Memory Management** (Bash): Intelligent memory purging for macOS
- **Disk Management** (Bash): Find disk devices by label
- **File Size Comparison** (Python): Compare file sizes and detect corruption
- **Symlink Repair** (Python): Fix broken symbolic links
- **Duplicate File Manager** (Python): Remove duplicate files keeping larger versions
- **Path Replacement** (Python): Bulk path updates with JSON configuration

### 🎬 Rendering Tools
- **Email Notifications** (Bash): Automated notifications for completed renders
- **Nuke Integration** (Bash): Streamlined Nuke rendering with progress tracking

### 📊 Data Processing
- **DayOne Journal Splitter** (Python): Split DayOne exports into individual files
- **Pinboard Export** (Python): Backup Pinboard bookmarks

### 📚 Shared Libraries
- **Common Functions** (Bash): Reusable validation and utility functions
- **Media Functions** (Bash): Specialized video/audio processing utilities
- **System Functions** (Bash): Cross-platform system information and management
- **AppleScript Integration** (Python): Modern macOS automation with error handling
- **File Copying Utilities** (Python): High-performance file operations with progress tracking
- **Hash Calculation** (Python): Optimized file hashing with multiple algorithms
- **Interactive Prompts** (Python): Enhanced user interaction utilities

## Architecture

### Security & Best Practices
- **No Hardcoded Credentials**: All sensitive data uses environment variables
- **Input Validation**: Comprehensive validation of all user inputs
- **Error Handling**: Proper error handling with `set -euo pipefail`
- **Path Safety**: Protection against path traversal attacks

### Code Organization
- **Modular Design**: Scripts organized by functional category
- **Shared Libraries**: Common functionality extracted to reusable modules
- **Consistent Interface**: Standardized help system across all scripts
- **Configuration Management**: Centralized configuration files

### Quality Assurance
- **Comprehensive Testing**: Automated test suite for all scripts
- **Syntax Validation**: All scripts validated for proper bash syntax
- **Functionality Testing**: Safe functional testing of key operations
- **Integration Testing**: Validation of shared library integration

## Getting Help

Each script includes comprehensive help documentation accessible via:

```bash
script_name.sh --help
# or
script_name.sh -h
```

For detailed documentation on specific scripts, see the navigation menu or browse the individual script documentation pages.

## Contributing

When contributing to this repository:

1. Follow existing code style and organization patterns
2. Include comprehensive help documentation in all scripts
3. Add appropriate error handling and input validation
4. Update documentation for any new features or changes
5. Test scripts thoroughly before submission

## License

This project is maintained by Alexander Kucera / babylondreams.de. Individual scripts may have specific licensing terms - please check script headers for details.

## Support

For issues, questions, or contributions, please refer to the individual script documentation or contact the maintainer.

---

*Last updated: July 2025*