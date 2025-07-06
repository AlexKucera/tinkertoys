# switch_paths.py

Bulk path replacement tool with JSON configuration support, flexible pattern matching, and comprehensive safety features for project migration and path management.

## Overview

switch_paths.py performs intelligent bulk find-and-replace operations on file paths within text files. It's designed for project migration scenarios where file paths need to be updated across multiple configuration files, scripts, or documentation.

## Features

- **JSON Configuration** - Store complex replacement patterns in configuration files
- **Flexible Pattern Matching** - Support for exact matches, regex patterns, and wildcards
- **Safety Features** - Dry-run mode, backup creation, and rollback capabilities
- **File Filtering** - Process specific file types or exclude certain files
- **Recursive Processing** - Handle entire directory trees
- **Detailed Reporting** - Comprehensive logs of all changes made

## Usage

### Basic Usage
```bash
# Simple path replacement
python3 switch_paths.py /project/files \
    --old-path "/old/base/path" \
    --new-path "/new/base/path"

# Dry-run to preview changes
python3 switch_paths.py /project/files \
    --old-path "/old/path" \
    --new-path "/new/path" \
    --dry-run

# Use JSON configuration file
python3 switch_paths.py /project/files \
    --config-file path_mappings.json
```

### Advanced Usage
```bash
# Filter by file extension
python3 switch_paths.py /project \
    --old-path "/old/path" \
    --new-path "/new/path" \
    --file-extensions .py .sh .conf \
    --recursive

# Create backups before modification
python3 switch_paths.py /project \
    --config-file mappings.json \
    --create-backup \
    --backup-suffix .backup

# Exclude specific files or patterns
python3 switch_paths.py /project \
    --old-path "/old/path" \
    --new-path "/new/path" \
    --exclude-patterns "*.log" "temp/*" \
    --recursive
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `directory` | - | Directory to process | Required |
| `--old-path` | - | Path to replace (if not using config file) | None |
| `--new-path` | - | Replacement path (if not using config file) | None |
| `--config-file` | `-c` | JSON configuration file with path mappings | None |
| `--recursive` | `-r` | Process subdirectories recursively | False |
| `--file-extensions` | `-e` | File extensions to process | All text files |
| `--exclude-patterns` | - | Patterns to exclude from processing | None |
| `--dry-run` | `-d` | Show what would be changed without modifying files | False |
| `--create-backup` | `-b` | Create backup files before modification | False |
| `--backup-suffix` | - | Suffix for backup files | `.bak` |
| `--verbose` | `-v` | Show detailed output | False |

## Configuration File Format

### JSON Configuration Structure
```json
{
  "description": "Project migration path mappings",
  "replacements": [
    {
      "name": "Update base directory",
      "old_path": "/old/project/base",
      "new_path": "/new/project/location",
      "pattern_type": "exact"
    },
    {
      "name": "Update config paths",
      "old_path": "/etc/oldapp/",
      "new_path": "/etc/newapp/",
      "pattern_type": "prefix"
    },
    {
      "name": "Update log file paths",
      "old_path": "(/var/log/)(\\w+)(\\.log)",
      "new_path": "/new/logs/$2.log", 
      "pattern_type": "regex"
    }
  ],
  "file_filters": {
    "include_extensions": [".py", ".sh", ".conf", ".yaml", ".json"],
    "exclude_patterns": ["*.pyc", "*.log", ".git/*"]
  },
  "options": {
    "create_backup": true,
    "backup_suffix": ".pre_migration",
    "case_sensitive": true
  }
}
```

### Pattern Types

#### Exact Match
```json
{
  "old_path": "/exact/path/to/replace",
  "new_path": "/new/exact/path",
  "pattern_type": "exact"
}
```

#### Prefix Match
```json
{
  "old_path": "/old/prefix/",
  "new_path": "/new/prefix/",
  "pattern_type": "prefix"
}
```

#### Regex Pattern
```json
{
  "old_path": "/logs/(\\w+)/(\\d+)/(.+\\.log)",
  "new_path": "/new_logs/$1/$2/$3",
  "pattern_type": "regex"
}
```

## Examples

### Example 1: Simple Project Migration
```bash
# Migrate project from /old/location to /new/location
python3 switch_paths.py /project/source \
    --old-path "/old/location" \
    --new-path "/new/location" \
    --recursive \
    --file-extensions .py .sh .conf \
    --create-backup \
    --verbose
