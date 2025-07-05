# Version Incrementer (version_up.sh)

Automatically increment version numbers in version files with timestamp tracking and history maintenance.

## Overview

The `version_up.sh` script provides automated version number management for projects. It intelligently increments semantic version numbers, maintains version history with timestamps, and creates new version files when needed. Perfect for release automation and project version tracking.

## Usage

```bash
version_up.sh [version_file]
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `version_file` | Optional | Path to version file (default: `version.txt`) |

### Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message and exit |

## Examples

### Basic Usage
```bash
# Increment version in default version.txt file
./version_up.sh

# Increment version in custom file
./version_up.sh my_version.txt

# Increment project-specific version
./version_up.sh ~/Projects/myapp/VERSION
```

### Development Workflow
```bash
# Pre-release version bump
./version_up.sh src/version.txt

# Build automation integration
./version_up.sh && make build

# Multiple project management
./version_up.sh frontend/version.txt
./version_up.sh backend/version.txt
./version_up.sh api/version.txt
```

### Automation Scripts
```bash
#!/bin/bash
# Release preparation script
./version_up.sh
NEW_VERSION=$(head -n 1 version.txt | cut -d' ' -f1)
echo "Building release $NEW_VERSION"
git add version.txt
git commit -m "Bump version to $NEW_VERSION"
git tag "v$NEW_VERSION"
```

## Features

### 🔢 Smart Version Management
- **Semantic Versioning**: Supports standard major.minor.patch format
- **Intelligent Incrementing**: Automatically increments the patch number
- **Flexible Formats**: Handles various version number formats
- **History Preservation**: Maintains complete version history

### 📅 Timestamp Tracking
- **Automatic Dating**: Adds timestamp to each version entry
- **ISO Format**: Uses standard YYYY-MM-DD date format
- **History Maintenance**: Keeps chronological record of all versions
- **Audit Trail**: Complete history of when versions were created

### 🛡️ Safety Features
- **Format Validation**: Validates version format before processing
- **File Creation**: Creates new version file if none exists
- **Backup Preservation**: Maintains existing version history
- **Input Validation**: Comprehensive validation of version formats

## Version Format Support

### Supported Formats
- `1.0.0` - Standard semantic versioning
- `2.15.3` - Major.minor.patch
- `0.1.0` - Pre-release versions
- `10.20.30` - Large version numbers

### Version Increment Logic
```
1.0.0 → 1.0.1
1.2.9 → 1.2.10
9.9.9 → 9.9.10
```

The script automatically handles:
- **Carry Logic**: Proper handling of digit overflow
- **Leading Zeros**: Maintains consistent formatting
- **Patch Increment**: Always increments the rightmost number

## How It Works

### Version Processing
1. **File Validation**: Checks if version file exists, creates if needed
2. **Format Parsing**: Reads and validates current version format
3. **Increment Calculation**: Applies smart increment logic
4. **Timestamp Addition**: Adds current date to new version
5. **History Update**: Prepends new version to history
6. **File Writing**: Saves updated version file

### Default Initialization
If no version file exists, creates one with:
```
1.0.0 - 2025-07-05
```

## File Format

### Version File Structure
```
1.2.1 - 2025-07-05
1.2.0 - 2025-07-01
1.1.9 - 2025-06-28
1.1.8 - 2025-06-25
```

Each line contains:
- **Version Number**: Semantic version in major.minor.patch format
- **Separator**: ` - ` (space-dash-space)
- **Date**: ISO format date (YYYY-MM-DD)

## Output Examples

### Successful Execution
```bash
Version incrementer working in: /Users/alex/Projects/myapp
Current version: 1.2.0
New version: 1.2.1
Date stamp: - 2025-07-05
✓ Version updated successfully!
Version file updated: version.txt

Updated version history:
  1.2.1 - 2025-07-05
  1.2.0 - 2025-07-01
  1.1.9 - 2025-06-28
  1.1.8 - 2025-06-25
  1.1.7 - 2025-06-20
