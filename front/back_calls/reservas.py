import requests
import qrcode

BACKEND_URL = 'https://abiertoia.pythonanywhere.com/api'

def obtener_mis_reservas(usuario_id):
    try:
        if not usuario_id:
            print("Usuario no autenticado")
            return []

        response = requests.get(
            f"{BACKEND_URL}/reservas",
            json={"usuario_id": usuario_id},
            timeout=5
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error backend: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        print(f"Error al obtener reservas: {e}")
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

def generar_qr(id_reserva, token):
    url = f"http://localhost:5000/reservas/confirmar-servicio/{id_reserva}/{token}"
    qr = qrcode.make(url)
    qr.save(f"static/qr_reserva_{id_reserva}.png")
    return f"static/qr_reserva_{id_reserva}.png"
