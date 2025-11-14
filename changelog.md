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