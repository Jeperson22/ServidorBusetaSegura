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
    global ultimo_estado
    if request.method == 'POST':
        data = request.get_json()
        # Espera que la app mande {"estado_puertas": "...", "lat": ..., "lon": ...}
        if data:
            ultimo_estado = data
        return 'OK'
    else:  # GET
        return jsonify(ultimo_estado)

@app.route('/desactivar_bomba', methods=['POST'])
def desactivar_bomba():
    global ultimo_evento
    data = request.get_json()
    print("Solicitud de DESACTIVAR BOMBA:", data)
    ultimo_evento = {
        "accion": "desactivar_bomba",
        "mensaje": "Recibido desde App2"
    }
    # Aquí puedes poner tu lógica para desactivar la bomba, enviar señal, etc.
    return jsonify({"status": "ok", "msg": "Bomba desactivada"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

