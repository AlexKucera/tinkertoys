# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a collection of utility scripts and automation tools ("tinkertoys") for various development and system administration tasks. The repository contains scripts in multiple languages (Bash, Python, Ruby) organized by language and purpose.

## Repository Structure

- `bash/` - Shell scripts for system administration, build automation, and media processing
- `python/` - Python utilities for file management, rendering stats, and data processing
- `ruby/` - Ruby scripts for task management integration
- `php/` - PHP utilities (minimal)

## Key Components

### Bash Scripts (`bash/`)
- **Log Collection System**: `log_collector/` contains a configurable log monitoring tool
  - `log_collector.sh` - Main script with extensive options for filtering and displaying logs
  - `log_sources.conf` - Configuration file defining log sources by category
- **Media Processing**: Scripts for video/image conversion (`convert_*.sh`)
- **System Utilities**: Various automation tools for macOS and development workflows
- **Application Management**: `appifiy.sh` for converting shell scripts to macOS apps

### Python Utilities (`python/`)
- **Render Statistics**: `renderstats.py` - Analyzes render times and frame sequences
- **File Management**: Scripts for comparing folders, managing symlinks, and file operations
- **Shared Library**: `lib/` directory contains reusable modules
  - `applescript.py` - Wrapper for running AppleScript from Python
  - `copyFile.py`, `hash_for_file.py`, `query_yes_no.py` - Common utilities

### Script Categories
- **Rendering/Media**: Scripts for 3D rendering (Maya, Nuke, Modo), video conversion
- **System Admin**: Azure VM management, application lists, environment setup
- **Development**: Build automation, path switching, version management

## Common Development Tasks

Since this is a collection of standalone scripts, there are no build or test commands. Each script is self-contained and executable.

### Running Scripts
- Bash scripts: `./script_name.sh [arguments]`
- Python scripts: `python script_name.py [arguments]`
- Most scripts include help via `--help` or `-h` flags

### Log Collector Usage
The log collector is the most complex tool in the repository:
```bash
cd bash/log_collector
./log_collector.sh --help                    # Show usage
./log_collector.sh --create-config          # Create example config
./log_collector.sh -t 10 -l 20              # Last 10 minutes, 20 lines each
```

## Architecture Notes

- **Self-contained**: Each script is designed to work independently
- **Cross-platform considerations**: Some scripts are macOS-specific (using AppleScript, Automator)
- **Configuration-driven**: Several scripts use external config files (like log_collector)
- **Legacy Python**: Some scripts use Python 2.7 syntax (older codebase)
- **Modular design**: Python scripts leverage shared utilities in the `lib/` directory

## File Conventions

- Scripts include author attribution (Alexander Kucera / babylondreams.de)
- Many scripts have embedded documentation and usage examples
- Configuration files use pipe-delimited format for structured data
- Scripts often include error handling and validation

## Important Notes

- This is a personal collection of tools - many paths and configurations are specific to the author's environment
- Some scripts reference external systems (Azure, specific file paths)
- The codebase mixes different Python versions and coding styles as it evolved over time
- Several scripts are designed for specific 3D rendering and media production workflows