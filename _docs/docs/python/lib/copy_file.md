# copyFile.py

Advanced file copying utilities with optimized buffering, progress tracking, verification, and comprehensive error handling for high-performance file operations.

## Overview

copyFile.py provides enterprise-grade file copying capabilities that outperform standard library functions through intelligent buffer optimization, progress tracking, and comprehensive verification features. Designed for scenarios requiring reliable, high-performance file operations with detailed reporting.

## Features

- **Optimized Performance** - Intelligent buffer sizing based on file characteristics
- **Progress Tracking** - Real-time progress callbacks for long operations
- **Verification Support** - Built-in file integrity verification
- **Backup Functionality** - Automatic backup creation with conflict resolution
- **Error Recovery** - Robust error handling with cleanup on failure
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Memory Efficient** - Constant memory usage regardless of file size

## Core Functions

### copy_file(src, dst, **options)

Advanced file copying with comprehensive options and optimizations.

**Parameters:**
- `src` (str/Path): Source file path
- `dst` (str/Path): Destination file path
- `buffer_size` (int): Buffer size for copying (default: 10MB)
- `preserve_file_date` (bool): Preserve original timestamps (default: True)
- `create_dirs` (bool): Create destination directories (default: True)
- `overwrite` (bool): Allow overwriting existing files (default: True)
- `progress_callback` (callable): Progress reporting function

**Returns:**
- `bool`: True if copy was successful

**Example:**
```python
from copyFile import copy_file

# Basic usage
success = copy_file("/source/file.txt", "/dest/file.txt")

# With progress tracking
def show_progress(bytes_copied, total_size):
    percent = (bytes_copied / total_size) * 100
    print(f"Progress: {percent:.1f}%")

copy_file(
    "/large/video.mp4", 
    "/backup/video.mp4",
    progress_callback=show_progress
)

# Optimized for specific scenarios
copy_file(
    "/source/database.db",
    "/backup/database.db", 
    buffer_size=1048576,  # 1MB buffer for large files
    preserve_file_date=True,
    create_dirs=True
)
```

## Advanced Functions

### copy_file_with_backup(src, dst, backup_suffix=".backup", **kwargs)

Copy file with automatic backup of existing destination.

**Parameters:**
- `src` (str/Path): Source file path
- `dst` (str/Path): Destination file path  
- `backup_suffix` (str): Suffix for backup files
- `**kwargs`: Additional arguments passed to copy_file()

**Example:**
```python
from copyFile import copy_file_with_backup

# Creates backup if destination exists
copy_file_with_backup(
    "/new/config.json",
    "/app/config.json",
    backup_suffix=".bak"
)
# If /app/config.json exists, creates /app/config.json.bak
```

### verify_copy(src, dst, check_size=True, check_hash=False)

Verify that a file copy was successful.

**Parameters:**
- `src` (str/Path): Source file path
- `dst` (str/Path): Destination file path
- `check_size` (bool): Verify file sizes match
- `check_hash` (bool): Verify content hashes match (slower)

**Returns:**
- `bool`: True if files match according to specified checks

**Example:**
```python
from copyFile import copy_file, verify_copy

# Copy and verify
if copy_file("/important/data.db", "/backup/data.db"):
    if verify_copy("/important/data.db", "/backup/data.db", check_hash=True):
        print("Copy verified successfully")
    else:
        print("Copy verification failed!")
```

## Performance Optimization

### Buffer Size Selection

The copy functions automatically optimize buffer sizes, but you can tune for specific scenarios:

```python
from copyFile import copy_file

# Small files (< 1MB) - default buffer
copy_file("config.txt", "backup/config.txt")

# Medium files (1-100MB) - moderate buffer
copy_file(
    "document.pdf", 
    "backup/document.pdf",
    buffer_size=65536  # 64KB
)

# Large files (> 100MB) - large buffer
copy_file(
    "video.mp4",
    "backup/video.mp4", 
    buffer_size=1048576  # 1MB
)

# Network storage - optimized for network latency
copy_file(
    "local_file.dat",
    "/network/share/file.dat",
    buffer_size=2097152  # 2MB
)
```

