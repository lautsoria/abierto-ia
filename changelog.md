## 30 de Noviembre, 2025

### Actualización crítica de esquema, seeds y rutas

**Base de Datos & Seeds:**
- Renombrada/ajustada la tabla de junction: ahora `barrios_servicios` (linkea `servicio_id` ↔ `barrio_id`).
- Seed de `usuarios`, `categorias`, `barrios` y `servicios` reescrita: inserciones en bloque con `UUID()` y referencias por subqueries.
- Se agregaron 10 servicios adicionales y se asegura que cada servicio tenga al menos 1 barrio asociado (inserción aleatoria); se añade un segundo barrio aleatorio a un subconjunto de servicios.
- Seeds de `reservas` ampliadas: generación aleatoria de reservas pasadas y aumento del volumen (hasta 60 registros) para pruebas.
- Seeds de `resenas` generadas a partir de reservas realizadas (hasta 3 reseñas por servicio) con fechas y puntajes aleatorios.

**Rutas / Backend:**
- Reemplazo consistente de `barrios_usuarios` por `barrios_servicios` en múltiples endpoints (`proveedores`, `servicios`, `reservas`, `servicios_top_rating`, etc.).
- `servicios`:
  - Endpoint `GET /servicios/todos` arreglado para devolver la lista completa de servicios (ahora incluye `proveedor` y `categoria`).
  - `DELETE` de servicio modificado para recibir JSON con `id` y ahora borra también registros en `barrios_servicios` relacionados.
  - Actualización de servicio: ahora `PATCH /servicios/mod` que recibe `data['id']` y simplifica los campos actualizados.
  - Mejor manejo de errores y logs agregados en varias rutas.
- `proveedores` y consultas relacionadas adaptadas para trabajar con `barrios_servicios` y mostrar ubicaciones por servicio.
- `usuarios`:
  - Endpoint de eliminación unificado (`/eliminar`) actualizado para recibir JSON; la lógica borra reseñas, reservas y datos relacionados antes de eliminar el usuario según su rol (`proveedor` o `cliente`).

**Otros cambios y notas:**
- Correcciones en `init_db.sql` (uso correcto de `UUID()` y reordenamiento/agrupación de inserts para consistencia).
- Ajustes en generación de datos (fechas, límites, formatos) para que sean más realistas y compatibles con la API.
- Pequeños refactors en controladores: impresión de excepciones para facilitar debugging y limpieza de queries.

Advertencia: estas migraciones y seeds modifican datos y relaciones; al aplicarlas en un entorno con datos reales es recomendable usar scripts de migración o reseed controlado.

## 25 de Noviembre, 2025

### Sistema de Reseñas - Endpoint POST

**Backend - Nuevo Endpoint:**
- Implementado `POST /resenas` para crear nuevas reseñas
- Recibe: `usuario_id`, `servicio_id`, `estrellas`, `descripcion`
- Genera UUID automático para cada reseña
- Retorna status 200 con mensaje de éxito

**Corrección de Schema:**
- Fixed `init_db.sql`: cambiado `UUID` a `UUID()` en tabla `resenas`

### Flujo de Confirmación de Servicio Mejorado

**Frontend - Confirmación (`app.py`):**
- Simplificado endpoint `/confirmar-servicio/<id_reserva>` (removido token de URL)
- Agregado `@jwt_required` para validar usuario autenticado
- Validación de que el usuario es dueño de la reserva (401 si no coincide)
- POST ahora envía reseña a `/resenas` en lugar de `/proveedores/añadir_puntuacion`
- Redirige a home después de enviar reseña exitosamente
- Confirmación de servicio (`estado = 'realizado'`) se ejecuta en GET

**Generación de QR Dinámica:**
- URL del QR ahora usa variable de entorno `PUBLIC_URL`
- Permite configurar IP local para acceso desde móviles en la misma red
- Default: `http://localhost:5000`

