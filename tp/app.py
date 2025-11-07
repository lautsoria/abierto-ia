from flask import Flask, render_template, abort

app = Flask(__name__)

# Lista de servicios
servicios = [
    {'id': 'electricista', 'nombre': 'Electricista'},
    {'id': 'plomeria', 'nombre': 'Plomería'},
    {'id': 'pintura', 'nombre': 'Pintura'},
    {'id': 'carpinteria', 'nombre': 'Carpintería'},
    {'id': 'cerrajeria', 'nombre': 'Cerrajería'},
    {'id': 'limpieza', 'nombre': 'Limpieza'},
    {'id': 'aire-acondicionado', 'nombre': 'Aire Acondicionado'},
    {'id': 'jardineria', 'nombre': 'Jardinería'}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services-general')
def services_general():
    return render_template('services-general.html', servicios=servicios)

# Ruta dinámica para cualquier servicio
@app.route('/service/<servicio_id>')
def mostrar_servicio(servicio_id):
    # Buscamos el servicio en la lista
    servicio = next((s for s in servicios if s['id'] == servicio_id), None)
    if servicio:
        return render_template('service_detail.html', servicio=servicio)
    else:
        abort(404)

@app.route('/clientes')
def clientes():
    return "<h1>Página de clientes</h1><p>Aquí iría el contenido para quienes buscan profesionales.</p>"

@app.route('/profesionales')
def profesionales():
    return "<h1>Página de profesionales</h1><p>Aquí iría el contenido para quienes ofrecen servicios.</p>"


if __name__ == '__main__':
    app.run(debug=True)


