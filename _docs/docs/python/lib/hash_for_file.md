# hash_for_file.py

Multi-algorithm file hashing utilities with streaming support, performance optimization, and comprehensive error handling for file integrity verification.

## Overview

hash_for_file.py provides fast, secure file hashing capabilities supporting multiple cryptographic algorithms. The module is designed for file integrity verification, deduplication, and content validation workflows with optimal performance for files of any size.

## Features

- **Multiple Hash Algorithms** - Blake2b, SHA256, SHA1, MD5 support
- **Streaming Processing** - Memory-efficient handling of large files
- **Performance Optimized** - Configurable buffer sizes for optimal I/O
- **Error Handling** - Comprehensive error management and reporting
- **Legacy Compatibility** - Backward compatibility with existing code
- **Modern Defaults** - Blake2b as secure, fast default algorithm

## Supported Algorithms

| Algorithm | Speed | Security | Use Case |
|-----------|-------|----------|----------|
| `blake2b` | Very Fast | High | **Recommended default** - Best balance of speed and security |
| `sha256` | Medium | High | Standards compliance, regulatory requirements |
| `sha1` | Fast | Medium | Legacy compatibility (avoid for new projects) |
| `md5` | Very Fast | Low | Legacy systems only (not cryptographically secure) |

## Usage

### Basic Usage
```python
from hash_for_file import hash_for_file

# Using default Blake2b algorithm
file_hash = hash_for_file("/path/to/file.txt")
print(f"Blake2b hash: {file_hash}")

# Specify algorithm
sha256_hash = hash_for_file("/path/to/file.txt", "sha256")
print(f"SHA256 hash: {sha256_hash}")

# Custom buffer size for performance tuning
hash_value = hash_for_file("/path/to/large_file.bin", "blake2b", 16384)
```

### Advanced Usage
```python
import os
from hash_for_file import hash_for_file

def verify_file_integrity(file_path, expected_hash, algorithm="blake2b"):
    """Verify file integrity against expected hash."""
    try:
        actual_hash = hash_for_file(file_path, algorithm)
        return actual_hash == expected_hash
    except RuntimeError as e:
        print(f"Hash verification failed: {e}")
        return False

def compare_files(file1, file2, algorithm="blake2b"):
    """Compare two files using hash comparison."""
    hash1 = hash_for_file(file1, algorithm)
    hash2 = hash_for_file(file2, algorithm)
    return hash1 == hash2

def get_file_fingerprint(file_path):
    """Get comprehensive file fingerprint."""
    stat = os.stat(file_path)
    return {
        'blake2b': hash_for_file(file_path, 'blake2b'),
        'sha256': hash_for_file(file_path, 'sha256'),
        'size': stat.st_size,
        'modified': stat.st_mtime
    }
```

## API Reference

### hash_for_file(file_path, algorithm='blake2b', block_size=8192)

Calculate hash for a file using specified algorithm.

**Parameters:**
- `file_path` (str): Path to the file to hash
- `algorithm` (str): Hash algorithm ('blake2b', 'sha256', 'sha1', 'md5')
- `block_size` (int): Buffer size for file reading (default: 8192 bytes)

**Returns:**
- `str`: Hexadecimal hash string

**Raises:**
- `ValueError`: If algorithm is not supported
- `RuntimeError`: If file cannot be read or processed

**Example:**
```python
# Basic usage with defaults
hash_value = hash_for_file("document.pdf")

# High-security hashing
secure_hash = hash_for_file("sensitive.doc", "sha256")

# Performance optimized for large files
large_file_hash = hash_for_file("video.mp4", "blake2b", 65536)
```

### hash_for_file_legacy(fileName, block_size=8192)

Legacy SHA1 hash function for backward compatibility.

**Parameters:**
- `fileName` (str): Path to file (legacy parameter name)
- `block_size` (int): Buffer size for reading

**Returns:**
- `str`: SHA1 hash as hexadecimal string

**Note:** This function is provided for backward compatibility only. Use `hash_for_file()` with explicit algorithm for new code.

## Performance Optimization

### Buffer Size Selection
Choose buffer size based on file characteristics and system:

```python
# Small files (< 1MB) - default buffer
hash_for_file("config.txt")  # Uses 8192 bytes

# Medium files (1MB - 100MB) - larger buffer
hash_for_file("document.pdf", "blake2b", 32768)  # 32KB buffer

# Large files (> 100MB) - maximum buffer
hash_for_file("video.mp4", "blake2b", 1048576)  # 1MB buffer

# SSD vs HDD optimization
if is_ssd_storage(file_path):
    buffer_size = 1048576  # 1MB for SSD
else:
    buffer_size = 65536    # 64KB for HDD

hash_value = hash_for_file(file_path, "blake2b", buffer_size)
```

