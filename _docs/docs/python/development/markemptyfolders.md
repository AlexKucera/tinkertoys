# markemptyfolders.py

Create placeholder files in empty directories to make them trackable with Git, with comprehensive options for cleanup and customization.

## Overview

markemptyfolders.py solves the common Git problem of empty directories not being tracked in version control. The script automatically finds empty directories and creates placeholder files (typically `.gitkeep`) to preserve the directory structure in your repository.

## Features

- **Automatic Discovery** - Finds all empty directories in a project tree
- **Customizable Placeholders** - Configure placeholder filename and content
- **Exclusion Rules** - Skip system directories and hidden folders
- **Cleanup Mode** - Remove placeholders from directories that are no longer empty
- **Dry Run Support** - Preview operations before making changes
- **Verbose Output** - Detailed logging of all operations

## Usage

### Basic Usage
```bash
# Mark empty folders with .gitkeep files
python3 markemptyfolders.py /path/to/project

# Use custom placeholder filename
python3 markemptyfolders.py /path/to/project --name "keepme.md"

# Dry run to see what would be done
python3 markemptyfolders.py /path/to/project --dry-run
```

### Advanced Usage
```bash
# Remove existing placeholders from non-empty directories
python3 markemptyfolders.py /path/to/project --cleanup

# Include hidden directories
python3 markemptyfolders.py /path/to/project --include-hidden

# Custom exclusions and verbose output
python3 markemptyfolders.py /path/to/project \
    --exclude .git .svn __pycache__ \
    --verbose
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `path` | - | Directory path to scan for empty folders | Required |
| `--name` | `-n` | Name for placeholder files | `.gitkeep` |
| `--content` | `-c` | Custom content for placeholder files | Default explanation |
| `--exclude` | - | Directory names to exclude | `.git .svn .hg __pycache__` |
| `--include-hidden` | - | Include hidden directories (starting with .) | False |
| `--cleanup` | - | Remove placeholder files from non-empty directories | False |
| `--dry-run` | - | Show what would be done without making changes | False |
| `--verbose` | `-v` | Show detailed output | False |

## Default Placeholder Content

When creating placeholder files, the script uses this default content:

```
This is a placeholder file to keep this directory trackable with Git.
Git doesn't track empty directories, so this file preserves the
directory structure in version control.

You can safely delete this file once the directory contains other files.
```

## Exclusion Rules

### Default Exclusions
The script automatically excludes common system directories:
- `.git` - Git repository metadata
- `.svn` - Subversion metadata  
- `.hg` - Mercurial metadata
- `__pycache__` - Python bytecode cache

### Custom Exclusions
```bash
# Add custom exclusions
python3 markemptyfolders.py /path/to/project \
    --exclude .git .svn node_modules .vscode
```

### Hidden Directory Handling
By default, hidden directories (starting with `.`) are excluded:

```bash
# Include hidden directories
python3 markemptyfolders.py /path/to/project --include-hidden
```

## Examples

### Example 1: New Project Setup
```bash
# Set up Git placeholders for a new project
cd /path/to/new/project
python3 markemptyfolders.py . --verbose
git add .
git commit -m "Add directory structure placeholders"
```

### Example 2: Cleanup After Development
```bash
# Remove unnecessary placeholders
python3 markemptyfolders.py /path/to/project --cleanup --verbose
```

### Example 3: Custom Documentation Placeholders
```bash
# Create custom README placeholders
python3 markemptyfolders.py /path/to/project \
    --name "README.md" \
    --content "# Directory Documentation\n\nThis directory is reserved for future content."
```

### Example 4: Selective Processing
```bash
# Process only source directories
python3 markemptyfolders.py /path/to/project/src \
    --exclude __pycache__ .pytest_cache \
    --name ".keep" \
    --dry-run
```

## Cleanup Mode

The cleanup mode removes placeholder files from directories that are no longer empty:

```bash
python3 markemptyfolders.py /path/to/project --cleanup
```

### Cleanup Logic
1. **Find Placeholders** - Locates all files matching the placeholder name
2. **Check Directory** - Counts other files in the same directory
3. **Remove if Populated** - Deletes placeholder if directory has other files
4. **Preserve if Empty** - Keeps placeholder in still-empty directories

### Cleanup Output
```
Cleaning up placeholder files named '.gitkeep'
Removed: /project/src/utils/.gitkeep (directory now has 3 other files)
Removed: /project/docs/api/.gitkeep (directory now has 1 other files)
Removed 2 placeholder files from non-empty directories
```

## Integration

### Git Workflow
```bash
#!/bin/bash
# Git pre-commit hook for directory structure

