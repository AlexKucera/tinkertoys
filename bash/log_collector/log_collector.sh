#!/bin/bash

# Configurable Log Collector Script
# Reads log sources from a configuration file and presents them in a readable format

# Default configuration
LINES=20
TIME_FILTER=""
OUTPUT_FILE=""
CONFIG_FILE="$(dirname "$0")/log_sources.conf"
SHOW_TIMESTAMPS=true
SEPARATOR="="
SEPARATOR_LENGTH=80

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
    local title="$1"
    local color="$2"
    
    echo -e "\n${color}$(printf '%*s' $SEPARATOR_LENGTH '' | tr ' ' $SEPARATOR)${NC}"
    echo -e "${color}$(printf '%*s' $(((SEPARATOR_LENGTH - ${#title}) / 2)) '' | tr ' ' ' ')${title}${NC}"
    echo -e "${color}$(printf '%*s' $SEPARATOR_LENGTH '' | tr ' ' $SEPARATOR)${NC}"
}

# Function to filter log by time
filter_by_time() {
    local log_file="$1"
    local minutes="$2"
    
    if [[ -z "$minutes" ]]; then
        cat "$log_file"
        return
    fi
    
    # Calculate cutoff timestamp in seconds since epoch
    local cutoff_seconds
    if command -v date >/dev/null 2>&1; then
        if date -d "now - ${minutes} minutes" '+%s' >/dev/null 2>&1; then
            # GNU date (Linux)
            cutoff_seconds=$(date -d "now - ${minutes} minutes" '+%s')
        elif date -v-${minutes}M '+%s' >/dev/null 2>&1; then
            # BSD date (macOS)
            cutoff_seconds=$(date -v-${minutes}M '+%s')
        else
            echo "Warning: Cannot calculate time filter, showing all lines" >&2
            cat "$log_file"
            return
        fi
    else
        echo "Warning: date command not available, showing all lines" >&2
        cat "$log_file"
        return
    fi
    
    # Debug: Show what we're filtering for
    local cutoff_readable
    if date -d "@$cutoff_seconds" '+%Y-%m-%d %H:%M:%S' >/dev/null 2>&1; then
        cutoff_readable=$(date -d "@$cutoff_seconds" '+%Y-%m-%d %H:%M:%S')
    else
        cutoff_readable=$(date -r "$cutoff_seconds" '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "unknown")
    fi
    echo "  → Filtering for entries newer than: $cutoff_readable" >&2
    
    local lines_processed=0
    local lines_matched=0
    
    # Read file and filter by timestamp
    while IFS= read -r line; do
        lines_processed=$((lines_processed + 1))
        local line_timestamp=""
        
        # Extract timestamp from your log format: [2025-07-04 10:32:58]
        if [[ $line =~ ^\[([0-9]{4}-[0-9]{2}-[0-9]{2}\ [0-9]{2}:[0-9]{2}:[0-9]{2})\] ]]; then
            line_timestamp="${BASH_REMATCH[1]}"
        fi
        
        # If no timestamp found, include the line (might be continuation)
        if [[ -z "$line_timestamp" ]]; then
            echo "$line"
            continue
        fi
        
        # Convert line timestamp to seconds since epoch
        local line_seconds
        if date -d "$line_timestamp" '+%s' >/dev/null 2>&1; then
            # GNU date
            line_seconds=$(date -d "$line_timestamp" '+%s')
        elif date -j -f "%Y-%m-%d %H:%M:%S" "$line_timestamp" '+%s' >/dev/null 2>&1; then
            # BSD date
            line_seconds=$(date -j -f "%Y-%m-%d %H:%M:%S" "$line_timestamp" '+%s')
        else
            # Can't parse timestamp, include the line
            echo "$line"
            continue
        fi
        
        # Compare timestamps and include if line is newer than cutoff
        if [[ "$line_seconds" -ge "$cutoff_seconds" ]]; then
            echo "$line"
            lines_matched=$((lines_matched + 1))
        fi
        
    done < "$log_file"
    
    echo "  → Processed $lines_processed lines, matched $lines_matched lines" >&2
}
print_log() {
    local log_file="$1"
    local description="$2"
    local color="$3"
    
    if [[ -f "$log_file" && -r "$log_file" ]]; then
        echo -e "${color}📄 $description${NC}"
        echo -e "${CYAN}Location: $log_file${NC}"
        
        if [[ $SHOW_TIMESTAMPS == true ]]; then
            local last_modified
            if command -v stat >/dev/null 2>&1; then
                last_modified=$(stat -c %y "$log_file" 2>/dev/null || stat -f %Sm "$log_file" 2>/dev/null)
                echo -e "${YELLOW}Last modified: $last_modified${NC}"
            fi
            
            # Show file size
            local file_size
            if command -v du >/dev/null 2>&1; then
                file_size=$(du -h "$log_file" 2>/dev/null | cut -f1)
                echo -e "${YELLOW}File size: $file_size${NC}"
            fi
        fi
        
        echo ""
        
        # Check if file is empty
        if [[ ! -s "$log_file" ]]; then
            echo -e "${YELLOW}  (File is empty)${NC}"
        else
            tail -n $LINES "$log_file" 2>/dev/null | while IFS= read -r line; do
                echo "  $line"
            done
        fi
        echo ""
    else
        echo -e "${RED}❌ $description${NC}"
        echo -e "${RED}   File not found or not readable: $log_file${NC}"
        echo ""
    fi
}

# Function to create example config file
create_example_config() {
    local config_file="$1"
    
    cat > "$config_file" << 'EOF'
# Log Sources Configuration File
# Format: CATEGORY|DESCRIPTION|LOG_PATH|COLOR
# Colors: RED, GREEN, YELLOW, BLUE, PURPLE, CYAN
# Lines starting with # are comments and will be ignored

# PHP Application Logs
PHP_APPS|Main Application Error Log|/var/log/php/app_error.log|RED
PHP_APPS|Main Application Access Log|/var/log/php/app_access.log|GREEN
PHP_APPS|API Error Log|/var/log/php/api_error.log|RED
PHP_APPS|Cron Jobs Log|/var/log/php/cron.log|YELLOW
PHP_APPS|Database Query Log|/var/log/php/db_queries.log|BLUE

# Python Application Logs
PYTHON_APPS|Main Python App Log|/var/log/python/main_app.log|GREEN
PYTHON_APPS|Data Processing Log|/var/log/python/data_processor.log|BLUE
PYTHON_APPS|ML Model Training Log|/var/log/python/ml_training.log|PURPLE
PYTHON_APPS|API Gateway Log|/var/log/python/api_gateway.log|CYAN
PYTHON_APPS|Task Queue Log|/var/log/python/celery.log|YELLOW

# Server Logs
SERVER|PHP-FPM Error Log|/var/log/php-fpm/error.log|RED
SERVER|PHP-FPM Slow Log|/var/log/php-fpm/slow.log|YELLOW
SERVER|Nginx Error Log|/var/log/nginx/error.log|RED
SERVER|Nginx Access Log|/var/log/nginx/access.log|GREEN
SERVER|System PHP Error Log|/var/log/php_errors.log|RED

# Custom Application Logs (adjust paths as needed)
CUSTOM|My Custom App Log|/home/user/apps/myapp/logs/app.log|GREEN
CUSTOM|Background Tasks Log|/home/user/apps/myapp/logs/tasks.log|BLUE
CUSTOM|Email Service Log|/home/user/apps/myapp/logs/email.log|PURPLE
CUSTOM|File Upload Log|/home/user/apps/myapp/logs/uploads.log|CYAN
CUSTOM|Authentication Log|/home/user/apps/myapp/logs/auth.log|YELLOW
EOF
    
    echo "Example configuration file created at: $config_file"
}

# Function to show usage
show_usage() {
    echo "Configurable Log Collector - Monitor multiple log sources"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -l, --lines NUM       Number of lines to show (default: 20, 0 = unlimited)"
    echo "  -t, --time MINUTES    Show only entries from last N minutes"
    echo "  -c, --config FILE     Configuration file path (default: ./log_sources.conf)"
    echo "  -o, --output FILE     Save output to file instead of displaying"
    echo "  -n, --no-timestamps   Don't show file timestamps and sizes"
    echo "  --create-config       Create example configuration file"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Time and Line Filtering:"
    echo "  -t 5                  Show entries from last 5 minutes only"
    echo "  -l 10                 Show last 10 lines only"
    echo "  -t 5 -l 10           Show entries from last 5 minutes, limit to 10 lines"
    echo "  -l 0                  Show all lines (no line limit)"
    echo ""
    echo "Configuration file format:"
    echo "  CATEGORY|DESCRIPTION|LOG_PATH|COLOR"
    echo ""
    echo "  Available colors: RED, GREEN, YELLOW, BLUE, PURPLE, CYAN"
    echo "  Lines starting with # are comments"
    echo ""
    echo "Examples:"
    echo "  $0                           # Use default config, show last 20 lines"
    echo "  $0 -l 50                     # Show last 50 lines from each log"
    echo "  $0 -t 10                     # Show entries from last 10 minutes only"
    echo "  $0 -t 5 -l 20               # Last 5 minutes, limited to 20 lines each"
    echo "  $0 -c /path/to/logs.conf     # Use custom configuration file"
    echo "  $0 -o daily_report.txt       # Save output to file"
    echo "  $0 --create-config           # Create example config file"
    echo "  $0 -t 30 -l 0 -o errors.txt  # Last 30 min, all lines, save to file"
    echo ""
    echo "Quick Start:"
    echo "  1. Run '$0 --create-config' to create example configuration"
    echo "  2. Edit log_sources.conf with your actual log file paths"
    echo "  3. Run '$0' to view your logs"
    echo ""
    echo "Configuration Example:"
    echo "  PHP_APPS|Main App Log|/var/www/app/logs/app.log|GREEN"
    echo "  PYTHON_APPS|Data Processing|/home/user/python/data.log|BLUE"
    echo "  SERVER|PHP Error Log|/var/log/php/error.log|RED"
    echo ""
}

# Function to get color code
get_color() {
    case "$1" in
        RED) echo "$RED" ;;
        GREEN) echo "$GREEN" ;;
        YELLOW) echo "$YELLOW" ;;
        BLUE) echo "$BLUE" ;;
        PURPLE) echo "$PURPLE" ;;
        CYAN) echo "$CYAN" ;;
        *) echo "$NC" ;;
    esac
}