### Performance Benchmarking

```python
import time
from copyFile import copy_file

def benchmark_copy_performance(source_file, dest_file, buffer_sizes):
    """Benchmark different buffer sizes for optimal performance."""
    results = {}
    
    for buffer_size in buffer_sizes:
        # Clean up any existing destination
        if os.path.exists(dest_file):
            os.remove(dest_file)
        
        start_time = time.time()
        success = copy_file(source_file, dest_file, buffer_size=buffer_size)
        end_time = time.time()
        
        if success:
            results[buffer_size] = end_time - start_time
            print(f"Buffer {buffer_size:8d}: {results[buffer_size]:.2f}s")
        else:
            print(f"Buffer {buffer_size:8d}: FAILED")
    
    return results

# Test different buffer sizes
buffer_sizes = [8192, 32768, 65536, 262144, 1048576]
results = benchmark_copy_performance(
    "/path/to/large_file.bin",
    "/tmp/test_copy.bin", 
    buffer_sizes
)

# Find optimal buffer size
optimal_buffer = min(results, key=results.get)
print(f"Optimal buffer size: {optimal_buffer} bytes")
```

## Progress Tracking

### Real-Time Progress Display

```python
import sys
from copyFile import copy_file

def progress_bar(bytes_copied, total_size, bar_length=50):
    """Display a progress bar in the terminal."""
    percent = bytes_copied / total_size
    filled = int(bar_length * percent)
    bar = '█' * filled + '-' * (bar_length - filled)
    
    # Clear line and show progress
    sys.stdout.write(f'\r[{bar}] {percent*100:.1f}% ')
    sys.stdout.write(f'({bytes_copied:,}/{total_size:,} bytes)')
    sys.stdout.flush()
    
    if bytes_copied == total_size:
        print()  # New line when complete

# Usage with progress bar
copy_file(
    "/large/dataset.zip", 
    "/backup/dataset.zip",
    progress_callback=progress_bar
)
```

### Detailed Progress Logging

```python
import logging
from datetime import datetime
from copyFile import copy_file

def detailed_progress_logger(bytes_copied, total_size):
    """Log detailed progress information."""
    percent = (bytes_copied / total_size) * 100
    mb_copied = bytes_copied / (1024 * 1024)
    mb_total = total_size / (1024 * 1024)
    
    logging.info(
        f"Copy progress: {percent:.1f}% "
        f"({mb_copied:.1f}/{mb_total:.1f} MB) "
        f"at {datetime.now().strftime('%H:%M:%S')}"
    )

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Copy with detailed logging
copy_file(
    "/source/large_file.bin",
    "/dest/large_file.bin",
    progress_callback=detailed_progress_logger
)
```

## Integration Examples

### Backup System Integration

```python
import os
import shutil
from pathlib import Path
from copyFile import copy_file_with_backup, verify_copy

class BackupManager:
    def __init__(self, source_dir, backup_dir):
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def backup_file(self, relative_path):
        """Backup a single file with verification."""
        source_file = self.source_dir / relative_path
        backup_file = self.backup_dir / relative_path
        
        # Create backup directory structure
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy with automatic backup of existing
        success = copy_file_with_backup(
            str(source_file),
            str(backup_file),
            backup_suffix=".old"
        )
        
        if success:
            # Verify the copy
            if verify_copy(str(source_file), str(backup_file), check_hash=True):
                return True
            else:
                print(f"Verification failed for {relative_path}")
                return False
        else:
            print(f"Copy failed for {relative_path}")
            return False
    
    def backup_directory(self, extensions=None):
        """Backup entire directory with optional file filtering."""
        success_count = 0
        failure_count = 0
        
        for file_path in self.source_dir.rglob('*'):
            if file_path.is_file():
                # Filter by extensions if specified
                if extensions and file_path.suffix.lower() not in extensions:
                    continue
                
                relative_path = file_path.relative_to(self.source_dir)
                
                if self.backup_file(relative_path):
                    success_count += 1
                    print(f"✓ Backed up: {relative_path}")
                else:
                    failure_count += 1
                    print(f"✗ Failed: {relative_path}")
        
        print(f"\nBackup complete: {success_count} successful, {failure_count} failed")
        return failure_count == 0

# Usage
backup_mgr = BackupManager("/important/documents", "/backup/documents")
backup_mgr.backup_directory(extensions=['.pdf', '.docx', '.xlsx'])
```

