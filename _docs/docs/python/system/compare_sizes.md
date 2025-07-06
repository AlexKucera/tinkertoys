# compareSizes.py

Compare file sizes or checksums between two directories for files with matching names, identifying corrupted or incomplete file copies with advanced verification options.

## Overview

compareSizes.py is a powerful file integrity verification tool that compares files between two directories using either file sizes or cryptographic checksums. It's designed to identify corrupted files, incomplete transfers, and data integrity issues in backup and synchronization workflows.

## Features

- **Dual Verification Modes** - File size comparison or cryptographic checksum validation
- **Multiple Hash Algorithms** - Blake2b, SHA256, MD5, and SHA1 support
- **Progress Tracking** - Real-time progress bars for large operations
- **Automatic Script Generation** - Creates copy scripts to fix mismatches
- **Comprehensive Reporting** - Detailed mismatch reports with statistics
- **Performance Optimized** - Efficient handling of large file sets
- **Security Hardened** - Uses modern, secure hash algorithms by default

## Usage

### Basic Usage
```bash
# Basic size comparison
python3 compareSizes.py /source/dir /dest/dir

# Compare only specific file types
python3 compareSizes.py /source/dir /dest/dir --filter .mov

# Use checksum comparison (more accurate but slower)
python3 compareSizes.py /source/dir /dest/dir --checksum
```

### Advanced Usage
```bash
# Use different hash algorithm
python3 compareSizes.py /source/dir /dest/dir \
    --checksum \
    --hash-algorithm sha256

# Generate script to fix mismatches
python3 compareSizes.py /source/dir /dest/dir \
    --generate-script

# Save detailed report and show verbose output
python3 compareSizes.py /source/dir /dest/dir \
    --output report.txt \
    --verbose
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `source_dir` | - | Source directory (copied from) | Required |
| `dest_dir` | - | Destination directory (copied to) | Required |
| `--filter` | `-f` | File extension filter (e.g., .mov, .txt, .jpg) | None |
| `--checksum` | - | Use checksum comparison instead of file size | False |
| `--hash-algorithm` | - | Hash algorithm for checksum comparison | `blake2b` |
| `--generate-script` | - | Generate Python script to copy mismatched files | False |
| `--output` | `-o` | Output file for detailed mismatch report | None |
| `--verbose` | `-v` | Show detailed output including file paths | False |

## Comparison Modes

### Size Comparison (Default)
Fast comparison using file sizes only:
- **Speed** - Very fast, no file content reading required
- **Accuracy** - Good for detecting truncated or incomplete files
- **Use Case** - Initial validation, large dataset screening

### Checksum Comparison (--checksum)
Cryptographic comparison using file content hashes:
- **Speed** - Slower, requires reading entire file contents
- **Accuracy** - Detects any content differences, even same-size corruption
- **Use Case** - Critical data validation, final verification

## Hash Algorithms

### Available Algorithms

| Algorithm | Speed | Security | Use Case |
|-----------|-------|----------|----------|
| `blake2b` | Fast | High | General purpose (default) |
| `sha256` | Medium | High | Standards compliance |
| `md5` | Very Fast | Low | Legacy compatibility only |
| `sha1` | Fast | Medium | Legacy systems |

### Algorithm Selection
```bash
# High security validation
python3 compareSizes.py /source /dest --checksum --hash-algorithm sha256

# Fast validation for large datasets
python3 compareSizes.py /source /dest --checksum --hash-algorithm blake2b

# Legacy system compatibility
python3 compareSizes.py /source /dest --checksum --hash-algorithm md5
```

## Output Formats

### Console Output
```
Comparing directories:
  Source:      /backup/media
  Destination: /archive/media
  Filter:      .mov

Scanning: /backup/media
Found 150 files in source directory

Scanning: /archive/media
Found 148 files in destination directory

Found 148 files with matching names
Using file size comparison

⚠ Found 3 mismatches:

File: movie_001.mov
  Source size:      2,847,392,816 bytes
  Destination size: 2,847,392,000 bytes

File: movie_002.mov
  Source size:      1,954,725,632 bytes
  Destination size: 1,954,720,000 bytes

File: movie_003.mov
  Source size:      3,247,891,456 bytes
  Destination size: 3,247,891,456 bytes

========================================
SUMMARY:
  Files compared: 148
  Mismatches:     3
  Success rate:   97.9%
