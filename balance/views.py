from flask import render_template
from . import app
from balance.models import *
from config import RUTA


@app.route('/')
def inicio():

    gestor = DBManager(RUTA)
    consulta = 'SELECT id, fecha, hora, origen, invertido, destino, obtenido, unitario FROM movimientos'
    movimientos = gestor.consultaSQL(consulta)

    return render_template('index.html', movs=movimientos)


@app.route('/comprar')
def compra():
    return 'Aquí se compran activos'


@app.route('/status')
def estado():
    return 'Aquí se comprueba el estado actual de la inversión'
