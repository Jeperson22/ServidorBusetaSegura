from flask import Flask, request, jsonify

app = Flask(__name__)

# Estado global almacenado
ultimo_estado = {
    "estado_puertas": "",
    "lat": 0.0,
    "lon": 0.0
}

# Último evento de bomba
ultimo_evento = {
    "accion": "",
    "mensaje": ""
}

@app.route('/datos', methods=['POST', 'GET'])
def datos():
    global ultimo_estado, ultimo_evento
    if request.method == 'POST':
        data = request.get_json()
        if data:
            ultimo_estado = data
        return 'OK'
    else:  # GET
        # Definir estado basado en el último evento
        if ultimo_evento.get("accion") == "desactivar_bomba":
            estado_bomba = "BLOQUEADA"
        elif ultimo_evento.get("accion") == "activar_bomba":
            estado_bomba = "ACTIVADA"
        else:
            estado_bomba = "DESCONOCIDA"
        return jsonify({
            **ultimo_estado,
            "estado_bomba": estado_bomba,
            "evento_bomba": ultimo_evento
        })

@app.route('/desactivar_bomba', methods=['POST'])
def desactivar_bomba():
    global ultimo_evento
    data = request.get_json()
    print("Solicitud de DESACTIVAR BOMBA:", data)
    ultimo_evento = {
        "accion": "desactivar_bomba",
        "mensaje": "Recibido desde App2"
    }
    return jsonify({"status": "ok", "msg": "Bomba bloqueada"})

@app.route('/activar_bomba', methods=['POST'])
def activar_bomba():
    global ultimo_evento
    data = request.get_json()
    print("Solicitud de ACTIVAR BOMBA:", data)
    ultimo_evento = {
        "accion": "activar_bomba",
        "mensaje": "Recibido desde App2"
    }
    return jsonify({"status": "ok", "msg": "Bomba activada"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