```

### New File Creation
```bash
Version incrementer working in: /Users/alex/Projects/newapp
Creating new version file with initial version 1.0.0
Current version: 1.0.0
New version: 1.0.1
✓ Version updated successfully!
```

## Configuration

### Environment Variables
No environment variables required. All configuration through file paths.

### Working Directory
- Script operates in the directory where it's executed
- Version files created/updated relative to current directory
- Reports working directory for confirmation

## Integration

### Build Automation
```bash
# Makefile integration
version:
	./version_up.sh
	@echo "New version: $$(head -n 1 version.txt | cut -d' ' -f1)"

release: version
	@echo "Building release..."
	# Build commands here
```

### Git Workflows
```bash
#!/bin/bash
# Git release workflow
./version_up.sh
VERSION=$(head -n 1 version.txt | cut -d' ' -f1)

git add version.txt
git commit -m "Bump version to $VERSION"
git tag "v$VERSION"
git push origin main --tags
```

### CI/CD Integration
```bash
# GitHub Actions / CI integration
- name: Increment Version
  run: |
    ./version_up.sh
    echo "NEW_VERSION=$(head -n 1 version.txt | cut -d' ' -f1)" >> $GITHUB_ENV

- name: Create Release
  run: |
    echo "Creating release for version $NEW_VERSION"
```

### Multi-Project Management
```bash
#!/bin/bash
# Update versions across multiple projects
PROJECTS=("frontend" "backend" "api" "docs")

for project in "${PROJECTS[@]}"; do
    echo "Updating $project version..."
    ./version_up.sh "$project/version.txt"
done
```

## Best Practices

### Version File Management
1. **Consistent Location**: Keep version files in predictable locations
2. **Version Control**: Always commit version file changes
3. **Backup Strategy**: Ensure version files are backed up
4. **Documentation**: Document version increment policies

### Release Workflows
1. **Pre-Release Testing**: Test thoroughly before version increment
2. **Atomic Operations**: Combine version increment with related tasks
3. **Tag Creation**: Create git tags for version milestones
4. **Changelog Updates**: Update changelogs alongside version increments

### Automation Guidelines
1. **Script Integration**: Integrate with build and release scripts
2. **Error Handling**: Handle version increment failures gracefully
3. **Validation**: Verify version format before automated increments
4. **Logging**: Log version changes for audit purposes

## Error Handling

### Input Validation
- **File Format**: Validates version file format before processing
- **Version Format**: Ensures version follows expected pattern
- **File Permissions**: Checks write access to version file
- **Directory Access**: Validates working directory access

### Error Scenarios
- **Invalid Format**: "Invalid version format in version.txt: 'bad-format'"
- **Permission Denied**: "Failed to update version file"
- **Missing Directory**: Script reports working directory and creates files appropriately

## Troubleshooting

### Version Format Issues
- Ensure version follows major.minor.patch format
- Check for extra characters or spaces in version file
- Verify file encoding (should be plain text)

### File Permission Problems
- Check write permissions on version file and directory
- Ensure version file is not locked by other applications
- Verify disk space for file updates

### Integration Issues
- Test version increment manually before automation
- Verify file paths in automated scripts
- Check that working directory is correct

## Technical Details

### Dependencies
- **bash**: Modern bash shell
- **date**: Standard Unix date command
- **Shared Libraries**: Uses common.sh for utility functions

### Algorithm Details
```bash
# Version increment logic (simplified)
declare -a part=( ${version//\./ } )  # Split by dots
declare -i carry=1

for (( CNTR=${#part[@]}-1; CNTR>=0; CNTR-=1 )); do
    new=$((part[CNTR]+carry))
    # Handle overflow and carry logic
done
```

### Security Considerations
- **Path Validation**: All file paths validated before use
- **Safe File Operations**: Atomic file operations where possible
- **Input Sanitization**: Version format strictly validated

## See Also

- [App Builder](appifiy.md) - Create apps with version management
- [Common Functions](../lib/common.md) - Shared utility functions
- [Development Tools Overview](../overview.md#development-tools) - Related development utilities

---

*Script Location: `bash/development/version_up.sh`*  
*Author: Alexander Kucera / babylondreams.de*