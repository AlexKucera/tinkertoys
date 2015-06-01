# As per: http://stackoverflow.com/a/18462920

function log {
	echo "$1">>${LOG_FILE}
}

function message {
	echo "$1"
	echo "$1">>${LOG_FILE}
}

echo "Echoed to console only"
log "Written to log file only"
message "To console and log"