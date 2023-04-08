from flask import jsonify, request, session

from . import app
from balance.models import *
from config import API_URL, ENDPOINT, HEADERS, RUTA_PORTFOLIO


@app.route('/api/v1/consultar-cambio', methods=['POST'])
def consultaCrypto():
    origen = request.form.get('origen')
    destino = request.form.get('destino')

    invertido = request.form.get('invertido')
    invertido_float = float(invertido)

    cripto = API(API_URL, ENDPOINT, HEADERS)
    json = cripto.consultar_api(origen, destino)

    cambio = json.get('rate')
    cambio_float = float(cambio)

    obtenido = (invertido_float * cambio_float)
    unitario = 1/cambio_float

    return jsonify({'obtenido': obtenido, 'unitario': unitario})


@app.route('/api/v1/guardar-cambio', methods=['POST'])
def guardarCrypto():
    tabla = session['nombre_usuario']
    datos = request.get_json()

    gestor = DBManager(RUTA_PORTFOLIO)
    operacion = gestor.guardarDatos(tabla, datos)

    return jsonify({'success': operacion})
