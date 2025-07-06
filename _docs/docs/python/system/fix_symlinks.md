# fix_symlinks.py

Intelligent symlink repair and validation tool with comprehensive analysis, automatic fixing, and safety features for maintaining symlink integrity across filesystems.

## Overview

fix_symlinks.py is a robust tool for managing symbolic links in complex directory structures. It identifies broken symlinks, analyzes link patterns, and provides both automated and manual repair options with comprehensive safety features and detailed reporting.

## Features

- **Comprehensive Analysis** - Scans directory trees for all symlink types
- **Broken Link Detection** - Identifies symlinks with missing targets
- **Intelligent Repair** - Attempts to locate moved targets automatically
- **Safety Features** - Dry-run mode and backup creation
- **Detailed Reporting** - Comprehensive analysis and repair reports
- **Performance Optimized** - Efficient handling of large directory structures
- **Cross-Platform** - Works on Unix-like systems with symlink support

## Usage

### Basic Usage
```bash
# Scan for broken symlinks
python3 fix_symlinks.py /path/to/scan

# Fix broken symlinks with dry-run first
python3 fix_symlinks.py /path/to/scan --dry-run
python3 fix_symlinks.py /path/to/scan --fix

# Recursive scan with verbose output
python3 fix_symlinks.py /path/to/scan --recursive --verbose
```

### Advanced Usage
```bash
# Create backups before fixing
python3 fix_symlinks.py /path/to/scan \
    --fix \
    --backup \
    --recursive

# Generate repair script for manual review
python3 fix_symlinks.py /path/to/scan \
    --generate-script \
    --output-file repair_script.py

# Detailed analysis with report
python3 fix_symlinks.py /path/to/scan \
    --recursive \
    --report-file symlink_analysis.txt \
    --verbose
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `path` | - | Directory path to scan for symlinks | Required |
| `--recursive` | `-r` | Scan directories recursively | False |
| `--fix` | - | Attempt to fix broken symlinks | False |
| `--dry-run` | - | Show what would be done without making changes | False |
| `--backup` | - | Create backups before modifying symlinks | False |
| `--generate-script` | - | Generate Python script for manual fixes | False |
| `--output-file` | `-o` | Output file for generated script | `fix_symlinks_generated.py` |
| `--report-file` | - | File for detailed analysis report | None |
| `--verbose` | `-v` | Show detailed output | False |

## Symlink Analysis

### Detection Categories
The tool categorizes symlinks into several types:

1. **Valid Symlinks** - Links pointing to existing targets
2. **Broken Symlinks** - Links with missing targets
3. **Circular Links** - Links creating circular references
4. **Relative Links** - Links using relative paths
5. **Absolute Links** - Links using absolute paths

### Analysis Output
```
Symlink Analysis Report
=======================

Scanning: /home/user/projects
Mode: Recursive scan

SUMMARY:
--------
Total symlinks found: 45
Valid symlinks: 38
Broken symlinks: 7
Circular references: 0
Relative path links: 32
Absolute path links: 13

BROKEN SYMLINKS:
----------------
1. /home/user/projects/lib/old_library.so
   Target: /usr/local/lib/library_v1.so (missing)
   Suggested fix: Update to /usr/local/lib/library_v2.so

2. /home/user/projects/docs/manual.pdf
   Target: ../resources/docs/manual.pdf (missing)
   Suggested fix: Create target or update link

3. /home/user/projects/bin/tool
   Target: /opt/tools/legacy/tool (missing)
   Suggested fix: Update to /opt/tools/current/tool
```

## Repair Strategies

### Automatic Repair
The tool attempts several repair strategies:

1. **Target Search** - Look for moved files in nearby directories
2. **Version Updates** - Find newer versions of missing files
3. **Path Correction** - Fix common path issues
4. **Relative Path Conversion** - Convert broken absolute paths to relative

### Manual Repair Options
- **Script Generation** - Creates executable repair scripts
- **Interactive Mode** - Prompts for user decisions
- **Backup Creation** - Preserves original symlinks before changes

## Examples

### Example 1: Development Environment Cleanup
```bash
# Scan development project for broken symlinks
python3 fix_symlinks.py ~/projects/myapp \
    --recursive \
    --dry-run \
    --verbose

# Fix after reviewing dry-run output
python3 fix_symlinks.py ~/projects/myapp \
    --recursive \
    --fix \
    --backup
```

### Example 2: System Maintenance
```bash
# Check system directories for broken links
sudo python3 fix_symlinks.py /usr/local \
    --recursive \
    --report-file /var/log/symlink_audit.txt

