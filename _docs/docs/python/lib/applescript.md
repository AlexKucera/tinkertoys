# applescript.py

Modern macOS AppleScript integration with comprehensive error handling, timeout support, and convenient utility functions for automating macOS applications.

## Overview

applescript.py provides a secure, modern interface for executing AppleScript code from Python on macOS. It includes proper error handling, timeout support, string escaping utilities, and convenient functions for common macOS automation tasks.

## Features

- **Secure Execution** - No shell injection vulnerabilities with proper subprocess handling
- **Timeout Support** - Configurable timeouts to prevent hanging operations
- **Error Handling** - Comprehensive error reporting and exception management
- **String Escaping** - Automatic handling of quotes and special characters
- **Utility Functions** - Pre-built functions for common automation tasks
- **Cross-Platform Detection** - Graceful handling on non-macOS systems
- **Legacy Compatibility** - Backward compatibility with existing code

## Core Functions

### run_applescript(script, timeout=None)

Execute AppleScript code and return the output.

**Parameters:**
- `script` (str): AppleScript code to execute
- `timeout` (float, optional): Maximum execution time in seconds

**Returns:**
- `str`: Standard output from AppleScript

**Raises:**
- `AppleScriptError`: If script execution fails
- `OSError`: If osascript is not available
- `TimeoutExpired`: If script execution times out

**Example:**
```python
from applescript import run_applescript

# Simple AppleScript execution
result = run_applescript('return "Hello from AppleScript!"')
print(result)  # Output: Hello from AppleScript!

# With timeout
try:
    result = run_applescript('''
        tell application "Finder"
            return name of startup disk
        end tell
    ''', timeout=5.0)
    print(f"Startup disk: {result}")
except AppleScriptError as e:
    print(f"Script failed: {e}")
```

### quote_string(text)

Properly escape strings for use in AppleScript.

**Parameters:**
- `text` (str): Text to escape for AppleScript

**Returns:**
- `str`: Properly quoted string for AppleScript use

**Example:**
```python
from applescript import quote_string, run_applescript

# Handle strings with quotes
message = 'Hello "World" from Python!'
quoted = quote_string(message)

script = f'''
tell application "Finder"
    display dialog {quoted}
end tell
'''

run_applescript(script)
```

## Utility Functions

### get_app_info(app_name)

Get information about a running macOS application.

**Parameters:**
- `app_name` (str): Name of the application

**Returns:**
- `dict`: Application information with keys:
  - `running` (bool): Whether app is running
  - `visible` (bool): Whether app is visible (if running)
  - `frontmost` (bool): Whether app is frontmost (if running)

**Example:**
```python
from applescript import get_app_info

# Check if Finder is running and visible
finder_info = get_app_info("Finder")
if finder_info['running']:
    print(f"Finder is running, visible: {finder_info['visible']}")
else:
    print("Finder is not running")
```

### display_notification(title, subtitle="", message="", sound_name=None)

Display a macOS notification.

**Parameters:**
- `title` (str): Notification title
- `subtitle` (str, optional): Notification subtitle
- `message` (str, optional): Notification message
- `sound_name` (str, optional): Sound to play

**Example:**
```python
from applescript import display_notification

# Simple notification
display_notification("Process Complete", message="All files have been processed")

# Notification with sound
display_notification(
    "Backup Finished",
    subtitle="Daily Backup", 
    message="All files backed up successfully",
    sound_name="Glass"
)
```

## Advanced Usage Examples

### Application Control

```python
from applescript import run_applescript, quote_string

def control_music_app(action, track_name=None):
    """Control macOS Music app."""
    
    if action == "play":
        script = '''
        tell application "Music"
            play
        end tell
        '''
    
    elif action == "pause":
        script = '''
        tell application "Music"
            pause
        end tell
        '''
    
    elif action == "play_track" and track_name:
        quoted_track = quote_string(track_name)
        script = f'''
        tell application "Music"
            play track {quoted_track}
        end tell
        '''
    
    elif action == "get_current":
        script = '''
        tell application "Music"
            if player state is playing then
                return name of current track & " by " & artist of current track
            else
                return "Not playing"
            end if
        end tell
        '''
    
    try:
        result = run_applescript(script, timeout=10)
        return result
    except Exception as e:
        print(f"Music control failed: {e}")
        return None

# Usage examples
control_music_app("play")
current_track = control_music_app("get_current")
print(f"Now playing: {current_track}")
```

