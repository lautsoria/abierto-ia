#!/bin/bash

# Script to start both frontend and backend services

echo "Starting services..."

# Get the project root directory (parent of scripts folder)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/logs"

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "Virtual environment not found. Please create it first with: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
source "$PROJECT_ROOT/.venv/bin/activate"

# Start backend
echo "Starting backend on port 5500..."
cd "$PROJECT_ROOT/back"
python app.py > "$PROJECT_ROOT/logs/backend.log" 2>&1 &
BACK_PID=$!
echo "Backend started with PID: $BACK_PID"

# Wait a moment for backend to initialize
sleep 2

# Start frontend
echo "Starting frontend on port 5000..."
cd "$PROJECT_ROOT/front"
python app.py > "$PROJECT_ROOT/logs/frontend.log" 2>&1 &
FRONT_PID=$!
echo "Frontend started with PID: $FRONT_PID"

# Save PIDs to file for later shutdown
echo "$BACK_PID" > "$PROJECT_ROOT/logs/backend.pid"
echo "$FRONT_PID" > "$PROJECT_ROOT/logs/frontend.pid"

echo ""
echo "✓ Services started successfully!"
echo "  - Backend: http://localhost:5500 (PID: $BACK_PID)"
echo "  - Frontend: http://localhost:5000 (PID: $FRONT_PID)"
echo ""
echo "Logs are available at:"
echo "  - Backend: $PROJECT_ROOT/logs/backend.log"
echo "  - Frontend: $PROJECT_ROOT/logs/frontend.log"
echo ""
echo "To stop services, run: ./scripts/stop.sh"
