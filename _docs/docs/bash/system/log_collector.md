# Log Collector (log_collector.sh)

Advanced log collection and filtering system with category-based organization and time-based queries.

## Overview

The log collector is a standalone, comprehensive log monitoring tool that provides advanced filtering, category-based organization, and flexible time-based queries. Designed for system administrators and developers who need powerful log analysis capabilities.

## Location

```
bash/system/log_collector/
├── log_collector.sh      # Main script
└── log_sources.conf      # Configuration file
```

## Features

- **Category-Based Filtering**: Organize logs by system, application, security, etc.
- **Time-Based Queries**: Filter logs by time ranges
- **Configurable Sources**: Define custom log sources and categories
- **Advanced Options**: Multiple output formats and filtering options
- **Standalone Design**: Self-contained with comprehensive functionality

## Basic Usage

```bash
cd bash/system/log_collector/

# Show usage information
./log_collector.sh --help

# Create example configuration
./log_collector.sh --create-config

# Basic log collection (last 10 minutes)
./log_collector.sh -t 10 -l 20
```

## Configuration

The `log_sources.conf` file defines log sources by category using pipe-delimited format:

```
system|/var/log/system.log|System messages
application|/var/log/app.log|Application logs
security|/var/log/auth.log|Security events
```

## Advanced Features

- **Multiple Categories**: Filter logs by specific categories
- **Custom Time Ranges**: Flexible time-based filtering
- **Output Control**: Configurable line limits and formatting
- **Real-time Monitoring**: Live log tail functionality
- **Export Options**: Multiple output formats for analysis

## Independence

This script is intentionally kept standalone and does not use shared libraries, making it portable and self-contained for system administration tasks.

## See Also
- [Log Size Checker](checkLogSize.md) - Monitor log file sizes
- [System Administration Overview](../overview.md#system-administration) - Related tools

---

*Script Location: `bash/system/log_collector/log_collector.sh`*  
*Author: Alexander Kucera / babylondreams.de*