### Estilos Mercado Libre - Página de Confirmación

**Rediseño completo de `confirmado.css`:**
- Header verde con gradiente (#00a650 → #008a43) estilo ML
- Check icon con imagen personalizable (check-verified.png)
- Card con bordes sutiles y sombra mínima
- Info box con fondo gris claro para tips
- Form inputs con focus state azul ML (#3483fa)
- Botón de envío azul ML con hover states
- Responsive design para móviles

**Template `confirmado.html`:**
- Nueva estructura: container → header → card → body
- Info box con ícono 💡 y mensaje sobre importancia de reseñas
- Labels más descriptivos ("¿Cómo calificarías el servicio?")
- Placeholder mejorado en textarea
- Fixed: `url_for('confirmar_servicio', id_reserva=reserva)` con parámetro correcto

### Página de Reservas - Mejoras UI

**Badges de Estado (`reservas.html`):**
- Agregados badges visuales para mostrar estado de cada reserva
- Colores por estado:
  - `pendiente` → badge-warning (amarillo)
  - `confirmado` → badge-primary (azul)
  - `realizado` → badge-success (verde)
  - otros → badge-danger (rojo)
- Badge mostrado junto al botón "Ver Detalle"

**Ordenamiento:**
- Reservas ahora ordenadas ASC por `fecha_servicio` (más próximas primero)
- Cambiado tanto para clientes como proveedores en `reservas.py`

**Estilos (`reservas.css`):**
- Variables CSS en `:root` para colores consistentes
- Clases `.badge-*` para estados con colores específicos
- `.btn-success` agregado con estilo igual a `.btn-primary`
- Botón "Generar QR" cambió de `btn-sm` a tamaño regular
- Contenedor compatible con template base

### Navegación y Compatibilidad

**Base Template (`base.html`):**
- Link #categorias cambiado a `{{ url_for('home') }}#categorias`
- Funciona correctamente desde cualquier página

**Template `editar_perfil.html`:**
- Ya compatible con base template
- CSS sin estilos de body (usa container)

### Acceso desde Red Local (QR desde móvil)

**Configuración de Red:**
- Flask debe correr con `--host=0.0.0.0` para aceptar conexiones externas
- Puerto 5000 abierto en UFW: `sudo ufw allow 5000`
- Acceso desde móvil: `http://<IP-local>:5000`
- Variable `PUBLIC_URL` en .env para URL correcta en QR

### Correcciones Varias

**Backend:**
- `auth.py`: Removido import no usado de `datetime`
- `reservas.py`: Removido parámetro `token` de `confirmar_servicio()`

**Frontend:**
- `editar_perfil.html`: Ahora recibe `data` para mostrar nav correctamente
- `app.py`: Puerto cambiado de 1230 a 1234
- Limpieza de código: removidos comentarios TODO y líneas vacías extra

---

### Sistema de Confirmación de Servicio con QR

**Generación de QR:**
- Implementado sistema de códigos QR para confirmar servicios realizados
- Proveedores pueden generar QR desde la página de reservas
- QR contiene URL de confirmación: `/reservas/confirmar-servicio/{id_reserva}/{token}`
- Imagen QR guardada en `static/qr_reserva_{id}.png`

**Endpoint de Confirmación:**
- Simplificado endpoint `POST /reservas/confirmar-servicio/<id_reserva>/<token>`
- Eliminada dependencia de columna `token_qr` - ahora usa el ID de reserva como token
- Actualiza estado de reserva a 'realizado' al escanear QR válido

### Limpieza y Refactorización de Código

**Backend - Auth (`auth.py`):**
- Eliminado código comentado de bcrypt (hashing de contraseñas no implementado aún)
- Removido logger no utilizado
- Simplificados imports innecesarios
- Agregado `datetime` import para uso futuro
- Query de login ahora incluye `fecha_registro` del usuario

**Backend - Reservas (`reservas.py`):**
- Cambiado `GET /reservas` de JSON body a query parameters (`request.args`)
- Fixed alias incorrecto: `uc.id` → `u.id` en JOIN de usuarios para reservas de proveedor
- Eliminada validación de rol redundante (else branch)
- Mejorado manejo de errores: `str(e)` en lugar de `e` directamente
- Comentado endpoint `/reservas/<id>/token` (deprecado - ya no se usa `token_qr`)

**Base de Datos (`init_db.sql`):**
- Eliminada columna `token_qr` de tabla `reservas` (simplificación del modelo)
- Actualizado INSERT de reservas dummy para reflejar nuevo schema

### Mejoras en Frontend

**Página de Reservas (`reservas.html`):**
- Botón de generar QR ahora solo visible para proveedores
- Corregido `url_for('generarqr')` con parámetro `id_reserva`
- Variable de rol obtenida directamente del JWT en lugar de request adicional

**Flujo de Mis Reservas (`app.py`):**
- Admins ahora ven todas las reservas automáticamente (`/reservas/todas`)
- Eliminado request redundante a `/usuarios/{id}` para obtener rol
- Rol se obtiene directamente de `get_jwt()['rol']`
- Simplificada lógica de obtención de reservas según rol

**Registro de Proveedores:**
- Proveedores nuevos son redirigidos a completar perfil después del registro
- Mensaje flash cambiado de "Inicio de sesión exitoso" a "Usuario creado con éxito"

**Generación de QR (`calls.py`):**
- URL de confirmación actualizada a `/reservas/confirmar-servicio/{id}/{token}`

## 21 de Noviembre, 2025

### Sistema de Redirección Post-Login

**Implementación de Next URL:**
- Implementado flujo completo de redirección usando query parameter `?next=`
- Cuando usuario no autenticado intenta acceder a ruta protegida:
  1. `@jwt.unauthorized_loader` captura la URL solicitada
  2. Redirige a `/auth?next=/ruta/original`
  3. Template `auth.html` incluye `next` en forms de login/register
  4. Después de login exitoso, redirige a URL original
- Validación de seguridad: solo permite redirecciones internas

### Sistema de Reseñas en Páginas de Servicio

**Backend - Endpoint de Reseñas:**
- Corregido query SQL en `obtener_resenas_servicio()`:
  - Fixed typo: `i.id` → `u.id` en JOIN de usuarios
  - Agregada coma faltante entre columnas SELECT
  - Agregado `dictionary=True` al cursor para retornar dicts en lugar de tuplas
  - Implementada conversión de datetime a ISO string con `.isoformat()`
- Query ahora retorna: `usuario`, `puntuacion`, `comentarios_cliente`, `fecha`

**Frontend - Display de Reseñas:**
- Implementado loop Jinja2 en `servicio.html` para mostrar reseñas dinámicamente
- Sistema de estrellas: genera `★` por cada punto de puntuación
- Formateo de fecha: muestra solo fecha (sin hora) con string slicing `[:10]`
- Manejo de estado vacío: mensaje "Aún no hay reseñas" cuando `resenas` está vacío
- Agregado nombre de usuario y fecha en cada reseña

**Corrección de Rating:**
- Fixed `calificacion_promedio` display: ahora muestra 1 decimal con `round(servicio.calificacion_promedio, 1)`
- Ejemplo: `4.666667` → `4.7`


## 20 de Noviembre, 2025

### Sistema de Reservas Completo

**Backend - Endpoints de Reservas:**
- Implementado endpoint `POST /reservas` para crear reservas
  - Validación de servicio existente antes de crear reserva
  - Genera UUID automático para cada reserva
  - Guarda: usuario_id, servicio_id, fecha_servicio, hora_servicio, direccion, comentarios_cliente
  - Estado por defecto: 'pendiente'
- Implementado endpoint `GET /reservas/<id>` para obtener detalles de una reserva específica
  - Retorna información completa: servicio, proveedor, cliente, categoría
  - Incluye datos del proveedor: nombre, teléfono, ubicaciones (barrios)
  - Convierte Decimal a float para serialización JSON
  - Formatea fechas a ISO string
- Implementado endpoint `PUT /reservas/<id>` para actualizar estado de reserva
  - Permite modificar: estado, comentarios_cliente, fecha_servicio
  - Validación de estados permitidos: 'pendiente', 'realizado', 'cancelado'
- Implementado endpoint `GET /reservas/servicio/<id>` para obtener reservas de un servicio
  - Filtra solo reservas pendientes
  - Formatea hora_servicio de INT a string "HH:00"
  - Usado para mostrar horarios NO disponibles en el checkout

**Frontend - Flujo de Reserva:**
- Creado `checkout.html`: página de confirmación de reserva
  - Muestra preview del servicio con imagen y proveedor
  - Formulario con: fecha, hora (dropdown dinámico), dirección, notas, mensaje
  - Date picker con rango de 15 días desde hoy
  - Validación de dirección (mínimo 5 caracteres)
- Implementado sistema de horarios dinámicos:
  - Los horarios disponibles se calculan en `obtener_servicio_por_id()` usando hora_inicio, hora_fin, duracion
  - JavaScript deshabilita horarios ya reservados al seleccionar fecha
  - Alert si todos los horarios están ocupados
- Creado `reserva.html`: página de confirmación post-reserva
  - Banner de éxito con animación
  - Card con todos los detalles: servicio, fecha/hora, dirección, proveedor, precio
  - Badge de estado (pendiente/realizado/cancelado)
  - Info card con próximos pasos
  - Botones: "Volver al inicio", "Ver mis reservas"
- Creado `reserva.css`: estilos Mercado Libre inspired
  - Green gradient para banner de éxito
  - Cards con box-shadow sutil
  - Responsive design para móviles
  - Animación de entrada para el ícono de éxito

**Modularización de Llamadas al Backend:**
- Agregadas funciones en `front/back_calls/calls.py`:
  - `reservar()`: POST request para crear reserva
  - `obtener_reserva_por_id()`: GET request para obtener detalles
  - `no_disponibles()`: GET request para obtener reservas existentes de un servicio
- Parsing de hora: convierte "08:00" string a integer 8 antes de enviar al backend

**Correcciones de Bugs:**
- Fixed JWT expiration handling: cambiado de `render_template('home.html')` a `redirect(url_for('home'))` en error handlers
- Fixed `/auth` route para limpiar cookies expiradas con `set_cookie('access_token_cookie', '', max_age=0)`
- Fixed route conflicts: función POST renombrada de `reserva()` a `crear_reserva()`
- Fixed GET route para reserva individual: ahora es `/reserva/<reserva_id>`
- Fixed `url_for()` syntax en Jinja2: cambiado de `{{ url_for('reserva'), servicio=servicio.id }}` a `{{ url_for('crear_reserva', servicio=servicio.id) }}`
- Fixed HTTP method: cambiado de `requests.get()` a `requests.post()` en función `reservar()`
- Fixed template rendering: removido `.strftime()` para fechas (vienen como ISO strings del backend)
- Fixed price formatting: agregado `| float` filter en Jinja2

**Datos de Prueba:**
- Agregado campo `direccion` a las 10 reservas dummy en `init_db.sql`
- Direcciones random de CABA: Av. Santa Fe, Av. Corrientes, Av. Cabildo, etc.

### Migración de Schema: Ubicaciones a Barrios

**Cambios en Base de Datos:**
- Eliminada columna `proveedores.ubicacion` (VARCHAR)
- Creada tabla `barrios` con UUID y nombre
- Creada tabla junction `barrios_usuarios` para relación muchos-a-muchos
- Insertados 48 barrios de CABA
- Updated seed data: proveedores ahora asociados a barrios específicos

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