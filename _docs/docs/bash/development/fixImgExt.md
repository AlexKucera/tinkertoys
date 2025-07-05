# Image Extension Fixer (fixImgExt.sh)

Automatically correct image file extensions based on actual file content rather than current extension.

## Overview

The `fixImgExt.sh` script analyzes image files to determine their true format and corrects file extensions accordingly. This is particularly useful for fixing incorrectly named files, batch processing image collections, and ensuring accurate file type identification.

## Usage

```bash
fixImgExt.sh [OPTIONS]
```

### Options

| Option | Parameter | Description |
|--------|-----------|-------------|
| `-f` | FILE | Process a single file with file path |
| `-d` | DIRECTORY | Process all files in the specified directory |
| `-r` | | Use with `-d` to process directories recursively |
| `-s` | | Show detailed information for each file processed |
| `-v` | | Log corrected files to `fixImgExt_info.txt` |
| `-h` | | Show help message and exit |

## Examples

### Single File Processing
```bash
# Fix extension for a single image
./fixImgExt.sh -f /path/to/image.wrong

# Fix with detailed output
./fixImgExt.sh -f -s /path/to/image.jpg
```

### Directory Processing
```bash
# Fix all images in a directory
./fixImgExt.sh -d /path/to/images/

# Process recursively with logging
./fixImgExt.sh -d -r -v /path/to/image_collection/

# Detailed processing with verbose output
./fixImgExt.sh -d -s -v /Users/alex/Pictures/
```

### Batch Operations
```bash
# Process camera imports (often have generic extensions)
./fixImgExt.sh -d -r -v ~/Pictures/Camera_Import/

# Fix web downloads (may have incorrect extensions)
./fixImgExt.sh -d -s ~/Downloads/images/

# Process design project files
./fixImgExt.sh -d -r -v ~/Projects/design_assets/
```

## Features

### 🔍 Content-Based Detection
- **True Format Recognition**: Uses `file` command to detect actual image format
- **Extension Correction**: Matches file extension to actual content
- **Format Support**: Supports major image formats (JPEG, PNG, GIF, TIFF, BMP, etc.)
- **Professional Formats**: Handles PSD, XCF, SVG, and WebM files

### 🛡️ Safety Features
- **Collision Prevention**: Avoids overwriting existing files
- **Incremental Naming**: Uses `filename_0.ext`, `filename_1.ext` for conflicts
- **Path Validation**: Prevents path traversal attacks
- **Backup Logging**: Optional logging of all changes made

### 📊 Detailed Reporting
- **Progress Feedback**: Shows what files are being processed
- **Change Logging**: Optional logging to `fixImgExt_info.txt`
- **Detailed View**: Optional verbose output showing file analysis
- **Statistics**: Reports successful corrections and any issues

## Supported Formats

| Format | Extensions | Description |
|--------|------------|-------------|
| JPEG | `.jpeg`, `.jpg` | Standard photo format |
| PNG | `.png` | Lossless web format |
| GIF | `.gif` | Animated/web graphics |
| TIFF | `.tif`, `.tiff` | Professional/print format |
| BMP | `.bmp` | Windows bitmap |
| PSD | `.psd` | Adobe Photoshop |
| XCF | `.xcf` | GIMP native format |
| SVG | `.svg` | Vector graphics |
| WebM | `.webm` | Web video/animation |

## How It Works

### File Analysis Process
1. **Input Validation**: Verifies file/directory exists and is accessible
2. **Content Detection**: Uses `file` command to determine actual format
3. **Extension Matching**: Compares current extension with detected format
4. **Conflict Resolution**: Handles naming conflicts with incremental naming
5. **Safe Renaming**: Performs the file rename operation
6. **Logging**: Records changes if verbose logging enabled

### Directory Processing
1. **Path Traversal**: Walks through directory structure (recursive if `-r` specified)
2. **File Filtering**: Processes all files, not just those with image extensions
3. **Batch Processing**: Handles multiple files efficiently
4. **Progress Reporting**: Provides feedback on processing status

## Configuration

### Logging Configuration
- **Log File**: `fixImgExt_info.txt` in current directory
- **Log Format**: Lists all successfully corrected files
- **Append Mode**: Each run appends to existing log file

