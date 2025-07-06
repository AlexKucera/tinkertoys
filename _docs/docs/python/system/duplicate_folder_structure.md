# duplicate_folder_structure.py

Modern Python tool for duplicating directory structures without copying files. Creates an exact replica of folder hierarchies while preserving the complete directory tree structure.

## Overview

duplicate_folder_structure.py creates a complete copy of a directory tree structure without copying any files. This is useful for creating template directory structures, preparing backup locations, or setting up parallel folder hierarchies for different purposes.

I created both a Python and Shell version since they serve slightly different use cases:

 - Python version (duplicate_folder_structure.py): For integration into Python workflows, with advanced features like progress tracking and flexible configuration
 - Shell version (duplicate_folder_structure.sh): For quick command-line use and shell scripting integration

## Features

- **Structure-Only Duplication** - Copies directory hierarchy without any files
- **Flexible Naming** - Automatic destination generation with suffix/prefix options  
- **Safety Features** - Dry-run mode, path validation, and confirmation prompts
- **Progress Tracking** - Real-time progress display for large directory trees
- **Error Handling** - Comprehensive error reporting and recovery
- **Cross-Platform** - Works on macOS, Linux, and Windows
- **Performance Optimized** - Efficient processing of large directory structures

## Usage

### Basic Usage
```bash
# Duplicate structure to specific destination
python3 duplicate_folder_structure.py /source/project /backup/structure

# Generate destination with suffix
python3 duplicate_folder_structure.py /project --suffix "_backup"

# Generate destination with prefix  
python3 duplicate_folder_structure.py /data --prefix "structure_"

# Dry-run to preview what would be created
python3 duplicate_folder_structure.py /source /dest --dry-run
```

### Advanced Usage
```bash
# Verbose output with detailed progress
python3 duplicate_folder_structure.py /large/project /backup --verbose

# Skip confirmation prompts
python3 duplicate_folder_structure.py /source /dest --force

# Combine options for automated workflows
python3 duplicate_folder_structure.py /project \
    --suffix "_template" \
    --verbose \
    --force
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `source` | - | Source directory to duplicate structure from | Required |
| `destination` | - | Destination directory (optional with --suffix/--prefix) | None |
| `--suffix` | - | Add suffix to source directory name for destination | None |
| `--prefix` | - | Add prefix to source directory name for destination | None |
| `--dry-run` | - | Show what would be done without making changes | False |
| `--verbose` | `-v` | Show detailed output and progress | False |
| `--force` | - | Skip confirmation prompts | False |

## Examples

### Example 1: Project Template Creation
```bash
# Create a template structure for new projects
python3 duplicate_folder_structure.py /master/project_template /new/client_project --verbose

# Result: All directories from project_template are created in client_project
# Files are not copied, leaving clean directory structure
```

### Example 2: Backup Structure Preparation
```bash
# Prepare backup directory structure
python3 duplicate_folder_structure.py /important/data --suffix "_backup_structure"

# Creates: /important/data_backup_structure/
# With all subdirectories from /important/data/ but no files
```

### Example 3: Parallel Environment Setup
```bash
# Set up development, staging, and production structures
python3 duplicate_folder_structure.py /app/production --prefix "dev_" --force
python3 duplicate_folder_structure.py /app/production --prefix "staging_" --force

# Creates parallel directory structures for different environments
```

### Example 4: Large Directory Tree Processing
```bash
# Process large directory with progress tracking
python3 duplicate_folder_structure.py /massive/dataset /backup/structure \
    --verbose \
    --dry-run

# Review output, then execute:
python3 duplicate_folder_structure.py /massive/dataset /backup/structure --verbose
```

## Advanced Features

### Automatic Path Generation

The tool can automatically generate destination paths using patterns:

```bash
# Suffix generation
python3 duplicate_folder_structure.py /project --suffix "_folders"
# Creates: /project_folders/

# Prefix generation  
python3 duplicate_folder_structure.py /data --prefix "structure_"
# Creates: /structure_data/

# Default generation (if no suffix/prefix specified with explicit destination)
python3 duplicate_folder_structure.py /source
# Would create: /source_structure/ (but requires confirmation)
```

### Path Validation and Safety

The tool includes comprehensive safety checks:

```python
# Prevents dangerous operations
duplicate_folder_structure.py / /backup           # Error: Critical path
duplicate_folder_structure.py /source /source     # Error: Same path  
duplicate_folder_structure.py /parent /parent/sub # Error: Destination inside source
```

### Progress Tracking for Large Operations

For directories with many subdirectories, the tool provides progress feedback:

```
Found 1,247 directories to duplicate

