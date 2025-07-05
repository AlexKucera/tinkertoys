# Python Scripts Overview

Collection of Python utilities for file management, data processing, and workflow automation.

## Available Scripts

### File Management
- **compareFolders.py** - Directory comparison and analysis
- **fix_symlinks.py** - Symlink repair and validation
- **keepLargerVersion.py** - Intelligent file version management
- **markemptyfolders.py** - Empty directory identification

### Media & Design
- **bd_show_used_aftereffects_footage.py** - After Effects project analysis
- **convert_psd_to_exr.py** - Photoshop to EXR conversion
- **sg_thumb.py** - Thumbnail generation

### Data Processing
- **blog_post_timestamp.py** - Blog post timestamp management
- **blog_post_transform.py** - Blog content transformation
- **DayOne_split.py** - DayOne journal processing
- **exportPinboard.py** - Pinboard bookmark export
- **renderstats.py** - Render statistics analysis

### System Utilities
- **checkProjectsRaid.py** - RAID system monitoring
- **compareSizes.py** - File size comparison utilities
- **switch_paths.py** - Path switching for project management
- **timer.py** - Timing and performance utilities

### Shared Libraries
- **lib/applescript.py** - AppleScript integration
- **lib/copyFile.py** - Safe file copying utilities
- **lib/hash_for_file.py** - File hashing functions
- **lib/query_yes_no.py** - Interactive user prompts

## Architecture

The Python scripts follow a modular design with shared utilities in the `lib/` directory. Most scripts are designed for specific workflow automation tasks and include comprehensive error handling.

## Requirements

- **Python 3.6+** - Modern Python features
- **Platform-specific libraries** - Some scripts require macOS-specific functionality
- **Third-party packages** - Individual scripts may have specific dependencies

## Usage Patterns

Most Python scripts can be run directly:
```bash
python script_name.py [arguments]
```

Some scripts include command-line interfaces and help systems accessible via:
```bash
python script_name.py --help
```

---

*Note: Detailed documentation for individual Python scripts will be added as needed. Most scripts include docstrings and inline documentation.*