### Algorithm Performance Comparison
```python
import time
from hash_for_file import hash_for_file

def benchmark_algorithms(file_path):
    """Benchmark different hash algorithms."""
    algorithms = ["blake2b", "sha256", "sha1", "md5"]
    results = {}
    
    for algorithm in algorithms:
        start_time = time.time()
        hash_value = hash_for_file(file_path, algorithm)
        end_time = time.time()
        
        results[algorithm] = {
            'hash': hash_value,
            'time': end_time - start_time
        }
    
    return results

# Example output:
# {
#     'blake2b': {'hash': 'a1b2c3...', 'time': 0.125},
#     'sha256':  {'hash': 'd4e5f6...', 'time': 0.203},
#     'sha1':    {'hash': 'g7h8i9...', 'time': 0.156},
#     'md5':     {'hash': 'j0k1l2...', 'time': 0.089}
# }
```

## Integration Examples

### File Deduplication
```python
import os
from collections import defaultdict
from hash_for_file import hash_for_file

def find_duplicate_files(directory):
    """Find duplicate files by hash comparison."""
    hash_to_files = defaultdict(list)
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                file_hash = hash_for_file(file_path, "blake2b")
                hash_to_files[file_hash].append(file_path)
            except RuntimeError as e:
                print(f"Error hashing {file_path}: {e}")
    
    # Return only groups with duplicates
    duplicates = {k: v for k, v in hash_to_files.items() if len(v) > 1}
    return duplicates

# Usage
duplicates = find_duplicate_files("/home/user/documents")
for hash_value, file_list in duplicates.items():
    print(f"Duplicate files (hash: {hash_value[:16]}...):")
    for file_path in file_list:
        print(f"  {file_path}")
```

### Backup Verification
```python
from hash_for_file import hash_for_file

class BackupVerifier:
    def __init__(self, algorithm="blake2b"):
        self.algorithm = algorithm
        self.hash_database = {}
    
    def create_baseline(self, directory):
        """Create hash database for backup verification."""
        for root, dirs, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, directory)
                
                try:
                    file_hash = hash_for_file(file_path, self.algorithm)
                    self.hash_database[relative_path] = file_hash
                except RuntimeError as e:
                    print(f"Warning: Could not hash {file_path}: {e}")
    
    def verify_backup(self, backup_directory):
        """Verify backup against baseline hashes."""
        results = {
            'verified': [],
            'corrupted': [],
            'missing': []
        }
        
        # Check each file in baseline
        for relative_path, expected_hash in self.hash_database.items():
            backup_file = os.path.join(backup_directory, relative_path)
            
            if not os.path.exists(backup_file):
                results['missing'].append(relative_path)
                continue
            
            try:
                actual_hash = hash_for_file(backup_file, self.algorithm)
                if actual_hash == expected_hash:
                    results['verified'].append(relative_path)
                else:
                    results['corrupted'].append(relative_path)
            except RuntimeError as e:
                results['corrupted'].append(relative_path)
        
        return results

# Usage
verifier = BackupVerifier("sha256")
verifier.create_baseline("/important/data")
results = verifier.verify_backup("/backup/data")

print(f"Verified: {len(results['verified'])} files")
print(f"Corrupted: {len(results['corrupted'])} files")
print(f"Missing: {len(results['missing'])} files")
```

### Content-Based File Organization
```python
import shutil
from pathlib import Path
from hash_for_file import hash_for_file

def organize_by_content(source_dir, target_dir):
    """Organize files by content hash to eliminate duplicates."""
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    target_path.mkdir(exist_ok=True)
    
    processed_hashes = set()
    stats = {'processed': 0, 'duplicates': 0, 'errors': 0}
    
    for file_path in source_path.rglob('*'):
        if not file_path.is_file():
            continue
        
        try:
            file_hash = hash_for_file(str(file_path), "blake2b")
            stats['processed'] += 1
            
            if file_hash in processed_hashes:
                stats['duplicates'] += 1
                print(f"Duplicate found: {file_path} (hash: {file_hash[:16]}...)")
                continue
            
            # Create organized path: first 2 chars / next 2 chars / hash.ext
            hash_dir = target_path / file_hash[:2] / file_hash[2:4]
            hash_dir.mkdir(parents=True, exist_ok=True)
            
            target_file = hash_dir / f"{file_hash}{file_path.suffix}"
            shutil.copy2(file_path, target_file)
            
            processed_hashes.add(file_hash)
            
        except RuntimeError as e:
            stats['errors'] += 1
            print(f"Error processing {file_path}: {e}")
    
    return stats

# Usage
stats = organize_by_content("/messy/photos", "/organized/photos")
print(f"Processed: {stats['processed']}, Duplicates: {stats['duplicates']}, Errors: {stats['errors']}")
```

