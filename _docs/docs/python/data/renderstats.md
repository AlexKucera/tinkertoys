# renderstats.py

Analyze render statistics for image sequences, calculate render times, identify missing frames, and detect corrupted files.

## Overview

renderstats.py is a comprehensive tool for analyzing rendered image sequences. It examines directories containing sequential images (like render outputs), identifies missing frames, detects corrupted files, and calculates detailed render statistics based on file modification times.

## Features

- **Frame Sequence Analysis** - Automatic detection of image sequence patterns
- **Missing Frame Detection** - Identifies gaps in frame sequences
- **Corruption Detection** - Finds files smaller than minimum expected size
- **Render Time Statistics** - Calculates total, average, min, and max render times
- **Recursive Processing** - Can analyze entire directory trees
- **Multiple Output Formats** - Console output or file reports
- **Flexible Configuration** - Customizable minimum file sizes and output formats

## Usage

### Basic Usage
```bash
# Analyze current directory
python3 renderstats.py .

# Analyze specific directory
python3 renderstats.py /path/to/renders

# Recursive analysis of all subdirectories
python3 renderstats.py /path/to/renders --recursive
```

### Advanced Usage
```bash
# Write reports to files instead of stdout
python3 renderstats.py /path/to/renders --file

# Custom output filename and minimum file size
python3 renderstats.py /path/to/renders \
    --name "render_report.txt" \
    --min-size 256

# Recursive with verbose output
python3 renderstats.py /path/to/renders \
    --recursive \
    --verbose
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `input` | - | Input directory or file to analyze | Required |
| `--recursive` | `-r` | Process all subdirectories recursively | False |
| `--file` | `-f` | Write statistics to file instead of stdout | False |
| `--name` | `-n` | Output filename for statistics | `renderstats.txt` |
| `--min-size` | - | Minimum file size in bytes for valid files | `128` |
| `--verbose` | `-v` | Show detailed progress information | False |

## Supported Image Sequences

The script automatically detects common image sequence naming patterns:

### Supported Patterns
- `render_001.exr`, `render_002.exr`, ...
- `shot_0150.jpg`, `shot_0151.jpg`, ...
- `frame.1001.png`, `frame.1002.png`, ...
- `beauty_v001_0100.tiff`, `beauty_v001_0101.tiff`, ...

### Sequence Detection
- Uses regex pattern matching to identify frame numbers
- Supports various numbering schemes (3-6 digits)
- Handles different separators (underscores, dots, hyphens)
- Works with any image file extension

## Analysis Features

### Frame Analysis
- **Frame Range Detection** - Identifies first and last frame numbers
- **Sequence Validation** - Checks for complete frame sequences
- **Gap Detection** - Finds missing frames in sequences
- **Range Reporting** - Groups consecutive frames into ranges

### File Integrity
- **Size Validation** - Identifies suspiciously small files
- **Corruption Detection** - Flags potential render failures
- **Custom Thresholds** - Configurable minimum file sizes
- **Pattern Analysis** - Correlates file sizes with render quality

### Render Statistics
- **Total Render Time** - Time from first to last frame completion
- **Average Frame Time** - Mean time per frame
- **Performance Analysis** - Fastest and slowest frame times
- **Timeline Analysis** - Render progression over time

## Output Format

### Console Output
```
Analysis for: /path/to/renders
============================================================

FRAME ANALYSIS:
Frame range: 1001 to 1100
Total frames found: 98
Continuous ranges: 1001-1050, 1052-1100

MISSING FRAMES (2):
Missing: 1051

CORRUPTED FILES (1 files < 128 bytes):
Frames: 1055

