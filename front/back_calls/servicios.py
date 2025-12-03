import requests
import logging

BACKEND_URL = 'http://localhost:5500/api'

def obtener_servicios_por_categoria(nombre, ubicacion=None, ordenar=None, precio_min=None, precio_max=None):
    """Obtiene servicios por categoría con filtros y ordenamiento """
    try:
        params = {}
        if ubicacion:
            params['ubicacion'] = ubicacion
        if ordenar:
            params['ordenar'] = ordenar
        if precio_min:
            params['precio_min'] = precio_min
        if precio_max:
            params['precio_max'] = precio_max

        print(params)

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

def obtener_servicios_proveedor(proveedor_id):
    """Obtiene todos los servicios de un proveedor"""
    try:
        response = requests.get(
            f'{BACKEND_URL}/servicios/proveedor/{proveedor_id}',
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener servicios del proveedor: {e}")
        return []

def obtener_resenas_servicio(id):
    try:
        response = requests.get(
            f'{BACKEND_URL}/resenas/{id}',
            timeout=2
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(e)
        return None  
    