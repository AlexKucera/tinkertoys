# Disk Device Finder (getDiskDevice.sh)

Find disk device identifiers by searching for volume labels on macOS systems.

## Usage

```bash
getDiskDevice.sh [label]
```

### Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `label` | Optional | Disk label to search for | BackupSystem |

## Features
- **Label-Based Lookup**: Find disks by human-readable names
- **Device Identification**: Returns BSD device identifiers (e.g., /dev/disk2s1)
- **macOS Integration**: Uses diskutil for accurate disk information
- **Mount Status**: Works with both mounted and unmounted volumes

## Examples

```bash
# Search for default "BackupSystem" disk
./getDiskDevice.sh

# Find Time Machine disk
./getDiskDevice.sh "Time Machine"

# Find external drive
./getDiskDevice.sh "My External Drive"

# Use in scripts
DEVICE=$(./getDiskDevice.sh "Backup Drive")
if [[ -n "$DEVICE" ]]; then
    echo "Found backup disk at $DEVICE"
fi
```

## Exit Codes
- **0**: Disk found successfully
- **1**: Disk not found or error occurred

## Use Cases
- **Backup Scripts**: Locate backup drives automatically
- **Maintenance Tasks**: Find specific volumes for operations
- **System Administration**: Automate disk-based workflows

## See Also
- [System Functions](../lib/system_functions.md) - Disk management utilities
- [System Administration Overview](../overview.md#system-administration) - Related tools

---

*Script Location: `bash/system/getDiskDevice.sh`*  
*Author: Alexander Kucera / babylondreams.de*