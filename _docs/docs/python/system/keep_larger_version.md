# keepLargerVersion.py

Automated duplicate file management with intelligent size-based selection, comprehensive CLI interface, and safe operation modes for file deduplication workflows.

## Overview

keepLargerVersion.py intelligently manages duplicate files by automatically keeping the larger version and removing smaller duplicates. The tool is designed for scenarios where file size indicates completeness or quality, such as media files, documents, or backup archives.

## Features

- **Intelligent Duplicate Detection** - Identifies files with identical names in directory trees
- **Size-Based Selection** - Automatically keeps the larger version of duplicate files
- **Safety Features** - Dry-run mode and comprehensive confirmation prompts
- **Flexible Filtering** - File extension and size filtering options
- **Detailed Reporting** - Comprehensive analysis and operation reports
- **Backup Support** - Optional backup creation before file removal
- **Performance Optimized** - Efficient handling of large directory structures

## Usage

### Basic Usage
```bash
# Find and remove duplicate files (dry-run first)
python3 keepLargerVersion.py /path/to/scan --dry-run

# Execute the operation after reviewing dry-run
python3 keepLargerVersion.py /path/to/scan --execute

# Recursive scan with verbose output
python3 keepLargerVersion.py /path/to/scan --recursive --verbose
```

### Advanced Usage
```bash
# Filter by file extension
python3 keepLargerVersion.py /path/to/scan \
    --filter-extension .jpg \
    --recursive \
    --execute

# Create backups before removal
python3 keepLargerVersion.py /path/to/scan \
    --execute \
    --create-backup \
    --backup-dir /safe/backup/location

# Size-based filtering
python3 keepLargerVersion.py /path/to/scan \
    --min-size 1048576 \
    --max-size 104857600 \
    --recursive
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `directory` | - | Directory to scan for duplicates | Required |
| `--recursive` | `-r` | Scan subdirectories recursively | False |
| `--execute` | `-e` | Execute file removal (required for actual removal) | False |
| `--dry-run` | - | Show what would be done without making changes | True (default) |
| `--filter-extension` | `-f` | Filter by file extension (e.g., .jpg, .mp4) | None |
| `--min-size` | - | Minimum file size in bytes | None |
| `--max-size` | - | Maximum file size in bytes | None |
| `--create-backup` | - | Create backup before removing files | False |
| `--backup-dir` | - | Directory for backup files | `./backup_YYYYMMDD_HHMMSS` |
| `--verbose` | `-v` | Show detailed output | False |

## Duplicate Detection Logic

### File Matching
The tool identifies duplicates based on:

1. **Filename Matching** - Files with identical names (case-sensitive)
2. **Extension Consideration** - Considers files with same base name but different extensions as separate
3. **Path Independence** - Matches files regardless of directory location
4. **Size Comparison** - Compares file sizes to determine which to keep

### Selection Strategy
When duplicates are found:

1. **Size Comparison** - Larger file is always kept
2. **Equal Sizes** - First found file is kept (with warning)
3. **Zero-Byte Files** - Special handling for empty files
4. **Access Permissions** - Checks file permissions before removal

## Safety Features

### Dry-Run Mode (Default)
By default, the tool runs in dry-run mode showing what would be done:

```bash
python3 keepLargerVersion.py /photos
```

Output:
```
Duplicate File Analysis
=======================

Scanning: /photos
Mode: Dry-run (no files will be removed)

DUPLICATES FOUND:
-----------------

vacation.jpg (2 versions found):
  KEEP:   /photos/2023/vacation.jpg (2.5 MB)
  REMOVE: /photos/backup/vacation.jpg (1.8 MB)
  Savings: 1.8 MB

document.pdf (3 versions found):
  KEEP:   /photos/docs/document.pdf (850 KB)
  REMOVE: /photos/old/document.pdf (820 KB)
  REMOVE: /photos/temp/document.pdf (800 KB)
  Savings: 1.6 MB

SUMMARY:
--------
Total duplicates found: 2 sets
Files that would be removed: 3
Total space that would be saved: 3.4 MB

Run with --execute to perform the removal.
```

### Backup Creation
Optional backup before file removal:

```bash
python3 keepLargerVersion.py /photos --execute --create-backup
```

Creates timestamped backup directory with copies of files before removal.

## Examples

### Example 1: Photo Collection Cleanup
```bash
# Clean up photo collection with duplicates
python3 keepLargerVersion.py ~/Pictures \
    --filter-extension .jpg \
    --recursive \
    --dry-run \
    --verbose

# After reviewing results, execute
python3 keepLargerVersion.py ~/Pictures \
    --filter-extension .jpg \
    --recursive \
    --execute \
    --create-backup
