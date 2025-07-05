#!/usr/bin/env python3
# encoding: utf-8
"""
compareSizes.py

Compare file sizes (or checksums) between two directories for files with matching names.
Identifies corrupted or incomplete file copies by detecting size mismatches.

Created by Alexander Kucera on 2013-05-22.
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Import hash function from lib
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from hash_for_file import hash_for_file

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


def scan_directory_for_comparison(directory: str, filter_extension: str = None) -> Dict[str, str]:
    """Scan directory and create a mapping of filenames to full paths.
    
    Args:
        directory: Directory to scan
        filter_extension: File extension filter
        
    Returns:
        Dictionary mapping filenames to full paths
    """
    file_map = {}
    directory_path = Path(directory)
    
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    
    if not directory_path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    
    print(f"Scanning: {directory}")
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if not filter_extension or filename.lower().endswith(filter_extension.lower()):
                full_path = os.path.join(root, filename)
                file_map[filename] = full_path
    
    return file_map


def compare_files(left_files: Dict[str, str], right_files: Dict[str, str],
                 use_checksum: bool = False, hash_algorithm: str = 'blake2b',
                 verbose: bool = False) -> Tuple[List[Tuple[str, str, str, int, int]], int]:
    """Compare files between two directories.
    
    Args:
        left_files: Dictionary of filename -> path for left directory
        right_files: Dictionary of filename -> path for right directory
        use_checksum: Whether to use checksum comparison instead of size
        hash_algorithm: Hash algorithm for checksum comparison
        verbose: Show progress information
        
    Returns:
        Tuple of (mismatches_list, total_matches)
        mismatches_list contains (filename, left_path, right_path, left_value, right_value)
    """
    # Find matching filenames
    left_names = set(left_files.keys())
    right_names = set(right_files.keys())
    matches = left_names.intersection(right_names)
    
    if not matches:
        print("No matching filenames found between directories.")
        return [], 0
    
    print(f"Found {len(matches)} files with matching names")
    
    if use_checksum:
        print(f"Using {hash_algorithm} checksum comparison (this may take a while...)")
    else:
        print("Using file size comparison")
    
    mismatches = []
    
    # Use tqdm for progress bar if available and needed
    if HAS_TQDM and (verbose or use_checksum):
        iterator = tqdm(matches, desc="Comparing files")
    else:
        iterator = matches
    
    for filename in iterator:
        left_path = left_files[filename]
        right_path = right_files[filename]
        
        try:
            if use_checksum:
                left_value = hash_for_file(left_path, hash_algorithm)
                right_value = hash_for_file(right_path, hash_algorithm)
            else:
                left_value = os.path.getsize(left_path)
                right_value = os.path.getsize(right_path)
            
            if left_value != right_value:
                mismatches.append((filename, left_path, right_path, left_value, right_value))
                
        except Exception as e:
            print(f"Error comparing {filename}: {e}")
            continue
    
    return mismatches, len(matches)


def generate_copy_script(mismatches: List[Tuple[str, str, str, int, int]], 
                        output_dir: str, script_name: str = "fix_mismatches.py") -> str:
    """Generate a Python script to copy mismatched files.
    
    Args:
        mismatches: List of file mismatches
        output_dir: Directory where to write the script
        script_name: Name of the script file
        
    Returns:
        Path to the generated script
    """
    script_path = os.path.join(output_dir, script_name)
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write("#!/usr/bin/env python3\n")
        f.write("# encoding: utf-8\n")
        f.write('"""\n')
        f.write("Auto-generated script to fix file mismatches.\n")
        f.write("This script will copy files from source to destination to fix size/checksum mismatches.\n")
        f.write('"""\n\n')
        f.write("import shutil\n")
        f.write("import os\n")
        f.write("import sys\n\n")
        f.write("def copy_file_with_backup(src, dst):\n")
        f.write('    """Copy file with backup of existing destination."""\n')
        f.write("    if os.path.exists(dst):\n")
        f.write("        backup_path = dst + '.backup'\n")
        f.write("        shutil.copy2(dst, backup_path)\n")
        f.write(f'        print(f"Backed up {{dst}} to {{backup_path}}")\n')
        f.write("    \n")
        f.write("    shutil.copy2(src, dst)\n")
        f.write(f'    print(f"Copied {{src}} to {{dst}}")\n\n')
        f.write("def main():\n")
        f.write(f'    print("Fixing {len(mismatches)} mismatched files...")\n')
        f.write("    \n")
        
        for filename, left_path, right_path, left_value, right_value in mismatches:
            f.write(f"    # {filename}\n")
            f.write(f'    copy_file_with_backup(r"{left_path}", r"{right_path}")\n')
            f.write("    \n")
        
        f.write('    print("All files copied successfully!")\n\n')
        f.write('if __name__ == "__main__":\n')
        f.write("    main()\n")
    
    # Make script executable
    os.chmod(script_path, 0o755)
    
    return script_path


