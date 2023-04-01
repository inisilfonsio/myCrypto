from datetime import date
from passlib.hash import pbkdf2_sha256
import requests
import sqlite3

from config import API_URL, CAMPOS_TABLA, ENDPOINT, HEADERS


class User:

    def __init__(self, id, nombre, contrasena):
        self.id = id
        self.nombre = nombre
        self.contrasena = contrasena

    def verificarContrasena(self, contrasena, contrasena_encriptada):
        verificacion = pbkdf2_sha256.verify(
            contrasena, contrasena_encriptada)

        return verificacion


class DBManager:
    """
    Clase para interactuar con la base de datos SQLite
    """
    CAMPOS = '''id INTEGER PRIMARY KEY NOT NULL UNIQUE, 
                fecha TEXT NO NULL, 
                hora TEXT NOT NULL,
                origen TEXT NOT NULL,
                invertido NUMERIC NOT NULL,
                destino TEXT NOT NULL,
                obtenido NUMERIC NOT NULL,
                unitario NUMERIC NOT NULL'''

    def __init__(self, ruta):
        self.ruta = ruta

    def comprobarUsuario(self, user):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        peticion = f"SELECT * FROM usuarios WHERE usuario = '{user.nombre}'"

        cursor.execute(peticion)
        result = cursor.fetchone()

        if result != None:
            contrasena_encriptada = result[2]
            contrasena = user.contrasena
            verificacion = User.verificarContrasena(
                0, contrasena, contrasena_encriptada)
            usuario = User(result[0], result[1], verificacion)
            return usuario

        else:
            return None

    def crearTabla(self, usuario):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        peticion = f'''CREATE TABLE {usuario} ({self.CAMPOS})'''
        cursor.execute(peticion)
        conexion.commit()
        conexion.close()

    def consultaSQL(self, consulta):
        # 1. Conectar a la base de datos
        conexion = sqlite3.connect(self.ruta)

        # 2. Abrir un cursor
        cursor = conexion.cursor()

        # 3. Ejecutar la consulta SQL sobre ese cursor
        cursor.execute(consulta)

        # 4. Tratar los datos
        # 4.1 obtener los datos
        datos = cursor.fetchall()

        self.activoss = []
        nombres_columna = []
        for columna in cursor.description:
            nombres_columna.append(columna[0])

        for dato in datos:
            indice = 0
            activos = {}
            for nombre in nombres_columna:
                activos[nombre] = dato[indice]
                indice += 1

            self.activoss.append(activos)

        # 5. Cerrar la conexión
        conexion.close()

        # 6. Devolver la colección de resultados
        return self.activoss

    def obtenerActivo(self, usuario, id):
        """
        Obtiene un activo a partir de su ID de la base de datos
        """
        consulta = f'SELECT {CAMPOS_TABLA} FROM {usuario} WHERE id=?'
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta, (id,))

        datos = cursor.fetchone()
        resultado = None

        if datos:
            nombres_columna = []
            for column in cursor.description:
                nombres_columna.append(column[0])

            activos = {}
            indice = 0
            for nombre in nombres_columna:
                activos[nombre] = datos[indice]
                indice += 1

            print(f'Fecha ANTES: {activos["fecha"]}')
            activos['fecha'] = date.fromisoformat(activos['fecha'])
            print(f'DESPUÉS:  {activos["fecha"]}')

            resultado = activos

        conexion.close()
        return resultado


class APIError(Exception):
    pass


class CriptoModel:
    '''
    Obtiene una consulta sobre el valor de cambio entre dos activos
    '''

    origen = ''
    destino = ''

    def __init__(self):
        self.cambio = 0.0

    def consultar_cambio(self):
        url = f'{API_URL}{ENDPOINT}/{self.origen}/{self.destino}'
        response = requests.get(url, headers=HEADERS)
        print(
            f"Has solicitado {response.headers.get('x-ratelimit-used')}/100 peticiones")

        if response.status_code == 200:
            exchange = response.json()
            self.cambio = exchange.get("rate")
        else:
            raise APIError(
                f'Error {response.status_code} {response.reason} al consultar la API'
            )
