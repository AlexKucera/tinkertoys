# compareFolders.py

Advanced directory comparison and synchronization analysis tool with comprehensive filtering, recursive scanning, and detailed reporting capabilities.

## Overview

compareFolders.py performs in-depth analysis of two directory structures to identify missing files, size differences, and synchronization issues. The tool is designed for backup validation, mirror maintenance, and large-scale directory synchronization workflows.

## Features

- **Recursive Directory Scanning** - Deep analysis of entire directory trees
- **Missing File Detection** - Identifies files present in one directory but not the other
- **Size Comparison** - Detects files with different sizes between directories
- **Advanced Filtering** - File extension, size, and date filtering options
- **Progress Tracking** - Real-time progress updates for large datasets
- **Multiple Output Formats** - Console, file, and structured reporting
- **Performance Optimization** - Efficient handling of large directory structures

## Usage

### Basic Usage
```bash
# Compare two directories
python3 compareFolders.py /source/dir /destination/dir

# Recursive comparison with progress
python3 compareFolders.py /source/dir /destination/dir --recursive --verbose

# Generate detailed report file
python3 compareFolders.py /source/dir /destination/dir \
    --output-file comparison_report.txt
```

### Advanced Usage
```bash
# Filter by file extension
python3 compareFolders.py /source/dir /destination/dir \
    --filter-extension .mov \
    --recursive

# Size-based filtering
python3 compareFolders.py /source/dir /destination/dir \
    --min-size 1048576 \
    --max-size 10737418240

# Generate copy script for missing files
python3 compareFolders.py /source/dir /destination/dir \
    --generate-script \
    --recursive
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `source_dir` | - | Source directory path | Required |
| `dest_dir` | - | Destination directory path | Required |
| `--recursive` | `-r` | Scan directories recursively | False |
| `--filter-extension` | `-f` | Filter by file extension (e.g., .mov, .jpg) | None |
| `--min-size` | - | Minimum file size in bytes | None |
| `--max-size` | - | Maximum file size in bytes | None |
| `--output-file` | `-o` | Output file for detailed report | None |
| `--generate-script` | - | Generate copy script for missing files | False |
| `--show-sizes` | - | Show file sizes in output | False |
| `--verbose` | `-v` | Show detailed progress information | False |

## Comparison Analysis

### File Detection
The script identifies three categories of files:

1. **Missing in Destination** - Files present in source but not destination
2. **Missing in Source** - Files present in destination but not source  
3. **Size Mismatches** - Files present in both but with different sizes

### Comparison Logic
- **Filename Matching** - Compares files by relative path from root
- **Size Comparison** - Byte-perfect size matching
- **Case Sensitivity** - Respects filesystem case sensitivity rules
- **Symbolic Links** - Handles symlinks according to target filesystem

## Output Formats

### Console Output
```
Comparing directories:
  Source:      /backup/photos
  Destination: /archive/photos

Scanning directories...
Found 1,250 files in source directory
Found 1,180 files in destination directory

COMPARISON RESULTS:
==================

Missing in destination (70 files):
  vacation2023/IMG_001.jpg (2.5 MB)
  vacation2023/IMG_002.jpg (2.8 MB)
  work/presentation.pptx (15.2 MB)
  ...

Missing in source (0 files):
  (No files missing in source)

Size mismatches (0 files):
  (No size mismatches found)

SUMMARY:
========
Total files compared: 1,180
Files missing in destination: 70
Files missing in source: 0
Size mismatches: 0
```

### File Report
When using `--output-file`, creates detailed reports with:
- Complete file lists with full paths
- File sizes and timestamps
- Summary statistics
- Recommended actions

## Filtering Options

### File Extension Filtering
```bash
# Compare only video files
python3 compareFolders.py /source /dest --filter-extension .mov

# Compare only image files  
python3 compareFolders.py /source /dest --filter-extension .jpg
```

### Size-Based Filtering
```bash
# Files larger than 100MB
python3 compareFolders.py /source /dest --min-size 104857600

# Files between 1MB and 1GB
python3 compareFolders.py /source /dest \
    --min-size 1048576 \
    --max-size 1073741824
```

## Script Generation

### Copy Script Creation
The `--generate-script` option creates executable scripts to synchronize directories:

```bash
python3 compareFolders.py /source /dest --generate-script
```

Creates `sync_missing_files.py`:
```python
#!/usr/bin/env python3
"""Auto-generated script to copy missing files."""
import shutil
import os

def copy_missing_files():
    # Copy missing files from source to destination
    shutil.copy2("/source/file1.jpg", "/dest/file1.jpg")
    shutil.copy2("/source/file2.mov", "/dest/file2.mov")
    # ... more copy operations

if __name__ == "__main__":
    copy_missing_files()
```

## Examples

### Example 1: Backup Validation
```bash
# Verify backup completeness
python3 compareFolders.py /home/user/documents /backup/documents \
    --recursive \
    --verbose \
    --output-file backup_validation.txt
