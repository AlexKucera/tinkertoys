#!/usr/bin/env python3
# encoding: utf-8
"""
applescript.py

Python wrapper for executing AppleScript on macOS.
Provides simple functions to run AppleScript code from Python and handle string escaping.

Based on work by Dr. Drang:
http://www.leancrew.com/all-this/2013/03/combining-python-and-applescript/

Modernized for Python 3 by Alexander Kucera
Copyright (c) 2024 BabylonDreams. All rights reserved.
"""

import platform
import subprocess
import sys
from typing import Optional, Union


class AppleScriptError(Exception):
    """Exception raised when AppleScript execution fails."""
    pass


def is_macos() -> bool:
    """Check if running on macOS."""
    return platform.system() == "Darwin"


def run_applescript(script: str, timeout: Optional[float] = None) -> str:
    """Run the given AppleScript and return the standard output.
    
    Args:
        script: AppleScript code to execute
        timeout: Maximum time to wait for script completion (seconds)
        
    Returns:
        Standard output from the AppleScript as a string
        
    Raises:
        AppleScriptError: If script execution fails
        OSError: If osascript is not available
        TimeoutExpired: If script times out
    """
    if not is_macos():
        raise AppleScriptError("AppleScript is only available on macOS")
    
    try:
        # Run osascript with the script as stdin
        process = subprocess.Popen(
            ['osascript', '-'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        stdout, stderr = process.communicate(input=script, timeout=timeout)
        
        if process.returncode != 0:
            raise AppleScriptError(f"AppleScript execution failed: {stderr.strip()}")
        
        return stdout.strip()
    
    except subprocess.TimeoutExpired:
        process.kill()
        raise AppleScriptError(f"AppleScript execution timed out after {timeout} seconds")
    
    except FileNotFoundError:
        raise OSError("osascript command not found. Are you running on macOS?")
    
    except Exception as e:
        raise AppleScriptError(f"Unexpected error running AppleScript: {e}")


def quote_string(text: str) -> str:
    """Return the AppleScript equivalent of the given string.
    
    Properly escapes quotes and other special characters for use in AppleScript.
    
    Args:
        text: String to quote for AppleScript
        
    Returns:
        Properly quoted string for use in AppleScript
    """
    if text is None:
        return '""'
    
    # Replace double quotes with AppleScript quote concatenation
    escaped = text.replace('"', '" & quote & "')
    return f'"{escaped}"'


def run_applescript_function(function_name: str, *args, **kwargs) -> str:
    """Run a specific AppleScript function with arguments.
    
    Args:
        function_name: Name of the AppleScript function to call
        *args: Positional arguments to pass to the function
        **kwargs: Keyword arguments (timeout)
        
    Returns:
        Result from the AppleScript function
    """
    timeout = kwargs.get('timeout')
    
    # Convert arguments to AppleScript format
    as_args = []
    for arg in args:
        if isinstance(arg, str):
            as_args.append(quote_string(arg))
        elif isinstance(arg, bool):
            as_args.append("true" if arg else "false")
        elif isinstance(arg, (int, float)):
            as_args.append(str(arg))
        else:
            as_args.append(quote_string(str(arg)))
    
    # Build the function call
    args_str = ", ".join(as_args) if as_args else ""
    script = f"{function_name}({args_str})"
    
    return run_applescript(script, timeout=timeout)


def get_app_info(app_name: str) -> dict:
    """Get information about a macOS application.
    
    Args:
        app_name: Name of the application
        
    Returns:
        Dictionary with application information
    """
    script = f'''
    tell application "System Events"
        try
            set appProcess to first process whose name is {quote_string(app_name)}
            set appVisible to visible of appProcess
            set appFrontmost to frontmost of appProcess
            return "visible:" & appVisible & ",frontmost:" & appFrontmost
        on error
            return "not_running"
        end try
    end tell
    '''
    
    try:
        result = run_applescript(script)
        if result == "not_running":
            return {"running": False}
        
        # Parse the result
        info = {"running": True}
        for pair in result.split(","):
            key, value = pair.split(":")
            info[key] = value.lower() == "true"
        
        return info
    
    except AppleScriptError:
        return {"running": False}


def display_notification(title: str, subtitle: str = "", message: str = "", 
                        sound_name: str = None) -> None:
    """Display a macOS notification.
    
    Args:
        title: Notification title
        subtitle: Notification subtitle
        message: Notification message
        sound_name: Optional sound name
    """
    parts = [f"with title {quote_string(title)}"]
    
    if subtitle:
        parts.append(f"subtitle {quote_string(subtitle)}")
    
    if message:
        parts.append(f"message {quote_string(message)}")
    
    if sound_name:
        parts.append(f"sound name {quote_string(sound_name)}")
    
    script = f"display notification \"\" {' '.join(parts)}"
    run_applescript(script)


# Legacy aliases for backward compatibility
asrun = run_applescript
asquote = quote_string


def main():
    """Example usage of the module."""
    if not is_macos():
        print("This module only works on macOS")
        return 1
    
    # Example 1: Simple AppleScript
    try:
        result = run_applescript('return "Hello from AppleScript!"')
        print(f"Result: {result}")
    except AppleScriptError as e:
        print(f"Error: {e}")
    
    # Example 2: Using string quoting
    name = 'John "Johnny" Doe'
    script = f'''
    tell application "Finder"
        display dialog "Hello, " & {quote_string(name)}
    end tell
    '''
    
    print(f"Generated script:\n{script}")
    
    # Example 3: Get app info
    try:
        finder_info = get_app_info("Finder")
        print(f"Finder info: {finder_info}")
    except AppleScriptError as e:
        print(f"Error getting app info: {e}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())