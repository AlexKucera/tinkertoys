# Log Size Checker (checkLogSize.sh)

Monitor log file sizes and validate they stay within specified limits for automated monitoring and maintenance.

## Usage

```bash
checkLogSize.sh [log_file] [max_size_kb]
```

### Arguments

| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `log_file` | Optional | Path to log file | ~/Documents/scripts/mount_unmount_bootable.log |
| `max_size_kb` | Optional | Maximum size in KB | 128 |

## Exit Codes
- **0**: File size within limits
- **1**: File size exceeds limit or error occurred

## Examples

```bash
# Check default log file
./checkLogSize.sh

# Check custom log with 256KB limit
./checkLogSize.sh /var/log/my.log 256

# Check with 1MB limit
./checkLogSize.sh ~/logs/debug.log 1024
```

## Automation

```bash
# Cron job for daily monitoring
0 9 * * * /path/to/checkLogSize.sh /var/log/app.log 500 || echo "Log file too large"

# Script integration
if ./checkLogSize.sh ~/app.log 1000; then
    echo "Log size OK"
else
    echo "Log rotation needed"
    logrotate ~/app.log
fi
```

## See Also
- [Log Collector](log_collector.md) - Advanced log processing
- [System Functions](../lib/system_functions.md) - Log management utilities

---

*Script Location: `bash/system/checkLogSize.sh`*  
*Author: Alexander Kucera / babylondreams.de*