## Error Handling

### Common Exceptions
```python
from hash_for_file import hash_for_file

def safe_hash_file(file_path, algorithm="blake2b"):
    """Safely hash a file with comprehensive error handling."""
    try:
        return hash_for_file(file_path, algorithm)
    
    except ValueError as e:
        print(f"Invalid algorithm or parameters: {e}")
        return None
    
    except RuntimeError as e:
        if "No such file" in str(e):
            print(f"File not found: {file_path}")
        elif "Permission denied" in str(e):
            print(f"Permission denied: {file_path}")
        elif "Is a directory" in str(e):
            print(f"Path is a directory: {file_path}")
        else:
            print(f"Runtime error: {e}")
        return None
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage with error handling
result = safe_hash_file("/path/to/file.txt")
if result:
    print(f"Hash: {result}")
else:
    print("Hashing failed")
```

### Validation and Recovery
```python
def validate_and_retry_hash(file_path, max_retries=3):
    """Validate file and retry hashing if needed."""
    import os
    import time
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    
    for attempt in range(max_retries):
        try:
            return hash_for_file(file_path, "blake2b")
        
        except RuntimeError as e:
            if attempt == max_retries - 1:
                raise e
            
            print(f"Retry {attempt + 1}/{max_retries} for {file_path}")
            time.sleep(1)  # Brief delay before retry
    
    return None
```

## Performance Considerations

### Memory Usage
- **Constant Memory** - Memory usage independent of file size
- **Streaming Processing** - Files processed in small chunks
- **Buffer Optimization** - Configurable buffer sizes for different scenarios

### I/O Optimization
```python
# Optimize for different storage types
def get_optimal_buffer_size(file_path):
    """Determine optimal buffer size based on file and storage characteristics."""
    import os
    
    file_size = os.path.getsize(file_path)
    
    # Small files
    if file_size < 1024 * 1024:  # < 1MB
        return 8192  # 8KB
    
    # Medium files
    elif file_size < 100 * 1024 * 1024:  # < 100MB
        return 65536  # 64KB
    
    # Large files
    else:
        return 1048576  # 1MB

# Usage
optimal_buffer = get_optimal_buffer_size("/path/to/file")
hash_value = hash_for_file("/path/to/file", "blake2b", optimal_buffer)
```

### Concurrent Processing
```python
import concurrent.futures
from hash_for_file import hash_for_file

def hash_files_concurrently(file_list, algorithm="blake2b", max_workers=4):
    """Hash multiple files concurrently for better performance."""
    def hash_single_file(file_path):
        try:
            return file_path, hash_for_file(file_path, algorithm)
        except RuntimeError as e:
            return file_path, f"ERROR: {e}"
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {
            executor.submit(hash_single_file, file_path): file_path 
            for file_path in file_list
        }
        
        for future in concurrent.futures.as_completed(future_to_file):
            file_path, result = future.result()
            results[file_path] = result
    
    return results

# Usage
file_list = ["/path/file1.txt", "/path/file2.txt", "/path/file3.txt"]
hashes = hash_files_concurrently(file_list)
```

## Migration from Legacy Versions

### Updating Existing Code
```python
# Old code using SHA1
from hash_for_file import hash_for_file_legacy
old_hash = hash_for_file_legacy("/path/to/file")

# New code with explicit algorithm
from hash_for_file import hash_for_file
new_hash = hash_for_file("/path/to/file", "sha1")  # Same result
secure_hash = hash_for_file("/path/to/file", "blake2b")  # Better security
```

### Batch Migration Script
```python
def migrate_hash_database(old_db_file, new_db_file):
    """Migrate hash database from SHA1 to Blake2b."""
    import json
    
    # Load old database
    with open(old_db_file, 'r') as f:
        old_db = json.load(f)
    
    # Migrate to new hashes
    new_db = {}
    for file_path, old_sha1_hash in old_db.items():
        if os.path.exists(file_path):
            try:
                new_hash = hash_for_file(file_path, "blake2b")
                new_db[file_path] = {
                    'blake2b': new_hash,
                    'sha1_legacy': old_sha1_hash  # Keep for reference
                }
            except RuntimeError as e:
                print(f"Could not migrate {file_path}: {e}")
    
    # Save new database
    with open(new_db_file, 'w') as f:
        json.dump(new_db, f, indent=2)
```

---

*hash_for_file.py provides secure, high-performance file hashing with multiple algorithm support, streaming processing, and comprehensive error handling for all file integrity verification needs.*