#!/usr/bin/env python3
# encoding: utf-8
"""
DayOne_split.py

Split DayOne Markdown export into separate files per day.
Converts a single DayOne export file into multiple journal entries organized by date.

Created by Alexander Kucera on 2013-05-16.
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# Try to import parsedatetime (optional dependency)
try:
    import parsedatetime
    HAS_PARSEDATETIME = True
except ImportError:
    HAS_PARSEDATETIME = False


def parse_date_from_line(line: str) -> Optional[datetime]:
    """Parse date from a DayOne export line.
    
    Args:
        line: Line containing date information
        
    Returns:
        Parsed datetime object or None if parsing fails
    """
    # Remove the "Date:" prefix and clean up
    date_text = line[7:].strip()
    
    if HAS_PARSEDATETIME:
        # Use parsedatetime if available
        try:
            cal = parsedatetime.Calendar()
            parsed_tuple = cal.parse(date_text)
            return datetime.fromtimestamp(parsed_tuple[0])
        except Exception:
            pass
    
    # Fallback: try common date formats
    date_formats = [
        "%B %d, %Y at %I:%M %p",  # January 15, 2013 at 10:30 AM
        "%B %d, %Y at %H:%M",     # January 15, 2013 at 22:30
        "%B %d, %Y",              # January 15, 2013
        "%Y-%m-%d %H:%M:%S",      # 2013-01-15 10:30:00
        "%Y-%m-%d",               # 2013-01-15
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_text, fmt)
        except ValueError:
            continue
    
    print(f"Warning: Could not parse date: {date_text}")
    return None


def split_dayone_export(input_file: Path, output_dir: Path, 
                       prefix: str = "journal_", suffix: str = "_dayone-export",
                       extension: str = "md", date_format: str = "%Y-%m-%d",
                       verbose: bool = False) -> int:
    """Split DayOne export into separate files per day.
    
    Args:
        input_file: Path to DayOne export file
        output_dir: Directory to write split files
        prefix: Filename prefix for split files
        suffix: Filename suffix for split files
        extension: File extension for split files
        date_format: Date format for filenames
        verbose: Show detailed output
        
    Returns:
        Number of files created
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Export file not found: {input_file}")
    
    if not input_file.is_file():
        raise ValueError(f"Path is not a file: {input_file}")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing DayOne export: {input_file}")
    print(f"Output directory: {output_dir}")
    
    files_created = 0
    current_date = None
    current_file = None
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Process first line to get initial date
            first_line = f.readline().strip()
            
            if first_line.startswith("Date:"):
                current_date = parse_date_from_line(first_line)
                if current_date:
                    date_str = current_date.strftime(date_format)
                    filename = f"{prefix}{date_str}{suffix}.{extension}"
                    file_path = output_dir / filename
                    
                    current_file = open(file_path, 'w', encoding='utf-8')
                    current_file.write(first_line + "\n")
                    files_created += 1
                    
                    if verbose:
                        print(f"Created: {file_path}")
            else:
                # If first line doesn't contain date, create a fallback file
                filename = f"{prefix}unknown_date{suffix}.{extension}"
                file_path = output_dir / filename
                current_file = open(file_path, 'w', encoding='utf-8')
                current_file.write(first_line + "\n")
                files_created += 1
                
                if verbose:
                    print(f"Created fallback file: {file_path}")
            
            # Process remaining lines
            for line in f:
                line = line.rstrip('\n\r')
                
                if line.startswith("Date:"):
                    # Found a new date entry
                    new_date = parse_date_from_line(line)
                    
                    if new_date and current_date:
                        new_date_str = new_date.strftime(date_format)
                        current_date_str = current_date.strftime(date_format)
                        
                        if new_date_str != current_date_str:
                            # Close current file and open new one
                            if current_file:
                                current_file.close()
                            
                            current_date = new_date
                            filename = f"{prefix}{new_date_str}{suffix}.{extension}"
                            file_path = output_dir / filename
                            
                            current_file = open(file_path, 'w', encoding='utf-8')
                            files_created += 1
                            
                            if verbose:
                                print(f"Created: {file_path}")
                
                # Write line to current file
                if current_file:
                    current_file.write(line + "\n")
        
        if current_file:
            current_file.close()
        
        print(f"Successfully created {files_created} files")
        return files_created
    
    except Exception as e:
        if current_file:
            current_file.close()
        raise RuntimeError(f"Error processing export file: {e}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Split DayOne Markdown export into separate files per day.",
        epilog="""
Examples:
  # Basic usage
  %(prog)s DayOne.md
  
  # Specify output directory
  %(prog)s DayOne.md --output-dir /path/to/split/files
  
  # Custom filename format
  %(prog)s DayOne.md --prefix "diary_" --suffix "_export" --extension txt
  
  # Custom date format for filenames
  %(prog)s DayOne.md --date-format "%%Y_%%m_%%d"
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "input_file",
        help="DayOne export file (Markdown format)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        help="Output directory for split files (default: same as input file)"
    )
    parser.add_argument(
        "--prefix", "-p",
        default="journal_",
        help="Filename prefix for split files (default: journal_)"
    )
    parser.add_argument(
        "--suffix", "-s",
        default="_dayone-export",
        help="Filename suffix for split files (default: _dayone-export)"
    )
    parser.add_argument(
        "--extension", "-e",
        default="md",
        help="File extension for split files (default: md)"
    )
    parser.add_argument(
        "--date-format", "-d",
        default="%Y-%m-%d",
        help="Date format for filenames (default: %%Y-%%m-%%d)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    try:
        args = parser.parse_args()
        
        input_file = Path(args.input_file).resolve()
        
        if args.output_dir:
            output_dir = Path(args.output_dir).resolve()
        else:
            output_dir = input_file.parent
        
        if not HAS_PARSEDATETIME:
            print("Warning: parsedatetime not available. Using basic date parsing.")
            print("Install with: pip install parsedatetime")
            print()
        
        files_created = split_dayone_export(
            input_file,
            output_dir,
            args.prefix,
            args.suffix,
            args.extension,
            args.date_format,
            args.verbose
        )
        
        return 0
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