### File System Operations

```python
from applescript import run_applescript, quote_string
import os

def finder_operations(operation, path=None, target_path=None):
    """Perform Finder operations via AppleScript."""
    
    if operation == "reveal":
        # Reveal file in Finder
        if not os.path.exists(path):
            raise ValueError(f"Path does not exist: {path}")
        
        quoted_path = quote_string(path)
        script = f'''
        tell application "Finder"
            reveal POSIX file {quoted_path}
            activate
        end tell
        '''
    
    elif operation == "move_to_trash":
        # Move file to trash
        quoted_path = quote_string(path)
        script = f'''
        tell application "Finder"
            move POSIX file {quoted_path} to trash
        end tell
        '''
    
    elif operation == "get_selection":
        # Get currently selected files in Finder
        script = '''
        tell application "Finder"
            set selected_items to selection
            set file_paths to {}
            repeat with item_ref in selected_items
                set end of file_paths to POSIX path of (item_ref as alias)
            end repeat
            return file_paths as string
        end tell
        '''
    
    elif operation == "new_folder":
        # Create new folder
        quoted_path = quote_string(path)
        folder_name = quote_string(os.path.basename(target_path))
        script = f'''
        tell application "Finder"
            make new folder at POSIX file {quoted_path} with properties {{name:{folder_name}}}
        end tell
        '''
    
    try:
        result = run_applescript(script, timeout=15)
        return result
    except Exception as e:
        print(f"Finder operation failed: {e}")
        return None

# Usage examples
finder_operations("reveal", "/Users/alex/Documents/important.pdf")
selected_files = finder_operations("get_selection")
finder_operations("new_folder", "/Users/alex/Desktop", "New Project")
```

### Email Automation

```python
from applescript import run_applescript, quote_string

class MailAutomation:
    """Automate Apple Mail using AppleScript."""
    
    def __init__(self):
        self.timeout = 30  # Email operations can be slow
    
    def send_email(self, to_address, subject, body, attachments=None):
        """Send email via Apple Mail."""
        
        quoted_to = quote_string(to_address)
        quoted_subject = quote_string(subject)
        quoted_body = quote_string(body)
        
        script = f'''
        tell application "Mail"
            set new_message to make new outgoing message with properties {{
                subject: {quoted_subject},
                content: {quoted_body},
                visible: true
            }}
            
            tell new_message
                make new to recipient at end of to recipients with properties {{
                    address: {quoted_to}
                }}
        '''
        
        # Add attachments if provided
        if attachments:
            for attachment_path in attachments:
                if os.path.exists(attachment_path):
                    quoted_attachment = quote_string(attachment_path)
                    script += f'''
                make new attachment with properties {{
                    file name: POSIX file {quoted_attachment}
                }} at after the last paragraph
                    '''
        
        script += '''
            end tell
            
            send new_message
        end tell
        '''
        
        try:
            run_applescript(script, timeout=self.timeout)
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
    
    def get_unread_count(self):
        """Get count of unread emails."""
        script = '''
        tell application "Mail"
            return unread count of inbox
        end tell
        '''
        
        try:
            result = run_applescript(script, timeout=10)
            return int(result)
        except Exception as e:
            print(f"Failed to get unread count: {e}")
            return 0
    
    def mark_as_read(self, message_count=1):
        """Mark recent messages as read."""
        script = f'''
        tell application "Mail"
            set recent_messages to messages 1 thru {message_count} of inbox
            repeat with msg in recent_messages
                set read status of msg to true
            end repeat
        end tell
        '''
        
        try:
            run_applescript(script, timeout=15)
            return True
        except Exception as e:
            print(f"Failed to mark as read: {e}")
            return False

# Usage
mail = MailAutomation()

# Send automated report
mail.send_email(
    "manager@company.com",
    "Daily Report - " + datetime.now().strftime("%Y-%m-%d"),
    "Please find today's report attached.",
    attachments=["/path/to/report.pdf"]
)

# Check for new emails
unread = mail.get_unread_count()
print(f"You have {unread} unread emails")
```

