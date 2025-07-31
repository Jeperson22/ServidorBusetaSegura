from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable global para almacenar último estado
ultimo_estado = {
    "estado_puertas": "",
    "lat": 0.0,
    "lon": 0.0
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
