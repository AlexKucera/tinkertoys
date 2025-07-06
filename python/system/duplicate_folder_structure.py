#!/usr/bin/env python3
"""
Duplicate Folder Structure Tool

Creates a duplicate of a directory tree structure without copying files.
Only creates directories, preserving the exact folder hierarchy.

Author: Alexander Kucera
Contact: babylondreams.de

Usage:
    python3 duplicate_folder_structure.py SOURCE DESTINATION [OPTIONS]
    python3 duplicate_folder_structure.py /path/to/source /path/to/destination
    python3 duplicate_folder_structure.py /project --suffix "_backup"
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple
import time

# Add lib directory to path for shared utilities
sys.path.append(str(Path(__file__).parent.parent / 'lib'))

try:
    from query_yes_no import query_yes_no
except ImportError:
    def query_yes_no(question: str, default: str = "no") -> bool:
        """Fallback if query_yes_no not available."""
        response = input(f"{question} (y/N): ").lower().strip()
        return response.startswith('y')


class FolderStructureDuplicator:
    """Creates duplicate directory structures without copying files."""
    
    def __init__(self, source: Path, destination: Path, verbose: bool = False):
        self.source = Path(source).resolve()
        self.destination = Path(destination).resolve()
        self.verbose = verbose
        self.dirs_created = 0
        self.dirs_skipped = 0
        self.errors = []
        
    def validate_paths(self) -> bool:
        """Validate source and destination paths."""
        if not self.source.exists():
            print(f"Error: Source directory does not exist: {self.source}")
            return False
            
        if not self.source.is_dir():
            print(f"Error: Source is not a directory: {self.source}")
            return False
            
        if self.destination.exists() and not self.destination.is_dir():
            print(f"Error: Destination exists but is not a directory: {self.destination}")
            return False
            
        if self.source == self.destination:
            print("Error: Source and destination cannot be the same")
            return False
            
        if self.destination.is_relative_to(self.source):
            print("Error: Destination cannot be inside source directory")
            return False
            
        return True
    
    def get_directory_tree(self) -> List[Path]:
        """Get all directories in the source tree."""
        directories = []
        
        try:
            for item in self.source.rglob('*'):
                if item.is_dir():
                    directories.append(item)
        except PermissionError as e:
            self.errors.append(f"Permission denied accessing: {e}")
        except Exception as e:
            self.errors.append(f"Error scanning directory tree: {e}")
            
        return sorted(directories)
    
    def create_directory_structure(self, dry_run: bool = False) -> bool:
        """Create the directory structure."""
        directories = self.get_directory_tree()
        
        if not directories:
            print("No directories found to duplicate")
            return True
            
        print(f"Found {len(directories)} directories to duplicate")
        
        if dry_run:
            print(f"\nDRY RUN - Would create directories in: {self.destination}")
            print("=" * 50)
        else:
            print(f"\nCreating directory structure in: {self.destination}")
            print("=" * 50)
            
        # Create base destination directory
        if not dry_run:
            try:
                self.destination.mkdir(parents=True, exist_ok=True)
                if self.verbose:
                    print(f"Created base directory: {self.destination}")
            except Exception as e:
                print(f"Error creating base directory: {e}")
                return False
        
        # Process each directory
        for directory in directories:
            try:
                # Calculate relative path from source
                relative_path = directory.relative_to(self.source)
                target_dir = self.destination / relative_path
                
                if dry_run:
                    if self.verbose:
                        print(f"Would create: {target_dir}")
                    self.dirs_created += 1
                else:
                    if target_dir.exists():
                        if self.verbose:
                            print(f"Already exists: {target_dir}")
                        self.dirs_skipped += 1
                    else:
                        target_dir.mkdir(parents=True, exist_ok=True)
                        if self.verbose:
                            print(f"Created: {target_dir}")
                        self.dirs_created += 1
                        
            except Exception as e:
                error_msg = f"Error processing {directory}: {e}"
                self.errors.append(error_msg)
                if self.verbose:
                    print(f"Error: {error_msg}")
                    
        return True
    
    def show_summary(self, dry_run: bool = False):
        """Display operation summary."""
        print("\n" + "=" * 50)
        
        if dry_run:
            print("DRY RUN SUMMARY:")
            print(f"Directories that would be created: {self.dirs_created}")
        else:
            print("OPERATION SUMMARY:")
            print(f"Directories created: {self.dirs_created}")
            print(f"Directories already existing: {self.dirs_skipped}")
            
        if self.errors:
            print(f"Errors encountered: {len(self.errors)}")
            if self.verbose:
                print("\nErrors:")
                for error in self.errors:
                    print(f"  - {error}")
        else:
            print("No errors encountered")
            
        print(f"Source: {self.source}")
        print(f"Destination: {self.destination}")


def generate_destination_path(source: Path, suffix: Optional[str] = None, 
                            prefix: Optional[str] = None) -> Path:
    """Generate destination path with suffix or prefix."""
    if suffix:
        return source.parent / f"{source.name}{suffix}"
    elif prefix:
        return source.parent / f"{prefix}{source.name}"
    else:
        return source.parent / f"{source.name}_structure"


def main():
    parser = argparse.ArgumentParser(
        description="Duplicate directory structure without copying files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /project/source /backup/structure
  %(prog)s /project --suffix "_folders"
  %(prog)s /data --prefix "structure_" --verbose
  %(prog)s /source /dest --dry-run --verbose

This tool creates an exact copy of a directory tree structure without
copying any files. Only directories are created, preserving the exact
folder hierarchy from the source.
        """
    )
    
    parser.add_argument('source', 
                       help='Source directory to duplicate structure from')
    
    parser.add_argument('destination', nargs='?',
                       help='Destination directory (optional if using --suffix/--prefix)')
    
    parser.add_argument('--suffix', 
                       help='Add suffix to source directory name for destination')
    
    parser.add_argument('--prefix',
                       help='Add prefix to source directory name for destination')
    
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output')
    
    parser.add_argument('--force', action='store_true',
                       help='Skip confirmation prompts')
    
    args = parser.parse_args()
    
    # Validate arguments
    source = Path(args.source)
    
    if args.destination:
        destination = Path(args.destination)
    elif args.suffix or args.prefix:
        destination = generate_destination_path(source, args.suffix, args.prefix)
    else:
        parser.error("Must provide destination or use --suffix/--prefix")
    
    # Create duplicator instance
    duplicator = FolderStructureDuplicator(source, destination, args.verbose)
    
    # Validate paths
    if not duplicator.validate_paths():
        sys.exit(1)
    
    # Show operation details
    print(f"Source directory: {duplicator.source}")
    print(f"Destination directory: {duplicator.destination}")
    
    if args.dry_run:
        print("Mode: DRY RUN (no changes will be made)")
    else:
        print("Mode: EXECUTE (directories will be created)")
    
    # Confirmation for non-dry-run operations
    if not args.dry_run and not args.force:
        if destination.exists():
            if not query_yes_no(f"Destination exists. Continue?", "no"):
                print("Operation cancelled by user")
                sys.exit(0)
        else:
            if not query_yes_no("Proceed with directory creation?", "yes"):
                print("Operation cancelled by user")
                sys.exit(0)
    
    # Record start time
    start_time = time.time()
    
    # Execute operation
    try:
        success = duplicator.create_directory_structure(args.dry_run)
        
        if success:
            duplicator.show_summary(args.dry_run)
            
            # Show timing
            elapsed = time.time() - start_time
            print(f"Operation completed in {elapsed:.2f} seconds")
            
            if args.dry_run:
                print(f"\nTo execute: {' '.join(sys.argv).replace('--dry-run', '')}")
            
            sys.exit(0 if not duplicator.errors else 1)
        else:
            print("Operation failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()