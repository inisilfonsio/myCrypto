from datetime import date, datetime
from passlib.hash import pbkdf2_sha256
import requests
import sqlite3

from config import CAMPOS_TABLA


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

    def guardarDatos(self, tabla, datos):
        campos = ', '.join(datos.keys())
        valores = ', '.join(['?'] * len(datos))
        consulta = f"INSERT INTO {tabla} ({campos}) VALUES ({valores})"
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute(consulta, list(datos.values()))
            conexion.commit()
            conexion.close()
            return True

        except Exception as ex:
            print("Error al guardar los datos: ", ex)
            return False

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

        self.activos = []
        nombres_columna = []
        for columna in cursor.description:
            nombres_columna.append(columna[0])

        for dato in datos:
            indice = 0
            activos = {}
            for nombre in nombres_columna:
                activos[nombre] = dato[indice]
                indice += 1

            self.activos.append(activos)

        # 5. Cerrar la conexión
        conexion.close()

        # 6. Devolver la colección de resultados
        return self.activos

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


class CriptoView:
    """
Modelo <==> Controlador <==> Vista

Modelo <////////> Vista  NUNCA hay comunicación entre Modelo y Vista

La vista interactúa con el usuario:
1. entrada de datos
2. muestra datos
TODO: Clase CriptoView
"""

    def pedir_monedas(self):
        origen = input('¿Qué moneda quieres cambiar? ')
        origen = origen.upper()
        destino = input('¿Qué moneda deseas obtener? ')
        destino = destino.upper()

        return (origen, destino)

    def mostrar_cambio(self, origen, destino, cambio):
        print(f'Un {origen} vale lo mismo que {cambio:,.2f} {destino}')

    def quieres_seguir(self):
        seguir = input('¿Quieres consultar de nuevo? (S/N) ')
        return seguir


class API:

    def __init__(self, api_url, endpoint, headers):
        self.api_url = api_url
        self.endpoint = endpoint
        self.headers = headers

    def consultar_api(self, origen, destino):
        url = f"{self.api_url}{self.endpoint}/{origen}/{destino}"
        response = requests.get(url, headers=self.headers)
        print(
            f"Has solicitado {response.headers.get('x-ratelimit-used')}/100 peticiones")

        if response.status_code == 200:
            exchange = response.json()
            print(response.json())
            return exchange
        else:
            raise APIError(f"Error {response.status_code}: {response.reason}")

    def errores_api(self):
        url = f"{self.api_url}{self.endpoint}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()["errors"]
        else:
            raise APIError(f"Error {response.status_code}: {response.reason}")


class APIError(Exception):
    """Clase de excepción personalizada para errores de la API"""

    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response

    def __str__(self):
        if self.status_code:
            return f"{self.message}. Código de estado: {self.status_code}."
        else:
            return self.message
