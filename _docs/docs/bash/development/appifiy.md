# App Builder (appifiy.sh)

Convert shell scripts into native macOS .app bundles for easier distribution and execution.

## Overview

The `appifiy.sh` script transforms any shell script into a macOS application bundle (.app), making it possible to run command-line tools through the Finder or Dock. This is particularly useful for creating user-friendly interfaces for automation scripts.

## Usage

```bash
appifiy.sh script_file.sh [app_name]
```

### Arguments

| Argument | Type | Description |
|----------|------|-------------|
| `script_file` | Required | Path to the shell script to convert |
| `app_name` | Optional | Custom name for the app (defaults to script filename) |

### Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message and exit |

## Examples

### Basic Usage
```bash
# Convert script using default name
./appifiy.sh my-script.sh

# This creates: my-script.app
```

### Custom App Name
```bash
# Convert with custom name
./appifiy.sh backup-script.sh "Backup Tool"

# This creates: Backup Tool.app
```

### Convert Utility Scripts
```bash
# Convert a log monitor into an app
./appifiy.sh checkLogSize.sh "Log Monitor"

# Convert a media processor
./appifiy.sh convert_movie_to_h264.sh "Video Converter"
```

## Features

### 🔧 Core Functionality
- **Native App Bundle Creation**: Generates proper macOS .app structure
- **Automatic Naming**: Uses script filename if no app name provided
- **Executable Setup**: Sets proper permissions for the contained script
- **Error Prevention**: Checks for existing apps to prevent overwrites

### 🛡️ Safety Features
- **Input Validation**: Verifies script file exists before processing
- **Collision Detection**: Prevents overwriting existing .app bundles
- **Path Validation**: Ensures safe file operations

### 💡 User Experience
- **Simple Interface**: Single command converts any script
- **Clear Feedback**: Reports success and final app location
- **Help System**: Comprehensive help with examples

## How It Works

The script creates a standard macOS application bundle structure:

```
MyApp.app/
├── Contents/
    └── MacOS/
        └── MyApp          # Your original script
```

1. **Validation**: Checks that the source script exists
2. **Structure Creation**: Creates the .app bundle directory structure  
3. **Script Installation**: Copies your script to the MacOS directory
4. **Permission Setup**: Makes the script executable within the bundle
5. **Verification**: Reports successful creation with full path

## Requirements

### System Requirements
- **macOS**: Required for .app bundle creation
- **Bash**: Standard bash shell
- **File System Access**: Write permissions in current directory

### Input Requirements
- **Valid Script File**: Source script must exist and be readable
- **Unique Name**: App name must not conflict with existing .app bundles

## Configuration

No configuration files required. The script operates entirely from command-line arguments.

## Output

### Success Output
```
Creating app bundle: MyScript.app
Successfully created: /full/path/to/MyScript.app
```

### Error Scenarios
- **Missing Script**: "Error: Script file 'filename.sh' does not exist"
- **Existing App**: "Error: /path/MyScript.app already exists"
- **Missing Arguments**: Shows usage information

## Integration

### With Other Scripts
```bash
# Create apps for multiple scripts
for script in *.sh; do
    ./appifiy.sh "$script"
done

# Create themed app names
./appifiy.sh video_converter.sh "🎬 Video Converter"
./appifiy.sh log_monitor.sh "📊 Log Monitor"
```

### Automation Examples
```bash
# Build distribution package
./appifiy.sh main_tool.sh "Production Tool"
./appifiy.sh setup_helper.sh "Setup Assistant"
./appifiy.sh maintenance.sh "Maintenance Utility"
```

## Best Practices

### Script Preparation
1. **Test Scripts Thoroughly**: Ensure scripts work correctly before conversion
2. **Add Help Systems**: Include `--help` functionality in your scripts
3. **Handle Paths Properly**: Use absolute paths or relative to script location
4. **Error Handling**: Implement proper error handling in source scripts

### App Naming
1. **Descriptive Names**: Use clear, descriptive app names
2. **Avoid Conflicts**: Check for existing apps before conversion
3. **Consistent Naming**: Use consistent naming patterns for related tools

### Distribution
1. **Test App Bundles**: Test created apps on clean systems
2. **Include Documentation**: Provide README files with your apps
3. **Version Control**: Track both scripts and app bundles appropriately

## Troubleshooting

### Common Issues

**App Won't Launch**
- Check original script permissions and syntax
- Verify script doesn't require specific working directory
- Test original script independently first

**Permission Denied**
- Ensure write permissions in target directory
- Check that original script is readable

**App Already Exists**
- Remove existing .app bundle or choose different name
- Use `rm -rf "AppName.app"` to remove existing bundle

## Technical Details

### Based On
- Reference implementation: https://mathiasbynens.be/notes/shell-script-mac-apps
- Enhanced with modern error handling and validation

### Security Considerations
- **Input Validation**: All file paths validated before use
- **Safe Operations**: Prevents overwriting existing files
- **Path Safety**: No arbitrary path construction or traversal

### Limitations
- **macOS Only**: App bundles only work on macOS systems
- **Simple Bundle**: Creates basic app structure without advanced features
- **No Icon Support**: Generated apps use default system icon

## See Also

- [Version Incrementer](version_up.md) - For managing app versions
- [Shared Libraries](../lib/common.md) - Common validation functions used
- [Development Tools Overview](../overview.md#development-tools) - Other development utilities

---

*Script Location: `bash/development/appifiy.sh`*  
*Author: Alexander Kucera / babylondreams.de*