# Generate repair script for review
sudo python3 fix_symlinks.py /usr/local \
    --recursive \
    --generate-script \
    --output-file /root/symlink_repairs.py
```

### Example 3: Media Library Maintenance
```bash
#!/bin/bash
# Media library symlink maintenance script

MEDIA_DIR="/mnt/media"
LOG_DIR="/var/log/media_maintenance"
DATE=$(date +%Y%m%d)

mkdir -p "$LOG_DIR"

echo "Starting symlink maintenance: $(date)"

# Scan for issues
python3 fix_symlinks.py "$MEDIA_DIR" \
    --recursive \
    --report-file "$LOG_DIR/symlink_analysis_$DATE.txt" \
    --verbose

# Dry run to see what would be fixed
python3 fix_symlinks.py "$MEDIA_DIR" \
    --recursive \
    --dry-run > "$LOG_DIR/repair_preview_$DATE.txt"

# Generate repair script for manual review
python3 fix_symlinks.py "$MEDIA_DIR" \
    --recursive \
    --generate-script \
    --output-file "$LOG_DIR/repair_script_$DATE.py"

echo "Maintenance complete. Review files in $LOG_DIR"
```

### Example 4: Docker Volume Cleanup
```bash
# Clean up symlinks in Docker volumes
for volume in $(docker volume ls -q); do
    volume_path="/var/lib/docker/volumes/$volume/_data"
    echo "Checking volume: $volume"
    
    python3 fix_symlinks.py "$volume_path" \
        --recursive \
        --dry-run \
        --verbose
done
```

## Safety Features

### Dry-Run Mode
Preview operations without making changes:
```bash
python3 fix_symlinks.py /path --fix --dry-run
```

Output:
```
DRY RUN - No changes will be made
=====================================

Would fix broken symlink:
  Link: /path/to/broken_link
  Current target: /missing/file
  New target: /found/file
  Action: Update symlink target

Would remove broken symlink:
  Link: /path/to/unfixable_link
  Target: /completely/missing/target
  Action: Remove broken symlink
```

### Backup Creation
Automatic backup before modifications:
```bash
python3 fix_symlinks.py /path --fix --backup
```

Creates:
- `broken_link.backup` - Copy of original symlink
- `symlink_backup_YYYYMMDD_HHMMSS/` - Timestamped backup directory

## Generated Repair Scripts

### Script Structure
Generated scripts provide fine-grained control:

```python
#!/usr/bin/env python3
"""Auto-generated symlink repair script."""
import os
import shutil
from pathlib import Path

def backup_symlink(link_path, backup_dir):
    """Create backup of symlink before modification."""
    backup_path = backup_dir / Path(link_path).name
    shutil.copy2(link_path, backup_path, follow_symlinks=False)
    return backup_path

def fix_symlink_1():
    """Fix: /home/user/lib/library.so"""
    link_path = "/home/user/lib/library.so"
    old_target = "/usr/lib/old/library.so"
    new_target = "/usr/lib/current/library.so"
    
    print(f"Fixing: {link_path}")
    print(f"  Old target: {old_target}")
    print(f"  New target: {new_target}")
    
    # Create backup
    backup_path = backup_symlink(link_path, Path("/tmp/symlink_backups"))
    print(f"  Backup created: {backup_path}")
    
    # Remove old link and create new one
    os.unlink(link_path)
    os.symlink(new_target, link_path)
    print(f"  ✓ Fixed")

def main():
    """Run all repairs."""
    print("Symlink Repair Script")
    print("====================")
    
    # Create backup directory
    backup_dir = Path("/tmp/symlink_backups")
    backup_dir.mkdir(exist_ok=True)
    
    # Run repairs
    fix_symlink_1()
    # Additional repairs...
    
    print("\nAll repairs completed!")

if __name__ == "__main__":
    main()
```

## Advanced Features

### Intelligent Target Detection
The tool uses several strategies to find moved targets:

1. **Filename Search** - Look for files with same name in nearby directories
2. **Pattern Matching** - Match files based on naming patterns
3. **Version Detection** - Find newer versions of versioned files
4. **Content Analysis** - Compare file metadata when available

### Circular Reference Detection
Identifies and reports circular symlink chains:
```
CIRCULAR REFERENCE DETECTED:
/path/a -> /path/b -> /path/c -> /path/a

Resolution required: Break the circle by updating one link
```

### Cross-Filesystem Handling
- Detects symlinks crossing filesystem boundaries
- Provides warnings for potential mount point issues
- Suggests relative path alternatives where appropriate

## Integration

### System Administration
```python
import subprocess
import sys

