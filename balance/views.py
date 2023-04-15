from flask import jsonify, render_template, request, session
from flask_login import current_user

from . import app
from balance.models import *
from config import CAMPOS_TABLA, ENDPOINT, HEADERS, RUTA_PORTFOLIO


@app.route('/inicio')
def inicio():
    if 'nombre_usuario' in session:
        nombre_usuario = session['nombre_usuario']

    return render_template('prueba.html', user=current_user,
                           nombre_usuario=nombre_usuario)


@app.route('/comprar')
def compra():
    try:
        tabla = session['nombre_usuario']
        wallet = Cartera(RUTA_PORTFOLIO, tabla)
        cartera = wallet.obtenerCartera()

        resultado = {'status': 'success',
                     'message': 'Compra realizada con éxito'}
        status_code = 200

        return render_template('compra.html', cartera=cartera)

    except Exception as error:
        resultado = {
            "status": "error",
            "message": str(error)
        }
        status_code = 500

    return jsonify(resultado), status_code


@app.route('/status', methods=['GET', 'POST'])
def estado():
    if request.method == 'GET':
        return render_template('status.html')

    if request.method == 'POST':
        try:
            tabla = session['nombre_usuario']
            wallet = Cartera(RUTA_PORTFOLIO, tabla)
            cartera = wallet.obtenerCartera()

            invertido = cartera.get('EUR')
            valorTotalCartera = wallet.valor_actual_cartera() + invertido
            beneficio = round((valorTotalCartera - invertido)
                              * 100 / invertido, 2)

            resultado = {'status': 'success',
                         'message': 'Estado actualizado con éxito'}
            status_code = 200

            return jsonify({'invertido': invertido,
                            'valorTotalCartera': valorTotalCartera,
                            'beneficio': beneficio
                            })

        except Exception as error:
            resultado = {
                "status": "error",
                "message": str(error)
            }
            status_code = 500

        return jsonify(resultado), status_code
