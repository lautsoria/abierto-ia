#!/bin/bash

# Script to restart both frontend and backend services

echo "Restarting services..."

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Stop services
"$SCRIPT_DIR/stop.sh"

# Wait a moment
sleep 2

# Start services
"$SCRIPT_DIR/start.sh"