### System Information Gathering

```python
from applescript import run_applescript

def get_system_info():
    """Gather system information via AppleScript."""
    
    scripts = {
        'computer_name': '''
        tell application "System Events"
            return computer name of local domain
        end tell
        ''',
        
        'current_user': '''
        tell application "System Events"
            return name of current user
        end tell
        ''',
        
        'screen_resolution': '''
        tell application "Finder"
            return bounds of window of desktop
        end tell
        ''',
        
        'running_applications': '''
        tell application "System Events"
            return name of every application process whose visible is true
        end tell
        ''',
        
        'system_version': '''
        tell application "System Events"
            return system version
        end tell
        ''',
        
        'free_disk_space': '''
        tell application "Finder"
            return free space of startup disk
        end tell
        '''
    }
    
    system_info = {}
    
    for key, script in scripts.items():
        try:
            result = run_applescript(script, timeout=10)
            system_info[key] = result
        except Exception as e:
            system_info[key] = f"Error: {e}"
    
    return system_info

# Usage
info = get_system_info()
for key, value in info.items():
    print(f"{key}: {value}")
```

## Error Handling and Best Practices

### Comprehensive Error Handling

```python
from applescript import run_applescript, AppleScriptError, is_macos

def safe_applescript_execution(script_name, script_code, timeout=30):
    """Safely execute AppleScript with comprehensive error handling."""
    
    # Check if running on macOS
    if not is_macos():
        print("AppleScript is only available on macOS")
        return None
    
    try:
        print(f"Executing {script_name}...")
        result = run_applescript(script_code, timeout=timeout)
        print(f"✓ {script_name} completed successfully")
        return result
        
    except AppleScriptError as e:
        print(f"✗ AppleScript error in {script_name}: {e}")
        return None
        
    except TimeoutError:
        print(f"✗ {script_name} timed out after {timeout} seconds")
        return None
        
    except OSError as e:
        print(f"✗ System error in {script_name}: {e}")
        return None
        
    except Exception as e:
        print(f"✗ Unexpected error in {script_name}: {e}")
        return None

# Usage with error handling
script = '''
tell application "Terminal"
    do script "echo 'Hello from Terminal'"
end tell
'''

result = safe_applescript_execution("Terminal Hello", script)
```

### Retry Logic for Flaky Operations

```python
import time
from applescript import run_applescript, AppleScriptError

def retry_applescript(script, max_retries=3, delay=1.0, timeout=30):
    """Execute AppleScript with retry logic for flaky operations."""
    
    last_error = None
    
    for attempt in range(max_retries):
        try:
            result = run_applescript(script, timeout=timeout)
            if attempt > 0:
                print(f"✓ Succeeded on attempt {attempt + 1}")
            return result
            
        except AppleScriptError as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}")
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"All {max_retries} attempts failed")
                
        except Exception as e:
            # Don't retry for non-AppleScript errors
            print(f"Non-retryable error: {e}")
            raise
    
    # If we get here, all retries failed
    raise last_error

# Usage with retry logic
flaky_script = '''
tell application "SomeFlakeyApp"
    -- This might fail occasionally
    perform some action
end tell
'''

try:
    result = retry_applescript(flaky_script, max_retries=3, delay=2.0)
    print("Operation succeeded")
except AppleScriptError as e:
    print(f"Operation failed after retries: {e}")
```

## Integration Patterns

### CLI Tool Integration

```python
import argparse
from applescript import run_applescript, display_notification, is_macos

def create_notification_cli():
    """Command-line tool for sending macOS notifications."""
    
    if not is_macos():
        print("This tool only works on macOS")
        return 1
    
    parser = argparse.ArgumentParser(description="Send macOS notifications")
    parser.add_argument("title", help="Notification title")
    parser.add_argument("--message", "-m", help="Notification message")
    parser.add_argument("--subtitle", "-s", help="Notification subtitle") 
    parser.add_argument("--sound", help="Notification sound")
    
    args = parser.parse_args()
    
    try:
        display_notification(
            args.title,
            subtitle=args.subtitle or "",
            message=args.message or "",
            sound_name=args.sound
        )
        return 0
    except Exception as e:
        print(f"Failed to send notification: {e}")
        return 1

# Usage: python notify.py "Build Complete" -m "All tests passed" -s "Success"
```