```

### Example 2: Complex Migration with Configuration
Create `migration_config.json`:
```json
{
  "description": "Development to Production Migration", 
  "replacements": [
    {
      "name": "Update database paths",
      "old_path": "/dev/database/",
      "new_path": "/prod/database/",
      "pattern_type": "prefix"
    },
    {
      "name": "Update log directories", 
      "old_path": "/tmp/logs/",
      "new_path": "/var/log/app/",
      "pattern_type": "prefix"
    },
    {
      "name": "Update config files",
      "old_path": "/home/dev/config/",
      "new_path": "/etc/app/",
      "pattern_type": "prefix"
    }
  ],
  "file_filters": {
    "include_extensions": [".py", ".sh", ".conf", ".yaml"],
    "exclude_patterns": ["*.pyc", "*.log", "__pycache__/*"]
  },
  "options": {
    "create_backup": true,
    "backup_suffix": ".dev_backup"
  }
}
```

Execute migration:
```bash
python3 switch_paths.py /app/source \
    --config-file migration_config.json \
    --recursive \
    --dry-run  # Preview first

# After reviewing, execute
python3 switch_paths.py /app/source \
    --config-file migration_config.json \
    --recursive
```

### Example 3: Docker Container Path Updates
```json
{
  "description": "Update Docker volume paths",
  "replacements": [
    {
      "name": "Update volume mounts",
      "old_path": "(/host/data/)(\\w+)",
      "new_path": "/container/data/$2",
      "pattern_type": "regex"
    },
    {
      "name": "Update config mounts", 
      "old_path": "/host/config/",
      "new_path": "/etc/app/",
      "pattern_type": "prefix"
    }
  ],
  "file_filters": {
    "include_extensions": [".yml", ".yaml", ".json"],
    "exclude_patterns": [".git/*"]
  }
}
```

### Example 4: Windows to Linux Path Migration
```json
{
  "description": "Windows to Linux path migration",
  "replacements": [
    {
      "name": "Convert Windows drive paths",
      "old_path": "C:\\\\",
      "new_path": "/mnt/c/",
      "pattern_type": "exact"
    },
    {
      "name": "Convert backslashes to forward slashes",
      "old_path": "\\\\",
      "new_path": "/",
      "pattern_type": "exact"
    },
    {
      "name": "Update program files path",
      "old_path": "C:/Program Files/",
      "new_path": "/usr/local/",
      "pattern_type": "prefix"
    }
  ],
  "options": {
    "case_sensitive": false
  }
}
```

## Advanced Features

### Regex Pattern Replacement
Support for complex pattern matching with capture groups:

```json
{
  "name": "Update versioned paths",
  "old_path": "/app/version(\\d+)\\.(\\d+)/data/",
  "new_path": "/new_app/v$1.$2/storage/",
  "pattern_type": "regex"
}
```

### Conditional Replacements
Apply different replacements based on file context:

```json
{
  "replacements": [
    {
      "name": "Python imports", 
      "old_path": "from old_module",
      "new_path": "from new_module",
      "pattern_type": "exact",
      "file_types": [".py"]
    },
    {
      "name": "Shell script paths",
      "old_path": "/old/bin/",
      "new_path": "/new/bin/",
      "pattern_type": "prefix", 
      "file_types": [".sh", ".bash"]
    }
  ]
}
```

### Batch Processing Script
```bash
#!/bin/bash
# Batch process multiple projects

PROJECTS=(
    "/project1"
    "/project2" 
    "/project3"
)

CONFIG_FILE="standard_migration.json"
LOG_DIR="/var/log/path_migrations"

mkdir -p "$LOG_DIR"

for project in "${PROJECTS[@]}"; do
    project_name=$(basename "$project")
    log_file="$LOG_DIR/${project_name}_$(date +%Y%m%d_%H%M%S).log"
    
    echo "Processing $project..." | tee "$log_file"
    
    # Dry run first
    python3 switch_paths.py "$project" \
        --config-file "$CONFIG_FILE" \
        --recursive \
        --dry-run \
        --verbose >> "$log_file" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "Dry run successful, executing migration..." | tee -a "$log_file"
        
        # Execute migration
        python3 switch_paths.py "$project" \
            --config-file "$CONFIG_FILE" \
            --recursive \
            --create-backup \
            --verbose >> "$log_file" 2>&1
        
        if [ $? -eq 0 ]; then
            echo "✓ $project migrated successfully" | tee -a "$log_file"
        else
            echo "✗ $project migration failed" | tee -a "$log_file"
        fi
    else
        echo "✗ $project dry run failed" | tee -a "$log_file"
    fi
    
    echo "---" | tee -a "$log_file"
done
```

## Safety and Recovery Features

### Backup and Rollback
```bash
# Create timestamped backups
python3 switch_paths.py /project \
    --config-file migration.json \
    --create-backup \
    --backup-suffix ".backup_$(date +%Y%m%d_%H%M%S)"

# Rollback script
#!/bin/bash
# Rollback changes by restoring backups