def compare_directories(left_dir: str, right_dir: str, filter_extension: str = None,
                       use_checksum: bool = False, hash_algorithm: str = 'blake2b',
                       generate_script: bool = False, output_file: str = None,
                       verbose: bool = False) -> Tuple[int, int]:
    """Compare two directories for file size/checksum mismatches.
    
    Args:
        left_dir: Source directory
        right_dir: Destination directory
        filter_extension: File extension filter
        use_checksum: Use checksum instead of size comparison
        hash_algorithm: Hash algorithm for checksums
        generate_script: Generate copy script for mismatches
        output_file: Output file for mismatch report
        verbose: Show detailed output
        
    Returns:
        Tuple of (mismatches_count, total_matches)
    """
    print(f"Comparing directories:")
    print(f"  Source:      {left_dir}")
    print(f"  Destination: {right_dir}")
    
    if filter_extension:
        print(f"  Filter:      {filter_extension}")
    
    print()
    
    # Scan both directories
    left_files = scan_directory_for_comparison(left_dir, filter_extension)
    print(f"Found {len(left_files)} files in source directory")
    
    right_files = scan_directory_for_comparison(right_dir, filter_extension)
    print(f"Found {len(right_files)} files in destination directory")
    print()
    
    # Compare files
    mismatches, total_matches = compare_files(
        left_files, right_files, use_checksum, hash_algorithm, verbose
    )
    
    if not mismatches:
        print("✓ No mismatches found! All matching files have identical sizes/checksums.")
        return 0, total_matches
    
    print(f"\n⚠ Found {len(mismatches)} mismatches:")
    print()
    
    # Report mismatches
    for filename, left_path, right_path, left_value, right_value in mismatches:
        print(f"File: {filename}")
        if use_checksum:
            print(f"  Source checksum:      {left_value}")
            print(f"  Destination checksum: {right_value}")
        else:
            print(f"  Source size:      {left_value:,} bytes")
            print(f"  Destination size: {right_value:,} bytes")
        
        if verbose:
            print(f"  Source path:      {left_path}")
            print(f"  Destination path: {right_path}")
        print()
    
    # Generate copy script if requested
    if generate_script:
        script_path = generate_copy_script(mismatches, right_dir)
        print(f"Copy script generated: {script_path}")
        print("Review and run this script to fix the mismatches.")
        print()
    
    # Write report file if requested
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"File Size/Checksum Comparison Report\n")
            f.write(f"=====================================\n\n")
            f.write(f"Source directory: {left_dir}\n")
            f.write(f"Destination directory: {right_dir}\n")
            f.write(f"Comparison method: {'Checksum' if use_checksum else 'File size'}\n")
            f.write(f"Total matches: {total_matches}\n")
            f.write(f"Mismatches: {len(mismatches)}\n\n")
            
            for filename, left_path, right_path, left_value, right_value in mismatches:
                f.write(f"File: {filename}\n")
                if use_checksum:
                    f.write(f"  Source checksum: {left_value}\n")
                    f.write(f"  Destination checksum: {right_value}\n")
                else:
                    f.write(f"  Source size: {left_value:,} bytes\n")
                    f.write(f"  Destination size: {right_value:,} bytes\n")
                f.write(f"  Source path: {left_path}\n")
                f.write(f"  Destination path: {right_path}\n\n")
        
        print(f"Detailed report written to: {output_file}")
    
    return len(mismatches), total_matches


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Compare file sizes or checksums between two directories.",
        epilog="""
Examples:
  # Basic size comparison
  %(prog)s /source/dir /dest/dir
  
  # Compare only .mov files
  %(prog)s /source/dir /dest/dir --filter .mov
  
  # Use checksum comparison (slower but more accurate)
  %(prog)s /source/dir /dest/dir --checksum
  
  # Generate script to fix mismatches
  %(prog)s /source/dir /dest/dir --generate-script
  
  # Use different hash algorithm
  %(prog)s /source/dir /dest/dir --checksum --hash-algorithm sha256
  
  # Save detailed report
  %(prog)s /source/dir /dest/dir --output report.txt --verbose
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "source_dir",
        help="Source directory (copied from)"
    )
    parser.add_argument(
        "dest_dir",
        help="Destination directory (copied to)"
    )
    parser.add_argument(
        "--filter", "-f",
        help="File extension filter (e.g., .mov, .txt, .jpg)"
    )
    parser.add_argument(
        "--checksum",
        action="store_true",
        help="Use checksum comparison instead of file size (slower but more accurate)"
    )
    parser.add_argument(
        "--hash-algorithm",
        choices=['blake2b', 'sha256', 'md5'],
        default='blake2b',
        help="Hash algorithm for checksum comparison (default: blake2b)"
    )
    parser.add_argument(
        "--generate-script",
        action="store_true",
        help="Generate Python script to copy mismatched files"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for detailed mismatch report"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output including file paths"
    )
    
    try:
        args = parser.parse_args()
        
        if args.checksum:
            print("WARNING: Checksum comparison can be very slow for large files!")
            print("Consider testing with a small subset first.")
            print()
        
        # Compare directories
        mismatches, total_matches = compare_directories(
            args.source_dir,
            args.dest_dir,
            filter_extension=args.filter,
            use_checksum=args.checksum,
            hash_algorithm=args.hash_algorithm,
            generate_script=args.generate_script,
            output_file=args.output,
            verbose=args.verbose
        )
        
        # Summary
        print("=" * 60)
        print("SUMMARY:")
        print(f"  Files compared: {total_matches}")
        print(f"  Mismatches:     {mismatches}")
        
        if mismatches > 0:
            print(f"  Success rate:   {((total_matches - mismatches) / total_matches * 100):.1f}%")
            return 1  # Exit code 1 indicates mismatches found
        else:
            print(f"  Success rate:   100%")
            return 0  # Exit code 0 indicates no mismatches
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())