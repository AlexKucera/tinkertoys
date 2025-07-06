# DayOne_split.py

Split DayOne Markdown export into separate files per day with flexible date parsing and configurable output formats.

## Overview

DayOne_split.py processes exported DayOne journal files and splits them into individual daily journal entries. The script automatically parses dates from the export format and creates separate files for each day, making it easier to process or migrate journal entries.

## Features

- **Flexible Date Parsing** - Supports multiple date formats with fallback parsing
- **Configurable Output** - Customizable filename prefixes, suffixes, and extensions
- **Optional Dependencies** - Works with or without parsedatetime library
- **Error Handling** - Robust error handling for malformed exports
- **CLI Interface** - Full command-line interface with comprehensive options

## Usage

### Basic Usage
```bash
# Split a DayOne export file
python3 DayOne_split.py DayOne.md

# Specify output directory
python3 DayOne_split.py DayOne.md --output-dir /path/to/split/files
```

### Advanced Usage
```bash
# Custom filename format
python3 DayOne_split.py DayOne.md \
    --prefix "diary_" \
    --suffix "_export" \
    --extension txt

# Custom date format for filenames
python3 DayOne_split.py DayOne.md --date-format "%Y_%m_%d"

# Verbose output
python3 DayOne_split.py DayOne.md --verbose
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `input_file` | - | DayOne export file (Markdown format) | Required |
| `--output-dir` | `-o` | Output directory for split files | Same as input file |
| `--prefix` | `-p` | Filename prefix for split files | `journal_` |
| `--suffix` | `-s` | Filename suffix for split files | `_dayone-export` |
| `--extension` | `-e` | File extension for split files | `md` |
| `--date-format` | `-d` | Date format for filenames | `%Y-%m-%d` |
| `--verbose` | `-v` | Show detailed output | False |

## Date Format Examples

The `--date-format` option uses Python's strftime format:

- `%Y-%m-%d` → `2024-07-05` (default)
- `%Y_%m_%d` → `2024_07_05`
- `%B_%d_%Y` → `July_05_2024`
- `%y%m%d` → `240705`

## Supported Date Formats

The script can parse various date formats from DayOne exports:

- `January 15, 2013 at 10:30 AM`
- `January 15, 2013 at 22:30`
- `January 15, 2013`
- `2013-01-15 10:30:00`
- `2013-01-15`

## Output Structure

Given a DayOne export file, the script creates:

```
output_directory/
├── journal_2024-07-01_dayone-export.md
├── journal_2024-07-02_dayone-export.md
├── journal_2024-07-03_dayone-export.md
└── ...
```

Each file contains all journal entries for that specific date.

## Dependencies

### Required
- Python 3.11+
- Standard library modules only

### Optional
- **parsedatetime** - Enhanced date parsing capabilities
  ```bash
  pip install parsedatetime
  ```

## Error Handling

The script handles various error conditions gracefully:

- **File not found** - Clear error message if input file doesn't exist
- **Invalid dates** - Warning messages for unparseable dates with fallback handling
- **Write permissions** - Error handling for output directory creation issues
- **Malformed exports** - Robust parsing that handles unexpected format variations

## Examples

### Example 1: Basic Split
```bash
python3 DayOne_split.py ~/Desktop/DayOne.md
```
Creates files like `journal_2024-07-05_dayone-export.md` in the same directory.

### Example 2: Custom Organization
```bash
python3 DayOne_split.py ~/Desktop/DayOne.md \
    --output-dir ~/Documents/Journal \
    --prefix "entry_" \
    --suffix "" \
    --extension txt \
    --date-format "%Y/%m/%d"
```
Creates files like `entry_2024/07/05.txt` in the Journal directory.

### Example 3: Year-Month Organization
```bash
python3 DayOne_split.py ~/Desktop/DayOne.md \
    --output-dir ~/Documents/Journal \
    --date-format "%Y-%m/%d" \
    --verbose
```
Creates subdirectories by month: `2024-07/05_dayone-export.md`

## Implementation Details

### Date Parsing Strategy
1. **Primary**: Use parsedatetime library if available
2. **Fallback**: Try common date format patterns
3. **Graceful degradation**: Create fallback files for unparseable dates

### File Organization
- Creates output directories automatically if they don't exist
- Handles duplicate dates by appending to existing files
- Preserves original content formatting and structure

### Memory Efficiency
- Processes files line-by-line to handle large exports
- Minimal memory footprint regardless of export size

## Troubleshooting

### Common Issues

**Issue**: "Could not parse date" warnings
```
Solution: Install parsedatetime for better date parsing:
pip install parsedatetime
```

**Issue**: Permission denied errors
```
Solution: Ensure write permissions to output directory:
chmod 755 /path/to/output/directory
```

**Issue**: Empty output files
```
Solution: Check that input file is a valid DayOne export with "Date:" lines
```

### Debugging

Use the `--verbose` flag to see detailed processing information:

```bash
python3 DayOne_split.py DayOne.md --verbose
```

This shows:
- Files being created
- Date parsing results
- Processing progress
- Any warnings or issues

## Integration

### Workflow Integration
The script integrates well with automated workflows:

```bash
# Automated daily journal processing
python3 DayOne_split.py ~/Dropbox/DayOne.md \
    --output-dir ~/Documents/Journal/$(date +%Y) \
    --date-format "%m-%d" \
    --verbose
```

### Scripting Example
```python
import subprocess
import sys

def split_dayone_export(export_file, output_dir):
    """Split DayOne export using the script."""
    cmd = [
        sys.executable, "DayOne_split.py",
        export_file,
        "--output-dir", output_dir,
        "--verbose"
    ]
    return subprocess.run(cmd, capture_output=True, text=True)
```

---

*DayOne_split.py provides a robust solution for processing DayOne exports with extensive customization options and error handling.*