class SymlinkMaintenance:
    def __init__(self, base_paths):
        self.base_paths = base_paths
        self.results = {}
    
    def scan_all_paths(self):
        """Scan all configured paths for symlink issues."""
        for path in self.base_paths:
            print(f"Scanning {path}...")
            
            result = subprocess.run([
                sys.executable, "fix_symlinks.py",
                path, "--recursive", "--dry-run"
            ], capture_output=True, text=True)
            
            self.results[path] = {
                'success': result.returncode == 0,
                'output': result.stdout,
                'issues_found': 'Broken symlinks: 0' not in result.stdout
            }
    
    def generate_report(self):
        """Generate maintenance report."""
        issues_found = False
        
        for path, result in self.results.items():
            if result['issues_found']:
                print(f"Issues found in {path}")
                issues_found = True
        
        return issues_found

# Usage
maintenance = SymlinkMaintenance([
    "/home", "/usr/local", "/opt"
])
maintenance.scan_all_paths()

if maintenance.generate_report():
    print("Symlink maintenance required")
else:
    print("All symlinks are healthy")
```

### CI/CD Integration
```yaml
# GitHub Actions workflow
name: Symlink Health Check
on:
  schedule:
    - cron: '0 4 * * 1'  # Weekly on Monday at 4 AM

jobs:
  symlink-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Check project symlinks
      run: |
        python3 fix_symlinks.py . \
          --recursive \
          --dry-run \
          --report-file symlink_report.txt
          
    - name: Upload symlink report
      uses: actions/upload-artifact@v2
      with:
        name: symlink-health-report
        path: symlink_report.txt
        
    - name: Fail if broken symlinks found
      run: |
        if grep -q "Broken symlinks: [1-9]" symlink_report.txt; then
          echo "Broken symlinks detected!"
          exit 1
        fi
```

### Backup Workflows
```bash
#!/bin/bash
# Pre-backup symlink validation

BACKUP_SOURCE="/data"
BACKUP_LOG="/var/log/backup_prep.log"

echo "Pre-backup symlink validation: $(date)" >> "$BACKUP_LOG"

# Check for broken symlinks before backup
if python3 fix_symlinks.py "$BACKUP_SOURCE" \
    --recursive \
    --dry-run >> "$BACKUP_LOG" 2>&1; then
    echo "Symlink validation passed" >> "$BACKUP_LOG"
else
    echo "Symlink issues detected - fixing before backup" >> "$BACKUP_LOG"
    
    # Generate and review repair script
    python3 fix_symlinks.py "$BACKUP_SOURCE" \
        --recursive \
        --generate-script \
        --output-file "/tmp/pre_backup_fixes.py"
    
    echo "Review /tmp/pre_backup_fixes.py before proceeding"
    exit 1
fi

# Proceed with backup
echo "Starting backup process..." >> "$BACKUP_LOG"
```

## Troubleshooting

### Common Issues

**Issue**: Permission denied when scanning system directories
```bash
# Run with appropriate privileges
sudo python3 fix_symlinks.py /usr/local --recursive
```

**Issue**: Cannot find moved targets
```bash
# Use verbose mode to see search paths
python3 fix_symlinks.py /path --verbose --dry-run
```

**Issue**: Too many symlinks to process manually
```bash
# Generate script for batch processing
python3 fix_symlinks.py /path \
    --recursive \
    --generate-script \
    --output-file batch_fixes.py
```

### Debugging

Use verbose mode for detailed operation information:
```bash
python3 fix_symlinks.py /path --verbose --recursive --dry-run
```

This shows:
- Symlink discovery process
- Target validation attempts
- Repair strategy selection
- Detailed error information

## Best Practices

### Regular Maintenance
1. **Scheduled Scans** - Regular symlink health checks
2. **Pre-Backup Validation** - Check symlinks before backups
3. **Post-Migration Cleanup** - Fix symlinks after system changes
4. **Documentation** - Keep records of symlink patterns and purposes

### Safety Procedures
1. **Always Dry-Run First** - Preview changes before applying
2. **Create Backups** - Preserve original symlinks
3. **Test Repairs** - Verify fixed symlinks work correctly
4. **Gradual Deployment** - Fix critical symlinks first

### Performance Optimization
1. **Targeted Scans** - Focus on specific directories when possible
2. **Exclude System Areas** - Skip areas not requiring maintenance
3. **Batch Operations** - Group similar repairs together
4. **Resource Monitoring** - Monitor I/O during large scans

---

*fix_symlinks.py provides comprehensive symlink maintenance with intelligent repair capabilities, safety features, and integration options for system administration and development workflows.*