### Media Processing Pipeline

```python
import os
from copyFile import copy_file

class MediaProcessor:
    def __init__(self, input_dir, output_dir, temp_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        
        # Create directories
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(temp_dir, exist_ok=True)
    
    def process_video(self, video_file):
        """Process video file with staging through temp directory."""
        filename = os.path.basename(video_file)
        name, ext = os.path.splitext(filename)
        
        # Stage 1: Copy to temp for processing
        temp_file = os.path.join(self.temp_dir, filename)
        
        print(f"Staging {filename} for processing...")
        if not copy_file(
            video_file, 
            temp_file,
            buffer_size=2097152,  # 2MB buffer for video
            progress_callback=self._show_copy_progress
        ):
            print(f"Failed to stage {filename}")
            return False
        
        # Stage 2: Process video (placeholder)
        processed_file = os.path.join(self.temp_dir, f"{name}_processed{ext}")
        if not self._process_video_placeholder(temp_file, processed_file):
            print(f"Failed to process {filename}")
            return False
        
        # Stage 3: Copy to final destination
        output_file = os.path.join(self.output_dir, f"{name}_processed{ext}")
        
        print(f"Finalizing {filename}...")
        if copy_file(
            processed_file,
            output_file,
            buffer_size=2097152,
            progress_callback=self._show_copy_progress
        ):
            # Cleanup temp files
            os.remove(temp_file)
            os.remove(processed_file)
            print(f"✓ Completed: {filename}")
            return True
        else:
            print(f"Failed to finalize {filename}")
            return False
    
    def _show_copy_progress(self, bytes_copied, total_size):
        """Simple progress display."""
        percent = (bytes_copied / total_size) * 100
        if bytes_copied == total_size or percent % 10 < 1:  # Update every 10%
            print(f"  Progress: {percent:.0f}%")
    
    def _process_video_placeholder(self, input_file, output_file):
        """Placeholder for actual video processing."""
        # In real implementation, this would call ffmpeg, etc.
        return copy_file(input_file, output_file)

# Usage
processor = MediaProcessor("/input/videos", "/output/videos", "/tmp/processing")
processor.process_video("/input/videos/movie.mp4")
```

### Distributed File Synchronization

