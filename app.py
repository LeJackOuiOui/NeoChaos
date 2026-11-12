from flask import Flask, jsonify, request
import time
import random
from tareas import procesar_descuento, celery_app

app = Flask(__name__)


@app.route("/aplicar-descuento", methods=["POST"])
def aplicar_descuento():
    datos = request.json
    usuario_id = datos.get("usuario_id", "000")
    tarea = procesar_descuento.delay(usuario_id)

    return (
        jsonify(
            {
                "status": "Procesamdo la solicitud en segundo plano...",
                "task_id": tarea.id,
            }
        ),
        202,
    )


@app.route("/estado-descuento/<task_id>", methods=["GET"])
def verificar_estado(task_id):
    tarea = celery_app.AsyncResult(task_id)
    if tarea.state == "PENDING":
        return jsonify({"status": "Aún en la cola de tickets"}), 200
    elif tarea.state == "SUCCESS":
        return jsonify({"status": "Completado", "resultado": tarea.result}), 200
    else:
        return jsonify({"status": "Falló"}), 500


@app.route("/health")
def health():
    return "OK", 200


@app.route("/comprar", methods=["POST"])
def comprar():
    time.sleep(0.2)
    return "Compra realizada con éxito", 200


@app.route("/error_aleatorio")
def error_aleatorio():
    if random.randint(1, 5) == 1:
        raise RuntimeError("Fallo de conexión simulado")
    return "OK", 200


@app.route("/memoria_ram")
def fuga_ram():
    data = []
    for _ in range(1000000):
        data.append("X" * 1000)
    return "Procesado", 200


@app.route("/version")
def version():
    return {
        "version": "1.0.0",
        "mensaje": "API v1 Operativa",
    }, 200


if __name__ == "__main__":
    app.run(port=5000)
