from flask import flash, jsonify, redirect, render_template, request, session, url_for
from passlib.hash import pbkdf2_sha256

from . import app
from balance.models import *
from config import CAMPOS_TABLA, RUTA_PORTFOLIO


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        titulo = 'Iniciar Sesión'
        return render_template('auth/login.html', titulo=titulo)

    if request.method == 'POST':
        nombre_usuario = request.form['usuario']
        contrasena_usuario = request.form['contrasena']

        # Instanciamos usuario que recibo del formulario
        user = User(0, nombre_usuario, contrasena_usuario)

        gestor = DBManager(RUTA_PORTFOLIO)
        usuario_comp = gestor.comprobarUsuario(user)
        # usuario_comp puede ser una instancia de un usuario o un None

        try:
            if usuario_comp != None:
                if usuario_comp.contrasena:
                    session['nombre_usuario'] = nombre_usuario
                    resultado = {'status': 'success',
                                 'message': 'Inicio de sesión exitoso'}
                    status_code = 200
                    return redirect(url_for('inicio'))
                else:
                    flash('Contraseña Incorrecta')
                    resultado = {'status': 'error',
                                 'message': 'Contraseña incorrecta'}
                    status_code = 401
                    # TODO poner mensaje flash
                    return redirect(url_for('home'))

            else:
                resultado = {'status': 'error',
                             'message': 'Usuario no encontrado'}
                status_code = 404

        except Exception as error:
            resultado = {
                "status": "error",
                "message": str(error)
            }
            status_code = 500

        return jsonify(resultado), status_code


@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():

    if request.method == 'GET':
        titulo = 'Crear cuenta nueva'

        return render_template('auth/login.html', titulo=titulo)

    if request.method == 'POST':
        nombre_usuario = request.form['usuario']
        contrasena_usuario = request.form['contrasena']

        gestor = DBManager(RUTA_PORTFOLIO)
        nuevo_usuario = gestor.crearTabla(nombre_usuario)
        session['nombre_usuario'] = nombre_usuario
        resultado = {'status': 'success',
                     'message': 'Inicio de sesión exitoso'}
        status_code = 200
        return redirect(url_for('inicio'))

    return jsonify(resultado), status_code


@app.route('/inicio')
def inicio():
    if 'nombre_usuario' in session:
        nombre_usuario = session['nombre_usuario']

        gestor = DBManager(RUTA_PORTFOLIO)
        # TODO la tabla se debe llamar como el usuario
        consulta = f'SELECT {CAMPOS_TABLA} FROM "{nombre_usuario}"'
        movimientos = gestor.consultaSQL(consulta)

    return render_template('index.html', nombre_usuario=nombre_usuario, movs=movimientos)


@app.route('/comprar')
def compra():
    return render_template('compra.html')


@app.route('/status')
def estado():
    return 'Aquí se comprueba el estado actual de la inversión'