```

### Example 2: Media Archive Sync
```bash
# Check video archive synchronization
python3 compareFolders.py /production/footage /archive/footage \
    --filter-extension .mov \
    --recursive \
    --show-sizes \
    --generate-script
```

### Example 3: Large File Migration
```bash
# Find large files that need migration
python3 compareFolders.py /old_storage /new_storage \
    --min-size 1073741824 \
    --recursive \
    --verbose
```

### Example 4: Incremental Backup Check
```bash
#!/bin/bash
# Daily backup verification script

SOURCE="/home/user/projects"
BACKUP="/mnt/backup/projects"
REPORT="/var/log/backup_check_$(date +%Y%m%d).txt"

echo "Checking backup: $(date)" > "$REPORT"

python3 compareFolders.py "$SOURCE" "$BACKUP" \
    --recursive \
    --output-file "$REPORT" \
    --verbose

if [ $? -eq 0 ]; then
    echo "Backup check completed successfully"
else
    echo "Backup check failed - see $REPORT"
    exit 1
fi
```

## Performance Considerations

### Large Datasets
- **Memory Efficient** - Processes files incrementally
- **Progress Tracking** - Real-time updates for long operations
- **Interrupt Handling** - Graceful handling of cancellation
- **Resume Capability** - Can restart interrupted comparisons

### Network Filesystems
- **Optimized I/O** - Minimizes network filesystem calls
- **Batch Operations** - Groups filesystem operations efficiently
- **Timeout Handling** - Robust handling of slow network connections
- **Cache Utilization** - Leverages filesystem metadata caching

## Integration

### Backup Scripts
```python
import subprocess
import sys
from pathlib import Path

def validate_backup(source, destination):
    """Validate backup completeness using compareFolders."""
    cmd = [
        sys.executable, "compareFolders.py",
        str(source), str(destination),
        "--recursive", "--verbose"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Backup validation successful")
        return True
    else:
        print(f"Backup validation failed: {result.stderr}")
        return False

# Usage
if validate_backup("/home/user/docs", "/backup/docs"):
    print("Backup is complete and valid")
else:
    print("Backup needs attention")
```

### Synchronization Workflow
```bash
#!/bin/bash
# Complete synchronization workflow

SOURCE_DIR="/production/assets"
DEST_DIR="/archive/assets"
REPORT_DIR="/var/log/sync"

mkdir -p "$REPORT_DIR"
DATE=$(date +%Y%m%d_%H%M%S)

echo "Starting synchronization analysis..."

# Generate comparison report
python3 compareFolders.py "$SOURCE_DIR" "$DEST_DIR" \
    --recursive \
    --output-file "$REPORT_DIR/comparison_$DATE.txt" \
    --generate-script \
    --verbose

# Review and execute sync script
if [ -f sync_missing_files.py ]; then
    echo "Found missing files. Review sync script before execution:"
    echo "python3 sync_missing_files.py"
else
    echo "Directories are in sync"
fi
```

### CI/CD Integration
```yaml
# GitHub Actions workflow
name: Backup Validation
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  validate-backup:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Mount backup drive
      run: sudo mount /dev/backup /mnt/backup
      
    - name: Validate backup
      run: |
        python3 compareFolders.py /data /mnt/backup/data \
          --recursive \
          --output-file backup_report.txt
          
    - name: Upload report
      uses: actions/upload-artifact@v2
      with:
        name: backup-report
        path: backup_report.txt
```

## Error Handling

### Common Issues

**Issue**: Permission denied errors
```bash
# Fix file permissions
chmod -R +r /source/directory
chmod -R +r /destination/directory
```

**Issue**: "Directory not found" errors
```bash
# Verify paths exist and are accessible
ls -la /source/directory
ls -la /destination/directory
```

**Issue**: Out of memory with very large directories
```bash
# Use filtering to reduce memory usage
python3 compareFolders.py /source /dest \
    --filter-extension .jpg \
    --recursive
```

### Debugging

Use verbose mode for detailed operation information:

```bash
python3 compareFolders.py /source /dest --verbose --recursive
```

This shows:
- Directory scanning progress
- File discovery statistics
- Comparison operations
- Any errors or warnings

## Use Cases

### Data Migration
- **Server Migration** - Verify complete data transfer
- **Storage Upgrade** - Ensure all files copied correctly
- **Cloud Migration** - Validate cloud sync completeness

### Backup Management
- **Backup Verification** - Regular backup completeness checks
- **Incremental Validation** - Verify incremental backup integrity
- **Archive Maintenance** - Ensure archive completeness

### Synchronization
- **Mirror Maintenance** - Keep multiple copies synchronized
- **Team Collaboration** - Verify shared folder synchronization
- **Distributed Storage** - Maintain consistency across locations

---

*compareFolders.py provides comprehensive directory comparison with advanced filtering, performance optimization, and integration capabilities for backup validation and synchronization workflows.*