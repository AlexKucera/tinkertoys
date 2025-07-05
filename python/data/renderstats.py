#!/usr/bin/env python3
# encoding: utf-8
"""
renderstats.py

Analyze render statistics for image sequences.
Calculates render times, identifies missing frames, and detects corrupted files.

Created by Alexander Kucera
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Set, Tuple, Dict, Optional

# Import timer from development directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'development'))
from timer import timer, secondsToHoursMinutesSeconds

# Regex to match image sequence files (e.g., render_001.exr, shot_0150.jpg)
SEQ_REGEX = re.compile(r'^(?P<basename>.*[_\.])(?P<frame>\d+)(?P<extension>\..*)$')


def get_sequential_files(filenames: List[str]) -> Set[int]:
    """Extract frame numbers from sequential file names.
    
    Args:
        filenames: List of filenames to analyze
        
    Returns:
        Set of frame numbers found
    """
    frame_numbers = set()
    
    for filename in filenames:
        match = SEQ_REGEX.match(filename)
        if match:
            frame_num = int(match.group('frame'))
            frame_numbers.add(frame_num)
    
    return frame_numbers


def find_missing_frames(first_frame: int, last_frame: int, found_frames: Set[int], 
                       increment: int = 1) -> Set[int]:
    """Find missing frames in a sequence.
    
    Args:
        first_frame: First frame number
        last_frame: Last frame number
        found_frames: Set of frame numbers that exist
        increment: Frame increment (usually 1)
        
    Returns:
        Set of missing frame numbers
    """
    expected_frames = set(range(first_frame, last_frame + 1, increment))
    return expected_frames - found_frames


def group_consecutive_ranges(frame_numbers: Set[int]) -> List[Tuple[int, int]]:
    """Group consecutive frame numbers into ranges.
    
    Args:
        frame_numbers: Set of frame numbers
        
    Returns:
        List of (start, end) tuples representing consecutive ranges
    """
    if not frame_numbers:
        return []
    
    sorted_frames = sorted(frame_numbers)
    ranges = []
    start = sorted_frames[0]
    end = start
    
    for frame in sorted_frames[1:]:
        if frame == end + 1:
            end = frame
        else:
            ranges.append((start, end))
            start = end = frame
    
    ranges.append((start, end))
    return ranges


def format_frame_ranges(ranges: List[Tuple[int, int]]) -> str:
    """Format frame ranges for display.
    
    Args:
        ranges: List of (start, end) tuples
        
    Returns:
        Formatted string showing ranges
    """
    range_strings = []
    for start, end in ranges:
        if start == end:
            range_strings.append(str(start))
        else:
            range_strings.append(f"{start}-{end}")
    
    return ", ".join(range_strings)


def check_small_files(directory: Path, files: List[str], 
                     min_size: int = 128) -> List[str]:
    """Find files smaller than minimum size (likely corrupted).
    
    Args:
        directory: Directory containing files
        files: List of filenames to check
        min_size: Minimum file size in bytes
        
    Returns:
        List of filenames that are too small
    """
    small_files = []
    
    for filename in files:
        file_path = directory / filename
        try:
            if file_path.is_file() and file_path.stat().st_size < min_size:
                small_files.append(filename)
        except OSError:
            continue
    
    return small_files


def calculate_render_stats(directory: Path, files: List[str], 
                          output_filename: str) -> Dict[str, any]:
    """Calculate render statistics from file modification times.
    
    Args:
        directory: Directory containing render files
        files: List of filenames (excluding output file)
        output_filename: Name of output file to exclude
        
    Returns:
        Dictionary containing render statistics
    """
    mod_times = []
    render_times = []
    
    # Get modification times for all files except output file
    for filename in files:
        if filename == output_filename:
            continue
            
        file_path = directory / filename
        try:
            if file_path.is_file():
                mod_times.append(file_path.stat().st_mtime)
        except OSError:
            continue
    
    if len(mod_times) < 2:
        return {
            'total_files': len(mod_times),
            'total_time': 0,
            'avg_time_per_frame': 0,
            'max_frame_time': 0,
            'min_frame_time': 0,
            'error': 'Not enough files to calculate render times'
        }
    
    mod_times.sort()
    
    # Calculate time differences between consecutive frames
    for i in range(1, len(mod_times)):
        frame_time = mod_times[i] - mod_times[i-1]
        render_times.append(frame_time)
    
    total_time = mod_times[-1] - mod_times[0]
    avg_time = total_time / len(mod_times) if mod_times else 0
    max_time = max(render_times) if render_times else 0
    min_time = min(render_times) if render_times else 0
    
    return {
        'total_files': len(mod_times),
        'total_time': total_time,
        'avg_time_per_frame': avg_time,
        'max_frame_time': max_time,
        'min_frame_time': min_time
    }


def analyze_sequence(directory: Path, files: List[str], output_filename: str,
                    min_file_size: int = 128) -> str:
    """Analyze an image sequence for completeness and render statistics.
    
    Args:
        directory: Directory containing the sequence
        files: List of filenames in the directory
        output_filename: Name of output file to exclude
        min_file_size: Minimum file size for valid files
        
    Returns:
        Formatted analysis report
    """
    # Filter out the output file and non-sequence files
    sequence_files = [f for f in files if f != output_filename]
    
    # Get frame numbers
    frame_numbers = get_sequential_files(sequence_files)
    
    if not frame_numbers:
        return "No sequential files found in this directory."
    
    # Analyze frame ranges
    first_frame = min(frame_numbers)
    last_frame = max(frame_numbers)
    frame_ranges = group_consecutive_ranges(frame_numbers)
    
    report = f"\nAnalysis for: {directory}\n"
    report += "=" * 60 + "\n\n"
    
    # Frame range analysis
    report += "FRAME ANALYSIS:\n"
    report += f"Frame range: {first_frame} to {last_frame}\n"
    report += f"Total frames found: {len(frame_numbers)}\n"
    report += f"Continuous ranges: {format_frame_ranges(frame_ranges)}\n"
    
    # Check for missing frames
    missing_frames = find_missing_frames(first_frame, last_frame, frame_numbers)
    if missing_frames:
        missing_ranges = group_consecutive_ranges(missing_frames)
        report += f"\nMISSING FRAMES ({len(missing_frames)}):\n"
        report += f"Missing: {format_frame_ranges(missing_ranges)}\n"
    else:
        report += "\n✓ All frames present in sequence\n"
    
    # Check for small/corrupted files
    small_files = check_small_files(directory, sequence_files, min_file_size)
    if small_files:
        small_frame_numbers = get_sequential_files(small_files)
        if small_frame_numbers:
            small_ranges = group_consecutive_ranges(small_frame_numbers)
            report += f"\nCORRUPTED FILES ({len(small_files)} files < {min_file_size} bytes):\n"
            report += f"Frames: {format_frame_ranges(small_ranges)}\n"
    else:
        report += f"\n✓ No files smaller than {min_file_size} bytes\n"
    
    # Render time analysis
    stats = calculate_render_stats(directory, sequence_files, output_filename)
    
    if 'error' not in stats:
        report += "\nRENDER STATISTICS:\n"
        report += f"Total render time: {secondsToHoursMinutesSeconds(stats['total_time'])}\n"
        report += f"Files processed: {stats['total_files']}\n"
        report += f"Average per frame: {secondsToHoursMinutesSeconds(stats['avg_time_per_frame'])}\n"
        report += f"Fastest frame: {secondsToHoursMinutesSeconds(stats['min_frame_time'])}\n"
        report += f"Slowest frame: {secondsToHoursMinutesSeconds(stats['max_frame_time'])}\n"
    else:
        report += f"\nRENDER STATISTICS: {stats['error']}\n"
    
    return report


def process_directory(directory: str, output_filename: str, 
                     recursive: bool = False, write_to_file: bool = False,
                     min_file_size: int = 128, verbose: bool = False) -> int:
    """Process directory or directories for render statistics.
    
    Args:
        directory: Directory to analyze
        output_filename: Name for output file
        recursive: Whether to process subdirectories
        write_to_file: Whether to write output to file
        min_file_size: Minimum file size for valid files
        verbose: Show detailed output
        
    Returns:
        Number of directories processed
    """
    directory_path = Path(directory).resolve()
    
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    
    if directory_path.is_file():
        directory_path = directory_path.parent
    
    directories_processed = 0
    
    if recursive:
        print(f"Recursively analyzing: {directory_path}")
        
        for root, dirs, files in os.walk(directory_path):
            root_path = Path(root)
            
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            if files:
                if verbose:
                    print(f"\nProcessing: {root_path}")
                
                report = analyze_sequence(root_path, files, output_filename, min_file_size)
                
                if write_to_file:
                    output_path = root_path / output_filename
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(report)
                    if verbose:
                        print(f"Report written to: {output_path}")
                else:
                    print(report)
                
                directories_processed += 1
    else:
        print(f"Analyzing: {directory_path}")
        files = [f.name for f in directory_path.iterdir() if f.is_file()]
        
        report = analyze_sequence(directory_path, files, output_filename, min_file_size)
        
        if write_to_file:
            output_path = directory_path / output_filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report written to: {output_path}")
        else:
            print(report)
        
        directories_processed = 1
    
    return directories_processed


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Analyze render statistics for image sequences.",
        epilog="""
Examples:
  # Analyze current directory
  %(prog)s .
  
  # Analyze specific directory
  %(prog)s /path/to/renders
  
  # Recursive analysis of all subdirectories
  %(prog)s /path/to/renders --recursive
  
  # Write reports to files instead of stdout
  %(prog)s /path/to/renders --file
  
  # Custom output filename and minimum file size
  %(prog)s /path/to/renders --name "render_report.txt" --min-size 256
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "input",
        help="Input directory or file to analyze"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Process all subdirectories recursively"
    )
    parser.add_argument(
        "-f", "--file",
        action="store_true",
        help="Write statistics to file instead of stdout"
    )
    parser.add_argument(
        "-n", "--name",
        default="renderstats.txt",
        help="Output filename for statistics (default: renderstats.txt)"
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=128,
        help="Minimum file size in bytes for valid files (default: 128)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed progress information"
    )
    
    try:
        args = parser.parse_args()
        
        start_time = timer()
        
        directories_processed = process_directory(
            args.input,
            args.name,
            args.recursive,
            args.file,
            args.min_size,
            args.verbose
        )
        
        elapsed_time = timer(start_time, "Render Statistics Analysis")
        
        print(f"\nProcessed {directories_processed} directories")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())