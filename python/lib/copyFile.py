#!/usr/bin/env python3
# encoding: utf-8
"""
copyFile.py

Advanced file copying utilities with optimized buffering and error handling.

Created by Alexander Kucera on 2013-05-23.
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import os
import shutil
import stat
from pathlib import Path
from typing import Union, Optional, Callable


def copy_file(src: Union[str, Path], dst: Union[str, Path], 
              buffer_size: int = 10485760, preserve_file_date: bool = True,
              create_dirs: bool = True, overwrite: bool = True,
              progress_callback: Optional[Callable[[int, int], None]] = None) -> bool:
    """Copy a file to a new location with optimized buffering.
    
    Much faster performance than standard copy due to use of larger buffer
    and optimized buffer sizing based on file size.
    
    Args:
        src: Source file path
        dst: Destination file path (not directory)
        buffer_size: Buffer size to use during copy (default: 10MB)
        preserve_file_date: Preserve the original file date and permissions
        create_dirs: Create destination directories if they don't exist
        overwrite: Whether to overwrite existing destination file
        progress_callback: Optional callback function for progress reporting
                          Called with (bytes_copied, total_size)
    
    Returns:
        True if copy was successful
        
    Raises:
        FileNotFoundError: If source file doesn't exist
        FileExistsError: If destination exists and overwrite=False
        OSError: If copy operation fails
        ValueError: If source and destination are the same file
    """
    src_path = Path(src).resolve()
    dst_path = Path(dst).resolve()
    
    # Check source file exists
    if not src_path.exists():
        raise FileNotFoundError(f"Source file not found: {src_path}")
    
    if not src_path.is_file():
        raise ValueError(f"Source is not a file: {src_path}")
    
    # Check if source and destination are the same
    try:
        if src_path.samefile(dst_path):
            raise ValueError(f"Source and destination are the same file: {src_path}")
    except (OSError, FileNotFoundError):
        # Destination doesn't exist yet, which is fine
        pass
    
    # Check if destination exists
    if dst_path.exists() and not overwrite:
        raise FileExistsError(f"Destination file exists: {dst_path}")
    
    # Create destination directory if needed
    if create_dirs:
        dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get file size for buffer optimization and progress tracking
    file_size = src_path.stat().st_size
    
    # Optimize buffer size for small files
    optimized_buffer = min(buffer_size, file_size) if file_size > 0 else 1024
    
    # Check for special files
    src_stat = src_path.stat()
    if stat.S_ISFIFO(src_stat.st_mode):
        raise ValueError(f"Source is a named pipe: {src_path}")
    
    if dst_path.exists():
        dst_stat = dst_path.stat()
        if stat.S_ISFIFO(dst_stat.st_mode):
            raise ValueError(f"Destination is a named pipe: {dst_path}")
    
    # Perform the copy with progress tracking
    bytes_copied = 0
    try:
        with open(src_path, 'rb') as fsrc:
            with open(dst_path, 'wb') as fdst:
                while True:
                    chunk = fsrc.read(optimized_buffer)
                    if not chunk:
                        break
                    
                    fdst.write(chunk)
                    bytes_copied += len(chunk)
                    
                    if progress_callback:
                        progress_callback(bytes_copied, file_size)
        
        # Preserve file metadata if requested
        if preserve_file_date:
            shutil.copystat(src_path, dst_path)
        
        return True
    
    except Exception as e:
        # Clean up partial file on error
        if dst_path.exists():
            try:
                dst_path.unlink()
            except OSError:
                pass
        raise OSError(f"Copy failed: {e}")


def copy_file_with_backup(src: Union[str, Path], dst: Union[str, Path],
                         backup_suffix: str = ".backup", **kwargs) -> bool:
    """Copy file with automatic backup of existing destination.
    
    Args:
        src: Source file path
        dst: Destination file path
        backup_suffix: Suffix for backup file
        **kwargs: Additional arguments passed to copy_file()
    
    Returns:
        True if copy was successful
    """
    dst_path = Path(dst)
    
    # Create backup if destination exists
    if dst_path.exists():
        backup_path = dst_path.with_suffix(dst_path.suffix + backup_suffix)
        
        # Handle existing backup
        counter = 1
        while backup_path.exists():
            backup_path = dst_path.with_suffix(f"{dst_path.suffix}{backup_suffix}.{counter}")
            counter += 1
        
        shutil.copy2(dst_path, backup_path)
    
    return copy_file(src, dst, **kwargs)


def verify_copy(src: Union[str, Path], dst: Union[str, Path],
               check_size: bool = True, check_hash: bool = False) -> bool:
    """Verify that a file copy was successful.
    
    Args:
        src: Source file path
        dst: Destination file path
        check_size: Check file sizes match
        check_hash: Check file contents match (slower)
    
    Returns:
        True if files match according to specified checks
    """
    src_path = Path(src)
    dst_path = Path(dst)
    
    if not src_path.exists() or not dst_path.exists():
        return False
    
    if check_size:
        src_size = src_path.stat().st_size
        dst_size = dst_path.stat().st_size
        if src_size != dst_size:
            return False
    
    if check_hash:
        import hashlib
        
        def file_hash(filepath):
            hasher = hashlib.blake2b()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        
        return file_hash(src_path) == file_hash(dst_path)
    
    return True


# Legacy function for backward compatibility
def copyFile(src, dst, buffer_size=10485760, perserveFileDate=True):
    """Legacy function for backward compatibility."""
    return copy_file(src, dst, buffer_size, perserveFileDate)