### Automation Workflows

```python
from applescript import run_applescript, display_notification
import time

class MacOSWorkflow:
    """Automation workflow for macOS tasks."""
    
    def __init__(self, name):
        self.name = name
        self.steps = []
    
    def add_step(self, step_name, applescript_code, timeout=30):
        """Add a step to the workflow."""
        self.steps.append({
            'name': step_name,
            'script': applescript_code,
            'timeout': timeout
        })
    
    def execute(self, show_notifications=True):
        """Execute the complete workflow."""
        start_time = time.time()
        
        if show_notifications:
            display_notification(f"Starting {self.name}", message="Workflow beginning...")
        
        for i, step in enumerate(self.steps, 1):
            try:
                print(f"Step {i}/{len(self.steps)}: {step['name']}")
                
                result = run_applescript(step['script'], timeout=step['timeout'])
                
                print(f"✓ {step['name']} completed")
                
            except Exception as e:
                error_msg = f"Step {i} failed: {step['name']} - {e}"
                print(f"✗ {error_msg}")
                
                if show_notifications:
                    display_notification(
                        f"{self.name} Failed", 
                        message=error_msg,
                        sound_name="Basso"
                    )
                
                return False
        
        elapsed = time.time() - start_time
        success_msg = f"{self.name} completed in {elapsed:.1f} seconds"
        print(f"✓ {success_msg}")
        
        if show_notifications:
            display_notification(
                f"{self.name} Complete",
                message=success_msg,
                sound_name="Glass"
            )
        
        return True

# Example workflow
def create_daily_setup_workflow():
    """Create a workflow for daily work setup."""
    
    workflow = MacOSWorkflow("Daily Setup")
    
    # Open essential applications
    workflow.add_step("Open Terminal", '''
    tell application "Terminal"
        activate
        do script "cd ~/Projects"
    end tell
    ''')
    
    workflow.add_step("Open VS Code", '''
    tell application "Visual Studio Code"
        activate
    end tell
    ''')
    
    workflow.add_step("Check Calendar", '''
    tell application "Calendar"
        activate
    end tell
    ''')
    
    workflow.add_step("Set Do Not Disturb", '''
    tell application "System Events"
        tell process "Control Center"
            click menu bar item "Control Center" of menu bar 1
            delay 1
            click button "Do Not Disturb" of window 1
        end tell
    end tell
    ''')
    
    return workflow

# Execute workflow
daily_setup = create_daily_setup_workflow()
daily_setup.execute()
```

## Legacy Compatibility

### Backward Compatibility

```python
# Legacy aliases for existing code
asrun = run_applescript
asquote = quote_string

# Migration examples
def migrate_legacy_code():
    """Examples of migrating from legacy to new API."""
    
    # Old way (still works)
    result = asrun('return "Hello"')
    quoted = asquote("Text with \"quotes\"")
    
    # New way (recommended)
    result = run_applescript('return "Hello"', timeout=10)
    quoted = quote_string("Text with \"quotes\"")
    
    return result, quoted
```

---

*applescript.py provides modern, secure AppleScript integration for macOS automation with comprehensive error handling, timeout support, and convenient utility functions for common automation tasks.*


---

Based on:


http://www.leancrew.com/all-this/2013/03/combining-python-and-applescript/

Combining Python and AppleScript

March 6, 2013 at 10:34 PM by Dr. Drang

You may remember this post from last June, in which I had to rewrite a script that printed
out the current iTunes track. The original script was written in Python and used Hamish
Sanderson’s appscript library; the replacement was written in AppleScript.

I had to do the rewrite because an update to iTunes had broken the way appscript gets at
an application’s AppleScript dictionary. Hamish had stopped developing appscript because
Apple had deprecated the Carbon libraries he used to develop it and hadn’t replaced them
with Cocoa equivalents.

That post generated many thousands of words of commentary, most of it by Hamish and most
of the rest by Matt Neuburg. Although Matt came up with a clever workaround to
Ruby-appscript’s access to application dictionaries, and I thought seriously about
mimicking his work for Python-appscript, eventually I decided that I should just abandon
appscript. Because Apple has no proprietary interest in appscript, it will almost certainly
continue to make changes that undermine it.