# If no arguments provided, show brief help
if [[ $# -eq 0 ]] && [[ ! -f "$CONFIG_FILE" ]]; then
    echo -e "${YELLOW}Configurable Log Collector${NC}"
    echo -e "${YELLOW}No configuration file found. Get started with:${NC}"
    echo ""
    echo "  $0 --create-config    # Create example configuration"
    echo "  $0 --help            # Show detailed help"
    echo ""
    exit 0
fi
while [[ $# -gt 0 ]]; do
    case $1 in
        -l|--lines)
            LINES="$2"
            shift 2
            ;;
        -t|--time)
            TIME_FILTER="$2"
            shift 2
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -n|--no-timestamps)
            SHOW_TIMESTAMPS=false
            shift
            ;;
        --create-config)
            create_example_config "$CONFIG_FILE"
            exit 0
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if config file exists
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo -e "${RED}Configuration file not found: $CONFIG_FILE${NC}"
    echo -e "${YELLOW}Create one with: $0 --create-config${NC}"
    echo ""
    echo "For help, run: $0 --help"
    exit 1
fi

# Redirect output to file if specified
if [[ -n "$OUTPUT_FILE" ]]; then
    exec > >(tee "$OUTPUT_FILE")
fi

# Read and parse config file
declare -A categories
declare -a log_entries

