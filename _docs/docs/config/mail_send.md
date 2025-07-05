# Mail Configuration (mail_send.conf)

Email notification configuration for render completion alerts and system notifications.

## Configuration File

**Location**: `config/mail_send.conf`

### Basic Configuration
```bash
# SMTP server settings
FROM_ADDRESS="renders@yourcompany.com"
TO_ADDRESS="team@yourcompany.com"
SERVER="smtp.yourserver.com"
USER="smtp_username"

# Note: Password set via MAIL_PASSWORD environment variable
```

## Environment Variables

### Required
```bash
export MAIL_PASSWORD="your_smtp_password"
```

## SMTP Provider Examples

### Gmail/Google Workspace
```bash
FROM_ADDRESS="notifications@yourcompany.com"
TO_ADDRESS="alerts@yourcompany.com"
SERVER="smtp.gmail.com:587"
USER="notifications@yourcompany.com"
```

### Office 365
```bash
FROM_ADDRESS="system@yourcompany.com"
TO_ADDRESS="team@yourcompany.com"
SERVER="smtp.office365.com:587"
USER="system@yourcompany.com"
```

### Custom SMTP
```bash
FROM_ADDRESS="noreply@yourserver.com"
TO_ADDRESS="admin@yourserver.com"
SERVER="mail.yourserver.com:587"
USER="smtp_user"
```

## Security Setup

### App Passwords
For Gmail and Office 365, use app-specific passwords:

1. Enable 2-factor authentication
2. Generate app-specific password
3. Use app password as MAIL_PASSWORD

### Environment Variable Setup
```bash
# Add to ~/.bashrc or ~/.zshrc
export MAIL_PASSWORD="app_specific_password"

# For secure server deployment
echo 'export MAIL_PASSWORD="password"' >> /etc/environment
```

## Testing Configuration

### Test Email
```bash
# Test with mail notification script
./bash/rendering/mail_send.sh
```

### Manual Test
```bash
# Direct sendemail test
sendemail -f "test@yourcompany.com" \
          -t "admin@yourcompany.com" \
          -m "Test message" \
          -u "Test Subject" \
          -s "smtp.yourserver.com:587" \
          -xu "smtp_user" \
          -xp "$MAIL_PASSWORD"
```

## Used By

- [Mail Notifications](../bash/rendering/mail_send.md)
- [Nuke Render Automation](../bash/rendering/nukerender_bash.md)

---

*Configuration file: `config/mail_send.conf`*