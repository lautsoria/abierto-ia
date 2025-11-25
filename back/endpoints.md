# Definición de Endpoints de la API

Este documento define los endpoints para la API del marketplace de servicios.

---

## 🔒 Autenticación (/auth)

Rutas públicas para registrarse, iniciar sesión y manejar OAuth.

### `POST /auth/register`
* **Descripción:** Registra un nuevo usuario (cliente) con email y contraseña.
* **Autorización:** Pública.
* **Body (JSON):** `{ "email": "...", "password": "...", "name": "..." }`
* **Respuesta:** Mensaje de éxito o error.

### `POST /auth/login`
* **Descripción:** Autentica un usuario con email/contraseña.
* **Autorización:** Pública.
* **Body (JSON):** `{ "email": "...", "password": "..." }`
* **Respuesta:** `{ "token": "jwt-token-aqui" }` (o establece una cookie HttpOnly).

### `GET /auth/google`
* **Descripción:** Inicia el flujo de autenticación de Google. Redirige al usuario a la página de login de Google.
* **Autorización:** Pública.

---

## 👷 Proveedores (/proveedores)

Rutas para consultar información sobre los profesionales que ofrecen servicios.

### `GET /proveedores`
* **Descripción:** Devuelve una lista de todos los proveedores.
* **Filtros (Query Params):** Se puede filtrar por servicio. Ej: `?servicio=plomeria`
* **Autorización:** Pública.

### `GET /proveedores/<id>`
* **Descripción:** Devuelve los detalles de un proveedor específico por su ID.
* **Autorización:** Pública.

### `POST /proveedores`
* **Descripción:** Crea un nuevo proveedor en el sistema.
* **Autorización:** Debe presentar un certificado valido.

### `PUT /proveedores/<id>`
* **Descripción:** Actualiza la información de un proveedor.
* **Autorización:** Solo proveedores.

---

## 👤 Clientes (/clientes)

Rutas para gestionar los perfiles de los usuarios/clientes.

### `GET /clientes`
* **Descripción:** (Admin) Devuelve una lista de todos los clientes.
* **Autorización:** Solo Administradores.

### `GET /clientes/<id>`
* **Descripción:** Devuelve los detalles de un cliente específico.
* **Autorización:** Administradores o el propio usuario (self).

### `PUT /clientes/<id>`
* **Descripción:** Actualiza la información de un cliente (ej. preferencias, teléfono).
* **Autorización:** El propio usuario (self).

---

## 🗓️ Reservas (/reservas)

Rutas para gestionar las solicitudes de servicio.

### `POST /reservas`
* **Descripción:** Un cliente crea una nueva reserva para un servicio.
* **Autorización:** Requiere token de Cliente.
* **Body (JSON):** `{ "proveedor_id": 123, "servicio_id": 456, "fecha_hora": "..." }`

### `GET /mis-reservas`
* **Descripción:** Devuelve una lista de las reservas del usuario autenticado (sea este cliente o proveedor).
* **Autorización:** Requiere token (Cliente o Proveedor).

### `GET /reservas`
* **Descripción:** (Admin) Devuelve una lista de *todas* las reservas en el sistema.
* **Autorización:** Solo Administradores.

### `PUT /reservas/<id>`
* **Descripción:** Actualiza el estado de una reserva (ej. 'confirmada', 'completada', 'cancelada').
* **Autorización:** Administradores o el Proveedor asignado a la reserva.