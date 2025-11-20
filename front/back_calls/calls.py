import requests
import logging
BACKEND_URL = 'http://localhost:5500'

def obtener_cantidad_categoria(nombre):
    try:
        response = requests.get(f'{BACKEND_URL}/categoria/{nombre}')
        
        if response.status_code == 200:
            data = response.json()
            # la API retorna: { "categoria": "...", "total_profesionales": N }
            return data.get("total_profesionales", 0)
        return 0

    except Exception as e:
        print("Error al obtener cantidad categoria:", e)
        return 0

def obtener_servicios_destacados():
    """Obtiene servicios destacados desde el backend"""
    logging.info('Obteniendo servicios destacados')
    try:
        response = requests.get(  
            f'{BACKEND_URL}/servicios/top-rating',
            timeout=1
        )
        
        if response.status_code == 200:
            servicios = response.json()
            return servicios
        else:
            print(f" Error del backend: {response.status_code}")
            return []
            
    except requests.exceptions.Timeout:  
        print("Timeout: El backend tardó más de 5 segundos")
        return []
        
    except requests.exceptions.ConnectionError:  
        print(" Error: No se pudo conectar al backend en puerto 5500")
        print("¿Está corriendo el backend? Ejecuta: python backend/app.py")
        return []
        
    except requests.exceptions.RequestException as e:  
        print(f" Error al obtener servicios: {e}")
        return []

def obtener_proveedores(filtro_servicio=None):
    """Obtiene proveedores desde el backend"""
    try:
        url = f'{BACKEND_URL}/proveedores'
        if filtro_servicio:
            url += f'?servicio={filtro_servicio}'
        
        response = requests.get(url, timeout=5)  
        
        if response.status_code == 200:
            return response.json()
        return []
        
    except requests.exceptions.RequestException as e:  
        print(f"Error al obtener proveedores: {e}")
        return []

def obtener_proveedor_detalle(proveedor_id):
    """Obtiene detalles de un proveedor específico"""
    try:
        response = requests.get(  
            f'{BACKEND_URL}/proveedores/{proveedor_id}',
            timeout=1
        )
        
        if response.status_code == 200:
            return response.json()
        return None
        
    except requests.exceptions.RequestException as e:  
        print(f"Error al obtener proveedor: {e}")
        return None

def obtener_categorias():
    try:
        response = requests.get(  
            f'{BACKEND_URL}/categoria',
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        return None
        
    except requests.exceptions.RequestException as e:  
        print(f"Error al obtener categorias: {e}")
        return None

def registrar_usuario(user, email, password, provider):
    """Registra un nuevo usuario en el backend"""
    try:
        response = requests.post(
            f'{BACKEND_URL}/auth/register',
            json={
                'user': user,
                'email': email,
                'password': password,
                'provider': provider
            },
            timeout=5
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error al registrar usuario: {e}")
        return None

def login_usuario(credential, password):
    """Inicia sesión de un usuario en el backend"""
    try:
        response = requests.post(
            f'{BACKEND_URL}/auth/login',
            json={
                'credential': credential,
                'password': password
            },
            timeout=5
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error al iniciar sesión: {e}")
        return None

def obtener_servicios_por_categoria(nombre, ubicacion=None):
    """Obtiene servicios filtrados por categoría y opcionalmente por ubicación"""
    try:
        params = {}
        if ubicacion:
            params['ubicacion'] = ubicacion

        response = requests.get(
            f'{BACKEND_URL}/servicios/{nombre}',
            params=params,
            timeout=2
        )
        
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener servicios por categoría: {e}")
        return []

def obtener_ubicaciones():
    """Obtiene todas las ubicaciones disponibles"""
    try:
        response = requests.get(
            f'{BACKEND_URL}/ubicacion',
            timeout=2
        )
        
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener ubicaciones: {e}")
        return []

def obtener_servicio_por_id(id, horarios=False):
    """Obtiene los detalles de un servicio específico por ID"""
    try:
        response = requests.get(
            f'{BACKEND_URL}/servicios/id/{id}',
            timeout=2
        )
        
        if response.status_code == 200:
            servicio = response.json()
            
            if horarios:
                horarios_list = []
                hora_inicio = servicio.get('hora_inicio')
                hora_fin = servicio.get('hora_fin')
                duracion = servicio.get('duracion')

                if hora_inicio and hora_fin and duracion:
                    # no tiene en cuenta la hora de inicio, pero sera agregada a horarios
                    cant_turnos = ((hora_fin - duracion) - hora_inicio) / duracion + 1
                    # esta formula agrega 1h de transporte y descanso a la duracion del servicio, y calcula el ultimo
                    # turno para que el trabajador pueda terminar a tiempo su jornada laboral
                    # claramente esto funciona en un mundo utopico 
                    i = hora_inicio
                    while i <= (hora_fin - duracion):
                        horarios_list.append(f"{int(i):02d}:00")
                        i = i + duracion
                    
                    servicio['horarios'] = horarios_list
            
            return servicio

        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener servicio por ID: {e}")
        return None
    

def no_disponibles(id):
    """Obtiene las fechas no disponibles para un servicio"""
    try:
        response = requests.get(
            f'{BACKEND_URL}/reservas/servicio/{id}',
            timeout=2
        )
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener servicios por categoría: {e}")
        return []
    

def reservar(user_id, servicio_id, fecha, horario, direccion, mensaje):
    try:
        response = requests.post(
            f'{BACKEND_URL}/reservas',
            timeout=2,
            json={
                'usuario_id': user_id,
                'servicio_id': servicio_id,
                'fecha_servicio': fecha,
                'hora_servicio': horario,
                'direccion': direccion,
                'comentarios_cliente': mensaje
            }
        )
        return response
    except Exception as e:
        print(e)
        return None

def obtener_reserva_por_id(id):
    try:
        response = requests.get(
            f'{BACKEND_URL}/reservas/{id}',
            timeout=2
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(e)
        return None            