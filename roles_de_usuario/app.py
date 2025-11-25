from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

usuarios = []
servicios = []

@app.route("/", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = {
            "nombre": request.form["nombre"],
            "email": request.form["email"],
            "rol": request.form["rol"],
            "telefono": "",
            "zona": "",
            "rubro": ""
        }

        usuarios.append(usuario)

        session["usuario_actual"] = usuario

        if usuario["rol"] == "proveedor":
            return redirect("/completar-datos")
        else:
            return redirect("/editar-perfil")

    return render_template("registro.html")


@app.route("/completar-datos", methods=["GET", "POST"])
def completar_datos():
    usuario = session.get("usuario_actual")

    if usuario["rol"] != "proveedor":
        return redirect("/")

    if request.method == "POST":
        usuario["telefono"] = request.form["telefono"]
        usuario["zona"] = request.form["zona"]
        usuario["rubro"] = request.form["rubro"]

        return redirect("/editar-perfil")

    return render_template("completar_datos.html")


@app.route("/agregar-servicio", methods=["GET", "POST"])
def agregar_servicio():
    usuario = session.get("usuario_actual")

    if usuario["rol"] != "proveedor":
        return redirect("/")

    if request.method == "POST":
        servicio = {
            "titulo": request.form["titulo"],
            "descripcion": request.form["descripcion"],
            "precio": request.form["precio"],
            "proveedor": usuario["nombre"]
        }

        servicios.append(servicio)
        return redirect("/panel")

    return render_template("agregar_servicio.html")


@app.route("/editar-perfil", methods=["GET", "POST"])
def editar_perfil():
    usuario = session.get("usuario_actual")

    if request.method == "POST":
        usuario["nombre"] = request.form["nombre"]
        usuario["email"] = request.form["email"]

        if usuario["rol"] == "proveedor":
            usuario["telefono"] = request.form["telefono"]
            usuario["zona"] = request.form["zona"]
            usuario["rubro"] = request.form["rubro"]

        return redirect("/panel")

    if usuario["rol"] == "proveedor":
        return render_template("editar_proveedor.html", usuario=usuario)
    else:
        return render_template("editar_usuario.html", usuario=usuario)


@app.route("/panel")
def panel():
    usuario = session.get("usuario_actual")
    return render_template("panel.html", usuario=usuario, servicios=servicios)


if __name__ == "__main__":
    app.run(debug=True)

