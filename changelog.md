## 15 de Noviembre, 2025

### Arquitectura de Templates con Jinja2

**Implementación:**
- Implementada herencia de templates usando Jinja2
- `home.html` ahora extiende `base.html` para reutilizar header y footer
- Agregado sistema de bloques en `base.html`:
  - `{% block title %}` para títulos personalizados por página
  - `{% block styles %}` para CSS específico de cada página
  - `{% block content %}` para el contenido principal
  - `{% block scripts %}` para JavaScript específico de cada página
- CSS modular: `base.css` para estilos comunes, `home.css` para estilos específicos de home

**Navegación dinámica:**
- Header en `base.html` muestra opciones diferentes según estado de autenticación y rol:
  - Usuario no autenticado: "Categorías", "Ofertas", "Ingresá"
  - Usuario regular autenticado: "Categorías", "Ofertas", "Mi Perfil", "Ver 🛒"
  - Proveedor autenticado: "Registrar servicio", "Calendario", "Mi perfil", "Mis servicios"
- La lógica usa `{% if data %}` y `{% if data.provider %}` para determinar qué mostrar
- Variables pasadas a `render_template()` están disponibles en todo el árbol de herencia


### Scripts de Gestión de Servicios

**Implementación:**
- Creada carpeta `/scripts` con scripts bash para gestionar frontend y backend simultáneamente
- Implementado `start.sh`: Inicia ambos servicios (backend en puerto 5500, frontend en puerto 5000)
  - Activa automáticamente el entorno virtual
  - Guarda logs en carpeta `logs/`
  - Guarda PIDs de procesos para shutdown limpio
- Implementado `stop.sh`: Detiene ambos servicios de forma segura
  - Usa PIDs guardados para terminar procesos correctamente
  - Fallback a matar por puerto si los PIDs no existen
- Implementado `restart.sh`: Reinicia ambos servicios
- Agregado `scripts/README.md` con documentación de uso

### Mejoras en el Sistema de Roles

**Frontend:**
- Modificado `base.html` para mostrar navegación diferenciada según rol de usuario
- Proveedores ven: "Registrar servicio", "Calendario", "Mi perfil", "Mis servicios"
- Usuarios regulares ven: "Categorías", "Ofertas", "Ingresá", "Mis Compras", "Ver 🛒"
- La navegación se actualiza dinámicamente usando `data.role.role` del JWT

**Correcciones:**
- Fixeado bug en `register.js`: cambiado `checkbox.value` por `checkbox.checked` para obtener el valor booleano correcto del checkbox "Soy proveedor"

## 14 de Noviembre, 2025

### Sistema de Autenticación con JWT

**Implementación:**
- Configuré Flask-JWT-Extended para usar cookies HttpOnly en lugar de localStorage (más seguro contra XSS)
- Implementé endpoints de `/login`, `/register` en el backend
- Agregué manejo de roles: los tokens incluyen claim "provider" para usuarios proveedores
- Configuré CORS para permitir credenciales entre frontend (puerto 5000) y backend (puerto 5500)

**Protección de rutas:**
- Agregué decorador `@jwt_required(locations=['cookies'])` para proteger endpoints
- Implementé handlers personalizados (`@jwt.unauthorized_loader`, `@jwt.invalid_token_loader`) para redirigir automáticamente a login cuando el token es inválido
- La ruta `/home` ahora requiere autenticación válida
- La ruta `/` (registro/login) redirige a `/home` si el usuario ya está autenticado

**Correcciones:**
- Fixeé bug en login donde `providerData[0]` causaba crash cuando el usuario no era proveedor
- Fixeé bug donde el token de proveedor se sobrescribía por no tener `else` en la lógica condicional
- Agregué `credentials: 'include'` en todas las llamadas fetch del frontend para enviar cookies automáticamente

**Frontend:**
- Agregado checkbox "Soy proveedor" en formulario de registro
- Implementado flip-card para alternar entre login y registro
- JavaScript maneja submit de formularios con fetch API en lugar de forms tradicionales