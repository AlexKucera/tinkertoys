# exportPinboard.py

Export Pinboard bookmarks as XML files for backup and further processing with automated daily backup functionality.

## Overview

exportPinboard.py creates automated backups of your Pinboard bookmarks by connecting to the Pinboard API and downloading all bookmarks in XML format. The script supports both one-time exports and scheduled backups with date-based file organization.

## Features

- **Secure Authentication** - Uses external credentials file for API token storage
- **Automated Backup** - Date-based backup file organization
- **Current File Maintenance** - Maintains an always-current backup file
- **Error Handling** - Comprehensive error handling for network and API issues
- **Configurable Paths** - All file paths configurable via command line
- **Rate Limiting** - Respects Pinboard API rate limits

## Usage

### Basic Usage
```bash
# Export with default paths
python3 exportPinboard.py

# Specify custom output directory
python3 exportPinboard.py --output-dir /path/to/backups
```

### Advanced Usage
```bash
# Use custom credentials file
python3 exportPinboard.py --credentials /path/to/credentials.txt

# Custom date format for backup files
python3 exportPinboard.py --date-format "%Y-%m-%d"

# Export to specific file without date-based naming
python3 exportPinboard.py --output-file /path/to/bookmarks.xml

# Don't update current file
python3 exportPinboard.py --no-current --verbose
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output-dir` | `-o` | Output directory for backups | `~/Dropbox/Apps/pinboard/` |
| `--output-file` | `-f` | Specific output file (overrides date-based naming) | None |
| `--credentials` | `-c` | Path to credentials file | `[output-dir]/pinboard_credentials.txt` |
| `--date-format` | `-d` | Date format for backup filenames | `%m-%d` |
| `--current-file` | - | Path for 'current' bookmark file | `[output-dir]/most_current_bookmarks.xml` |
| `--api-url` | - | Pinboard API base URL | `https://api.pinboard.in/v1/` |
| `--no-current` | - | Don't create/update current bookmarks file | False |
| `--verbose` | `-v` | Show detailed output | False |

## Setup

### 1. Get Pinboard API Token
1. Log into your Pinboard account
2. Go to Settings → Password
3. Your API token is shown as `username:HEXSTRING`

### 2. Create Credentials File
Create a text file containing your credentials:
```
username:your_api_token_here
```

**Security Note**: Keep this file secure and never commit it to version control.

### 3. Set Permissions
```bash
chmod 600 /path/to/pinboard_credentials.txt
```

## Default File Organization

The script creates a hierarchical backup structure:

```
~/Dropbox/Apps/pinboard/
├── pinboard_credentials.txt          # Your API credentials
├── most_current_bookmarks.xml        # Always current backup
├── 2024/
│   ├── pinboard-backup.01-15.xml    # January 15th backup
│   ├── pinboard-backup.01-16.xml    # January 16th backup
│   └── ...
├── 2023/
│   ├── pinboard-backup.12-31.xml
│   └── ...
```

## Date Format Examples

The `--date-format` option uses Python's strftime format:

- `%m-%d` → `07-05` (default)
- `%Y-%m-%d` → `2024-07-05`
- `%B-%d` → `July-05`
- `%Y%m%d` → `20240705`

## API Integration

### Authentication
The script uses Pinboard's API token authentication:
- No OAuth required
- Simple username:token format
- Secure token storage in external file

### API Endpoint
Uses the `/posts/all` endpoint to retrieve all bookmarks:
```
https://api.pinboard.in/v1/posts/all?auth_token=username:token
```

### Rate Limiting
- Respects Pinboard's API rate limits
- Includes timeout handling for slow responses
- Proper error handling for rate limit exceeded (429) responses

## Dependencies

### Required
- Python 3.11+
- Standard library modules only

### Optional
- **pytz** - For timezone-aware timestamps
  ```bash
  pip install pytz
  ```

## Error Handling

The script handles various error conditions:

- **Authentication failures** (401) - Invalid credentials
- **Rate limiting** (429) - API rate limit exceeded
- **Network errors** - Connection timeouts, DNS failures
- **File system errors** - Permission issues, disk space
- **API errors** - Malformed responses, server errors

## Examples

### Example 1: Daily Automated Backup
```bash
# Add to crontab for daily backup at 2 AM
0 2 * * * /usr/bin/python3 /path/to/exportPinboard.py --verbose
```

### Example 2: Custom Organization
```bash
python3 exportPinboard.py \
    --output-dir ~/Backups/Pinboard \
    --date-format "%Y-%m-%d" \
    --credentials ~/.config/pinboard/credentials
```

### Example 3: One-time Export
```bash
python3 exportPinboard.py \
    --output-file ~/Desktop/pinboard-export-$(date +%Y%m%d).xml \
    --no-current
```

## Output Format

The exported XML follows Pinboard's standard format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<posts user="username" update="2024-07-05T12:00:00Z" tag="">
    <post href="https://example.com" 
          description="Example Bookmark" 
          extended="Longer description here"
          meta="checksum" 
          hash="hash_value" 
          time="2024-07-05T10:30:00Z" 
          shared="yes" 
          toread="no" 
          tags="python programming" />
    <!-- More bookmarks... -->
</posts>
```

## Security Considerations

### Credential Storage
- Store credentials in a separate, secured file
- Use appropriate file permissions (600)
- Never hardcode credentials in scripts

### Network Security
- Uses HTTPS for all API communication
- Validates SSL certificates
- Includes timeout protection

### File Security
- Creates backup files with appropriate permissions
- Supports custom output locations outside of cloud sync
- Option to disable current file creation for added security

## Troubleshooting

### Common Issues

**Issue**: "Authentication failed" error
```
Solution: Check credentials file format and API token validity:
- Format: username:token (no spaces)
- Verify token in Pinboard settings
```

**Issue**: "Rate limit exceeded" error
```
Solution: Wait before retrying. Pinboard has strict rate limits:
- Wait at least 3 seconds between requests
- Use for scheduled backups, not frequent polling
```

**Issue**: Empty export file
```
Solution: Check API response and credentials:
python3 exportPinboard.py --verbose
```

### Debugging

Use verbose mode to see detailed operation information:

```bash
python3 exportPinboard.py --verbose
```

This shows:
- Credential file reading
- API request details
- File creation progress
- Any warnings or errors

## Integration

### Backup Scripts
```bash
#!/bin/bash
# Complete backup script with error handling

BACKUP_DIR="$HOME/Backups/Pinboard"
LOG_FILE="$BACKUP_DIR/backup.log"

echo "$(date): Starting Pinboard backup" >> "$LOG_FILE"

if python3 exportPinboard.py --output-dir "$BACKUP_DIR" --verbose; then
    echo "$(date): Backup completed successfully" >> "$LOG_FILE"
else
    echo "$(date): Backup failed" >> "$LOG_FILE"
    exit 1
fi
```

### Python Integration
```python
import subprocess
import sys
from pathlib import Path

def backup_pinboard(output_dir, verbose=False):
    """Create Pinboard backup using the script."""
    cmd = [
        sys.executable, "exportPinboard.py",
        "--output-dir", str(output_dir)
    ]
    if verbose:
        cmd.append("--verbose")
    
    return subprocess.run(cmd, capture_output=True, text=True)

# Usage
result = backup_pinboard(Path("~/Backups/Pinboard"), verbose=True)
if result.returncode == 0:
    print("Backup successful")
else:
    print(f"Backup failed: {result.stderr}")
```

---

*exportPinboard.py provides secure, automated Pinboard bookmark backup with flexible configuration and robust error handling.*