```

### Example 2: Document Archive Management
```bash
# Clean up document archives
python3 keepLargerVersion.py /archive/documents \
    --filter-extension .pdf \
    --min-size 10240 \
    --recursive \
    --execute
```

### Example 3: Media Library Optimization
```bash
#!/bin/bash
# Complete media library optimization script

MEDIA_DIR="/mnt/media"
BACKUP_DIR="/backup/media_cleanup_$(date +%Y%m%d)"
LOG_FILE="/var/log/media_cleanup.log"

echo "Starting media library cleanup: $(date)" | tee "$LOG_FILE"

# Process different media types
for extension in .mp4 .avi .mkv .mov; do
    echo "Processing $extension files..." | tee -a "$LOG_FILE"
    
    python3 keepLargerVersion.py "$MEDIA_DIR" \
        --filter-extension "$extension" \
        --recursive \
        --execute \
        --create-backup \
        --backup-dir "$BACKUP_DIR" \
        --verbose >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✓ $extension files processed successfully" | tee -a "$LOG_FILE"
    else
        echo "✗ Error processing $extension files" | tee -a "$LOG_FILE"
    fi
done

echo "Media cleanup completed: $(date)" | tee -a "$LOG_FILE"
```

### Example 4: Automated Backup Cleanup
```bash
# Weekly backup cleanup automation
python3 keepLargerVersion.py /backup/weekly \
    --recursive \
    --min-size 1024 \
    --execute \
    --verbose \
    > /var/log/backup_cleanup_$(date +%Y%m%d).log
```

## Advanced Features

### Size-Based Filtering
```bash
# Only process files between 1MB and 100MB
python3 keepLargerVersion.py /data \
    --min-size 1048576 \
    --max-size 104857600 \
    --recursive

# Only process large files (> 100MB)
python3 keepLargerVersion.py /videos \
    --min-size 104857600 \
    --filter-extension .mp4
```

### Multiple Extension Processing
```bash
#!/bin/bash
# Process multiple file types in sequence

EXTENSIONS=(".jpg" ".png" ".mp4" ".avi" ".pdf" ".docx")
TARGET_DIR="/cleanup/target"

for ext in "${EXTENSIONS[@]}"; do
    echo "Processing $ext files..."
    
    python3 keepLargerVersion.py "$TARGET_DIR" \
        --filter-extension "$ext" \
        --recursive \
        --execute \
        --verbose
    
    echo "Completed $ext files"
    echo "---"
done
```

## Detailed Reporting

### Verbose Output Analysis
With `--verbose` flag, get detailed analysis:

```
Duplicate File Analysis
=======================

Scanning: /test/duplicates
Mode: Execute (files will be removed)
Filter: .jpg files only
Minimum size: 1 MB

SCAN RESULTS:
------------
Total files scanned: 1,247
Filtered files: 856 .jpg files
Files meeting size criteria: 734

DUPLICATE ANALYSIS:
------------------

Set 1: vacation_sunset.jpg
  Files found: 3
  ├─ /test/duplicates/2023/vacation_sunset.jpg (3.2 MB) ← KEEP (largest)
  ├─ /test/duplicates/backup/vacation_sunset.jpg (3.1 MB) → REMOVE
  └─ /test/duplicates/temp/vacation_sunset.jpg (2.8 MB) → REMOVE
  Space saved: 5.9 MB

Set 2: family_portrait.jpg
  Files found: 2
  ├─ /test/duplicates/photos/family_portrait.jpg (4.1 MB) ← KEEP (largest)
  └─ /test/duplicates/old/family_portrait.jpg (4.0 MB) → REMOVE
  Space saved: 4.0 MB

OPERATION SUMMARY:
-----------------
Duplicate sets found: 2
Total files to remove: 3
Total space to save: 9.9 MB
Estimated time: < 1 second

SAFETY CHECKS:
-------------
✓ All target files are writable
✓ Backup directory has sufficient space
✓ No system files detected
✓ All operations are reversible

Proceeding with removal...
✓ Removed: /test/duplicates/backup/vacation_sunset.jpg
✓ Removed: /test/duplicates/temp/vacation_sunset.jpg  
✓ Removed: /test/duplicates/old/family_portrait.jpg

FINAL REPORT:
------------
Files removed: 3
Space freed: 9.9 MB
Backup created: /backup/keepLargerVersion_20240706_143022/
Operation completed successfully in 0.8 seconds
```

## Integration Patterns

### Python Script Integration
```python
import subprocess
import sys
from pathlib import Path

