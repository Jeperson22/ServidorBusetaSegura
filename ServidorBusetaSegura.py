from flask import Flask, request, jsonify
from flask_cors import CORS
import os, time

app = Flask(__name__)
CORS(app)  # si tu app web consume desde navegador

# (Para producción real, usa Redis/DB. Aquí RAM del proceso)
ultimo_estado = {"estado_puertas":"", "lat":0.0, "lon":0.0, "ts":0}
ultimo_evento = {"accion":"", "mensaje":"", "ts":0}

def now(): return int(time.time())

@app.route("/health")
def health(): return "OK", 200

# La buseta (ESP32) manda estado
@app.route("/datos", methods=["POST","GET"])
def datos():
    global ultimo_estado, ultimo_evento
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        data["ts"] = now()
        ultimo_estado = data
        return "OK"
    else:  # GET para que la app lea
        estado_bomba = (
            "ACTIVADA" if ultimo_evento.get("accion")=="activar_bomba"
            else "DESACTIVADA" if ultimo_evento.get("accion")=="desactivar_bomba"
            else "DESCONOCIDA"
        )
        return jsonify({**ultimo_estado, "estado_bomba":estado_bomba})

# La app publica un comando
@app.route("/activar_bomba", methods=["POST"])
def activar_bomba():
    global ultimo_evento
    payload = request.get_json(silent=True) or {}
    ultimo_evento = {"accion":"activar_bomba", "mensaje":payload.get("msg",""), "ts":now()}
    return jsonify({"status":"ok"})

@app.route("/desactivar_bomba", methods=["POST"])
def desactivar_bomba():
    global ultimo_evento
    payload = request.get_json(silent=True) or {}
    ultimo_evento = {"accion":"desactivar_bomba", "mensaje":payload.get("msg",""), "ts":now()}
    return jsonify({"status":"ok"})

# El módulo consulta el último comando (pull)
@app.route("/evento", methods=["GET"])
def evento():
    return jsonify(ultimo_evento)

# Render usa gunicorn; no arranques app.run en producción
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
