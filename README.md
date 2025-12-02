# Abierto IA - Plataforma de Servicios

> Trabajo Práctico Final - Introducción al Desarrollo de Software

Plataforma web para la conexión entre proveedores de servicios profesionales y clientes. Permite a los proveedores publicar sus servicios (plomería, electricidad, carpintería, limpieza, etc.) y a los clientes buscar, reservar y calificar dichos servicios.

## 🎯 Problema que Resuelve

La plataforma aborda la necesidad de conectar de manera eficiente a profesionales de servicios con clientes que buscan soluciones confiables. Los principales problemas que resuelve son:

- **Para Clientes**: Dificultad para encontrar profesionales confiables, comparar precios, ver calificaciones y hacer reservas de forma organizada
- **Para Proveedores**: Falta de visibilidad, gestión manual de reservas, ausencia de un sistema para recibir reseñas y validar su reputación
- **Para Ambos**: Inexistencia de un canal centralizado de comunicación y gestión de servicios con historial de transacciones

### Funcionalidades Principales

**Para Clientes:**
- Búsqueda y filtrado de servicios por categoría, ubicación, precio y calificación
- Sistema de reservas con selección de fecha y hora
- Visualización del historial de reservas
- Sistema de calificación y reseñas

**Para Proveedores:**
- Gestión completa de servicios (crear, editar, eliminar)
- Dashboard con estadísticas de servicios y reservas
- Visualización de reservas pendientes y confirmadas
- Acceso a reseñas y calificaciones recibidas

## 🏗️ Arquitectura del Sistema

El proyecto implementa una **arquitectura cliente-servidor con separación de responsabilidades**:

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE (Browser)                     │
│                     http://localhost:1234                    │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                │ HTTP Requests
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Flask App)                      │
│                     - Renderizado de Templates               │
│                     - Gestión de Sesiones JWT                │
│                     - Rutas de Usuario                       │
│                     - Port: 1234                             │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                │ RESTful API Calls
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                     BACKEND (Flask API)                      │
│                     - Lógica de Negocio                      │
│                     - Autenticación JWT                      │
│                     - Endpoints REST                         │
│                     - Port: 5500                             │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                │ SQL Queries
                                ↓
┌─────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS (MySQL)                     │
│                     - Usuarios y Roles                       │
│                     - Servicios y Categorías                 │
│                     - Reservas y Reseñas                     │
│                     - Relaciones Geográficas                 │
└─────────────────────────────────────────────────────────────┘
```

### Componentes Principales

#### 1. Frontend Application (`front/`)
Aplicación Flask que gestiona la interfaz de usuario:
- **Templates**: Vistas HTML con Jinja2 para renderizado dinámico
- **Rutas**: Controladores para autenticación, servicios, reservas, categorías, usuarios
- **Back Calls**: Capa intermedia que se comunica con la API backend
- **Estilos**: CSS con diseño inspirado en Mercado Libre (clean, professional)

#### 2. Backend API (`back/`)
API RESTful con Flask que implementa la lógica de negocio:
- **Endpoints**: `/api/auth`, `/api/servicios`, `/api/reservas`, `/api/categorias`, `/api/proveedores`, `/api/resenas`, `/api/usuarios`, `/api/ubicacion`
- **Autenticación**: JWT (JSON Web Tokens) almacenados en cookies HTTP-only
- **CORS**: Configurado para permitir comunicación entre frontend y backend
- **Base de Datos**: Conexión con MySQL mediante `mysql-connector-python`

#### 3. Base de Datos (MySQL)
Esquema relacional con las siguientes tablas principales:
- **usuarios**: Información de usuarios con roles (cliente/proveedor/admin)
- **servicios**: Catálogo de servicios con precios, horarios y descripciones
- **reservas**: Historial de reservas con estados (pendiente/confirmado/realizado/cancelado)
- **resenas**: Calificaciones y comentarios de clientes
- **categorias**: Clasificación de servicios (Plomería, Electricidad, etc.)
- **barrios**: Ubicaciones geográficas de Buenos Aires
- **barrios_servicios**: RelaciónMany-to-Many entre servicios y ubicaciones

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.1.2**: Framework web minimalista para Python
- **Flask-JWT-Extended 4.7.1**: Autenticación basada en tokens JWT
- **Flask-CORS 6.0.1**: Manejo de Cross-Origin Resource Sharing
- **mysql-connector-python 9.5.0**: Driver oficial de MySQL
- **python-dotenv 1.2.1**: Gestión de variables de entorno

### Frontend
- **Flask 3.1.2**: Servidor de aplicación para templates
- **Jinja2 3.1.6**: Motor de templates
- **HTML5/CSS3**: Estructura y estilos
- **JavaScript**: Interactividad del lado del cliente

### Librerías Adicionales
- **qrcode 8.2**: Generación de códigos QR para reservas
- **Pillow 12.0.0**: Procesamiento de imágenes
- **requests 2.32.5**: Cliente HTTP para comunicación entre frontend y backend

### Base de Datos
- **MySQL**: Sistema de gestión de base de datos relacional

## 📁 Estructura del Proyecto

```
abierto-ia/
├── back/                      # Backend API
│   ├── app.py                 # Aplicación principal del backend
│   ├── db/
│   │   ├── db.py              # Conexión a la base de datos
│   │   ├── init_db.py         # Inicialización de la BD
│   │   └── init_db.sql        # Script SQL de creación y carga
│   └── routes/                # Endpoints REST
│       ├── auth.py            # Autenticación y registro
│       ├── servicios.py       # CRUD de servicios
│       ├── reservas.py        # Gestión de reservas
│       ├── categorias.py      # Categorías de servicios
│       ├── provedores.py      # Gestión de proveedores
│       ├── resenas.py         # Reseñas y calificaciones
│       ├── usuarios.py        # Gestión de usuarios
│       └── ubicacion.py       # Ubicaciones geográficas
│
├── front/                     # Frontend Application
│   ├── app.py                 # Aplicación principal del frontend
│   ├── back_calls/            # Cliente API (comunicación con backend)
│   │   ├── auth.py
│   │   ├── servicios.py
│   │   ├── reservas.py
│   │   ├── categorias.py
│   │   ├── proveedores.py
│   │   └── ubicaciones.py
│   ├── routes/                # Controladores de vistas
│   │   ├── auth.py            # Login/Register
│   │   ├── servicios.py       # Vistas de servicios
│   │   ├── reservas.py        # Vistas de reservas
│   │   ├── categorias.py      # Búsqueda por categoría
│   │   └── usuarios.py        # Perfil de usuario
│   ├── templates/             # Plantillas HTML
│   │   ├── home.html
│   │   ├── register.html
│   │   ├── categoria.html
│   │   ├── mis_servicios.html
│   │   ├── editar_servicio.html
│   │   └── base/
│   │       └── base.html      # Template base
│   └── static/                # Recursos estáticos
│       ├── css/               # Hojas de estilo
│       ├── js/                # Scripts del cliente
│       └── images/            # Imágenes
│
├── .env                       # Variables de entorno
├── requirements.txt           # Dependencias de Python
├── main.py                    # Punto de entrada principal
└── README.md                  # Este archivo
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/lautsoria/abierto-ia.git
cd abierto-ia
```

2. **Crear y activar entorno virtual**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
Crear archivo `.env` en la raíz del proyecto:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=ids

JWT_SECRET_KEY=tu_clave_secreta_jwt
SECRET_KEY=tu_clave_secreta_flask
```

