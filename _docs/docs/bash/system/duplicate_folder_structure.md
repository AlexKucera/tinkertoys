# duplicate_folder_structure.sh

Efficient shell script for duplicating directory structures without copying files. Creates exact replicas of folder hierarchies using optimized find and mkdir operations.

## Overview

duplicate_folder_structure.sh creates a complete copy of a directory tree structure without copying any files. This shell script provides a fast, lightweight solution for creating template directory structures, preparing backup locations, or setting up parallel folder hierarchies.

I created both a Python and Shell version since they serve slightly different use cases:

 - Python version (duplicate_folder_structure.py): For integration into Python workflows, with advanced features like progress tracking and flexible configuration
 - Shell version (duplicate_folder_structure.sh): For quick command-line use and shell scripting integration


## Features

- **High Performance** - Optimized using `find` and `mkdir -p` for maximum efficiency
- **Flexible Naming** - Automatic destination generation with suffix/prefix options
- **Safety Features** - Dry-run mode, path validation, and confirmation prompts  
- **Progress Tracking** - Progress indicators for large directory operations
- **Error Handling** - Comprehensive error reporting with proper exit codes
- **Shell Integration** - Perfect for shell scripts and automation workflows
- **Resource Efficient** - Minimal memory usage regardless of directory size

## Usage

### Basic Usage
```bash
# Duplicate structure to specific destination
./duplicate_folder_structure.sh /source/project /backup/structure

# Generate destination with suffix
./duplicate_folder_structure.sh /project --suffix "_backup"

# Generate destination with prefix
./duplicate_folder_structure.sh /data --prefix "structure_"

# Dry-run to preview what would be created
./duplicate_folder_structure.sh /source /dest --dry-run
```

### Advanced Usage
```bash
# Verbose output with detailed progress
./duplicate_folder_structure.sh /large/project /backup --verbose

# Skip confirmation prompts for automation
./duplicate_folder_structure.sh /source /dest --force

# Combine options for automated workflows
./duplicate_folder_structure.sh /project \
    --suffix "_template" \
    --verbose \
    --force
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `SOURCE` | - | Source directory to duplicate structure from | Required |
| `DESTINATION` | - | Destination directory (optional with --suffix/--prefix) | None |
| `--suffix` | `-s` | Add suffix to source directory name for destination | None |
| `--prefix` | `-p` | Add prefix to source directory name for destination | None |
| `--dry-run` | `-d` | Show what would be done without making changes | False |
| `--verbose` | `-v` | Show detailed output and progress | False |
| `--force` | `-f` | Skip confirmation prompts | False |
| `--help` | `-h` | Show help message | - |

## Examples

### Example 1: Project Template Creation
```bash
# Create a template structure for new projects  
./duplicate_folder_structure.sh /master/project_template /new/client_project --verbose

# Output shows progress:
# Found 45 directories to duplicate
# Creating directory structure in: /new/client_project
# ================================================
# Created: /new/client_project/src
# Created: /new/client_project/src/components
# Created: /new/client_project/tests
# ...
# Operation completed in 0h:00m:02s
```

### Example 2: Backup Structure Preparation  
```bash
# Prepare backup directory structure
./duplicate_folder_structure.sh /important/data --suffix "_backup_structure"

# Creates: /important/data_backup_structure/
# With all subdirectories from /important/data/ but no files
```

### Example 3: Multiple Environment Setup
```bash
#!/bin/bash
# Set up development, staging, and production structures

SOURCE_ENV="/app/production"

./duplicate_folder_structure.sh "$SOURCE_ENV" --prefix "dev_" --force
./duplicate_folder_structure.sh "$SOURCE_ENV" --prefix "staging_" --force  
./duplicate_folder_structure.sh "$SOURCE_ENV" --prefix "test_" --force

echo "All environment structures created"
```

### Example 4: Large Directory Tree Processing
```bash
# Process large directory with progress tracking
./duplicate_folder_structure.sh /massive/dataset /backup/structure \
    --verbose \
    --dry-run

