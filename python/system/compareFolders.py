#!/usr/bin/env python3
# encoding: utf-8
"""
compareFolders.py

Compare two directories and find files that exist in one but not the other.
Useful for verifying file copies and identifying missing files.

Created by Alexander Kucera on 2013-05-22.
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Set, Tuple


def scan_directory(directory: str, filter_extension: str = None, 
                  include_subdirs: bool = True) -> Tuple[List[str], List[str]]:
    """Scan directory and return lists of filenames and full paths.
    
    Args:
        directory: Directory to scan
        filter_extension: File extension filter (e.g., '.mov', '.txt')
        include_subdirs: Whether to scan subdirectories recursively
        
    Returns:
        Tuple of (filenames, full_paths)
    """
    filenames = []
    full_paths = []
    
    directory_path = Path(directory)
    
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    
    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    print(f"Scanning: {directory}")
    
    if include_subdirs:
        # Recursive scan
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if not filter_extension or filename.lower().endswith(filter_extension.lower()):
                    filenames.append(filename)
                    full_paths.append(os.path.join(root, filename))
    else:
        # Non-recursive scan
        for item in directory_path.iterdir():
            if item.is_file():
                filename = item.name
                if not filter_extension or filename.lower().endswith(filter_extension.lower()):
                    filenames.append(filename)
                    full_paths.append(str(item))
    
    return filenames, full_paths


def find_differences(left_files: Set[str], right_files: Set[str], 
                    left_dir: str, right_dir: str) -> Tuple[List[str], List[str]]:
    """Find files that exist in one directory but not the other.
    
    Args:
        left_files: Set of filenames from left directory
        right_files: Set of filenames from right directory
        left_dir: Left directory name (for reporting)
        right_dir: Right directory name (for reporting)
        
    Returns:
        Tuple of (files_only_in_left, files_only_in_right)
    """
    only_in_left = sorted(list(left_files - right_files))
    only_in_right = sorted(list(right_files - left_files))
    
    return only_in_left, only_in_right


def write_differences_report(differences: List[str], output_file: str, 
                           append_mode: bool = True):
    """Write differences to a report file.
    
    Args:
        differences: List of different filenames
        output_file: Output file path
        append_mode: Whether to append to existing file
    """
    mode = 'a' if append_mode else 'w'
    
    with open(output_file, mode, encoding='utf-8') as f:
        for filename in differences:
            f.write(f"{filename}\n")


def compare_directories(left_dir: str, right_dir: str, filter_extension: str = None,
                       output_file: str = None, include_subdirs: bool = True,
                       verbose: bool = False) -> Tuple[int, int]:
    """Compare two directories and find differences.
    
    Args:
        left_dir: First directory to compare
        right_dir: Second directory to compare  
        filter_extension: File extension filter
        output_file: Output file for differences report
        include_subdirs: Whether to scan subdirectories
        verbose: Show detailed output
        
    Returns:
        Tuple of (files_only_in_left_count, files_only_in_right_count)
    """
    print(f"Comparing directories:")
    print(f"  Left:  {left_dir}")
    print(f"  Right: {right_dir}")
    
    if filter_extension:
        print(f"  Filter: {filter_extension}")
    
    if not include_subdirs:
        print("  Mode: Non-recursive (top-level only)")
    
    print()
    
    # Scan both directories
    left_names, left_paths = scan_directory(left_dir, filter_extension, include_subdirs)
    print(f"Found {len(left_names)} files in left directory")
    
    right_names, right_paths = scan_directory(right_dir, filter_extension, include_subdirs)
    print(f"Found {len(right_names)} files in right directory")
    print()
    
    # Find differences
    left_set = set(left_names)
    right_set = set(right_names)
    
    only_in_left, only_in_right = find_differences(left_set, right_set, left_dir, right_dir)
    
    # Report results
    total_differences = len(only_in_left) + len(only_in_right)
    
    if total_differences == 0:
        print("✓ No differences found! All files match.")
        return 0, 0
    
    print(f"Found {total_differences} differences:")
    print()
    
    if only_in_left:
        print(f"Files only in LEFT directory ({len(only_in_left)} files):")
        print(f"  {left_dir}")
        for filename in only_in_left:
            print(f"    {filename}")
        print()
    
    if only_in_right:
        print(f"Files only in RIGHT directory ({len(only_in_right)} files):")
        print(f"  {right_dir}")
        for filename in only_in_right:
            print(f"    {filename}")
        print()
    
    # Write report file if requested
    if output_file:
        all_differences = []
        
        if only_in_left:
            all_differences.append(f"# Files only in: {left_dir}")
            all_differences.extend(only_in_left)
            all_differences.append("")
        
        if only_in_right:
            all_differences.append(f"# Files only in: {right_dir}")
            all_differences.extend(only_in_right)
        
        write_differences_report(all_differences, output_file, append_mode=False)
        print(f"Differences report written to: {output_file}")
    
    return len(only_in_left), len(only_in_right)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Compare two directories and find files that exist in one but not the other.",
        epilog="""
Examples:
  # Basic comparison
  %(prog)s /path/to/source /path/to/destination
  
  # Compare only .mov files
  %(prog)s /path/to/source /path/to/destination --filter .mov
  
  # Non-recursive comparison (top-level only)
  %(prog)s /path/to/source /path/to/destination --no-subdirs
  
  # Save differences to file
  %(prog)s /path/to/source /path/to/destination --output differences.txt
  
  # Verbose output
  %(prog)s /path/to/source /path/to/destination --verbose
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "left_dir",
        help="First directory to compare (source)"
    )
    parser.add_argument(
        "right_dir", 
        help="Second directory to compare (destination)"
    )
    parser.add_argument(
        "--filter", "-f",
        help="File extension filter (e.g., .mov, .txt, .jpg)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for differences report"
    )
    parser.add_argument(
        "--no-subdirs",
        action="store_true",
        help="Don't scan subdirectories recursively"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    try:
        args = parser.parse_args()
        
        # Set default output file
        output_file = args.output
        if not output_file:
            output_file = os.path.expanduser("~/folder-differences.txt")
            print(f"Default output file: {output_file}")
            print()
        
        # Compare directories
        left_count, right_count = compare_directories(
            args.left_dir,
            args.right_dir,
            filter_extension=args.filter,
            output_file=output_file,
            include_subdirs=not args.no_subdirs,
            verbose=args.verbose
        )
        
        # Summary
        total_diff = left_count + right_count
        if total_diff > 0:
            print("=" * 60)
            print("SUMMARY:")
            print(f"  Files only in left:  {left_count}")
            print(f"  Files only in right: {right_count}")
            print(f"  Total differences:   {total_diff}")
            return 1  # Exit code 1 indicates differences found
        else:
            return 0  # Exit code 0 indicates no differences
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())