find /project -name "*.backup_*" | while read backup_file; do
    original_file="${backup_file%.backup_*}"
    if [ -f "$backup_file" ]; then
        echo "Restoring: $original_file"
        cp "$backup_file" "$original_file"
    fi
done
```

### Validation and Verification
```python
import json
import subprocess

def validate_migration(directory, config_file):
    """Validate migration results."""
    
    # Load configuration
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    validation_results = []
    
    for replacement in config['replacements']:
        old_path = replacement['old_path']
        
        # Search for remaining old paths
        cmd = ['grep', '-r', old_path, directory]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            validation_results.append({
                'replacement': replacement['name'],
                'remaining_occurrences': result.stdout.strip().split('\n')
            })
    
    return validation_results

# Usage
results = validate_migration('/project', 'migration.json')
if results:
    print("Migration incomplete. Remaining old paths found:")
    for result in results:
        print(f"- {result['replacement']}: {len(result['remaining_occurrences'])} occurrences")
else:
    print("Migration validation passed - no old paths found")
```

## Integration Patterns

### CI/CD Pipeline Integration
```yaml
# GitHub Actions workflow
name: Project Migration
on: 
  workflow_dispatch:
    inputs:
      config_file:
        description: 'Migration configuration file'
        required: true
        default: 'migration_config.json'

jobs:
  migrate-paths:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Validate configuration
      run: |
        python3 -c "import json; json.load(open('${{ github.event.inputs.config_file }}'))"
    
    - name: Dry run migration
      run: |
        python3 switch_paths.py . \
          --config-file "${{ github.event.inputs.config_file }}" \
          --recursive \
          --dry-run \
          --verbose > migration_preview.txt
    
    - name: Upload preview
      uses: actions/upload-artifact@v2
      with:
        name: migration-preview
        path: migration_preview.txt
    
    - name: Execute migration
      if: github.event.inputs.execute == 'true'
      run: |
        python3 switch_paths.py . \
          --config-file "${{ github.event.inputs.config_file }}" \
          --recursive \
          --create-backup \
          --verbose
```

### Docker Container Migration
```dockerfile
# Dockerfile for migration container
FROM python:3.11-slim

COPY switch_paths.py /usr/local/bin/
COPY migration_configs/ /configs/

WORKDIR /workspace

ENTRYPOINT ["python3", "/usr/local/bin/switch_paths.py"]
```

Usage:
```bash
# Run migration in container
docker run --rm -v /host/project:/workspace migration-tool \
    /workspace \
    --config-file /configs/production_migration.json \
    --recursive \
    --create-backup
```

## Error Handling and Troubleshooting

### Common Issues and Solutions

**Issue**: "Permission denied" errors
```bash
# Fix file permissions before migration
find /project -type f -exec chmod 644 {} \;
find /project -type d -exec chmod 755 {} \;
```

**Issue**: Binary files being processed
```bash
# Add file type detection to config
{
  "file_filters": {
    "exclude_patterns": ["*.exe", "*.dll", "*.so", "*.dylib", "*.pyc"]
  }
}
```

**Issue**: Regex patterns not matching
```bash
# Test regex patterns separately
python3 -c "
import re
pattern = r'/logs/(\w+)/(\d+)/(.+\.log)'
test_string = '/logs/app/2024/error.log'
match = re.search(pattern, test_string)
if match:
    print('Match found:', match.groups())
else:
    print('No match')
"
```

### Debugging and Logging
```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('switch_paths_debug.log'),
        logging.StreamHandler()
    ]
)

# Add logging to switch_paths.py for debugging
def debug_replacement(file_path, old_pattern, new_pattern, matches):
    """Log detailed replacement information."""
    logging.debug(f"File: {file_path}")
    logging.debug(f"Pattern: {old_pattern} -> {new_pattern}")
    logging.debug(f"Matches found: {len(matches)}")
    for i, match in enumerate(matches):
        logging.debug(f"  Match {i+1}: {match}")
```

## Best Practices

### Migration Planning
1. **Test on Copies** - Always test migrations on copies of important data
2. **Incremental Approach** - Process one replacement type at a time
3. **Validation Scripts** - Create scripts to validate migration results
4. **Rollback Planning** - Ensure ability to rollback changes

### Configuration Management
1. **Version Control** - Keep migration configs in version control
2. **Environment-Specific** - Create separate configs for different environments
3. **Documentation** - Document the purpose of each replacement
4. **Validation** - Validate JSON configuration files before use

### Safety Procedures
1. **Always Dry-Run First** - Review changes before execution
2. **Create Backups** - Use backup features for important files
3. **Monitor Progress** - Use verbose mode for long operations
4. **Verify Results** - Check that replacements worked as expected

---

*switch_paths.py provides comprehensive bulk path replacement capabilities with JSON configuration support, safety features, and flexible pattern matching for project migration and path management workflows.*