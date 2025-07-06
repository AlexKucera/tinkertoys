# query_yes_no.py

Enhanced interactive user prompts for yes/no questions and multiple choice selections with robust input handling and error management.

## Overview

query_yes_no.py provides reliable, user-friendly functions for interactive command-line prompts. It handles yes/no questions with configurable defaults and supports multiple choice selections with flexible input validation and error handling.

## Features

- **Simple Yes/No Prompts** - Classic binary choice prompts with defaults
- **Multiple Choice Support** - Extended functionality for complex selections
- **Flexible Input Handling** - Accepts various input formats and abbreviations
- **Robust Error Management** - Handles EOF, interruptions, and invalid input
- **Configurable Defaults** - Optional default values for automated workflows
- **Case Sensitivity Options** - Configurable case-sensitive or insensitive matching

## Basic Usage

### Yes/No Prompts
```python
from query_yes_no import query_yes_no

# Simple yes/no question with default "yes"
if query_yes_no("Do you want to continue?"):
    print("Continuing...")
else:
    print("Stopping...")

# Default "no"
if query_yes_no("Delete all files?", default="no"):
    print("Files deleted")
else:
    print("Files preserved")

# No default - user must provide answer
try:
    result = query_yes_no("Proceed with installation?", default=None)
    if result:
        install_software()
except KeyboardInterrupt:
    print("Installation cancelled")
```

### Multiple Choice Prompts
```python
from query_yes_no import query_choice

# Simple choice selection
choices = ["red", "green", "blue"]
color = query_choice("Choose a color:", choices)
print(f"You selected: {color}")

# With default selection
color = query_choice("Choose a color:", choices, default="blue")

# Case-sensitive choices
programming_languages = ["Python", "JavaScript", "Go"]
language = query_choice(
    "Select language:", 
    programming_languages, 
    case_sensitive=True
)

# Using index as default
action = query_choice(
    "Select action:", 
    ["start", "stop", "restart"], 
    default=0  # "start"
)
```

## API Reference

### query_yes_no(question, default="yes")

Ask a yes/no question with configurable default.

**Parameters:**
- `question` (str): Question text to display to user
- `default` (str, optional): Default answer ("yes", "no", or None)

**Returns:**
- `bool`: True for yes, False for no

**Raises:**
- `ValueError`: If default is not "yes", "no", or None
- `KeyboardInterrupt`: If user cancels with Ctrl+C

**Accepted Inputs:**
- Yes: "yes", "y", "ye", "YES", "Y", "Yes"
- No: "no", "n", "NO", "N", "No"
- Empty: Uses default if provided

**Example:**
```python
# Basic usage
proceed = query_yes_no("Continue with operation?")

# With explicit default
dangerous = query_yes_no("Delete everything?", default="no")

# Require explicit answer
confirmed = query_yes_no("Are you absolutely sure?", default=None)
```

### query_choice(question, choices, default=None, case_sensitive=False)

Ask a multiple choice question with flexible selection options.

**Parameters:**
- `question` (str): Question text to display
- `choices` (list): List of available choices
- `default` (str or int, optional): Default choice (string value or index)
- `case_sensitive` (bool): Whether choices are case-sensitive

**Returns:**
- `str`: Selected choice as string

**Raises:**
- `ValueError`: If choices list is empty or default is invalid
- `KeyboardInterrupt`: If user cancels with Ctrl+C

**Example:**
```python
# Basic multiple choice
options = ["create", "update", "delete"]
action = query_choice("Select action:", options)

# With string default
env = query_choice("Environment:", ["dev", "staging", "prod"], default="dev")

# With index default
priority = query_choice("Priority:", ["low", "medium", "high"], default=1)

# Case-sensitive matching
framework = query_choice(
    "Framework:", 
    ["Flask", "Django", "FastAPI"], 
    case_sensitive=True
)
```

## Advanced Examples

