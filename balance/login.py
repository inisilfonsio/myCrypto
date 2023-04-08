from flask import jsonify, redirect, render_template, request, session, url_for
from passlib.hash import pbkdf2_sha256

from . import app
from balance.models import *
from config import RUTA_PORTFOLIO, TABLA_USERS


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        titulo = 'Iniciar Sesión'
        return render_template('auth/login.html', titulo=titulo)

    if request.method == 'POST':
        nombre_usuario = request.form.get('usuario')
        contrasena_usuario = request.form.get('contrasena')

        # Instanciamos usuario que recibo del formulario
        user = User(0, nombre_usuario, contrasena_usuario)

        gestor = DBManager(RUTA_PORTFOLIO)
        usuario_comp = gestor.comprobarUsuario(user)
        # usuario_comp puede ser una instancia de un usuario o un None

        try:
            if usuario_comp != None:
                if usuario_comp.contrasena:
                    session['nombre_usuario'] = nombre_usuario
                    session['autentificacion'] = True
                    resultado = {'status': 'success',
                                 'message': 'Inicio de sesión exitoso'}
                    status_code = 200

                    return redirect(url_for('inicio'))

                else:
                    resultado = {'status': 'error',
                                 'message': 'Contraseña incorrecta'}
                    status_code = 401
                    session['autentificacion'] = False
                    # TODO  mensaje flash "contraseña incorrecta"

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
        titulo = 'Crear cuenta'

        return render_template('auth/newuser.html', titulo=titulo)

    if request.method == 'POST':
        nombre_usuario = request.form.get('usuario')
        contrasena_usuario = request.form.get('contrasena')
        # TODO agregar nuevo usuario a tabla usuario

        gestor = DBManager(RUTA_PORTFOLIO)
        nuevo_usuario = gestor.crearTabla(nombre_usuario)

        contrasena_usuario_hash = pbkdf2_sha256.hash(contrasena_usuario)
        tabla = TABLA_USERS
        datos = {'usuario': nombre_usuario,
                 'contrasena': contrasena_usuario_hash}
        agregar_usuario = gestor.guardarDatos(tabla, datos)

        session['nombre_usuario'] = nombre_usuario
        resultado = {'status': 'success',
                     'message': 'Inicio de sesión exitoso'}
        status_code = 200
        return redirect(url_for('inicio'))

    return jsonify(resultado), status_code


@app.route('/logout')
def logout():
    session.pop('nombre_usuario', None)
    return redirect(url_for('login'))