Ferreting out all my appscript-using programs and changing them into pure AppleScript or
some Python/AppleScript hybrid wasn’t appealing, so I decided to just wait until a script
broke before rewriting it. Recently, my script for automatically generating invoice emails
broke, and I rewrote it into a combination of two AppleScripts and one Python script. It
worked, but I wasn’t happy with the results—it seemed both kludgy and fragile. What I
needed was a more general way to run AppleScript code from within my Python scripts.

I’ve touched on this topic before. Back then, I thought Kenneth Reitz’s envoy module was
the solution. I still like the idea of envoy, but the GitHub page has no real documentation,
and Kenneth’s own site seems to have been purged of most of his coding work in favor of
writing, photography, and music. Besides, envoy is a bit more general-purpose than I need.
Basically, I just want one or two wrapper functions around Python’s subprocess module that
will allow me to

Write an AppleScript as a Python string.
Run it from within my Python program.
Collect any output it generates.
With this, I’ll be able to keep all the code in one script instead of artificially breaking
it up into separate AppleScript and Python parts.

Here’s the module, applescript.py:

 1  #!/usr/bin/python
 2
 3  import subprocess
 4
 5  def asrun(ascript):
 6    "Run the given AppleScript and return the standard output and error."
 7
 8    osa = subprocess.Popen(['osascript', '-'],
 9                           stdin=subprocess.PIPE,
10                           stdout=subprocess.PIPE)
11    return osa.communicate(ascript)[0]
12
13  def asquote(astr):
14    "Return the AppleScript equivalent of the given string."
15
16    astr = astr.replace('"', '" & quote & "')
17    return '"{}"'.format(astr)

Without line numbers
There are just two functions: asrun, which takes the AppleScript string as its only
argument, runs it, and returns the output, if any; and asquote, which reconfigures any
string into a string that AppleScript can parse.

There’s not much to either one of these functions, but I can think of two things worth a
little explanation. You’ll note that the Popen in asrun doesn’t change the stderr parameter
from its default value of None. That’s because I wanted any AppleScript errors that arise
to propagate out into the surrounding script and get handled like any other Python
error—shutting the program down unless it’s in a try block. And instead of simply
backslash-escaping double quotes in asquote, I do the more verbose thing of splitting
the string at the double quotes and reconcatenating it with quotes. Doing it this way
seemed more AppleScripty, but maybe that’s just me. You could certainly change Line 16 to

16    astr = astr.replace('"', r'\"')

Without line numbers
if you think that’s better. The double backslash is necessary to get around Python’s
escaping rules. The raw string gets around Python’s escaping rules.

I have applescript.py saved in /Library/Python/2.7/site-packages so it’s available to all
my scripts. I have a feeling I’ll be changing it as I use it and find that it fails under
certain conditions. So far, though, it’s done what I want.

Here’s a short script using both asrun and asquote:

 1  #!/usr/bin/python
 2
 3  from applescript import asrun, asquote
 4
 5  subject = 'A new email'
 6
 7  body = '''This is the body of my "email."
 8  I hope it comes out right.
 9
10  Regards,
11  Dr. Drang
12  '''
13  ascript = '''
14  tell application "Mail"
15    activate
16    make new outgoing message with properties {{visible:true, subject:{0}, content:{1}}}
17  end tell
18  '''.format(asquote(subject), asquote(body))
19
20  print ascript
21  asrun(ascript)

Without line numbers
This does pretty much what you’d expect: after printing out the AppleScript source, it runs
it through osascript to create a new message in Mail with the Subject and Content fields
filled. Except for the format placeholders, and the doubled braces that format requires,
the AppleScript in Lines 14-17 is exactly as I’d write it in the AppleScript Editor. I
know Clark Goble will disagree, but I prefer this to the appscript syntax, which I found
awkward because it didn’t feel like real Python.

Since Hamish Sanderson and Matt Neuburg inadvertently contributed to this post, I should
recommend their AppleScript books. Hamish’s is the book I reach for now when I have an
AppleScript question; Matt’s is more concise and has excellent sections on the structure
and philosophy of AppleScript. And if you’re interested in scripting Mail, this tutorial
by Ben Waldie at MacTech is a great place to start and may well be where you finish.