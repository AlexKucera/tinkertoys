#!/usr/bin/env python3
# encoding: utf-8
"""
keepLargerVersion.py

Keeps the larger of two identically named files. Doesn't care about file extensions.
If two files have the same size, the older one is kept.

This script finds duplicate files (by name without extension) and removes the smaller
version, keeping only the larger file. Useful for cleaning up duplicate downloads
or media files.

Created by Alexander Kucera
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


def find_duplicate_names(search_path: Path, extensions: List[str] = None) -> Dict[str, List[Path]]:
    """Find files with duplicate names (ignoring extensions).
    
    Args:
        search_path: Directory to search for duplicate files
        extensions: List of file extensions to include (None for all)
        
    Returns:
        Dictionary mapping base names to list of file paths
    """
    name_to_paths = defaultdict(list)
    
    if not search_path.exists():
        raise ValueError(f"Search path does not exist: {search_path}")
    
    if not search_path.is_dir():
        raise ValueError(f"Search path is not a directory: {search_path}")
    
    print(f"Scanning for files in: {search_path}")
    
    for file_path in search_path.rglob('*'):
        if file_path.is_file():
            # Check extension filter
            if extensions and file_path.suffix.lower() not in extensions:
                continue
                
            # Get base name without extension
            base_name = file_path.stem
            name_to_paths[base_name].append(file_path)
    
    # Filter to only duplicates
    duplicates = {name: paths for name, paths in name_to_paths.items() if len(paths) > 1}
    
    return duplicates


def analyze_duplicates(duplicates: Dict[str, List[Path]]) -> List[Tuple[str, List[Tuple[Path, int, float]]]]:
    """Analyze duplicate files and prepare removal decisions.
    
    Args:
        duplicates: Dictionary of duplicate file groups
        
    Returns:
        List of tuples containing (base_name, [(path, size, creation_time), ...])
    """
    analyzed = []
    
    for base_name, paths in duplicates.items():
        file_info = []
        
        for file_path in paths:
            try:
                stat = file_path.stat()
                file_info.append((file_path, stat.st_size, stat.st_ctime))
            except OSError as e:
                print(f"Warning: Could not stat {file_path}: {e}")
                continue
        
        if len(file_info) > 1:
            analyzed.append((base_name, file_info))
    
    return analyzed


def decide_which_to_keep(file_info: List[Tuple[Path, int, float]]) -> Tuple[Path, List[Path]]:
    """Decide which file to keep and which to remove.
    
    Args:
        file_info: List of (path, size, creation_time) tuples
        
    Returns:
        Tuple of (file_to_keep, files_to_remove)
    """
    # Sort by size (descending), then by creation time (ascending - older first)
    sorted_files = sorted(file_info, key=lambda x: (-x[1], x[2]))
    
    keep_file = sorted_files[0][0]
    remove_files = [info[0] for info in sorted_files[1:]]
    
    return keep_file, remove_files


def remove_duplicate_files(search_path: str, extensions: List[str] = None, 
                          dry_run: bool = True, verbose: bool = False) -> Tuple[int, int, int]:
    """Remove duplicate files, keeping the larger version.
    
    Args:
        search_path: Directory to search
        extensions: File extensions to include
        dry_run: If True, only show what would be done
        verbose: Show detailed information
        
    Returns:
        Tuple of (files_removed, duplicates_found, errors)
    """
    search_path_obj = Path(search_path).resolve()
    
    # Find duplicates
    duplicates = find_duplicate_names(search_path_obj, extensions)
    
    if not duplicates:
        print("No duplicate files found.")
        return 0, 0, 0
    
    print(f"Found {len(duplicates)} groups of duplicate files:")
    
    if verbose:
        for name, paths in duplicates.items():
            print(f"  {name}: {len(paths)} files")
    
    print()
    
    # Analyze duplicates
    analyzed = analyze_duplicates(duplicates)
    
    removed_count = 0
    error_count = 0
    
    for base_name, file_info in analyzed:
        print(f"Processing duplicate group: {base_name}")
        
        if len(file_info) < 2:
            print("  ⚠ Skipped: Could not analyze all files")
            continue
        
        keep_file, remove_files = decide_which_to_keep(file_info)
        
        # Show file details
        if verbose:
            print(f"  Files found:")
            for path, size, ctime in file_info:
                status = "KEEP" if path == keep_file else "REMOVE"
                print(f"    {status}: {path} ({size:,} bytes)")
        
        print(f"  → Keeping: {keep_file} ({keep_file.stat().st_size:,} bytes)")
        
        # Remove smaller files
        for remove_file in remove_files:
            try:
                file_size = remove_file.stat().st_size
                
                if dry_run:
                    print(f"  [DRY RUN] Would remove: {remove_file} ({file_size:,} bytes)")
                else:
                    remove_file.unlink()
                    print(f"  ✓ Removed: {remove_file} ({file_size:,} bytes)")
                
                removed_count += 1
                
            except OSError as e:
                print(f"  ✗ Error removing {remove_file}: {e}")
                error_count += 1
        
        print()
    
    return removed_count, len(duplicates), error_count


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Remove duplicate files, keeping the larger version.",
        epilog="""
Examples:
  # Dry run on a directory (recommended first)
  %(prog)s /path/to/media --dry-run
  
  # Actually remove duplicates
  %(prog)s /path/to/media --execute
  
  # Only process video files
  %(prog)s /path/to/media --extensions .mp4 .mkv .avi --execute
  
  # Verbose output
  %(prog)s /path/to/media --verbose --dry-run
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "search_path",
        help="Directory to search for duplicate files"
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        help="File extensions to include (e.g., .mp4 .mkv .avi)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Show what would be done without making changes (default)"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually remove the duplicate files (overrides --dry-run)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    try:
        args = parser.parse_args()
        
        # Determine if this is a dry run
        dry_run = not args.execute
        
        # Process extensions
        extensions = None
        if args.extensions:
            extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                         for ext in args.extensions]
            print(f"Filtering for extensions: {', '.join(extensions)}")
        
        if dry_run:
            print("=" * 60)
            print("DRY RUN MODE - No files will be removed")
            print("Use --execute to actually remove duplicate files")
            print("=" * 60)
        else:
            print("=" * 60)
            print("EXECUTING REMOVAL - Files will be deleted!")
            print("=" * 60)
        
        print(f"Search path: {Path(args.search_path).resolve()}")
        print()
        
        # Process files
        removed, duplicates, errors = remove_duplicate_files(
            args.search_path, 
            extensions, 
            dry_run, 
            args.verbose
        )
        
        # Summary
        print("=" * 60)
        print("SUMMARY:")
        print(f"  Duplicate groups found: {duplicates}")
        if dry_run:
            print(f"  Would remove: {removed} files")
        else:
            print(f"  Removed: {removed} files")
        print(f"  Errors: {errors}")
        
        if dry_run and removed > 0:
            print(f"\nTo actually remove these files, run with --execute")
        
        # Calculate space saved
        if not dry_run and removed > 0:
            print(f"  Duplicate cleanup completed successfully!")
        
        return 0 if errors == 0 else 1
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())