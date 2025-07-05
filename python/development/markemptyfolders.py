#!/usr/bin/env python3
# encoding: utf-8
"""
markemptyfolders.py

Create placeholder files in empty directories to make them trackable with Git.
Git doesn't track empty directories, so this script creates .gitkeep or custom
placeholder files to preserve the directory structure in version control.

Created by Alexander Kucera on 2013-05-22.
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Set


def find_empty_directories(root_path: Path, exclude_dirs: Set[str] = None,
                          exclude_hidden: bool = True) -> List[Path]:
    """Find all empty directories in the given path.
    
    Args:
        root_path: Root directory to search
        exclude_dirs: Set of directory names to exclude (e.g., {'.git', '.svn'})
        exclude_hidden: Whether to exclude hidden directories
        
    Returns:
        List of empty directory paths
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', '.svn', '.hg', '__pycache__', '.DS_Store'}
    
    empty_directories = []
    
    for current_dir in root_path.rglob('*'):
        if not current_dir.is_dir():
            continue
            
        # Skip excluded directories
        if current_dir.name in exclude_dirs:
            continue
            
        # Skip hidden directories if requested
        if exclude_hidden and current_dir.name.startswith('.'):
            continue
            
        # Check if directory is empty (no files or subdirectories)
        try:
            contents = list(current_dir.iterdir())
            if not contents:
                empty_directories.append(current_dir)
        except (OSError, PermissionError):
            continue
    
    return empty_directories


def create_placeholder_file(directory: Path, filename: str = '.gitkeep',
                           content: str = None, verbose: bool = False) -> bool:
    """Create a placeholder file in the given directory.
    
    Args:
        directory: Directory where to create the placeholder
        filename: Name of the placeholder file
        content: Content for the placeholder file
        verbose: Show detailed output
        
    Returns:
        True if file was created successfully
    """
    if content is None:
        content = (
            "This is a placeholder file to keep this directory trackable with Git.\n"
            "Git doesn't track empty directories, so this file preserves the\n"
            "directory structure in version control.\n"
            "\n"
            "You can safely delete this file once the directory contains other files.\n"
        )
    
    placeholder_path = directory / filename
    
    # Don't overwrite existing files
    if placeholder_path.exists():
        if verbose:
            print(f"Placeholder already exists: {placeholder_path}")
        return False
    
    try:
        with open(placeholder_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        if verbose:
            print(f"Created: {placeholder_path}")
        
        return True
        
    except (OSError, PermissionError) as e:
        print(f"Error creating placeholder in {directory}: {e}")
        return False


def remove_placeholder_files(root_path: Path, filename: str = '.gitkeep',
                            verbose: bool = False) -> int:
    """Remove placeholder files from directories that are no longer empty.
    
    Args:
        root_path: Root directory to search
        filename: Name of placeholder files to remove
        verbose: Show detailed output
        
    Returns:
        Number of placeholder files removed
    """
    removed_count = 0
    
    for placeholder_path in root_path.rglob(filename):
        if not placeholder_path.is_file():
            continue
            
        directory = placeholder_path.parent
        
        # Count other files in the directory (excluding the placeholder)
        other_files = [f for f in directory.iterdir() 
                      if f.is_file() and f.name != filename]
        
        # If directory has other files, remove the placeholder
        if other_files:
            try:
                placeholder_path.unlink()
                removed_count += 1
                if verbose:
                    print(f"Removed: {placeholder_path} (directory now has {len(other_files)} other files)")
            except (OSError, PermissionError) as e:
                print(f"Error removing {placeholder_path}: {e}")
    
    return removed_count


def mark_empty_folders(root_path: str, placeholder_name: str = '.gitkeep',
                      custom_content: str = None, exclude_dirs: Set[str] = None,
                      exclude_hidden: bool = True, dry_run: bool = False,
                      verbose: bool = False) -> int:
    """Mark empty folders with placeholder files.
    
    Args:
        root_path: Root directory to process
        placeholder_name: Name for placeholder files
        custom_content: Custom content for placeholder files
        exclude_dirs: Directories to exclude from processing
        exclude_hidden: Whether to exclude hidden directories
        dry_run: Show what would be done without making changes
        verbose: Show detailed output
        
    Returns:
        Number of placeholder files created
    """
    root_path_obj = Path(root_path).resolve()
    
    if not root_path_obj.exists():
        raise ValueError(f"Path does not exist: {root_path}")
    
    if not root_path_obj.is_dir():
        raise ValueError(f"Path is not a directory: {root_path}")
    
    print(f"Scanning for empty directories in: {root_path_obj}")
    
    # Find empty directories
    empty_dirs = find_empty_directories(root_path_obj, exclude_dirs, exclude_hidden)
    
    if not empty_dirs:
        print("No empty directories found.")
        return 0
    
    print(f"Found {len(empty_dirs)} empty directories")
    
    if dry_run:
        print("\nDRY RUN - Would create placeholder files in:")
        for directory in empty_dirs:
            placeholder_path = directory / placeholder_name
            print(f"  {placeholder_path}")
        return len(empty_dirs)
    
    # Create placeholder files
    created_count = 0
    for directory in empty_dirs:
        if create_placeholder_file(directory, placeholder_name, custom_content, verbose):
            created_count += 1
    
    return created_count


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Create placeholder files in empty directories for Git tracking.",
        epilog="""
Examples:
  # Mark empty folders with .gitkeep files
  %(prog)s /path/to/project
  
  # Use custom placeholder filename
  %(prog)s /path/to/project --name "keepme.md"
  
  # Dry run to see what would be done
  %(prog)s /path/to/project --dry-run
  
  # Remove existing placeholders from non-empty directories
  %(prog)s /path/to/project --cleanup
  
  # Include hidden directories
  %(prog)s /path/to/project --include-hidden
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "path",
        help="Directory path to scan for empty folders"
    )
    parser.add_argument(
        "--name", "-n",
        default=".gitkeep",
        help="Name for placeholder files (default: .gitkeep)"
    )
    parser.add_argument(
        "--content", "-c",
        help="Custom content for placeholder files"
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        default=[".git", ".svn", ".hg", "__pycache__"],
        help="Directory names to exclude (default: .git .svn .hg __pycache__)"
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden directories (starting with .)"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Remove placeholder files from directories that are no longer empty"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    try:
        args = parser.parse_args()
        
        if args.dry_run:
            print("=" * 60)
            print("DRY RUN MODE - No files will be created")
            print("=" * 60)
        
        exclude_dirs = set(args.exclude) if args.exclude else set()
        
        if args.cleanup:
            # Cleanup mode: remove placeholder files from non-empty directories
            print(f"Cleaning up placeholder files named '{args.name}'")
            removed_count = remove_placeholder_files(
                Path(args.path), 
                args.name, 
                args.verbose
            )
            print(f"Removed {removed_count} placeholder files from non-empty directories")
        else:
            # Normal mode: create placeholder files in empty directories
            created_count = mark_empty_folders(
                args.path,
                args.name,
                args.content,
                exclude_dirs,
                not args.include_hidden,
                args.dry_run,
                args.verbose
            )
            
            if args.dry_run:
                print(f"\nWould create {created_count} placeholder files")
            else:
                print(f"Created {created_count} placeholder files")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())