### Processing Options
- **Recursive Mode**: Process subdirectories when using `-d` option
- **Verbose Mode**: Show detailed file information during processing
- **Logging Mode**: Record all successful corrections to log file

## Output Examples

### Standard Output
```bash
Corrected!    /path/to/file.wrong    /path/to/file.jpg
Info!         No change needed       file.png
Warning!      Currently supported formats: JPEG, GIF, PNG, TIFF, BMP, GIMP XCF, PSD, SVG, WebM
```

### Detailed Output (with `-s`)
```bash
---------------------------------------------------------------------------------------
  file path:-               /Users/alex/image.wrong
  dir:-                     /Users/alex
  file name with ext:-      image.wrong
  file name:-               image
---------------------------------------------------------------------------------------
Corrected!    /Users/alex/image.wrong    /Users/alex/image.jpg
```

### Log File Content (with `-v`)
```
--------------------------------NEW RUN--------------------------------
/Users/alex/Pictures/photo.jpg
/Users/alex/Pictures/graphic.png
/Users/alex/Pictures/design.psd
```

## Integration

### With Media Workflows
```bash
# Process camera imports
./fixImgExt.sh -d -r -v ~/Pictures/$(date +%Y-%m)/

# Clean up download directory
./fixImgExt.sh -d -v ~/Downloads/
```

### Automated Processing
```bash
#!/bin/bash
# Daily image cleanup script
IMPORT_DIR="~/Pictures/Daily_Import"
LOG_FILE="/var/log/image_fixes.log"

./fixImgExt.sh -d -r -v "$IMPORT_DIR"
echo "$(date): Processed $IMPORT_DIR" >> "$LOG_FILE"
```

### Project Workflows
```bash
# Fix extensions in design project
./fixImgExt.sh -d -r -s ~/Projects/client_work/assets/

# Process web asset directory
./fixImgExt.sh -d -v ~/Web_Projects/images/
```

## Best Practices

### Before Processing
1. **Backup Important Files**: Make backups before batch processing
2. **Test on Small Set**: Try on a few files before large batch operations
3. **Check Permissions**: Ensure write access to target directories
4. **Review File Types**: Understand what formats you're working with

### During Processing
1. **Use Verbose Mode**: Enable `-v` for logging important changes
2. **Monitor Output**: Watch for warnings about unsupported formats
3. **Check Progress**: Use `-s` for detailed view on complex operations
4. **Handle Conflicts**: Be aware of incremental naming for duplicates

### After Processing
1. **Review Log File**: Check `fixImgExt_info.txt` for list of changes
2. **Verify Results**: Spot-check corrected files
3. **Clean Up**: Remove log file if no longer needed
4. **Document Changes**: Keep record of batch operations performed

## Error Handling

### Input Validation
- **File Existence**: Verifies files exist before processing
- **Directory Access**: Checks directory permissions
- **Path Safety**: Prevents directory traversal attacks

### Processing Errors
- **Unsupported Formats**: Clear warnings for unrecognized file types
- **Permission Issues**: Graceful handling of read-only files
- **Naming Conflicts**: Automatic resolution with incremental naming

## Troubleshooting

### No Changes Made
- Check that files actually have incorrect extensions
- Verify file formats are supported
- Ensure write permissions in target directory

### Permission Denied Errors
- Run with appropriate file system permissions
- Check that files are not locked by other applications
- Verify directory write access

### Unexpected Results
- Some files may have ambiguous formats
- Hidden files or system files may be processed
- Network drives may have slower performance

## Technical Details

### Dependencies
- **file**: Unix file type detection command
- **bash**: Modern bash shell with getopts support
- **Shared Libraries**: Uses common.sh for validation functions

### Security Considerations
- **Path Validation**: All file paths validated for safety
- **No Arbitrary Execution**: No dynamic command construction
- **Safe Renaming**: Atomic file operations where possible

### Original Attribution
- Original script by "Ten Elite Brains" <atqueensu@gmail.com>
- Enhanced by Alexander Kucera / babylondreams.de

## See Also

- [Media Processing Tools](../overview.md) - Related media utilities
- [Common Functions](../lib/common.md) - Shared validation functions
- [Development Tools Overview](../overview.md#development-tools) - Other development utilities

---

*Script Location: `bash/development/fixImgExt.sh`*  
*Original Author: Ten Elite Brains*  
*Enhanced by: Alexander Kucera / babylondreams.de*