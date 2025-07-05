#!/usr/bin/env python3
# encoding: utf-8
"""
hash_for_file.py

Calculate hash values for files using various algorithms.
"""

import hashlib
from typing import Union


def hash_for_file(file_path: str, algorithm: str = 'blake2b', block_size: int = 8192) -> str:
    """Calculate hash for a file.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (blake2b, sha256, sha1, md5)
        block_size: Block size for reading file
        
    Returns:
        Hexadecimal hash string
    """
    if algorithm == 'blake2b':
        hasher = hashlib.blake2b()
    elif algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    elif algorithm == 'md5':
        hasher = hashlib.md5()
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    try:
        with open(file_path, 'rb') as f:  # Open in binary mode
            for chunk in iter(lambda: f.read(block_size), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (OSError, IOError) as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}")


# Legacy function for backward compatibility
def hash_for_file_legacy(fileName, block_size=8192):
    """Legacy SHA1 hash function for backward compatibility."""
    return hash_for_file(fileName, 'sha1', block_size)
