#!/usr/bin/env python3
# encoding: utf-8
"""
timer.py

Timing utilities for debugging and performance measurement.
Can be used as a library or as a command-line stopwatch.

Created by Alexander Kucera
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import argparse
import sys
import time
import timeit
from typing import Optional


def secondsToHoursMinutesSeconds(seconds: float) -> str:
    """Convert seconds to human-readable format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string (e.g., "2 hours 30 minutes 15.25 seconds")
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    parts = []
    if hours != 0:
        parts.append(f"{int(hours)} hours")
    if minutes != 0:
        parts.append(f"{int(minutes)} minutes")
    
    parts.append(f"{seconds:.2f} seconds")
    
    return " ".join(parts)


def timer(elapsed: float = 0.0, name: str = '') -> float:
    """Timer function for debugging and performance measurement.
    
    Args:
        elapsed: Start time from a previous call (0.0 to start timing)
        name: Optional name for the timer
        
    Returns:
        Current time (use for subsequent calls)
        
    Example:
        start = timer()
        # ... do some work ...
        timer(start, "my operation")
    """
    current_time = timeit.default_timer()
    
    if elapsed != 0.0:
        running_time = current_time - elapsed
        time_string = secondsToHoursMinutesSeconds(running_time)
        prefix = f"{name} " if name else ""
        print(f"{prefix}Running Time: {time_string}")
    
    return current_time


class Stopwatch:
    """A simple stopwatch class for timing operations."""
    
    def __init__(self, name: str = "Stopwatch"):
        self.name = name
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.lap_times: list = []
    
    def start(self) -> None:
        """Start the stopwatch."""
        self.start_time = timeit.default_timer()
        self.end_time = None
        self.lap_times = []
        print(f"{self.name}: Started")
    
    def lap(self, label: str = None) -> float:
        """Record a lap time.
        
        Args:
            label: Optional label for the lap
            
        Returns:
            Lap time in seconds
        """
        if self.start_time is None:
            raise RuntimeError("Stopwatch not started")
        
        current_time = timeit.default_timer()
        
        if self.lap_times:
            lap_time = current_time - self.lap_times[-1][1]
        else:
            lap_time = current_time - self.start_time
        
        label = label or f"Lap {len(self.lap_times) + 1}"
        self.lap_times.append((label, current_time))
        
        print(f"{self.name}: {label} - {secondsToHoursMinutesSeconds(lap_time)}")
        return lap_time
    
    def stop(self) -> float:
        """Stop the stopwatch and return total time.
        
        Returns:
            Total elapsed time in seconds
        """
        if self.start_time is None:
            raise RuntimeError("Stopwatch not started")
        
        self.end_time = timeit.default_timer()
        total_time = self.end_time - self.start_time
        
        print(f"{self.name}: Stopped")
        print(f"{self.name}: Total time - {secondsToHoursMinutesSeconds(total_time)}")
        
        return total_time
    
    def reset(self) -> None:
        """Reset the stopwatch."""
        self.start_time = None
        self.end_time = None
        self.lap_times = []
        print(f"{self.name}: Reset")
    
    def status(self) -> None:
        """Show current status."""
        if self.start_time is None:
            print(f"{self.name}: Not started")
        elif self.end_time is None:
            current_time = timeit.default_timer()
            elapsed = current_time - self.start_time
            print(f"{self.name}: Running - {secondsToHoursMinutesSeconds(elapsed)}")
        else:
            total_time = self.end_time - self.start_time
            print(f"{self.name}: Stopped - {secondsToHoursMinutesSeconds(total_time)}")


