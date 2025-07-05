# Application List Updater (application_list_updater.sh)

Generate comprehensive lists of installed applications for backup and restoration purposes.

## Overview

Creates detailed inventories of all installed applications on macOS systems, including system applications, user applications, Homebrew packages, and App Store applications. Essential for system migration, backup planning, and software auditing.

## Usage

```bash
application_list_updater.sh [output_file]
```

### Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `output_file` | Optional | Path for output file | ~/Documents/ApplicationList.txt |

## Features

- **Complete Coverage**: Lists applications from multiple sources
- **Organized Output**: Categorizes applications by installation method
- **Homebrew Integration**: Includes both packages and casks
- **App Store Detection**: Identifies Mac App Store applications
- **Timestamp Tracking**: Includes generation date for reference

## Application Sources

| Category | Location | Description |
|----------|----------|-------------|
| System Apps | /Applications | Standard macOS applications |
| User Apps | ~/Applications | User-specific applications |
| Homebrew Packages | brew list | Command-line tools and libraries |
| Homebrew Casks | brew list --cask | GUI applications installed via Homebrew |
| App Store | mas list | Mac App Store applications |

## Examples

```bash
# Generate default application list
./application_list_updater.sh

# Custom output location
./application_list_updater.sh ~/Backups/apps_$(date +%Y%m%d).txt

# Store in project directory
./application_list_updater.sh ./system_apps.txt
```

## Output Format

```
Application List - Generated Mon Jul  5 13:30:00 CEST 2025
==================================================

This file lists all installed applications for restoration purposes.
Note: Actual applications are not backed up, only their names.

=== SYSTEM APPLICATIONS ===
Activity Monitor
App Store
Calculator
Calendar
...

=== HOMEBREW PACKAGES ===
ffmpeg
git
node
...

=== HOMEBREW CASKS ===
visual-studio-code
chrome
firefox
...

=== MAC APP STORE APPLICATIONS ===
Xcode (497799835)
Pages (409201541)
...
```

## Integration

### Backup Workflows
```bash
#!/bin/bash
# System backup script
BACKUP_DATE=$(date +%Y%m%d)
BACKUP_DIR="~/Backups/$BACKUP_DATE"

mkdir -p "$BACKUP_DIR"
./application_list_updater.sh "$BACKUP_DIR/applications.txt"
```

### System Migration
```bash
# Pre-migration inventory
./application_list_updater.sh ~/Desktop/old_system_apps.txt

# Post-migration comparison
./application_list_updater.sh ~/Desktop/new_system_apps.txt
diff ~/Desktop/old_system_apps.txt ~/Desktop/new_system_apps.txt
```

## See Also
- [System Functions](../lib/system_functions.md) - System information utilities
- [System Administration Overview](../overview.md#system-administration) - Related tools

---

*Script Location: `bash/system/application_list_updater.sh`*  
*Author: Alexander Kucera / babylondreams.de*