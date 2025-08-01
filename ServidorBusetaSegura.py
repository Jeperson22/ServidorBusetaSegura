from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable global para almacenar último estado
ultimo_estado = {
    "estado_puertas": "",
    "lat": 0.0,
    "lon": 0.0
}

# Nuevo: variable para eventos de desactivar bomba
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
        estado_bomba = "BLOQUEADA" if ultimo_evento.get("accion") == "desactivar_bomba" else "ACTIVA"
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
    return jsonify({"status": "ok", "msg": "Bomba desactivada"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