echo "Checking for empty directories..."
python3 /tools/markemptyfolders.py . --dry-run

if [ $? -eq 0 ]; then
    echo "Directory structure preserved"
else
    echo "Adding placeholder files..."
    python3 /tools/markemptyfolders.py . --verbose
    git add .gitkeep
fi
```

### Build Scripts
```bash
#!/bin/bash
# Project initialization script

echo "Setting up project structure..."

# Create initial directories
mkdir -p {src,tests,docs,config}/{api,utils,models}

# Add Git placeholders
python3 markemptyfolders.py . --verbose

# Initialize Git repository
git init
git add .
git commit -m "Initial project structure"
```

### CI/CD Integration
```yaml
# GitHub Actions workflow
name: Check Directory Structure
on: [push, pull_request]

jobs:
  check-structure:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Check for empty directories
      run: |
        python3 markemptyfolders.py . --dry-run
        if [ $? -ne 0 ]; then
          echo "Empty directories found without placeholders"
          exit 1
        fi
```

## Directory Structure Analysis

### Before Processing
```
project/
├── src/
│   ├── api/          # Empty
│   ├── models/       # Empty
│   └── utils/
│       └── helpers.py
├── tests/            # Empty
├── docs/
│   └── README.md
└── config/           # Empty
```

### After Processing
```
project/
├── src/
│   ├── api/
│   │   └── .gitkeep  # Added
│   ├── models/
│   │   └── .gitkeep  # Added
│   └── utils/
│       └── helpers.py
├── tests/
│   └── .gitkeep      # Added
├── docs/
│   └── README.md
└── config/
    └── .gitkeep      # Added
```

## Performance Considerations

### Large Repositories
- **Efficient Scanning** - Uses `pathlib.rglob()` for fast directory traversal
- **Memory Efficient** - Processes directories one at a time
- **I/O Optimized** - Minimal file system operations

### Network Filesystems
- **Batch Operations** - Groups file operations when possible
- **Error Handling** - Graceful handling of permission issues
- **Timeout Resistance** - Continues processing if individual operations fail

## Troubleshooting

### Common Issues

**Issue**: Permission denied errors
```
Solution: Ensure write permissions to target directories:
chmod -R u+w /path/to/project
```

**Issue**: Placeholders not being created
```
Solution: Check exclusion rules and directory permissions:
python3 markemptyfolders.py /path/to/project --verbose --dry-run
```

**Issue**: Too many placeholder files created
```
Solution: Use exclusion rules to skip unwanted directories:
python3 markemptyfolders.py /path/to/project \
    --exclude .git .svn node_modules .vscode __pycache__
```

### Debugging

Use verbose and dry-run modes together for detailed analysis:

```bash
python3 markemptyfolders.py /path/to/project --verbose --dry-run
```

This shows:
- Directories being scanned
- Exclusion rule applications
- Files that would be created
- Any errors or issues encountered

## Best Practices

### Repository Setup
1. **Run Early** - Execute during initial project setup
2. **Include in Documentation** - Document placeholder strategy in README
3. **Automate** - Include in project initialization scripts
4. **Regular Cleanup** - Periodically remove unnecessary placeholders

### Placeholder Management
1. **Consistent Naming** - Use standard names like `.gitkeep` or `.keep`
2. **Descriptive Content** - Include helpful explanations in placeholder files
3. **Version Control** - Commit placeholders with meaningful messages
4. **Team Communication** - Ensure team understands placeholder purpose

### Automation
1. **Pre-commit Hooks** - Automatically check for empty directories
2. **CI/CD Integration** - Validate directory structure in pipelines
3. **Build Scripts** - Include in project setup automation
4. **Documentation** - Keep usage examples in project docs

---

*markemptyfolders.py provides comprehensive directory structure preservation for Git repositories with flexible configuration and cleanup capabilities.*