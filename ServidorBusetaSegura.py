from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable global para almacenar último estado
ultimo_estado = {
    "estado_puertas": "",
    "lat": 0.0,
    "lon": 0.0
}

# Variable para almacenar el último evento (por ejemplo: bloquear bomba)
ultimo_evento = {
    "accion": "",
    "mensaje": ""
}

@app.route('/datos', methods=['POST', 'GET'])
def datos():
    global ultimo_estado
    if request.method == 'POST':
        data = request.get_json()
        # Espera que la app mande {"estado_puertas": "...", "lat": ..., "lon": ...}
        if data:
            ultimo_estado = data
        return 'OK'
    else:  # GET
        return jsonify(ultimo_estado)

@app.route('/bloquear_bomba', methods=['POST'])
def bloquear_bomba():
    global ultimo_evento
    data = request.get_json()
    print("Solicitud de BLOQUEAR BOMBA:", data)
    ultimo_evento = {
        "accion": "bloquear_bomba",
        "mensaje": "Recibido desde App2"
    }
    return jsonify({"status": "ok", "msg": "Bomba bloqueada"})

@app.route('/evento', methods=['GET', 'POST'])
def evento():
    global ultimo_evento
    if request.method == 'GET':
        evento = ultimo_evento.copy()
        ultimo_evento = {"accion": "", "mensaje": ""}
        return jsonify(evento)
    else:
        ultimo_evento = {"accion": "", "mensaje": ""}
        return jsonify({"status": "reseteado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