# Review the dry-run output, then execute:
./duplicate_folder_structure.sh /massive/dataset /backup/structure --verbose

# Output for large operations:
# Found 1,247 directories to duplicate
# Creating directory structure in: /backup/structure
# Processed 100/1247 directories...
# Processed 200/1247 directories...
# ...
# Operation completed in 0h:02m:15s
```

## Advanced Features

### Automatic Path Generation

The script can automatically generate destination paths using patterns:

```bash
# Suffix generation
./duplicate_folder_structure.sh /project --suffix "_folders"
# Creates: /project_folders/

# Prefix generation  
./duplicate_folder_structure.sh /data --prefix "structure_"
# Creates: /structure_data/

# Cannot use both suffix and prefix
./duplicate_folder_structure.sh /data --suffix "_a" --prefix "b_"
# Error: Cannot use both --suffix and --prefix
```

### Path Validation and Safety

The script includes comprehensive safety checks:

```bash
# Prevents dangerous operations
./duplicate_folder_structure.sh / /backup           # Error: Protected path
./duplicate_folder_structure.sh /source /source     # Error: Same path  
./duplicate_folder_structure.sh /parent /parent/sub # Error: Destination inside source
```

### Performance Optimization

The script uses optimized shell operations for maximum performance:

```bash
# Uses find with null-terminated output for safety
find "$source" -type d -print0 | while IFS= read -r -d '' dir; do
    # Process each directory efficiently
done

# Batch directory creation with mkdir -p
mkdir -p "$target_dir"
```

## Integration Examples

### Shell Script Integration

```bash
#!/bin/bash
# Project initialization script

setup_project_structure() {
    local template_dir="$1"
    local project_name="$2"
    local base_dir="/projects"
    
    local project_dir="$base_dir/$project_name"
    
    echo "Setting up project: $project_name"
    
    # Create directory structure
    if ./duplicate_folder_structure.sh "$template_dir" "$project_dir" --force --verbose; then
        echo "✓ Directory structure created"
        
        # Additional setup
        setup_config_files "$project_dir"
        set_permissions "$project_dir"
        
        echo "✓ Project setup complete: $project_dir"
        return 0
    else
        echo "✗ Failed to create project structure"
        return 1
    fi
}

setup_config_files() {
    local project_dir="$1"
    # Copy template configuration files
    cp /templates/config.template "$project_dir/config.ini"
    cp /templates/README.template "$project_dir/README.md"
}

set_permissions() {
    local project_dir="$1"
    # Set appropriate permissions
    find "$project_dir" -type d -exec chmod 755 {} \;
}

# Usage
setup_project_structure "/templates/web_app" "new_client_site"
```

### Automated Backup Workflow

```bash
#!/bin/bash
# Backup structure preparation script

BACKUP_BASE="/backup/structures"
LOG_FILE="/var/log/backup_prep.log"

prepare_backup_structures() {
    local -a source_dirs=("$@")
    local timestamp="$(date +%Y%m%d_%H%M%S)"
    
    echo "Starting backup structure preparation: $(date)" | tee -a "$LOG_FILE"
    
    for source in "${source_dirs[@]}"; do
        if [[ ! -d "$source" ]]; then
            echo "✗ Source does not exist: $source" | tee -a "$LOG_FILE"
            continue
        fi
        
        local source_name="$(basename "$source")"
        local backup_dest="$BACKUP_BASE/${source_name}_${timestamp}"
        
        echo "Preparing backup structure for: $source_name" | tee -a "$LOG_FILE"
        
        # Create backup directory structure
        if ./duplicate_folder_structure.sh "$source" "$backup_dest" --force --verbose >> "$LOG_FILE" 2>&1; then
            echo "✓ Structure prepared: $backup_dest" | tee -a "$LOG_FILE"
        else
            echo "✗ Failed: $source_name" | tee -a "$LOG_FILE"
        fi
    done
    
    echo "Backup structure preparation completed: $(date)" | tee -a "$LOG_FILE"
}

