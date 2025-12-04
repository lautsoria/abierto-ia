#!/bin/bash

echo "Reiniciando servicios..."


SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

"$SCRIPT_DIR/stop.sh"

sleep 2

"$SCRIPT_DIR/start.sh"
