#!/usr/bin/env python3
# encoding: utf-8
"""
exportPinboard.py

Export Pinboard bookmarks as XML files for backup and further processing.
Creates daily backups and maintains a current backup file.

Created by Alexander Kucera
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import os
import shutil
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

try:
    import pytz
    HAS_PYTZ = True
except ImportError:
    HAS_PYTZ = False


def read_credentials(credentials_file: Path) -> Tuple[str, str]:
    """Read Pinboard credentials from file.
    
    Args:
        credentials_file: Path to credentials file
        
    Returns:
        Tuple of (username, token)
        
    Raises:
        FileNotFoundError: If credentials file doesn't exist
        ValueError: If credentials format is invalid
    """
    if not credentials_file.exists():
        raise FileNotFoundError(f"Credentials file not found: {credentials_file}")
    
    try:
        with open(credentials_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    username, token = line.split(':', 1)
                    return username.strip(), token.strip()
        
        raise ValueError("No valid credentials found in file")
    
    except Exception as e:
        raise ValueError(f"Error reading credentials: {e}")


def export_pinboard_bookmarks(username: str, token: str, output_file: Path,
                             api_url: str = "https://api.pinboard.in/v1/",
                             verbose: bool = False) -> int:
    """Export Pinboard bookmarks to XML file.
    
    Args:
        username: Pinboard username
        token: Pinboard API token
        output_file: Output file path
        api_url: Pinboard API base URL
        verbose: Show detailed output
        
    Returns:
        Number of bytes written
        
    Raises:
        RuntimeError: If API request fails
    """
    # Construct API URL
    api_endpoint = f"{api_url}posts/all?auth_token={username}:{token}"
    
    if verbose:
        print(f"Fetching bookmarks from Pinboard API...")
        print(f"Output file: {output_file}")
    
    try:
        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Fetch bookmarks from API
        with urlopen(api_endpoint) as response:
            if response.status != 200:
                raise RuntimeError(f"API request failed with status {response.status}")
            
            bookmark_data = response.read()
            
            # Write to file
            with open(output_file, 'wb') as f:
                f.write(bookmark_data)
            
            if verbose:
                print(f"Successfully exported {len(bookmark_data)} bytes")
            
            return len(bookmark_data)
    
    except HTTPError as e:
        if e.code == 401:
            raise RuntimeError("Authentication failed. Check your credentials.")
        elif e.code == 429:
            raise RuntimeError("Rate limit exceeded. Please wait and try again.")
        else:
            raise RuntimeError(f"HTTP error {e.code}: {e.reason}")
    
    except URLError as e:
        raise RuntimeError(f"Network error: {e.reason}")
    
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")


def create_backup_filename(base_dir: Path, date_format: str = "%m-%d") -> Path:
    """Create backup filename based on current date.
    
    Args:
        base_dir: Base directory for backups
        date_format: Date format for filename
        
    Returns:
        Path to backup file
    """
    if HAS_PYTZ:
        now = datetime.now(pytz.UTC)
    else:
        now = datetime.utcnow()
    
    year = now.strftime("%Y")
    date_str = now.strftime(date_format)
    
    year_dir = base_dir / year
    filename = f"pinboard-backup.{date_str}.xml"
    
    return year_dir / filename


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Export Pinboard bookmarks as XML files.",
        epilog="""
Examples:
  # Basic usage with default paths
  %(prog)s
  
  # Specify custom output directory
  %(prog)s --output-dir /path/to/backups
  
  # Use custom credentials file
  %(prog)s --credentials /path/to/credentials.txt
  
  # Custom date format for backup files
  %(prog)s --date-format "%%Y-%%m-%%d"
  
  # Export to specific file without date-based naming
  %(prog)s --output-file /path/to/bookmarks.xml
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        help="Output directory for backups (default: ~/Dropbox/Apps/pinboard/)"
    )
    parser.add_argument(
        "--output-file", "-f",
        help="Specific output file (overrides date-based naming)"
    )
    parser.add_argument(
        "--credentials", "-c",
        help="Path to credentials file (default: [output-dir]/pinboard_credentials.txt)"
    )
    parser.add_argument(
        "--date-format", "-d",
        default="%m-%d",
        help="Date format for backup filenames (default: %%m-%%d)"
    )
    parser.add_argument(
        "--current-file",
        help="Path for 'current' bookmark file (default: [output-dir]/most_current_bookmarks.xml)"
    )
    parser.add_argument(
        "--api-url",
        default="https://api.pinboard.in/v1/",
        help="Pinboard API base URL (default: https://api.pinboard.in/v1/)"
    )
    parser.add_argument(
        "--no-current",
        action="store_true",
        help="Don't create/update current bookmarks file"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    try:
        args = parser.parse_args()
        
        # Set up paths
        if args.output_dir:
            output_dir = Path(args.output_dir).resolve()
        else:
            output_dir = Path.home() / "Dropbox" / "Apps" / "pinboard"
        
        if args.credentials:
            credentials_file = Path(args.credentials).resolve()
        else:
            credentials_file = output_dir / "pinboard_credentials.txt"
        
        if args.current_file:
            current_file = Path(args.current_file).resolve()
        else:
            current_file = output_dir / "most_current_bookmarks.xml"
        
        # Determine output file
        if args.output_file:
            output_file = Path(args.output_file).resolve()
        else:
            output_file = create_backup_filename(output_dir, args.date_format)
        
        if not HAS_PYTZ:
            print("Warning: pytz not available. Using system UTC time.")
            print("Install with: pip install pytz")
            print()
        
        # Read credentials
        if args.verbose:
            print(f"Reading credentials from: {credentials_file}")
        
        username, token = read_credentials(credentials_file)
        
        # Export bookmarks
        bytes_written = export_pinboard_bookmarks(
            username, token, output_file, args.api_url, args.verbose
        )
        
        print(f"Successfully exported {bytes_written} bytes to: {output_file}")
        
        # Create current file copy if requested
        if not args.no_current:
            shutil.copy2(output_file, current_file)
            if args.verbose:
                print(f"Updated current file: {current_file}")
        
        return 0
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())