### Configuration Wizard
```python
from query_yes_no import query_yes_no, query_choice

def setup_wizard():
    """Interactive setup wizard using prompts."""
    config = {}
    
    print("=== Application Setup Wizard ===")
    
    # Database configuration
    if query_yes_no("Configure database connection?"):
        db_types = ["sqlite", "postgresql", "mysql"]
        config['database'] = query_choice("Database type:", db_types)
        
        if config['database'] != "sqlite":
            config['db_host'] = input("Database host: ")
            config['db_port'] = input("Database port: ")
    
    # API configuration
    if query_yes_no("Enable API server?", default="yes"):
        config['api_enabled'] = True
        
        port_options = ["8000", "8080", "3000"]
        config['api_port'] = query_choice("API port:", port_options, default="8000")
        
        if query_yes_no("Enable authentication?", default="no"):
            auth_methods = ["jwt", "session", "api_key"]
            config['auth_method'] = query_choice("Auth method:", auth_methods)
    
    # Environment selection
    environments = ["development", "staging", "production"]
    config['environment'] = query_choice(
        "Target environment:", 
        environments, 
        default="development"
    )
    
    # Confirmation
    print("\nConfiguration Summary:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    if query_yes_no("\nSave this configuration?"):
        save_config(config)
        print("Configuration saved!")
    else:
        print("Configuration discarded.")
    
    return config

def save_config(config):
    """Save configuration to file."""
    import json
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
```

### Interactive File Operations
```python
import os
import shutil
from query_yes_no import query_yes_no, query_choice

def interactive_file_manager(directory):
    """Interactive file management with user prompts."""
    if not os.path.exists(directory):
        if query_yes_no(f"Directory {directory} doesn't exist. Create it?"):
            os.makedirs(directory)
        else:
            return
    
    while True:
        # List files
        files = os.listdir(directory)
        if not files:
            print("Directory is empty")
            if not query_yes_no("Continue anyway?"):
                break
        else:
            print(f"\nFiles in {directory}:")
            for i, filename in enumerate(files, 1):
                print(f"  {i}. {filename}")
        
        # Action selection
        actions = ["add file", "delete file", "rename file", "exit"]
        action = query_choice("\nSelect action:", actions, default="exit")
        
        if action == "exit":
            break
        elif action == "add file":
            filename = input("Enter filename: ")
            filepath = os.path.join(directory, filename)
            with open(filepath, 'w') as f:
                f.write("# New file created by interactive manager\n")
            print(f"Created: {filename}")
        
        elif action == "delete file" and files:
            target = query_choice("Select file to delete:", files)
            if query_yes_no(f"Really delete {target}?", default="no"):
                os.remove(os.path.join(directory, target))
                print(f"Deleted: {target}")
        
        elif action == "rename file" and files:
            old_name = query_choice("Select file to rename:", files)
            new_name = input("Enter new name: ")
            old_path = os.path.join(directory, old_name)
            new_path = os.path.join(directory, new_name)
            shutil.move(old_path, new_path)
            print(f"Renamed: {old_name} -> {new_name}")

# Usage
interactive_file_manager("/tmp/test_dir")
```

### Deployment Confirmation
```python
def deployment_workflow():
    """Safe deployment with multiple confirmation steps."""
    
    # Environment selection
    environments = ["staging", "production"]
    target_env = query_choice("Deploy to which environment?", environments)
    
    if target_env == "production":
        print("⚠️  WARNING: You are deploying to PRODUCTION!")
        if not query_yes_no("Are you absolutely sure?", default="no"):
            print("Deployment cancelled")
            return False
        
        # Additional production checks
        checks = [
            "All tests are passing",
            "Code review is complete", 
            "Database migrations are ready",
            "Monitoring is configured"
        ]
        
        print("\nPre-deployment checklist:")
        for check in checks:
            if not query_yes_no(f"✓ {check}?", default="no"):
                print(f"❌ Failed: {check}")
                print("Please complete all checks before deploying")
                return False
        
        # Final confirmation
        if not query_yes_no("\n🚀 Deploy to production now?", default="no"):
            print("Deployment cancelled")
            return False
    
    # Deployment options
    deploy_options = ["full", "rolling", "canary"]
    strategy = query_choice("Deployment strategy:", deploy_options, default="rolling")
    
    print(f"\nDeploying to {target_env} using {strategy} strategy...")
    return True
```

## Error Handling

### Graceful Interruption Handling
```python
def safe_interactive_session():
    """Example of handling user interruptions gracefully."""
    try:
        while True:
            if not query_yes_no("Continue session?"):
                print("Session ended by user choice")
                break
            
            # Simulate some work
            action = query_choice("What to do?", ["work", "rest", "quit"])
            
            if action == "quit":
                break
            elif action == "work":
                print("Working...")
            else:
                print("Resting...")
    
    except KeyboardInterrupt:
        print("\n\nSession interrupted by user (Ctrl+C)")
        if query_yes_no("Save progress before exiting?", default="yes"):
            print("Progress saved")
        print("Goodbye!")
    
    except EOFError:
        print("\nInput stream closed unexpectedly")
        print("Exiting...")
```

