# Configuration Setup Guide

Complete guide for configuring the Tinkertoys scripts collection for your environment.

## Overview

The configuration system uses centralized configuration files in the `config/` directory to manage settings for various tools and services. This approach keeps sensitive information separate from scripts and allows for easy customization.

## Configuration Files

### Core Configuration Files

| File | Purpose | Required For |
|------|---------|--------------|
| `mail_send.conf` | Email notifications | Rendering scripts, notifications |
| `log_sources.conf` | Log collection sources | Log collector system |

## Setup Process

### 1. Email Configuration

#### Create Mail Configuration
```bash
cp config/mail_send.conf.example config/mail_send.conf
```

#### Edit Mail Settings
```bash
# Email notification configuration
FROM_ADDRESS="renders@yourcompany.com"
TO_ADDRESS="team@yourcompany.com"
SERVER="smtp.yourserver.com"
USER="smtp_username"
# Note: PASS is set via environment variable for security
```

#### Set Environment Variables
```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export MAIL_PASSWORD="your_smtp_password"
```

### 2. Log Collection Setup

#### Configure Log Sources
Edit `config/log_sources.conf` to define log sources by category:

```
# Format: category|log_path|description
system|/var/log/system.log|System messages and events
application|/var/log/app.log|Application-specific logs
security|/var/log/auth.log|Authentication and security events
custom|/path/to/custom.log|Custom application logs
```

### 3. Environment Variables

#### Required Variables
```bash
# Email notifications
export MAIL_PASSWORD="your_smtp_password"

# Nuke rendering (if using Nuke scripts)
export NUKEPATH="/Applications/Nuke/Nuke15.0v4/Nuke15.0v4"

# Custom log location (optional)
export LOG_FILE="/var/log/tinkertoys.log"
```

#### Shell Profile Setup
Add environment variables to your shell profile:

```bash
# ~/.bashrc or ~/.zshrc
export MAIL_PASSWORD="your_smtp_password"
export NUKEPATH="/Applications/Nuke/Nuke15.0v4/Nuke15.0v4"
export PATH="/path/to/tinkertoys/bash:$PATH"
```

### 4. Dependencies Installation

#### Required Software
```bash
# FFmpeg for media processing
brew install ffmpeg

# SendEmail for notifications
brew install sendemail
# or download from: http://caspian.dotconf.net/menu/Software/SendEmail/

# Optional: Nuke for rendering scripts
# Install from Foundry website
```

#### Python Dependencies
```bash
# If using Python scripts
pip install -r requirements.txt  # if available
```

### 5. Permissions Setup

#### Script Permissions
```bash
# Make all scripts executable
find bash/ -name "*.sh" -exec chmod +x {} \;
```

#### Directory Permissions
```bash
# Ensure log directories exist and are writable
mkdir -p ~/logs
chmod 755 ~/logs

# For system logs (if needed)
sudo mkdir -p /var/log/tinkertoys
sudo chown $(whoami) /var/log/tinkertoys
```

## Testing Configuration

### Email Configuration Test
```bash
# Test email notifications
./bash/rendering/mail_send.sh
```

### Log Collection Test
```bash
# Test log collector
cd bash/system/log_collector/
./log_collector.sh --help
./log_collector.sh -t 10 -l 5
```

### Media Processing Test
```bash
# Test media functions (requires FFmpeg)
./bash/media/convert_movie_to_h264.sh --help
```

## Security Best Practices

### Sensitive Information
1. **Never commit passwords** to version control
2. **Use environment variables** for all credentials
3. **Set appropriate file permissions** on configuration files
4. **Regularly rotate passwords** and update configurations

### File Permissions
```bash
# Secure configuration files
chmod 600 config/mail_send.conf
chmod 644 config/log_sources.conf
```

### Environment Variables
```bash
# Verify environment variables are set
echo "Mail password set: $([[ -n "$MAIL_PASSWORD" ]] && echo "Yes" || echo "No")"
echo "Nuke path set: $([[ -n "$NUKEPATH" ]] && echo "Yes" || echo "No")"
```

## Troubleshooting

### Common Issues

#### Email Not Working
1. Check SMTP server settings in `mail_send.conf`
2. Verify `MAIL_PASSWORD` environment variable is set
3. Test network connectivity to SMTP server
4. Check firewall settings

#### Scripts Not Found
1. Verify scripts are executable: `ls -la bash/`
2. Check PATH includes script directories
3. Use absolute paths if needed

#### Permission Denied
1. Check file permissions: `ls -la config/`
2. Verify directory write permissions
3. Check ownership of files and directories

#### Missing Dependencies
1. Install required software (FFmpeg, sendemail, etc.)
2. Verify commands are in PATH: `which ffmpeg`
3. Check version compatibility

### Validation Commands
```bash
# Validate configuration
./bash/test_all_scripts.sh

# Quick validation
./bash/quick_test.sh

# Comprehensive validation
./bash/final_validation.sh
```

## Advanced Configuration

### Custom Log Locations
```bash
# Per-script log files
export LOG_FILE="/var/log/media_processing.log"
./bash/media/convert_movie_to_h264.sh input.mov

# Temporary log for specific operations
LOG_FILE="./operation_$(date +%Y%m%d).log" ./bash/script.sh
```

### Integration with System Services
```bash
# systemd service example (Linux)
[Unit]
Description=Tinkertoys Background Service
After=network.target

[Service]
Type=simple
Environment=MAIL_PASSWORD=your_password
Environment=LOG_FILE=/var/log/tinkertoys.log
ExecStart=/path/to/tinkertoys/bash/script.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

### Backup Configuration
```bash
# Backup configuration files
tar -czf tinkertoys_config_$(date +%Y%m%d).tar.gz config/

# Restore configuration
tar -xzf tinkertoys_config_backup.tar.gz
```

## See Also
- [Mail Configuration](mail_send.md) - Detailed email setup
- [Log Sources Configuration](log_sources.md) - Log collection setup
- [Bash Scripts Overview](../bash/overview.md) - Script usage patterns

---

*Configuration files located in: `config/`*  
*Author: Alexander Kucera / babylondreams.de*