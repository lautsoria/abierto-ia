from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    if request.method == 'POST':
        descripcion = request.form.get('descripcion')
        ubicacion = request.form.get('ubicacion')
        telefono = request.form.get('telefono')

        print(f"Datos recibidos: Descripción={descripcion}, Ubicación={ubicacion}, Teléfono={telefono}")

        return redirect(url_for('home'))

    return render_template('proveedores.html')


@app.route('/complete-profile', methods=['GET', 'POST'])
def complete_profile():
    if request.method == 'POST':
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')

        print(f"Perfil completado: Categoría={categoria}, Descripción={descripcion}")

        return redirect(url_for('home'))

    return render_template('complete_profile.html')

if __name__ == '__main__':
    app.run(debug=True)
