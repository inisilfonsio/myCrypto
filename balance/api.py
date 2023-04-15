from flask import jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user

from . import app
from balance.models import *
from config import API_URL, ENDPOINT, HEADERS, RUTA_PORTFOLIO, CAMPOS_TABLA


@app.route('/api/v1/consultar-cambio', methods=['POST'])
def consultaCrypto():
    origen = request.form.get('origen')
    destino = request.form.get('destino')

    invertido = request.form.get('invertido')
    resultado = True if invertido and invertido != '' else False

    try:
        invertido_float = abs(float(invertido))

        if resultado:
            # Realizamos consulta a la API
            cripto = API(API_URL, ENDPOINT, HEADERS)
            consulta_json = cripto.consultar_api(origen, destino)
            cambio = consulta_json.get('rate')
            cambio_float = float(cambio)
            unitario = 1/cambio_float

            # Verificamos si tenemos fondos suficientes
            tabla = session['nombre_usuario']
            wallet = Cartera(RUTA_PORTFOLIO, tabla)
            cartera = wallet.obtenerCartera()
            tienes_fondos = wallet.verificarFondos(origen, invertido_float)

            obtenido = (invertido_float * cambio_float)

    except (TypeError, ValueError, UnboundLocalError):
        resultado = False

    return jsonify({'obtenido': obtenido, 'unitario': unitario, 'tienes_fondos': tienes_fondos, 'resultado': resultado})


@app.route('/api/v1/guardar-cambio', methods=['POST'])
def guardarCrypto():
    tabla = session['nombre_usuario']
    datos = request.get_json()
    print(datos)

    gestor = DBManager(RUTA_PORTFOLIO)
    operacion = gestor.guardarDatos(tabla, datos)

    return jsonify({'success': operacion})


@app.route('/api/v1/movimientos')
def obtener_movimientos():
    try:
        try:
            page = int(request.args.get('p', DEFAULT_PAG))
        except:
            page = DEFAULT_PAG

        try:
            per_page = int(request.args.get('r', PAG_SIZE))
        except:
            per_page = PAG_SIZE

        nombre_usuario = session['nombre_usuario']
        gestor = DBManager(RUTA_PORTFOLIO)
        consulta = f'SELECT {CAMPOS_TABLA} FROM "{nombre_usuario}"'
        movimientos = gestor.consultaSQL(
            consulta, page, per_page)

        consultaTotal = f'SELECT COUNT(*) FROM "{nombre_usuario}"'
        movTotal = gestor.consultaSQL(consultaTotal)
        total = movTotal[0].get('COUNT(*)')

        if len(movimientos) > 0:
            resultado = {
                'status': 'success',
                'results': movimientos,
                'total': total
            }
            status_code = 200
        else:
            resultado = {
                'status': 'error',
                'message': f'No hay movimientos en el sistema'
            }
            status_code = 404

    except Exception as error:
        resultado = {
            "status": "error",
            "message": str(error)
        }
        status_code = 500

    return jsonify(resultado), status_code