RENDER STATISTICS:
Total render time: 2 hours 15 minutes 30.50 seconds
Files processed: 98
Average per frame: 1 minutes 23.78 seconds
Fastest frame: 45.20 seconds
Slowest frame: 3 minutes 12.10 seconds
```

### File Output
When using `--file` option, creates detailed reports with:
- Complete analysis summary
- File-by-file details
- Statistics breakdown
- Timestamp information

## Examples

### Example 1: Basic Analysis
```bash
python3 renderstats.py ~/Renders/Shot001
```
Analyzes a single shot directory and displays results in console.

### Example 2: Batch Processing
```bash
python3 renderstats.py ~/Renders --recursive --file --verbose
```
Processes all shots in the Renders directory, creating individual report files.

### Example 3: Quality Control
```bash
python3 renderstats.py ~/Renders/Shot001 \
    --min-size 1024 \
    --name "qc_report.txt" \
    --file
```
Generates quality control report with stricter file size requirements.

### Example 4: Pipeline Integration
```bash
# Process multiple shot directories
for shot in ~/Renders/Shot*; do
    python3 renderstats.py "$shot" \
        --file \
        --name "$(basename "$shot")_stats.txt"
done
```

## Render Time Calculation

### Methodology
The script calculates render times based on file modification timestamps:

1. **Collects Timestamps** - Gets modification time for all sequence files
2. **Sorts Chronologically** - Orders files by completion time
3. **Calculates Intervals** - Measures time between consecutive frames
4. **Aggregates Statistics** - Computes total, average, min, max times

### Accuracy Considerations
- **File System Precision** - Limited by filesystem timestamp resolution
- **Network Rendering** - May be affected by clock synchronization
- **Parallel Rendering** - Works best with sequential rendering
- **Post-Processing** - Excludes files modified after rendering

## Integration

### Pipeline Scripts
```bash
#!/bin/bash
# Render analysis pipeline

RENDER_DIR="$1"
REPORT_DIR="$HOME/Reports"

echo "Analyzing renders in: $RENDER_DIR"

# Generate comprehensive report
python3 renderstats.py "$RENDER_DIR" \
    --recursive \
    --file \
    --name "render_analysis_$(date +%Y%m%d).txt" \
    --verbose

# Generate summary for email
python3 renderstats.py "$RENDER_DIR" \
    --min-size 256 > "$REPORT_DIR/summary.txt"
```

### Python Integration
```python
import subprocess
import sys
from pathlib import Path

def analyze_renders(render_dir, output_file=None):
    """Analyze render directory and return statistics."""
    cmd = [
        sys.executable, "renderstats.py",
        str(render_dir),
        "--recursive"
    ]
    
    if output_file:
        cmd.extend(["--file", "--name", str(output_file)])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None

# Usage
stats = analyze_renders(Path("~/Renders/Shot001"))
if stats:
    print("Analysis completed successfully")
    print(stats)
```

## Dependencies

### Required
- Python 3.11+
- Standard library modules only

### Integration with Timer Module
- Imports timing utilities from `development/timer.py`
- Uses shared time formatting functions
- Consistent time display across tools

## Troubleshooting

### Common Issues

**Issue**: "No sequential files found" message
```
Solution: Check that directory contains properly named image sequences:
- Files should have frame numbers (render_001.exr)
- Use consistent naming patterns
- Verify file extensions are recognized
```

**Issue**: Incorrect render times
```
Solution: Verify file modification times are accurate:
- Check if files were copied (preserves original times)
- Ensure clock synchronization in network rendering
- Consider using --verbose to see timestamp details
```

**Issue**: Large number of "corrupted" files
```
Solution: Adjust minimum file size threshold:
python3 renderstats.py directory --min-size 1024
```

### Debugging

Use verbose mode for detailed processing information:

```bash
python3 renderstats.py directory --verbose
```

This shows:
- Files being processed
- Frame number detection
- Timestamp analysis
- Statistics calculations

## Performance Considerations

### Large Datasets
- **Memory Efficient** - Processes files incrementally
- **I/O Optimized** - Minimal file system calls
- **Scalable** - Handles thousands of files efficiently

### Network Filesystems
- **Timestamp Caching** - Caches file stats to reduce network calls
- **Batch Processing** - Groups operations for efficiency
- **Timeout Handling** - Graceful handling of slow network access

---

*renderstats.py provides comprehensive analysis of render sequences with detailed statistics and quality control features for production pipelines.*