```python
import json
import hashlib
from pathlib import Path
from copyFile import copy_file, verify_copy

class FileSynchronizer:
    def __init__(self, local_dir, remote_dir, manifest_file="sync_manifest.json"):
        self.local_dir = Path(local_dir)
        self.remote_dir = Path(remote_dir)
        self.manifest_file = self.local_dir / manifest_file
        self.manifest = self._load_manifest()
    
    def _load_manifest(self):
        """Load synchronization manifest."""
        if self.manifest_file.exists():
            with open(self.manifest_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_manifest(self):
        """Save synchronization manifest."""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def _get_file_info(self, file_path):
        """Get file information for sync tracking."""
        stat = file_path.stat()
        return {
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'hash': self._calculate_hash(file_path)
        }
    
    def _calculate_hash(self, file_path):
        """Calculate file hash for comparison."""
        hasher = hashlib.blake2b()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def sync_to_remote(self):
        """Synchronize local files to remote location."""
        synced_count = 0
        
        for file_path in self.local_dir.rglob('*'):
            if file_path.is_file() and file_path.name != self.manifest_file.name:
                relative_path = str(file_path.relative_to(self.local_dir))
                remote_path = self.remote_dir / relative_path
                
                # Check if file needs syncing
                current_info = self._get_file_info(file_path)
                
                needs_sync = False
                if relative_path not in self.manifest:
                    needs_sync = True
                    print(f"New file: {relative_path}")
                elif self.manifest[relative_path] != current_info:
                    needs_sync = True
                    print(f"Modified file: {relative_path}")
                
                if needs_sync:
                    # Ensure remote directory exists
                    remote_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    if copy_file(str(file_path), str(remote_path)):
                        # Verify copy
                        if verify_copy(str(file_path), str(remote_path), check_hash=True):
                            self.manifest[relative_path] = current_info
                            synced_count += 1
                            print(f"✓ Synced: {relative_path}")
                        else:
                            print(f"✗ Verification failed: {relative_path}")
                    else:
                        print(f"✗ Copy failed: {relative_path}")
        
        self._save_manifest()
        print(f"\nSync complete: {synced_count} files updated")
        return synced_count

# Usage
sync = FileSynchronizer("/local/project", "/remote/backup")
sync.sync_to_remote()
```

## Error Handling and Recovery

### Comprehensive Error Handling

```python
import os
import shutil
from copyFile import copy_file, verify_copy

def robust_file_copy(source, destination, max_retries=3):
    """Copy file with retry logic and comprehensive error handling."""
    
    for attempt in range(max_retries):
        try:
            print(f"Copy attempt {attempt + 1}/{max_retries}")
            
            # Attempt copy
            success = copy_file(
                source, 
                destination,
                create_dirs=True,
                preserve_file_date=True
            )
            
            if not success:
                raise RuntimeError("Copy operation returned False")
            
            # Verify copy
            if not verify_copy(source, destination, check_size=True):
                raise RuntimeError("Copy verification failed")
            
            print(f"✓ Successfully copied: {source} -> {destination}")
            return True
            
        except FileNotFoundError:
            print(f"✗ Source file not found: {source}")
            return False
            
        except PermissionError as e:
            print(f"✗ Permission denied: {e}")
            if attempt < max_retries - 1:
                print("Waiting before retry...")
                time.sleep(2)
            else:
                return False
                
        except OSError as e:
            print(f"✗ System error: {e}")
            if attempt < max_retries - 1:
                # Clean up partial copy
                if os.path.exists(destination):
                    try:
                        os.remove(destination)
                    except OSError:
                        pass
                print("Retrying...")
                time.sleep(1)
            else:
                return False
                
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
    
    print(f"✗ Failed to copy after {max_retries} attempts")
    return False

# Usage with error handling
if robust_file_copy("/source/important.db", "/backup/important.db"):
    print("Backup completed successfully")
else:
    print("Backup failed - manual intervention required")
```

## Legacy Compatibility

### Backward Compatibility Function

```python
# Legacy function for existing code
def copyFile(src, dst, buffer_size=10485760, perserveFileDate=True):
    """Legacy function for backward compatibility."""
    return copy_file(
        src, 
        dst, 
        buffer_size=buffer_size, 
        preserve_file_date=perserveFileDate
    )

# Migration example
def migrate_legacy_code():
    """Example of migrating from legacy to new API."""
    
    # Old way
    success = copyFile("/old/file.txt", "/new/file.txt", 32768, True)
    
    # New way (recommended)
    success = copy_file(
        "/old/file.txt", 
        "/new/file.txt",
        buffer_size=32768,
        preserve_file_date=True,
        create_dirs=True,
        overwrite=True
    )
    
    return success
```

---

*copyFile.py provides enterprise-grade file copying with performance optimization, progress tracking, verification capabilities, and comprehensive error handling for reliable, high-performance file operations.*