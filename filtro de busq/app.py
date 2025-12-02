from models.servicio import Servicio
from app import db


@app.route("/buscar", methods=["GET"])
def buscar():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("buscar.html", servicios=[], query="")

    # Consulta SQL con ilike (insensible a mayúsculas)
    resultados = Servicio.query.filter(
        Servicio.nombre.ilike(f"%{query}%")
    ).all()

    return render_template("buscar.html", servicios=resultados, query=query)
