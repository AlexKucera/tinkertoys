# Log Sources Configuration (log_sources.conf)

Configuration file defining log sources and categories for the advanced log collection system.

## Configuration File

**Location**: `config/log_sources.conf`

### Format
```
category|log_path|description
```

### Example Configuration
```
system|/var/log/system.log|System messages and kernel events
application|/var/log/app.log|Application-specific logging
security|/var/log/auth.log|Authentication and security events
network|/var/log/network.log|Network connectivity and traffic
database|/var/log/mysql/error.log|Database errors and warnings
web|/var/log/apache2/access.log|Web server access logs
mail|/var/log/mail.log|Email server notifications
custom|/path/to/custom.log|Custom application logs
```

## Categories

### Standard Categories
- **system** - Core system messages
- **application** - Application-specific logs
- **security** - Security and authentication
- **network** - Network-related events
- **database** - Database operations
- **web** - Web server logs
- **mail** - Email system logs

### Custom Categories
Add your own categories for specific applications or services:
```
render|/var/log/render.log|3D rendering operations
backup|/var/log/backup.log|Backup system status
monitoring|/var/log/monitor.log|System monitoring alerts
```

## Usage Examples

### System Administration
```
system|/var/log/syslog|System daemon messages
kernel|/var/log/kern.log|Kernel messages
auth|/var/log/auth.log|User authentication
cron|/var/log/cron.log|Scheduled task execution
```

### Development Environment
```
app|/var/log/myapp.log|Main application logs
debug|/var/log/myapp_debug.log|Debug information
error|/var/log/myapp_error.log|Error tracking
performance|/var/log/performance.log|Performance metrics
```

### Production Services
```
nginx|/var/log/nginx/access.log|Web server access
redis|/var/log/redis/redis.log|Cache server logs
postgres|/var/log/postgresql/postgres.log|Database operations
docker|/var/log/docker.log|Container operations
```

## Log Collection Usage

### Category-Based Filtering
```bash
# Collect system logs only
./log_collector.sh -c system -t 60

# Multiple categories
./log_collector.sh -c "system,security" -t 30
```

### Time-Based Queries
```bash
# Last hour from all sources
./log_collector.sh -t 60 -l 50

# Last 24 hours from specific category
./log_collector.sh -c application -t 1440
```

## Best Practices

### File Paths
1. **Use absolute paths** for all log file locations
2. **Verify file permissions** - ensure log files are readable
3. **Check file existence** before adding to configuration
4. **Consider log rotation** - paths should account for rotated logs

### Category Naming
1. **Use descriptive names** that clearly indicate log source
2. **Keep names short** for command-line convenience
3. **Use consistent naming** across similar services
4. **Avoid special characters** in category names

### Descriptions
1. **Provide clear descriptions** for each log source
2. **Include service names** where applicable
3. **Note any special formatting** or important details
4. **Keep descriptions concise** but informative

## Troubleshooting

### File Not Found
- Verify log file paths exist
- Check file permissions (must be readable)
- Ensure services are actually writing to specified paths

### Permission Denied
- Add read permissions: `chmod +r /var/log/logfile`
- Add user to appropriate groups for log access
- Use sudo if necessary for system logs

### Empty Results
- Verify logs are being written to specified files
- Check that time range includes recent activity
- Ensure log format is compatible with collection tools

## Used By

- [Log Collector](../bash/system/log_collector.md) - Advanced log processing system

---

*Configuration file: `config/log_sources.conf`*