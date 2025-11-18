## 17 de Noviembre, 2025

### Colección de Tests API con Bruno

**Implementación:**
- Creada colección completa de tests API usando Bruno (herramienta open-source de testing)
- Estructura organizada en carpetas: `/Auth`, `/Servicios`, `/Proveedores`, `/Categorias`
- **11 tests totales** cubriendo todos los endpoints del backend:
  - Auth: Register, Register Provider, Login
  - Servicios: Top Rating, Filter by Category, Filter by Price Range
  - Proveedores: Get All, Filter by Service, Get by ID
  - Categorias: Get Category Count, Get All Categories
- Configurado entorno `Local` con variables: base_url, test_user, test_email, test_password
- Agregadas assertions automáticas para validar status codes, estructura de respuestas y tipos de datos
- Incluido `README.md` con instrucciones de instalación y uso de Bruno CLI

**Características:**
- Variables aleatorias (`{{$randomInt}}`) en tests de registro para evitar duplicados
- Manejo automático de cookies para JWT authentication
- Tests parametrizados con query strings y path parameters
- Validación de campos requeridos en respuestas

### Conversión de Tipos Decimales en MySQL

**Problema identificado:**
- MySQL Connector Python retorna resultados de `AVG()` como objetos `Decimal` (no como `float`)
- `Decimal` no es JSON serializable, causaba `TypeError` al retornar respuestas

**Solución implementada:**
- Agregada conversión manual de `Decimal` a `float` en todos los endpoints de `/servicios`:
  - `/categoria/<nombre>`: Convierte `rating` a float
  - `/top-rating`: Convierte `rating` a float
  - `/precio`: Convierte `rating` y `precio` a float
- Loop post-query convierte valores antes de `jsonify()`

**Mapeo de tipos MySQL → Python:**
- `INT`, `BIGINT` → `int`
- `FLOAT`, `DOUBLE` → `float`
- `DECIMAL`, `AVG()` → `Decimal` (requiere conversión manual)

### Optimización de Endpoint de Categorías

**Problema original:**
- Frontend hacía **9 requests HTTP** para mostrar categorías:
  - 1 request para obtener lista de nombres
  - 8 requests adicionales (uno por cada categoría) para obtener conteo de profesionales
- Endpoint `/categorias/buscar_existentes` no existía en el backend

**Solución:**
- Creado nuevo endpoint `/categorias/buscar_existentes`:
  - Retorna TODAS las categorías con sus conteos en una sola query
  - Usa `COUNT(DISTINCT s.proveedor_id)` con `LEFT JOIN` y `GROUP BY`
  - Reduce de 9 requests a **1 solo request**
- Simplificado código del frontend:
  - Eliminado loop que hacía requests individuales
  - Ahora solo agrega iconos a los datos ya completos del backend
- Marcada función `obtener_cantidad_categoria()` como DEPRECATED

### Corrección de Template home.html

**Problemas identificados:**
- Template esperaba campos inexistentes: `servicio.titulo`, `servicio.reviews`, `servicio.destacado`
- Error `ValueError: Unknown format code 'f' for object of type 'str'` al formatear precios
- Faltaba validación de datos opcionales (rating, imagen)

**Correcciones aplicadas:**
- Mapeado correcto de campos del backend:
  - `servicio.titulo` → `servicio.nombre`
  - `servicio.reviews` → `servicio.reviews_count`
  - `servicio.destacado` → Lógica basada en `servicio.rating >= 4.5`
- Agregado filtro Jinja2 para conversión de precio: `servicio.precio | float`
- Agregadas validaciones con `{% if servicio.rating %}` para evitar errores con datos nulos
- Placeholder de imagen si falta: `https://via.placeholder.com/300x200?text=Servicio`
- Mensaje de fallback para servicios sin reviews

### Expansión de Base de Datos

**Nuevos servicios agregados (10 adicionales):**
- Plomería: Destapación de cañerías ($4,500)
- Electricidad: Instalación de tomas ($3,200), Revisión de tablero eléctrico ($5,500)
- Carpintería: Reparación de puertas ($3,800), Instalación de estanterías ($6,500)
- Limpieza: Limpieza de oficinas ($8,000), Limpieza de vidrios ($2,200)
- Jardinería: Mantenimiento de jardín ($4,200)
- Pintura: Pintura de interiores ($12,000), Pintura de fachadas ($18,000)

**Total: 15 servicios** distribuidos en 6 categorías

**Sistema de Reseñas Completo:**
- Generadas ~40 reseñas distribuidas entre todos los servicios
- Distribución realista de puntuaciones:
  - 20% dan 3 estrellas
  - 40% dan 4 estrellas
  - 40% dan 5 estrellas (sesgo positivo realista)
- 15 comentarios variados predefinidos
- Reseñas distribuidas en los últimos 60 días
- Promedio de 2-4 reseñas por servicio
- Solo usuarios no-proveedores pueden dejar reseñas

**Resultado:**
- Todos los servicios ahora tienen ratings visibles
- Endpoint `/servicios/top-rating` retorna datos completos
- Home page muestra servicios destacados con estrellas y conteo de reviews

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