Creating directory structure in: /backup/structure
==================================================
Created: /backup/structure/subdir1
Created: /backup/structure/subdir1/nested
Created: /backup/structure/subdir2
...

==================================================
OPERATION SUMMARY:
Directories created: 1,247
Directories already existing: 0
No errors encountered
Source: /source/project
Destination: /backup/structure
Operation completed in 2.34 seconds
```

## Integration Examples

### Python Script Integration

```python
import subprocess
import sys
from pathlib import Path

class StructureDuplicator:
    def __init__(self, script_path="duplicate_folder_structure.py"):
        self.script_path = script_path
    
    def duplicate_structure(self, source, destination, dry_run=False, verbose=False):
        """Duplicate directory structure programmatically."""
        cmd = [sys.executable, self.script_path, str(source), str(destination)]
        
        if dry_run:
            cmd.append("--dry-run")
        if verbose:
            cmd.append("--verbose")
        
        # Always use --force for programmatic calls
        cmd.append("--force")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'errors': result.stderr
        }
    
    def create_template_structure(self, template_dir, new_project_dir):
        """Create new project from template structure."""
        print(f"Creating project structure from template: {template_dir}")
        
        # First, dry-run to check
        result = self.duplicate_structure(template_dir, new_project_dir, dry_run=True)
        
        if result['success']:
            print("Template structure validated. Creating directories...")
            # Execute the duplication
            result = self.duplicate_structure(template_dir, new_project_dir, verbose=True)
            
            if result['success']:
                print(f"✓ Project structure created: {new_project_dir}")
                return True
            else:
                print(f"✗ Failed to create structure: {result['errors']}")
                return False
        else:
            print(f"✗ Template validation failed: {result['errors']}")
            return False

# Usage
duplicator = StructureDuplicator()
duplicator.create_template_structure("/templates/web_app", "/projects/new_client")
```

### Automated Workflow Integration

```bash
#!/bin/bash
# Project setup automation script

PROJECT_TEMPLATE="/templates/standard_project"
CLIENT_NAME="$1"
PROJECT_BASE="/projects"

if [[ -z "$CLIENT_NAME" ]]; then
    echo "Usage: $0 <client_name>"
    exit 1
fi

NEW_PROJECT="${PROJECT_BASE}/${CLIENT_NAME}"

echo "Setting up new project for: $CLIENT_NAME"

# Create directory structure
python3 duplicate_folder_structure.py "$PROJECT_TEMPLATE" "$NEW_PROJECT" --verbose --force

if [[ $? -eq 0 ]]; then
    echo "✓ Directory structure created"
    
    # Additional setup steps
    echo "Setting up configuration files..."
    cp "$PROJECT_TEMPLATE/config.template" "$NEW_PROJECT/config.ini"
    
    # Set permissions
    chmod -R 755 "$NEW_PROJECT"
    
    echo "✓ Project setup complete: $NEW_PROJECT"
else
    echo "✗ Failed to create project structure"
    exit 1
fi
```

### Backup Preparation Workflow

```python
#!/usr/bin/env python3
"""
Backup structure preparation script
Creates empty directory structures for organized backups
"""

import argparse
import sys
from pathlib import Path
import subprocess
from datetime import datetime

