# timer.py

Comprehensive timing utilities for debugging, performance measurement, interactive stopwatch functionality, and command benchmarking.

## Overview

timer.py provides both library functions for programmatic timing and a full CLI application for interactive timing operations. It includes stopwatch functionality, command execution timing, countdown timers, and performance benchmarking tools.

## Features

- **Library Functions** - Import and use timing functions in your scripts
- **Interactive Stopwatch** - Full-featured CLI stopwatch with lap times
- **Command Timing** - Benchmark command execution with statistics
- **Countdown Timer** - Visual countdown with cancellation support
- **Performance Analysis** - Statistical analysis of multiple runs
- **Human-Readable Output** - Automatic formatting of time durations

## Usage

### Library Usage
```python
from timer import timer, secondsToHoursMinutesSeconds, Stopwatch

# Basic timing
start = timer()
# ... do some work ...
timer(start, "Operation completed")

# Advanced stopwatch
sw = Stopwatch("Database Query")
sw.start()
# ... perform query ...
sw.lap("Connection established")
# ... process results ...
sw.stop()
```

### CLI Usage
```bash
# Interactive stopwatch
python3 timer.py --interactive

# Time a command execution
python3 timer.py --command "ls -la"

# Time with multiple iterations
python3 timer.py --command "python script.py" --iterations 5

# Countdown timer
python3 timer.py --countdown 300
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--interactive` | `-i` | Run interactive stopwatch mode | False |
| `--command` | `-c` | Command to time (e.g., 'ls -la') | None |
| `--iterations` | `-n` | Number of iterations for command timing | 1 |
| `--countdown` | `-t` | Countdown timer in seconds | None |
| `--name` | - | Name for the timer | `Timer` |

## Library Functions

### timer(elapsed=0.0, name='')
Basic timing function for simple operations:

```python
# Start timing
start_time = timer()

# End timing with label
elapsed = timer(start_time, "Processing completed")
```

**Parameters:**
- `elapsed` - Start time from previous call (0.0 to start)
- `name` - Optional name for the timer operation

**Returns:** Current timestamp for subsequent calls

### secondsToHoursMinutesSeconds(seconds)
Convert seconds to human-readable format:

```python
# Convert duration to readable format
readable = secondsToHoursMinutesSeconds(3725.5)
# Returns: "1 hours 2 minutes 5.50 seconds"
```

### Stopwatch Class
Advanced timing with lap functionality:

```python
# Create named stopwatch
stopwatch = Stopwatch("Performance Test")

# Control operations
stopwatch.start()
stopwatch.lap("Checkpoint 1")
stopwatch.lap("Checkpoint 2")
total_time = stopwatch.stop()

# Status checking
stopwatch.status()
stopwatch.reset()
```

## Interactive Stopwatch Mode

### Commands
- `start` - Start the timer
- `lap` - Record a lap time
- `stop` - Stop the timer
- `reset` - Reset the timer
- `status` - Show current status
- `quit` - Exit the application

### Example Session
```
Interactive Stopwatch: Performance Test
Commands: start, lap, stop, reset, status, quit

timer> start
Performance Test: Started

timer> lap
Performance Test: Lap 1 - 12.34 seconds

timer> lap
Performance Test: Lap 2 - 8.76 seconds

timer> stop
Performance Test: Stopped
Performance Test: Total time - 21.10 seconds
```

## Command Timing

### Single Execution
```bash
python3 timer.py --command "python script.py"
```

Output:
```
Timing command: python script.py
Execution time: 2 minutes 15.30 seconds
```

### Multiple Iterations
```bash
python3 timer.py --command "python script.py" --iterations 5
```

Output:
```
Timing command: python script.py
Running 5 iterations...
Iteration 1: 2 minutes 15.30 seconds
Iteration 2: 2 minutes 12.85 seconds
Iteration 3: 2 minutes 14.10 seconds
Iteration 4: 2 minutes 13.45 seconds
Iteration 5: 2 minutes 16.20 seconds

Results for 5 iterations:
  Average: 2 minutes 14.38 seconds
  Minimum: 2 minutes 12.85 seconds
  Maximum: 2 minutes 16.20 seconds
```

## Countdown Timer