# Usage
prepare_backup_structures "/home/user" "/var/www" "/opt/applications"
```

### CI/CD Pipeline Integration

```bash
#!/bin/bash
# CI/CD deployment structure setup

setup_deployment_structure() {
    local environment="$1"
    local version="$2"
    
    local source_structure="/templates/deployment_template"
    local deployment_base="/deployments"
    local deployment_dir="$deployment_base/${environment}_${version}"
    
    echo "Setting up deployment structure for $environment v$version"
    
    # Create deployment directory structure
    if ./duplicate_folder_structure.sh "$source_structure" "$deployment_dir" --force; then
        echo "✓ Deployment structure created: $deployment_dir"
        
        # Set environment-specific permissions
        case "$environment" in
            "production")
                chmod -R 755 "$deployment_dir"
                ;;
            "staging"|"development")  
                chmod -R 775 "$deployment_dir"
                ;;
        esac
        
        # Create environment marker
        echo "$environment" > "$deployment_dir/.environment"
        echo "$version" > "$deployment_dir/.version"
        
        return 0
    else
        echo "✗ Failed to create deployment structure"
        return 1
    fi
}

# Usage in CI/CD pipeline
ENVIRONMENT="${CI_ENVIRONMENT_NAME:-development}"
VERSION="${CI_COMMIT_SHORT_SHA:-unknown}"

setup_deployment_structure "$ENVIRONMENT" "$VERSION"
```

### Batch Processing Script

```bash
#!/bin/bash
# Batch directory structure duplication