class DuplicateManager:
    def __init__(self, base_directory):
        self.base_directory = Path(base_directory)
        self.script_path = "keepLargerVersion.py"
    
    def analyze_duplicates(self, file_extension=None, recursive=True):
        """Analyze duplicates without removing files."""
        cmd = [
            sys.executable, self.script_path,
            str(self.base_directory),
            "--dry-run", "--verbose"
        ]
        
        if recursive:
            cmd.append("--recursive")
        
        if file_extension:
            cmd.extend(["--filter-extension", file_extension])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'errors': result.stderr
        }
    
    def remove_duplicates(self, file_extension=None, create_backup=True):
        """Remove duplicates after analysis."""
        cmd = [
            sys.executable, self.script_path,
            str(self.base_directory),
            "--execute", "--recursive"
        ]
        
        if file_extension:
            cmd.extend(["--filter-extension", file_extension])
        
        if create_backup:
            cmd.append("--create-backup")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0

# Usage
manager = DuplicateManager("/media/photos")

# Analyze first
analysis = manager.analyze_duplicates(".jpg")
if analysis['success']:
    print("Analysis completed. Found duplicates to remove.")
    
    # Execute removal
    if manager.remove_duplicates(".jpg", create_backup=True):
        print("Duplicates removed successfully")
    else:
        print("Failed to remove duplicates")
```

### Monitoring and Alerting
```python
import smtplib
from email.mime.text import MIMEText
import subprocess

def automated_cleanup_with_alerts(directory, email_recipient):
    """Automated cleanup with email alerts."""
    
    # Run analysis
    result = subprocess.run([
        "python3", "keepLargerVersion.py",
        directory, "--recursive", "--dry-run"
    ], capture_output=True, text=True)
    
    if "duplicates found" in result.stdout:
        # Send notification
        msg = MIMEText(f"Duplicate cleanup needed in {directory}\n\n{result.stdout}")
        msg['Subject'] = f'Duplicate Files Found: {directory}'
        msg['From'] = 'system@company.com'
        msg['To'] = email_recipient
        
        # Send email (configure SMTP as needed)
        smtp = smtplib.SMTP('localhost')
        smtp.send_message(msg)
        smtp.quit()
        
        return True
    else:
        print("No duplicates found")
        return False

# Schedule this function to run periodically
automated_cleanup_with_alerts("/important/data", "admin@company.com")
```

## Error Handling and Recovery

### Comprehensive Error Handling
```python
def safe_duplicate_removal(directory, **options):
    """Safely remove duplicates with comprehensive error handling."""
    
    try:
        # Validate directory
        if not os.path.exists(directory):
            raise ValueError(f"Directory does not exist: {directory}")
        
        if not os.access(directory, os.R_OK):
            raise PermissionError(f"Cannot read directory: {directory}")
        
        # Run dry-run first
        print("Running analysis...")
        dry_run_cmd = [
            "python3", "keepLargerVersion.py",
            directory, "--dry-run", "--verbose"
        ]
        
        result = subprocess.run(dry_run_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Analysis failed: {result.stderr}")
        
        # Parse results
        if "No duplicates found" in result.stdout:
            print("No duplicates found")
            return True
        
        # Confirm with user
        print(result.stdout)
        if not input("Proceed with removal? (y/N): ").lower().startswith('y'):
            print("Operation cancelled by user")
            return False
        
        # Execute removal
        execute_cmd = [
            "python3", "keepLargerVersion.py",
            directory, "--execute", "--create-backup", "--verbose"
        ]
        
        result = subprocess.run(execute_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Duplicates removed successfully")
            print(result.stdout)
            return True
        else:
            print("✗ Removal failed")
            print(result.stderr)
            return False
    
    except Exception as e:
        print(f"Error during duplicate removal: {e}")
        return False

# Usage with error handling
if safe_duplicate_removal("/media/photos", recursive=True):
    print("Cleanup completed successfully")
else:
    print("Cleanup failed - manual intervention required")
```

## Best Practices

### Safe Operation Workflow
1. **Always Dry-Run First** - Review what will be removed
2. **Create Backups** - Use `--create-backup` for important files
3. **Filter Appropriately** - Use extension and size filters to target specific files
4. **Verify Results** - Check that intended files were removed
5. **Monitor Disk Space** - Ensure sufficient space for backups

### Performance Optimization
1. **Use Filters** - Reduce processing time with appropriate filters
2. **Size Thresholds** - Skip very small files if not relevant
3. **Incremental Processing** - Process one extension type at a time
4. **Resource Monitoring** - Monitor system resources during operation

### Data Safety
1. **Test on Copies** - Test the tool on copies of important data first
2. **Backup Strategy** - Have independent backups before cleanup
3. **Verification** - Verify that kept files are actually larger and intact
4. **Rollback Plan** - Know how to restore from backups if needed

---

*keepLargerVersion.py provides intelligent duplicate file management with comprehensive safety features, detailed reporting, and flexible filtering options for automated file deduplication workflows.*