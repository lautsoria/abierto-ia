#!/bin/bash


echo "Levantando aplicacion"

# Buscamos el directorio del proyecto en general
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p "$PROJECT_ROOT/logs"

# Vemos si hay un .venv creado
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "venv no encontrado. Creando uno..."
    python3 -m venv .venv
    exit 1
fi

# Lo activamos
source "$PROJECT_ROOT/.venv/bin/activate"


pip install -r "$PROJECT_ROOT/requirements.txt"

# Start backend
echo "Backend en puerto 5500..."
cd "$PROJECT_ROOT/back"
python app.py > "$PROJECT_ROOT/logs/backend.log" 2>&1 &
BACK_PID=$!
echo "Backend corriendo PID: $BACK_PID"

sleep 2

echo "Frontend en puerto 5000..."
cd "$PROJECT_ROOT/front"
python app.py > "$PROJECT_ROOT/logs/frontend.log" 2>&1 &
FRONT_PID=$!
echo "Frontend corriendo PID: $FRONT_PID"

echo "$BACK_PID" > "$PROJECT_ROOT/logs/backend.pid"
echo "$FRONT_PID" > "$PROJECT_ROOT/logs/frontend.pid"

echo ""
echo "✓ Servicios corriendo correctamente!"
echo "  - Backend: http://localhost:5500 (PID: $BACK_PID)"
echo "  - Frontend: http://localhost:5000 (PID: $FRONT_PID)"
echo ""
echo "Logs en:"
echo "  - Backend: $PROJECT_ROOT/logs/backend.log"
echo "  - Frontend: $PROJECT_ROOT/logs/frontend.log"
echo ""
echo "Para detener los servicios correr: ./scripts/stop.sh"