def interactive_stopwatch(name: str = "Timer") -> None:
    """Run an interactive stopwatch from the command line.
    
    Args:
        name: Name for the stopwatch
    """
    stopwatch = Stopwatch(name)
    
    print(f"\nInteractive Stopwatch: {name}")
    print("Commands:")
    print("  start  - Start the timer")
    print("  lap    - Record a lap time")
    print("  stop   - Stop the timer")
    print("  reset  - Reset the timer")
    print("  status - Show current status")
    print("  quit   - Exit")
    print()
    
    while True:
        try:
            command = input("timer> ").strip().lower()
            
            if command == "start":
                stopwatch.start()
            elif command == "lap":
                if stopwatch.start_time is None:
                    print("Timer not started. Use 'start' first.")
                else:
                    stopwatch.lap()
            elif command == "stop":
                if stopwatch.start_time is None:
                    print("Timer not started. Use 'start' first.")
                else:
                    stopwatch.stop()
            elif command == "reset":
                stopwatch.reset()
            elif command == "status":
                stopwatch.status()
            elif command in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            elif command == "help":
                print("Commands: start, lap, stop, reset, status, quit")
            elif command == "":
                continue
            else:
                print(f"Unknown command: {command}. Type 'help' for commands.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("Goodbye!")
            break


def time_command(command: list, iterations: int = 1) -> None:
    """Time the execution of a command.
    
    Args:
        command: Command and arguments to execute
        iterations: Number of times to run the command
    """
    import subprocess
    
    print(f"Timing command: {' '.join(command)}")
    if iterations > 1:
        print(f"Running {iterations} iterations...")
    
    times = []
    
    for i in range(iterations):
        start_time = timeit.default_timer()
        
        try:
            result = subprocess.run(command, check=True, capture_output=True)
            end_time = timeit.default_timer()
            execution_time = end_time - start_time
            times.append(execution_time)
            
            if iterations > 1:
                print(f"Iteration {i+1}: {secondsToHoursMinutesSeconds(execution_time)}")
            
        except subprocess.CalledProcessError as e:
            print(f"Command failed with exit code {e.returncode}")
            return
        except FileNotFoundError:
            print(f"Command not found: {command[0]}")
            return
    
    if iterations == 1:
        print(f"Execution time: {secondsToHoursMinutesSeconds(times[0])}")
    else:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\nResults for {iterations} iterations:")
        print(f"  Average: {secondsToHoursMinutesSeconds(avg_time)}")
        print(f"  Minimum: {secondsToHoursMinutesSeconds(min_time)}")
        print(f"  Maximum: {secondsToHoursMinutesSeconds(max_time)}")


def main():
    """Main function for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Timing utilities for debugging and performance measurement.",
        epilog="""
Examples:
  # Interactive stopwatch
  %(prog)s --interactive
  
  # Time a command execution
  %(prog)s --command "ls -la"
  
  # Time a command multiple times
  %(prog)s --command "python script.py" --iterations 5
  
  # Simple countdown timer
  %(prog)s --countdown 300
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run interactive stopwatch mode"
    )
    parser.add_argument(
        "--command", "-c",
        help="Command to time (e.g., 'ls -la')"
    )
    parser.add_argument(
        "--iterations", "-n",
        type=int,
        default=1,
        help="Number of iterations for command timing (default: 1)"
    )
    parser.add_argument(
        "--countdown", "-t",
        type=int,
        help="Countdown timer in seconds"
    )
    parser.add_argument(
        "--name",
        default="Timer",
        help="Name for the timer (default: Timer)"
    )
    
    try:
        args = parser.parse_args()
        
        if args.interactive:
            interactive_stopwatch(args.name)
        elif args.command:
            command_parts = args.command.split()
            time_command(command_parts, args.iterations)
        elif args.countdown:
            print(f"Countdown: {args.countdown} seconds")
            try:
                for remaining in range(args.countdown, 0, -1):
                    print(f"\r{remaining:3d} seconds remaining...", end="", flush=True)
                    time.sleep(1)
                print("\r  0 seconds remaining... Time's up!")
            except KeyboardInterrupt:
                print("\nCountdown cancelled.")
        else:
            # Default: interactive mode
            interactive_stopwatch(args.name)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())