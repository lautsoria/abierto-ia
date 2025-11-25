#!/bin/bash

# Script to stop both frontend and backend services

echo "Stopping services..."

# Get the project root directory (parent of scripts folder)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Check if PID files exist
if [ ! -f "$PROJECT_ROOT/logs/backend.pid" ] && [ ! -f "$PROJECT_ROOT/logs/frontend.pid" ]; then
    echo "No PID files found. Services might not be running."
    echo "Trying to find and kill processes by port..."
    
    # Try to kill processes on the ports
    lsof -ti:5500 | xargs kill -9 2>/dev/null && echo "Killed process on port 5500" || echo "No process found on port 5500"
    lsof -ti:5000 | xargs kill -9 2>/dev/null && echo "Killed process on port 5000" || echo "No process found on port 5000"
    exit 0
fi

# Stop backend
if [ -f "$PROJECT_ROOT/logs/backend.pid" ]; then
    BACK_PID=$(cat "$PROJECT_ROOT/logs/backend.pid")
    if ps -p $BACK_PID > /dev/null 2>&1; then
        echo "Stopping backend (PID: $BACK_PID)..."
        kill $BACK_PID 2>/dev/null
        sleep 1
        # Force kill if still running
        if ps -p $BACK_PID > /dev/null 2>&1; then
            kill -9 $BACK_PID 2>/dev/null
        fi
        echo "Backend stopped"
    else
        echo "Backend process not found (might have already stopped)"
    fi
    rm "$PROJECT_ROOT/logs/backend.pid"
fi

# Stop frontend
if [ -f "$PROJECT_ROOT/logs/frontend.pid" ]; then
    FRONT_PID=$(cat "$PROJECT_ROOT/logs/frontend.pid")
    if ps -p $FRONT_PID > /dev/null 2>&1; then
        echo "Stopping frontend (PID: $FRONT_PID)..."
        kill $FRONT_PID 2>/dev/null
        sleep 1
        # Force kill if still running
        if ps -p $FRONT_PID > /dev/null 2>&1; then
            kill -9 $FRONT_PID 2>/dev/null
        fi
        echo "Frontend stopped"
    else
        echo "Frontend process not found (might have already stopped)"
    fi
    rm "$PROJECT_ROOT/logs/frontend.pid"
fi

echo ""
echo "✓ Services stopped successfully!"
