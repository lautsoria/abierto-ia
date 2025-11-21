from flask import Flask, render_template, request

app = Flask(__name__)

servicios = []

@app.route("/", methods=["GET", "POST"])
def agregar_servicio():
    if request.method == "POST":
        servicio = {
            "nombre": request.form["nombre"],
            "telefono": request.form["telefono"],
            "zona": request.form["zona"],
            "tipo": request.form["tipoServicio"],
            "descripcion": request.form["descripcion"],
            "precio": request.form["precio"]
        }

        servicios.append(servicio)

        return render_template("agregar_servicio.html",
                               mensaje=" Servicio publicado correctamente")

    return render_template("agregar_servicio.html")

@app.route("/servicios")
def ver_servicios():
    return {"servicios": servicios}

if __name__ == "__main__":
    app.run(debug=True)