```

### Checksum Output
```
WARNING: Checksum comparison can be very slow for large files!
Consider testing with a small subset first.

Comparing directories:
  Source:      /important/docs
  Destination: /backup/docs

Using blake2b checksum comparison (this may take a while...)
Comparing files: 100%|████████████| 1250/1250 [02:15<00:00,  9.23it/s]

⚠ Found 2 mismatches:

File: document.pdf
  Source checksum:      a1b2c3d4e5f6...
  Destination checksum: f6e5d4c3b2a1...

File: spreadsheet.xlsx
  Source checksum:      123456789abc...
  Destination checksum: cba987654321...
```

## Script Generation

### Automatic Fix Scripts
The `--generate-script` option creates executable Python scripts to fix mismatches:

```bash
python3 compareSizes.py /source /dest --generate-script
```

Creates `fix_mismatches.py`:
```python
#!/usr/bin/env python3
"""Auto-generated script to fix file mismatches."""
import shutil
import os

def copy_file_with_backup(src, dst):
    """Copy file with backup of existing destination."""
    if os.path.exists(dst):
        backup_path = dst + '.backup'
        shutil.copy2(dst, backup_path)
        print(f"Backed up {dst} to {backup_path}")
    
    shutil.copy2(src, dst)
    print(f"Copied {src} to {dst}")

def main():
    print("Fixing 3 mismatched files...")
    
    # movie_001.mov
    copy_file_with_backup(r"/source/movie_001.mov", r"/dest/movie_001.mov")
    
    # movie_002.mov
    copy_file_with_backup(r"/source/movie_002.mov", r"/dest/movie_002.mov")
    
    print("All files copied successfully!")

if __name__ == "__main__":
    main()
```

## Examples

### Example 1: Media Archive Validation
```bash
# Validate video archive integrity
python3 compareSizes.py /production/footage /archive/footage \
    --filter .mov \
    --verbose \
    --output archive_validation.txt
```

### Example 2: Critical Data Verification
```bash
# High-security checksum validation
python3 compareSizes.py /sensitive/data /backup/data \
    --checksum \
    --hash-algorithm sha256 \
    --generate-script
```

### Example 3: Incremental Backup Check
```bash
#!/bin/bash
# Daily backup integrity check

SOURCE="/home/user/documents"
BACKUP="/mnt/backup/documents" 
REPORT="/var/log/backup_integrity_$(date +%Y%m%d).txt"

echo "Checking backup integrity: $(date)" | tee "$REPORT"

python3 compareSizes.py "$SOURCE" "$BACKUP" \
    --output "$REPORT" \
    --verbose

if [ $? -eq 0 ]; then
    echo "Backup integrity check passed" | tee -a "$REPORT"
else
    echo "Backup integrity issues found" | tee -a "$REPORT"
    # Send alert email
    mail -s "Backup Integrity Alert" admin@company.com < "$REPORT"
fi
```

### Example 4: Large Dataset Screening
```bash
# Fast screening of large video archive
python3 compareSizes.py /terabyte/archive /mirror/archive \
    --filter .mov \
    --verbose

# Follow up with checksum validation for mismatches only
if [ $? -ne 0 ]; then
    echo "Size mismatches found. Running checksum validation..."
    python3 compareSizes.py /terabyte/archive /mirror/archive \
        --filter .mov \
        --checksum \
        --hash-algorithm blake2b
fi
```

## Performance Optimization

### Large File Handling
- **Progress Bars** - Visual feedback for long operations using tqdm
- **Streaming Hashes** - Memory-efficient hash calculation
- **Interrupt Handling** - Graceful cancellation with Ctrl+C
- **Resume Capability** - Can restart interrupted operations

### Memory Management
```python
# Internal optimization features:
# - Files processed one at a time
# - Hash calculations use streaming approach
# - Memory usage independent of file size
# - Efficient directory scanning
```

### Network Filesystems
- **Batch Operations** - Reduces network round trips
- **Metadata Caching** - Leverages filesystem caching
- **Error Recovery** - Handles network timeouts gracefully

## Integration

### Backup Validation Workflow
```python
import subprocess
import sys