batch_duplicate_structures() {
    local config_file="$1"
    local dry_run="${2:-false}"
    
    # Config file format: source_dir|destination_pattern|options
    while IFS='|' read -r source dest_pattern options; do
        # Skip comments and empty lines
        [[ "$source" =~ ^#.*$ ]] || [[ -z "$source" ]] && continue
        
        echo "Processing: $source"
        
        # Build command
        local cmd_args=("$source")
        
        # Add destination or pattern
        if [[ "$dest_pattern" == --* ]]; then
            cmd_args+=("$dest_pattern")
        else
            cmd_args+=("$dest_pattern")
        fi
        
        # Add additional options
        if [[ -n "$options" ]]; then
            read -ra opts <<< "$options"
            cmd_args+=("${opts[@]}")
        fi
        
        # Add dry-run if requested
        if [[ "$dry_run" == true ]]; then
            cmd_args+=("--dry-run")
        fi
        
        # Execute command
        echo "Executing: ./duplicate_folder_structure.sh ${cmd_args[*]}"
        
        if ./duplicate_folder_structure.sh "${cmd_args[@]}"; then
            echo "✓ Completed: $source"
        else
            echo "✗ Failed: $source"
        fi
        
        echo "---"
        
    done < "$config_file"
}

# Example config file (batch_config.txt):
# /projects/template_a|--suffix "_copy"|--verbose
# /projects/template_b|/backup/template_b_structure|--force
# /data/important|--prefix "backup_"|--verbose --force

# Usage
batch_duplicate_structures "batch_config.txt" true   # Dry-run first
batch_duplicate_structures "batch_config.txt" false  # Execute
```

## Error Handling and Recovery

### Comprehensive Error Handling

The script includes robust error handling for common scenarios:

```bash
# Invalid source directory
./duplicate_folder_structure.sh /nonexistent /dest
# Error: source directory '/nonexistent' does not exist

# Source is not a directory  
./duplicate_folder_structure.sh /etc/passwd /dest
# Error: source directory '/etc/passwd' does not exist

# Destination inside source (prevents infinite recursion)
./duplicate_folder_structure.sh /parent /parent/child
# Error: Destination cannot be inside source directory

# Permission issues are handled gracefully
./duplicate_folder_structure.sh /restricted /dest
# Error: Failed to create directory: /dest/restricted_subdir
# Errors encountered: 5
# (Continues with accessible directories)
```

### Recovery and Validation

```bash
#!/bin/bash
# Structure validation and recovery script

validate_structure() {
    local source="$1"
    local destination="$2"
    
    echo "Validating structure duplication..."
    
    # Count directories in source
    local source_count
    source_count=$(find "$source" -type d | wc -l)
    
    # Count directories in destination  
    local dest_count
    dest_count=$(find "$destination" -type d 2>/dev/null | wc -l)
    
    if [[ "$source_count" -eq "$dest_count" ]]; then
        echo "✓ Structure validation passed: $source_count directories"
        return 0
    else
        echo "✗ Structure validation failed:"
        echo "  Source: $source_count directories"
        echo "  Destination: $dest_count directories"
        return 1
    fi
}

retry_failed_duplication() {
    local source="$1"
    local destination="$2"
    local max_retries="${3:-3}"
    
    for ((i=1; i<=max_retries; i++)); do
        echo "Attempt $i/$max_retries: Duplicating structure"
        
        if ./duplicate_folder_structure.sh "$source" "$destination" --force; then
            if validate_structure "$source" "$destination"; then
                echo "✓ Structure duplication successful on attempt $i"
                return 0
            fi
        fi
        
        echo "Attempt $i failed, retrying..."
        sleep 2
    done
    
    echo "✗ Structure duplication failed after $max_retries attempts"
    return 1
}

# Usage
retry_failed_duplication "/complex/source" "/backup/destination"
```

## Performance Considerations

### Optimization for Large Directory Trees

```bash
# For very large directory structures, monitor progress
./duplicate_folder_structure.sh /massive/dataset /backup \
    --verbose \
    2>&1 | tee duplication.log

# The script automatically shows progress for large operations:
# Processed 100/1247 directories...
# Processed 200/1247 directories...
```

### Benchmarking Performance

```bash
#!/bin/bash
# Benchmark duplicate_folder_structure.sh performance

benchmark_duplication() {
    local source="$1"
    local destination_base="$2"
    local iterations="${3:-3}"
    
    echo "Benchmarking directory structure duplication"
    echo "Source: $source"
    echo "Iterations: $iterations"
    echo ""
    
    local total_time=0
    local successful_runs=0
    
    for ((i=1; i<=iterations; i++)); do
        local dest="${destination_base}_test_${i}"
        
        # Clean up any existing destination
        [[ -d "$dest" ]] && rm -rf "$dest"
        
        echo "Iteration $i:"
        local start_time=$(date +%s)
        
        if ./duplicate_folder_structure.sh "$source" "$dest" --force; then
            local end_time=$(date +%s)
            local duration=$((end_time - start_time))
            
            echo "  Time: ${duration}s"
            total_time=$((total_time + duration))
            ((successful_runs++))
        else
            echo "  FAILED"
        fi
        
        echo ""
    done
    
    if [[ $successful_runs -gt 0 ]]; then
        local avg_time=$((total_time / successful_runs))
        echo "Results:"
        echo "  Successful runs: $successful_runs/$iterations"
        echo "  Average time: ${avg_time}s"
        echo "  Total time: ${total_time}s"
    else
        echo "No successful runs"
    fi
}

# Usage
benchmark_duplication "/large/source" "/tmp/benchmark" 5
```

## Best Practices

### Directory Structure Planning
1. **Test First** - Always use `--dry-run` to preview operations
2. **Use Descriptive Names** - Choose clear suffix/prefix patterns
3. **Validate Paths** - Ensure source paths are correct before execution
4. **Check Permissions** - Verify write access to destination areas

### Shell Script Integration
1. **Use --force Flag** - For automated scripts to skip prompts
2. **Capture Exit Codes** - Check `$?` after script execution
3. **Log Operations** - Redirect output to log files for audit trails
4. **Handle Errors** - Implement proper error handling in calling scripts

### Safety Procedures
1. **Backup Important Paths** - Don't duplicate over critical directories
2. **Test on Copies** - Test with non-critical data first
3. **Monitor Disk Space** - Ensure adequate space for new structures
4. **Document Operations** - Keep records of structure duplications

---

*duplicate_folder_structure.sh provides high-performance directory structure duplication with optimized shell operations, comprehensive error handling, and seamless integration capabilities for automation workflows.*