5. **Inicializar la base de datos**
```bash
# Ejecutar el script SQL
mysql -u root -p < back/db/init_db.sql

# O usar el script de Python
python back/db/init_db.py
```

6. **Iniciar el backend**
```bash
cd back
python app.py
```
El backend estará disponible en `http://localhost:5500`

7. **Iniciar el frontend** (en otra terminal)
```bash
cd front
python app.py
```
El frontend estará disponible en `http://localhost:1234`

## 📊 Modelo de Datos

### Diagrama Entidad-Relación (Simplificado)

```
usuarios (1) ──────< (N) reservas (N) >────── (1) servicios
    │                                              │
    │                                              │
    │                                       (1) proveedor
    │                                              │
    │                                              │
    └──────> (1) roles                    (N) categorias (1)
    │                                              │
    │                                              │
    └──────> (N) resenas                          └──> (N) barrios_servicios (N) >──── (1) barrios
```

### Relaciones Clave
- Un **usuario** puede tener el rol de cliente, proveedor o admin
- Un **proveedor** puede ofrecer múltiples **servicios**
- Un **servicio** pertenece a una **categoría** y puede estar disponible en múltiples **barrios**
- Un **cliente** puede crear múltiples **reservas**
- Una **reserva** puede tener una **reseña** asociada

## 🔐 Autenticación y Seguridad

- **JWT (JSON Web Tokens)**: Autenticación stateless basada en tokens
- **Cookies HTTP-only**: Los tokens JWT se almacenan en cookies seguras
- **Validación de roles**: Middleware para proteger rutas según el tipo de usuario
- **Hashing de contraseñas**: (Nota: Implementar bcrypt en producción)

## 📝 Endpoints de la API

### Autenticación
- `POST /api/auth/register` - Registro de usuarios
- `POST /api/auth/login` - Inicio de sesión
- `POST /api/auth/logout` - Cierre de sesión

### Servicios
- `GET /api/servicios` - Listar servicios (con filtros)
- `GET /api/servicios/<id>` - Obtener servicio específico
- `POST /api/servicios` - Crear servicio (proveedor)
- `PUT /api/servicios/<id>` - Actualizar servicio (proveedor)
- `DELETE /api/servicios/<id>` - Eliminar servicio (proveedor)

### Reservas
- `GET /api/reservas` - Listar reservas del usuario
- `POST /api/reservas` - Crear nueva reserva
- `PUT /api/reservas/<id>` - Actualizar estado de reserva

### Reseñas
- `GET /api/resenas/servicio/<id>` - Obtener reseñas de un servicio
- `POST /api/resenas` - Crear reseña

### Categorías y Ubicaciones
- `GET /api/categorias` - Listar categorías
- `GET /api/ubicacion/barrios` - Listar barrios disponibles

## 👥 Equipo de Desarrollo

Proyecto desarrollado por estudiantes de Introducción al Desarrollo de Software.

## 📄 Licencia

Este proyecto es un trabajo académico desarrollado para la materia Introducción al Desarrollo de Software.

