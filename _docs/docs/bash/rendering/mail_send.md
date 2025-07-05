# Mail Notifications (mail_send.sh)

Send email notifications for completed renders with timing information and system details.

## Overview

Automated email notification system for render completion with detailed timing statistics, machine identification, and professional formatting. Essential for long-running render processes and distributed rendering workflows.

## Usage

```bash
mail_send.sh
```

## Features

- **Render Timing**: Tracks start time, end time, and total duration
- **Machine Identification**: Includes hostname in notifications
- **Professional Formatting**: Clean, informative email content
- **Error Handling**: Validates email configuration and connectivity

## Configuration

### Email Settings
Edit `config/mail_send.conf`:
```bash
FROM_ADDRESS="renders@yourcompany.com"
TO_ADDRESS="team@yourcompany.com"
SERVER="smtp.yourserver.com"
USER="smtp_username"
# PASS set via environment variable
```

### Environment Variables
```bash
export MAIL_PASSWORD="your_smtp_password"
```

## Examples

```bash
# Basic render notification
./mail_send.sh

# Integration with render scripts
./render_job.sh && ./mail_send.sh

# Conditional notifications
if render_command; then
    ./mail_send.sh
else
    echo "Render failed - notification not sent"
fi
```

## Email Content

The notification includes:
- **Machine Name**: Which system completed the render
- **Start Time**: When the render began
- **End Time**: When the render completed  
- **Duration**: Total render time in hours:minutes:seconds format
- **Professional Formatting**: Clean, readable layout

## Requirements

- **sendemail**: Command-line email utility
- **SMTP Access**: Configured email server
- **Network Connectivity**: For email delivery

## Security

- **No Hardcoded Passwords**: Uses environment variables
- **Validated Configuration**: Checks all required settings
- **Error Reporting**: Clear messages for configuration issues

## See Also
- [Nuke Render Automation](nukerender_bash.md) - Integrated render notifications
- [Mail Configuration](../../config/mail_send.md) - Email setup details

---

*Script Location: `bash/rendering/mail_send.sh`*  
*Author: Alexander Kucera / babylondreams.de*