### Basic Countdown
```bash
python3 timer.py --countdown 300
```

Output:
```
Countdown: 300 seconds
300 seconds remaining...
299 seconds remaining...
...
  1 seconds remaining...
  0 seconds remaining... Time's up!
```

### Cancellation
Press `Ctrl+C` to cancel countdown:
```
Countdown cancelled.
```

## Examples

### Example 1: Script Performance Analysis
```python
#!/usr/bin/env python3
from timer import Stopwatch

def analyze_performance():
    sw = Stopwatch("Data Processing")
    sw.start()
    
    # Load data
    load_data()
    sw.lap("Data loaded")
    
    # Process data
    process_data()
    sw.lap("Data processed")
    
    # Save results
    save_results()
    sw.stop()

if __name__ == "__main__":
    analyze_performance()
```

### Example 2: Database Benchmark
```bash
# Time database operations
python3 timer.py --command "psql -c 'SELECT COUNT(*) FROM large_table;'" --iterations 10
```

### Example 3: Build Time Monitoring
```python
import subprocess
from timer import timer

def time_build():
    start = timer()
    
    # Run build
    result = subprocess.run(['make', 'all'], check=True)
    
    timer(start, "Build completed")
    return result.returncode == 0
```

### Example 4: Automated Testing
```bash
#!/bin/bash
echo "Running test suite with timing..."

python3 timer.py --command "pytest tests/" --name "Test Suite"
python3 timer.py --command "flake8 src/" --name "Linting"
python3 timer.py --command "mypy src/" --name "Type Checking"
```

## Integration

### CI/CD Pipeline
```yaml
# GitHub Actions example
- name: Run timed tests
  run: |
    python3 timer.py --command "pytest tests/" --iterations 3
```

### Development Workflow
```python
# Development timing decorator
from functools import wraps
from timer import timer

def timed(name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = timer()
            result = func(*args, **kwargs)
            timer(start, f"{name} - {func.__name__}")
            return result
        return wrapper
    return decorator

@timed("Database Operation")
def fetch_user_data(user_id):
    # Implementation here
    pass
```

### Performance Monitoring
```python
#!/usr/bin/env python3
import sys
from timer import Stopwatch

class PerformanceMonitor:
    def __init__(self):
        self.stopwatch = Stopwatch("System Monitor")
    
    def monitor_system(self):
        self.stopwatch.start()
        
        # Check system resources
        self.check_cpu()
        self.stopwatch.lap("CPU check")
        
        # Check memory
        self.check_memory()
        self.stopwatch.lap("Memory check")
        
        # Check disk
        self.check_disk()
        self.stopwatch.lap("Disk check")
        
        self.stopwatch.stop()

if __name__ == "__main__":
    monitor = PerformanceMonitor()
    monitor.monitor_system()
```

## Error Handling

### Common Errors
- **Command not found** - Clear error message for invalid commands
- **Permission denied** - Handles execution permission issues
- **Keyboard interruption** - Graceful handling of Ctrl+C
- **Invalid arguments** - Validation of numeric inputs

### Exception Handling
```python
from timer import Stopwatch, timer

try:
    sw = Stopwatch("Critical Operation")
    sw.start()
    # ... risky operation ...
    sw.stop()
except KeyboardInterrupt:
    print("Operation cancelled by user")
except Exception as e:
    print(f"Operation failed: {e}")
finally:
    # Cleanup if needed
    pass
```

## Dependencies

### Required
- Python 3.11+
- Standard library modules only

### No External Dependencies
- Uses only built-in modules
- No additional packages required
- Works in minimal Python environments

## Advanced Features

### Lap Time Analysis
```python
sw = Stopwatch("Complex Operation")
sw.start()

for i in range(10):
    # Process batch
    process_batch(i)
    sw.lap(f"Batch {i+1}")

# All lap times are stored and can be analyzed
total_time = sw.stop()
```

### Statistical Analysis
The command timing feature provides:
- **Average execution time** across multiple runs
- **Minimum and maximum** execution times
- **Standard deviation** calculations (when running many iterations)
- **Performance consistency** analysis

---

*timer.py provides comprehensive timing utilities for development, debugging, and performance analysis with both library and CLI interfaces.*