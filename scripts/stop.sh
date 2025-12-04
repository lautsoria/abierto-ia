#!/bin/bash

# Script para detener los servicios de frontend y backend


# Obtener el directorio raíz del proyecto (padre de la carpeta scripts)
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Verificar si existen los archivos PID
if [ ! -f "$PROJECT_ROOT/logs/backend.pid" ] && [ ! -f "$PROJECT_ROOT/logs/frontend.pid" ]; then
    echo "No se encontraron archivos PID. Los servicios podrían no estar corriendo."
    echo "Intentando encontrar y matar procesos por puerto..."
    
    # Intentar matar procesos en los puertos
    lsof -ti:5500 | xargs kill -9 2>/dev/null && echo "Proceso en puerto 5500 terminado" || echo "No se encontró proceso en puerto 5500"
    lsof -ti:5000 | xargs kill -9 2>/dev/null && echo "Proceso en puerto 5000 terminado" || echo "No se encontró proceso en puerto 5000"
    exit 0
fi

# Detener backend
if [ -f "$PROJECT_ROOT/logs/backend.pid" ]; then
    BACK_PID=$(cat "$PROJECT_ROOT/logs/backend.pid")
    if ps -p $BACK_PID > /dev/null 2>&1; then
        echo "Deteniendo backend (PID: $BACK_PID)..."
        kill $BACK_PID 2>/dev/null
        sleep 1
        # Forzar kill si sigue corriendo
        if ps -p $BACK_PID > /dev/null 2>&1; then
            kill -9 $BACK_PID 2>/dev/null
        fi
        echo "Backend detenido"
    else
        echo "Proceso del backend no encontrado (podría haberse detenido ya)"
    fi
    rm "$PROJECT_ROOT/logs/backend.pid"
fi

# Detener frontend
if [ -f "$PROJECT_ROOT/logs/frontend.pid" ]; then
    FRONT_PID=$(cat "$PROJECT_ROOT/logs/frontend.pid")
    if ps -p $FRONT_PID > /dev/null 2>&1; then
        echo "Deteniendo frontend (PID: $FRONT_PID)..."
        kill $FRONT_PID 2>/dev/null
        sleep 1
        # Forzar kill si sigue corriendo
        if ps -p $FRONT_PID > /dev/null 2>&1; then
            kill -9 $FRONT_PID 2>/dev/null
        fi
        echo "Frontend detenido"
    else
        echo "Proceso del frontend no encontrado (podría haberse detenido ya)"
    fi
    rm "$PROJECT_ROOT/logs/frontend.pid"
fi

echo ""
echo "✓ ¡Servicios detenidos exitosamente!"
