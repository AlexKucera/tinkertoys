#!/usr/bin/env python3
# encoding: utf-8
"""
fix_symlinks.py

Python script to fix broken symlinks after moving directories.

Original concept from:
http://www.webarnes.ca/2011/09/python-script-to-fix-broken-symlinks/

Modernized and secured by Alexander Kucera
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple


def find_broken_symlinks(base_dir: str) -> List[Path]:
    """Find all broken symlinks in the given directory.
    
    Args:
        base_dir: Directory to search for broken symlinks
        
    Returns:
        List of broken symlink paths
    """
    broken_links = []
    base_path = Path(base_dir)
    
    if not base_path.exists():
        raise ValueError(f"Directory does not exist: {base_dir}")
    
    if not base_path.is_dir():
        raise ValueError(f"Path is not a directory: {base_dir}")
    
    print(f"Scanning for broken symlinks in: {base_path}")
    
    for item in base_path.rglob('*'):
        if item.is_symlink() and not item.exists():
            broken_links.append(item)
            
    return broken_links


def analyze_symlink(symlink_path: Path, old_base: str, new_base: str) -> Tuple[str, str, bool]:
    """Analyze a symlink and determine the new target.
    
    Args:
        symlink_path: Path to the symlink
        old_base: Old base directory path
        new_base: New base directory path
        
    Returns:
        Tuple of (old_target, new_target, can_fix)
    """
    try:
        # Get the raw target (may be broken)
        old_target = str(symlink_path.readlink())
        
        # Handle both absolute and relative links
        if old_target.startswith(old_base):
            # Direct replacement for absolute paths
            new_target = old_target.replace(old_base, new_base, 1)
            can_fix = True
        elif Path(old_target).is_absolute():
            # Absolute path that doesn't match old_base
            new_target = old_target
            can_fix = False
        else:
            # Relative path - try to resolve and fix
            old_resolved = symlink_path.parent / old_target
            old_resolved_str = str(old_resolved.resolve())
            
            if old_resolved_str.startswith(old_base):
                new_resolved = old_resolved_str.replace(old_base, new_base, 1)
                new_target = os.path.relpath(new_resolved, symlink_path.parent)
                can_fix = True
            else:
                new_target = old_target
                can_fix = False
                
        return old_target, new_target, can_fix
        
    except (OSError, ValueError) as e:
        return str(symlink_path.readlink()), "", False


def fix_symlink(symlink_path: Path, new_target: str, dry_run: bool = True) -> bool:
    """Fix a broken symlink by updating its target.
    
    Args:
        symlink_path: Path to the symlink to fix
        new_target: New target path for the symlink
        dry_run: If True, only show what would be done
        
    Returns:
        True if successful (or would be successful in dry run)
    """
    try:
        if dry_run:
            print(f"  [DRY RUN] Would update: {symlink_path}")
            print(f"            New target: {new_target}")
            return True
        else:
            # Remove old symlink and create new one
            symlink_path.unlink()
            symlink_path.symlink_to(new_target)
            print(f"  ✓ Fixed: {symlink_path}")
            print(f"    Target: {new_target}")
            return True
            
    except (OSError, ValueError) as e:
        print(f"  ✗ Error fixing {symlink_path}: {e}")
        return False


def main():
    """Main function to fix broken symlinks."""
    parser = argparse.ArgumentParser(
        description="Fix broken symlinks after moving directories.",
        epilog="""
Examples:
  # Dry run (recommended first)
  %(prog)s /new/location /old/location /new/location --dry-run
  
  # Actually fix the symlinks
  %(prog)s /new/location /old/location /new/location
  
  # Fix only symlinks in specific subdirectory
  %(prog)s /new/location/subdir /old/location /new/location
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "search_dir",
        help="Directory to search for broken symlinks"
    )
    parser.add_argument(
        "old_base",
        help="Old base directory path (what the symlinks currently point to)"
    )
    parser.add_argument(
        "new_base", 
        help="New base directory path (where files actually are now)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Show what would be done without making changes (default: True)"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually perform the fixes (overrides --dry-run)"
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
        
        if dry_run:
            print("=" * 60)
            print("DRY RUN MODE - No changes will be made")
            print("Use --execute to actually fix the symlinks")
            print("=" * 60)
        else:
            print("=" * 60)
            print("EXECUTING FIXES - Changes will be made!")
            print("=" * 60)
        
        # Validate input paths
        search_path = Path(args.search_dir).resolve()
        old_base = str(Path(args.old_base).resolve())
        new_base = str(Path(args.new_base).resolve())
        
        print(f"Search directory: {search_path}")
        print(f"Old base path:    {old_base}")
        print(f"New base path:    {new_base}")
        print()
        
        # Find broken symlinks
        broken_links = find_broken_symlinks(str(search_path))
        
        if not broken_links:
            print("No broken symlinks found.")
            return 0
            
        print(f"Found {len(broken_links)} broken symlinks:")
        print()
        
        fixed_count = 0
        skipped_count = 0
        error_count = 0
        
        for symlink in broken_links:
            old_target, new_target, can_fix = analyze_symlink(symlink, old_base, new_base)
            
            print(f"Symlink: {symlink}")
            if args.verbose:
                print(f"  Current target: {old_target}")
                
            if can_fix:
                if fix_symlink(symlink, new_target, dry_run):
                    fixed_count += 1
                else:
                    error_count += 1
            else:
                print(f"  ⚠ Skipped: Target doesn't match old base path")
                if args.verbose:
                    print(f"    Target: {old_target}")
                skipped_count += 1
            print()
        
        # Summary
        print("=" * 60)
        print("SUMMARY:")
        if dry_run:
            print(f"  Would fix: {fixed_count} symlinks")
        else:
            print(f"  Fixed: {fixed_count} symlinks")
        print(f"  Skipped: {skipped_count} symlinks")
        print(f"  Errors: {error_count} symlinks")
        
        if dry_run and fixed_count > 0:
            print(f"\nTo actually apply these fixes, run with --execute")
            
        return 0 if error_count == 0 else 1
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())