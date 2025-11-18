# Bruno API Tests - Mercado Servicios

Este directorio contiene pruebas de API usando [Bruno](https://www.usebruno.com/), una herramienta de testing de APIs open-source.

## Instalación

```bash
# Instalar Bruno CLI
npm install -g @usebruno/cli

# O descargar la aplicación de escritorio desde:
# https://www.usebruno.com/downloads
```

## Estructura de Tests

```
bruno-tests/
├── Auth/                    # Tests de autenticación
│   ├── Register.bru
│   ├── Register Provider.bru
│   └── Login.bru
├── Servicios/              # Tests de servicios
│   ├── Get Top Rated Services.bru
│   ├── Get Services By Category.bru
│   └── Get Services By Price Range.bru
├── Proveedores/            # Tests de proveedores
│   ├── Get All Proveedores.bru
│   ├── Get Proveedores By Service.bru
│   └── Get Proveedor By ID.bru
├── Categorias/             # Tests de categorías
│   ├── Get Category Count.bru
│   └── Get All Categories.bru
└── environments/           # Variables de entorno
    └── Local.bru
```

## Ejecutar Tests

### Con Bruno CLI:

```bash
# Ejecutar todos los tests
bru run --env Local

# Ejecutar una carpeta específica
bru run Auth --env Local
bru run Servicios --env Local

# Ejecutar un test específico
bru run Auth/Login.bru --env Local
```

### Con la aplicación Bruno:

1. Abre Bruno
2. Haz clic en "Open Collection"
3. Selecciona el directorio `bruno-tests`
4. Selecciona el entorno "Local" en el dropdown
5. Ejecuta los tests individualmente o en conjunto

## Variables de Entorno

El entorno `Local` incluye:

- `base_url`: http://localhost:5500
- `test_user`: juan_perez
- `test_email`: juan@gmail.com
- `test_password`: pass123

## Pre-requisitos

Antes de ejecutar los tests, asegúrate de que:

1. El backend esté corriendo en `http://localhost:5500`
2. La base de datos esté inicializada con datos de prueba
3. Los usuarios de prueba existan en la base de datos

```bash
# Iniciar backend
cd back
python app.py

# Inicializar base de datos (si es necesario)
python back/db/init_db.py
```

## Orden Recomendado de Ejecución

1. **Auth/Register** - Crear un nuevo usuario
2. **Auth/Login** - Iniciar sesión (guarda cookies)
3. **Servicios/** - Tests de servicios
4. **Proveedores/** - Tests de proveedores
5. **Categorias/** - Tests de categorías

## Notas

- Los tests de Auth usan variables aleatorias (`{{$randomInt}}`) para evitar duplicados
- Algunos tests requieren que existan datos en la base de datos
- Las cookies se mantienen automáticamente entre requests en Bruno