while IFS='|' read -r category description log_path color; do
    # Skip comments and empty lines
    [[ "$category" =~ ^#.*$ ]] && continue
    [[ -z "$category" ]] && continue
    
    # Store category for grouping
    categories["$category"]=1
    
    # Store log entry
    log_entries+=("$category|$description|$log_path|$color")
done < "$CONFIG_FILE"

# Main execution
echo -e "${GREEN}Custom Log Collection Report - $(date)${NC}"
echo -e "${GREEN}Configuration: $CONFIG_FILE${NC}"

if [[ -n "$TIME_FILTER" ]]; then
    echo -e "${GREEN}Time filter: Last $TIME_FILTER minutes${NC}"
fi
if [[ "$LINES" -ne 20 ]]; then
    if [[ "$LINES" -eq 0 ]]; then
        echo -e "${GREEN}Line limit: No limit${NC}"
    else
        echo -e "${GREEN}Line limit: $LINES lines per log${NC}"
    fi
fi

# Process logs by category
for category in $(printf '%s\n' "${!categories[@]}" | sort); do
    print_header "$category" "$BLUE"
    
    for entry in "${log_entries[@]}"; do
        IFS='|' read -r cat desc path col <<< "$entry"
        
        if [[ "$cat" == "$category" ]]; then
            color_code=$(get_color "$col")
            print_log "$path" "$desc" "$color_code"
        fi
    done
done

# Summary
print_header "SUMMARY" "$GREEN"
echo -e "${GREEN}✅ Log collection completed at $(date)${NC}"

if [[ -n "$TIME_FILTER" ]]; then
    echo -e "${GREEN}⏰ Time filter: Last $TIME_FILTER minutes${NC}"
fi
if [[ "$LINES" -ne 20 ]]; then
    if [[ "$LINES" -eq 0 ]]; then
        echo -e "${GREEN}📊 Lines: No limit${NC}"
    else
        echo -e "${GREEN}📊 Lines per log: $LINES${NC}"
    fi
else
    echo -e "${GREEN}📊 Lines per log: $LINES (default)${NC}"
fi

echo -e "${GREEN}📁 Configuration: $CONFIG_FILE${NC}"

if [[ -n "$OUTPUT_FILE" ]]; then
    echo -e "${GREEN}💾 Output saved to: $OUTPUT_FILE${NC}"
fi

echo -e "\n${YELLOW}💡 Tip: Use -t for time filtering, -l for line limits, edit $CONFIG_FILE to customize sources${NC}"