### Input Validation and Recovery
```python
def robust_configuration():
    """Configuration with validation and error recovery."""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Get user choices
            level = query_choice(
                "Log level:", 
                ["debug", "info", "warning", "error"],
                default="info"
            )
            
            if query_yes_no("Enable verbose output?"):
                verbose = True
            else:
                verbose = False
            
            # Validation
            if level == "debug" and not verbose:
                print("Warning: Debug level usually requires verbose output")
                if query_yes_no("Enable verbose for debug mode?"):
                    verbose = True
            
            return {'log_level': level, 'verbose': verbose}
        
        except (KeyboardInterrupt, EOFError):
            if attempt < max_retries - 1:
                print(f"\nRetry {attempt + 1}/{max_retries}")
                if query_yes_no("Try again?", default="yes"):
                    continue
            print("Configuration cancelled")
            return None
        
        except Exception as e:
            print(f"Unexpected error: {e}")
            if attempt < max_retries - 1:
                if query_yes_no("Retry configuration?"):
                    continue
            return None
    
    return None
```

## Integration Patterns

### CLI Tool Integration
```python
import argparse
from query_yes_no import query_yes_no, query_choice

def create_cli_with_interactive_mode():
    """CLI tool with optional interactive mode."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactive", "-i", action="store_true")
    parser.add_argument("--action", choices=["start", "stop", "restart"])
    parser.add_argument("--force", action="store_true")
    
    args = parser.parse_args()
    
    if args.interactive:
        # Interactive mode
        action = query_choice("Select action:", ["start", "stop", "restart"])
        force = query_yes_no("Force operation?", default="no")
    else:
        # Command-line mode
        action = args.action
        force = args.force
        
        # Prompt for dangerous operations if not forced
        if action == "stop" and not force:
            force = query_yes_no("Really stop the service?", default="no")
    
    if action and (force or action != "stop"):
        execute_action(action, force)
    else:
        print("Operation cancelled")

def execute_action(action, force):
    print(f"Executing: {action} (force: {force})")
```

### Testing Support
```python
import io
import sys
from contextlib import redirect_stdin
from query_yes_no import query_yes_no, query_choice

def test_interactive_functions():
    """Example of testing interactive functions with mocked input."""
    
    # Test yes/no with "yes" input
    test_input = io.StringIO("yes\n")
    with redirect_stdin(test_input):
        result = query_yes_no("Test question?")
        assert result == True
    
    # Test multiple choice
    test_input = io.StringIO("option2\n")
    with redirect_stdin(test_input):
        result = query_choice("Choose:", ["option1", "option2", "option3"])
        assert result == "option2"
    
    # Test with default
    test_input = io.StringIO("\n")  # Empty input, should use default
    with redirect_stdin(test_input):
        result = query_yes_no("Test with default?", default="yes")
        assert result == True
    
    print("All tests passed!")

# For automated testing environments
def mock_user_input(responses):
    """Context manager to mock user responses for testing."""
    class MockInput:
        def __init__(self, responses):
            self.responses = iter(responses)
        
        def __call__(self, prompt=""):
            try:
                response = next(self.responses)
                print(f"{prompt}{response}")  # Show what was "typed"
                return response
            except StopIteration:
                raise EOFError("No more mock responses")
    
    import builtins
    original_input = builtins.input
    builtins.input = MockInput(responses)
    
    try:
        yield
    finally:
        builtins.input = original_input

# Usage in tests
def test_configuration_wizard():
    responses = ["yes", "postgresql", "localhost", "5432", "no"]
    
    with mock_user_input(responses):
        config = setup_wizard()
        assert config['database'] == 'postgresql'
```

## Best Practices

### User Experience
1. **Clear Questions** - Use specific, unambiguous question text
2. **Sensible Defaults** - Provide safe defaults for common operations
3. **Confirmation for Destructive Actions** - Always confirm dangerous operations
4. **Progress Indication** - Show progress in multi-step processes

### Error Handling
1. **Graceful Interruption** - Handle Ctrl+C appropriately
2. **Input Validation** - Validate responses and provide helpful error messages
3. **Retry Logic** - Allow users to retry on errors
4. **Fallback Options** - Provide alternatives when primary options fail

### Code Organization
1. **Separation of Concerns** - Keep UI logic separate from business logic
2. **Testability** - Design for easy testing with mocked input
3. **Consistency** - Use consistent prompting patterns across application
4. **Documentation** - Document expected user interactions

---

*query_yes_no.py provides robust, user-friendly interactive prompts with comprehensive error handling and flexible configuration options for command-line applications.*