def validate_backup_integrity(source, destination, use_checksum=False):
    """Validate backup using compareSizes script."""
    cmd = [
        sys.executable, "compareSizes.py",
        source, destination
    ]
    
    if use_checksum:
        cmd.extend(["--checksum", "--hash-algorithm", "blake2b"])
    
    cmd.extend(["--verbose"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    return {
        'success': result.returncode == 0,
        'output': result.stdout,
        'errors': result.stderr
    }

# Usage
result = validate_backup_integrity("/data", "/backup", use_checksum=True)
if result['success']:
    print("Backup validation passed")
else:
    print(f"Backup validation failed: {result['errors']}")
```

### CI/CD Pipeline Integration
```yaml
# GitHub Actions example
name: Data Integrity Check
on:
  schedule:
    - cron: '0 3 * * *'  # Daily at 3 AM

jobs:
  integrity-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Mount storage
      run: |
        sudo mount /dev/storage1 /mnt/primary
        sudo mount /dev/storage2 /mnt/backup
        
    - name: Size comparison check
      run: |
        python3 compareSizes.py /mnt/primary /mnt/backup \
          --output size_check.txt \
          --verbose
          
    - name: Checksum verification (if size mismatches found)
      if: failure()
      run: |
        python3 compareSizes.py /mnt/primary /mnt/backup \
          --checksum \
          --hash-algorithm sha256 \
          --output checksum_check.txt \
          --generate-script
          
    - name: Upload reports
      uses: actions/upload-artifact@v2
      with:
        name: integrity-reports
        path: "*.txt"
```

### Production Monitoring
```bash
#!/bin/bash
# Production data integrity monitoring

ENVIRONMENTS=("staging" "production" "backup")
REPORT_DIR="/var/log/integrity_checks"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$REPORT_DIR"

for env in "${ENVIRONMENTS[@]}"; do
    echo "Checking $env environment..."
    
    SOURCE="/data/$env"
    MIRROR="/mirrors/$env"
    REPORT="$REPORT_DIR/${env}_integrity_$DATE.txt"
    
    # Fast size check first
    if python3 compareSizes.py "$SOURCE" "$MIRROR" \
        --output "$REPORT" \
        --verbose; then
        echo "$env: PASS - No integrity issues"
    else
        echo "$env: FAIL - Integrity issues detected"
        
        # Detailed checksum analysis
        python3 compareSizes.py "$SOURCE" "$MIRROR" \
            --checksum \
            --hash-algorithm blake2b \
            --output "${REPORT%.txt}_detailed.txt" \
            --generate-script
            
        # Alert operations team
        echo "Integrity issues in $env environment" | \
            mail -s "Data Integrity Alert: $env" ops-team@company.com \
            -A "$REPORT"
    fi
done
```

## Error Handling

### Common Issues

**Issue**: "No matching filenames found"
```
Solution: Check that both directories contain files with the same names
- Verify directory paths are correct
- Check if files have been renamed
- Use --verbose to see discovered files
```

**Issue**: Very slow checksum comparison
```
Solution: Optimize hash algorithm choice
python3 compareSizes.py /source /dest --checksum --hash-algorithm blake2b
```

**Issue**: Out of memory with large files
```
Solution: The script uses streaming hash calculation, but if issues persist:
- Check available system memory
- Process smaller subsets using --filter
- Monitor system resources during operation
```

### Debugging

Use verbose mode for detailed operation information:

```bash
python3 compareSizes.py /source /dest --verbose --checksum
```

This shows:
- Directory scanning progress
- File matching statistics
- Hash calculation progress
- Detailed mismatch information

## Best Practices

### Validation Strategy
1. **Tiered Approach** - Start with size comparison, then checksum critical files
2. **Regular Checks** - Schedule periodic integrity validation
3. **Documentation** - Keep logs of validation results
4. **Automation** - Integrate into backup and sync workflows

### Algorithm Selection
1. **Blake2b** - Best general-purpose choice (fast + secure)
2. **SHA256** - Use for compliance or interoperability requirements
3. **MD5** - Only for legacy system compatibility
4. **SHA1** - Avoid for new implementations (security concerns)

### Performance Tuning
1. **Filter Usage** - Use file filters to reduce dataset size
2. **Progress Monitoring** - Use verbose mode for long operations
3. **Resource Planning** - Account for CPU/I/O intensive operations
4. **Network Considerations** - Plan for bandwidth usage with checksums

---

*compareSizes.py provides comprehensive file integrity verification with multiple validation modes, modern hash algorithms, and automated fixing capabilities for data validation workflows.*