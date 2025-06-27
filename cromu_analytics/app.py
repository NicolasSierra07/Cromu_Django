from flask import Flask, request, jsonify
from analysis.stats import analizar_datos

app = Flask(__name__)

@app.route('/analizar/ahorros', methods=['POST'])
def analizar_ahorros():
    data = request.json
    resultado = analizar_datos(data)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
