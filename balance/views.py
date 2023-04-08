from flask import jsonify, render_template, session
from flask_login import current_user

from . import app
from balance.models import *
from config import CAMPOS_TABLA, RUTA_PORTFOLIO, CRIPTOS_DISPONIBLES


@app.route('/inicio')
def inicio():
    try:
        if 'nombre_usuario' in session:
            nombre_usuario = session['nombre_usuario']

            gestor = DBManager(RUTA_PORTFOLIO)
            consulta = f'SELECT {CAMPOS_TABLA} FROM "{nombre_usuario}"'
            movimientos = gestor.consultaSQL(consulta)

        return render_template('index.html', user=current_user,
                               nombre_usuario=nombre_usuario, movs=movimientos)

    except Exception as error:
        resultado = {
            "status": "error",
            "message": str(error)
        }
        status_code = 500

    return jsonify(resultado), status_code


@app.route('/comprar')
def compra():
    return render_template('compra.html', lista_cryptos=CRIPTOS_DISPONIBLES)


@app.route('/status')
def estado():
    return 'Aquí se comprueba el estado actual de la inversión'
