#!/usr/bin/env python3
# encoding: utf-8
"""
switch_paths.py

Replace file paths in text files (e.g., vrscene, config files).

This script reads a text file and replaces specified paths with new paths.
Useful for updating project files when assets have been moved or when
switching between different environments (e.g., local vs. network paths).

Created by Alexander Kucera
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def load_path_mappings_from_file(config_file: str) -> Dict[str, str]:
    """Load path mappings from a JSON configuration file.
    
    Args:
        config_file: Path to JSON config file
        
    Returns:
        Dictionary mapping old paths to new paths
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        if 'path_mappings' not in config:
            raise ValueError("Config file must contain 'path_mappings' key")
            
        return config['path_mappings']
        
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise ValueError(f"Error loading config file {config_file}: {e}")


def create_sample_config(config_file: str):
    """Create a sample configuration file.
    
    Args:
        config_file: Path where to create the sample config
    """
    sample_config = {
        "path_mappings": {
            "/old/path/textures/": "/new/path/textures/",
            "/old/path/models/": "/new/path/models/",
            "C:\\old\\windows\\path\\": "D:\\new\\windows\\path\\",
            "/Volumes/OldDrive/": "/Volumes/NewDrive/"
        },
        "description": "Map old paths to new paths. Paths are replaced in order."
    }
    
    with open(config_file, 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print(f"Sample configuration created: {config_file}")
    print("Edit this file to define your path mappings.")


def replace_paths_in_content(content: str, path_mappings: Dict[str, str], 
                           case_sensitive: bool = True) -> Tuple[str, List[str]]:
    """Replace paths in the given content.
    
    Args:
        content: Text content to process
        path_mappings: Dictionary of old_path -> new_path mappings
        case_sensitive: Whether path matching should be case sensitive
        
    Returns:
        Tuple of (modified_content, list_of_changes)
    """
    modified_content = content
    changes = []
    
    for old_path, new_path in path_mappings.items():
        if not case_sensitive:
            # For case-insensitive matching, we need to find all occurrences manually
            lower_content = modified_content.lower()
            lower_old_path = old_path.lower()
            
            start = 0
            while True:
                pos = lower_content.find(lower_old_path, start)
                if pos == -1:
                    break
                    
                # Extract the actual case from the original content
                actual_old_path = modified_content[pos:pos + len(old_path)]
                
                # Replace this occurrence
                modified_content = (modified_content[:pos] + 
                                  new_path + 
                                  modified_content[pos + len(old_path):])
                
                # Update the lowercase version for continued searching
                lower_content = modified_content.lower()
                
                changes.append(f"{actual_old_path} → {new_path}")
                start = pos + len(new_path)
        else:
            # Case-sensitive replacement
            if old_path in modified_content:
                count = modified_content.count(old_path)
                modified_content = modified_content.replace(old_path, new_path)
                changes.extend([f"{old_path} → {new_path}"] * count)
    
    return modified_content, changes


def process_file(input_file: str, output_file: str, path_mappings: Dict[str, str],
                case_sensitive: bool = True, backup: bool = True) -> Tuple[int, List[str]]:
    """Process a single file, replacing paths.
    
    Args:
        input_file: Input file path
        output_file: Output file path
        path_mappings: Dictionary of path mappings
        case_sensitive: Whether path matching should be case sensitive
        backup: Whether to create a backup of the original file
        
    Returns:
        Tuple of (number_of_changes, list_of_changes)
    """
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read input file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encodings
        for encoding in ['latin-1', 'cp1252']:
            try:
                with open(input_path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"Warning: File read with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError(f"Could not read file {input_file} with any supported encoding")
    
    # Create backup if requested
    if backup and input_path != output_path:
        backup_path = input_path.with_suffix(input_path.suffix + '.backup')
        backup_path.write_text(content, encoding='utf-8')
        print(f"Backup created: {backup_path}")
    
    # Replace paths
    modified_content, changes = replace_paths_in_content(content, path_mappings, case_sensitive)
    
    # Write output file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    return len(changes), changes


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Replace file paths in text files using configurable mappings.",
        epilog="""
Examples:
  # Create a sample configuration file
  %(prog)s --create-config paths.json
  
  # Process a file using a config file
  %(prog)s input.vrscene --config paths.json
  
  # Process with inline path mappings
  %(prog)s input.txt --old-path "/old/path/" --new-path "/new/path/"
  
  # Process multiple mappings
  %(prog)s input.txt --old-path "/old1/" --new-path "/new1/" --old-path "/old2/" --new-path "/new2/"
  
  # Case-insensitive replacement
  %(prog)s input.txt --config paths.json --ignore-case
  
  # Specify custom output file
  %(prog)s input.txt --config paths.json --output modified_input.txt
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "input_file",
        nargs='?',
        help="Input file to process"
    )
    parser.add_argument(
        "--config",
        help="JSON configuration file with path mappings"
    )
    parser.add_argument(
        "--old-path",
        action="append",
        help="Old path to replace (can be used multiple times)"
    )
    parser.add_argument(
        "--new-path", 
        action="append",
        help="New path replacement (must match number of --old-path arguments)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file (default: input_file with '_modified' suffix)"
    )
    parser.add_argument(
        "--ignore-case",
        action="store_true",
        help="Perform case-insensitive path matching"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup of original file"
    )
    parser.add_argument(
        "--create-config",
        help="Create a sample configuration file and exit"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    try:
        args = parser.parse_args()
        
        # Handle config creation
        if args.create_config:
            create_sample_config(args.create_config)
            return 0
        
        # Validate input
        if not args.input_file:
            parser.error("Input file is required (or use --create-config)")
        
        # Build path mappings
        path_mappings = {}
        
        # From config file
        if args.config:
            path_mappings.update(load_path_mappings_from_file(args.config))
        
        # From command line arguments
        if args.old_path and args.new_path:
            if len(args.old_path) != len(args.new_path):
                parser.error("Number of --old-path and --new-path arguments must match")
            
            for old, new in zip(args.old_path, args.new_path):
                path_mappings[old] = new
        
        if not path_mappings:
            parser.error("No path mappings specified. Use --config or --old-path/--new-path")
        
        # Determine output file
        input_path = Path(args.input_file)
        if args.output:
            output_file = args.output
        else:
            # Default: add '_modified' before the extension
            stem = input_path.stem
            suffix = input_path.suffix
            output_file = str(input_path.with_name(f"{stem}_modified{suffix}"))
        
        print(f"Input file: {args.input_file}")
        print(f"Output file: {output_file}")
        print(f"Path mappings: {len(path_mappings)} entries")
        
        if args.verbose:
            print("\nPath mappings:")
            for old, new in path_mappings.items():
                print(f"  {old} → {new}")
        
        print()
        
        # Process the file
        change_count, changes = process_file(
            args.input_file,
            output_file,
            path_mappings,
            case_sensitive=not args.ignore_case,
            backup=not args.no_backup
        )
        
        # Report results
        if change_count > 0:
            print(f"✓ Made {change_count} path replacements")
            
            if args.verbose:
                print("\nChanges made:")
                for change in changes:
                    print(f"  {change}")
                    
            print(f"\nModified file saved as: {output_file}")
        else:
            print("No path replacements were made")
            print(f"File copied to: {output_file}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())