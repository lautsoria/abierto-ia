# Scripts para gestionar el proyecto

Este directorio contiene scripts para iniciar y detener los servicios del proyecto (frontend y backend).

## Uso

### Iniciar servicios

```bash
./scripts/start.sh
```

Este script:
- Inicia el backend en el puerto 5500
- Inicia el frontend en el puerto 5000
- Guarda los logs en la carpeta `logs/`
- Guarda los PIDs de los procesos para poder detenerlos después

### Detener servicios

```bash
./scripts/stop.sh
```

Este script detiene ambos servicios (frontend y backend).

### Reiniciar servicios

```bash
./scripts/restart.sh
```

Este script detiene y vuelve a iniciar ambos servicios.

## Requisitos

- El entorno virtual debe estar creado en `.venv`
- Las dependencias deben estar instaladas (`pip install -r requirements.txt`)
- El archivo `.env` debe estar configurado correctamente

## Logs

Los logs de ambos servicios se guardan en:
- Backend: `logs/backend.log`
- Frontend: `logs/frontend.log`

## Permisos

Si obtienes un error de permisos, ejecuta:

```bash
chmod +x scripts/*.sh
```