def prepare_backup_structures(source_dirs, backup_base):
    """Prepare backup directory structures for multiple source directories."""
    
    backup_base = Path(backup_base)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    success_count = 0
    failure_count = 0
    
    for source in source_dirs:
        source_path = Path(source)
        if not source_path.exists():
            print(f"✗ Source does not exist: {source}")
            failure_count += 1
            continue
            
        # Create timestamped backup structure
        backup_dest = backup_base / f"{source_path.name}_{timestamp}"
        
        print(f"Preparing backup structure: {source_path.name}")
        
        # Use duplicate_folder_structure.py
        cmd = [
            sys.executable, "duplicate_folder_structure.py",
            str(source_path), str(backup_dest),
            "--verbose", "--force"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Structure prepared: {backup_dest}")
            success_count += 1
        else:
            print(f"✗ Failed: {source_path.name}")
            print(f"  Error: {result.stderr}")
            failure_count += 1
    
    print(f"\nSummary: {success_count} successful, {failure_count} failed")
    return failure_count == 0

def main():
    parser = argparse.ArgumentParser(description="Prepare backup directory structures")
    parser.add_argument("sources", nargs="+", help="Source directories")
    parser.add_argument("--backup-base", required=True, help="Base backup directory")
    
    args = parser.parse_args()
    
    if prepare_backup_structures(args.sources, args.backup_base):
        print("All backup structures prepared successfully")
        sys.exit(0)
    else:
        print("Some operations failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Usage:
# python3 backup_prep.py /home/user /var/www /opt/apps --backup-base /backup/structures
```

## Error Handling and Recovery

### Comprehensive Error Handling

The tool includes robust error handling for common scenarios:

```bash
# Invalid source directory
python3 duplicate_folder_structure.py /nonexistent /dest
# Error: Source directory does not exist: /nonexistent

# Source is not a directory
python3 duplicate_folder_structure.py /etc/passwd /dest  
# Error: Source is not a directory: /etc/passwd

# Destination inside source (prevents infinite recursion)
python3 duplicate_folder_structure.py /parent /parent/child
# Error: Destination cannot be inside source directory

# Permission issues
python3 duplicate_folder_structure.py /restricted /dest
# Error: Permission denied accessing: /restricted/private
```

### Recovery and Cleanup

```python
# Example recovery script for partial failures
import shutil
from pathlib import Path

def cleanup_partial_structure(failed_destination):
    """Clean up partially created structure after failure."""
    dest_path = Path(failed_destination)
    
    if dest_path.exists() and dest_path.is_dir():
        # Check if directory is empty or only contains empty subdirectories
        if is_empty_structure(dest_path):
            print(f"Cleaning up partial structure: {dest_path}")
            shutil.rmtree(dest_path)
            return True
    
    return False

def is_empty_structure(directory):
    """Check if directory structure contains only empty directories."""
    for item in directory.rglob('*'):
        if item.is_file():
            return False  # Found a file
    return True

# Usage after failed operation
cleanup_partial_structure("/failed/backup/structure")
```

## Performance Considerations

### Optimization for Large Directory Trees

```bash
# For very large directory structures, use verbose mode to track progress
python3 duplicate_folder_structure.py /massive/dataset /backup \
    --verbose \
    2>&1 | tee duplication.log

# Monitor system resources during operation
# The tool is memory-efficient and processes directories incrementally
```

### Benchmarking and Performance

```python
#!/usr/bin/env python3
"""Benchmark duplicate_folder_structure.py performance"""

import time
import subprocess
import sys
from pathlib import Path

def benchmark_duplication(source, destination_base, iterations=3):
    """Benchmark directory structure duplication."""
    
    times = []
    
    for i in range(iterations):
        dest = f"{destination_base}_test_{i}"
        
        # Clean up any existing destination
        if Path(dest).exists():
            shutil.rmtree(dest)
        
        start_time = time.time()
        
        result = subprocess.run([
            sys.executable, "duplicate_folder_structure.py",
            source, dest, "--force"
        ], capture_output=True)
        
        end_time = time.time()
        
        if result.returncode == 0:
            duration = end_time - start_time
            times.append(duration)
            print(f"Iteration {i+1}: {duration:.2f} seconds")
        else:
            print(f"Iteration {i+1}: FAILED")
    
    if times:
        avg_time = sum(times) / len(times)
        print(f"Average time: {avg_time:.2f} seconds")
        return avg_time
    
    return None

# Usage
benchmark_duplication("/large/source", "/tmp/benchmark")
```

## Best Practices

### Directory Structure Planning
1. **Test First** - Always use `--dry-run` to preview operations
2. **Use Descriptive Names** - Choose clear suffix/prefix patterns  
3. **Validate Paths** - Ensure source paths are correct before execution
4. **Check Permissions** - Verify write access to destination areas

### Automation Integration
1. **Use --force Flag** - For automated scripts to skip prompts
2. **Capture Output** - Log operations for audit trails
3. **Error Handling** - Check return codes and handle failures
4. **Progress Monitoring** - Use verbose mode for long operations

### Safety Procedures
1. **Backup Important Paths** - Don't duplicate over critical directories
2. **Test on Copies** - Test with non-critical data first
3. **Monitor Disk Space** - Ensure adequate space for new structures
4. **Document Operations** - Keep records of structure duplications

---

*duplicate_folder_structure.py provides efficient, safe directory structure duplication with comprehensive features for template creation, backup preparation, and parallel environment setup workflows.*