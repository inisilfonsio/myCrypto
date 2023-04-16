from passlib.hash import pbkdf2_sha256
import requests
import sqlite3

from config import API_URL, CRIPTOS_DISPONIBLES, DEFAULT_PAG, ENDPOINT, HEADERS, PAG_SIZE


class User:

    def __init__(self, id, nombre, contrasena):
        self.id = id
        self.nombre = nombre
        self.contrasena = contrasena

    def verificarContrasena(self, contrasena, contrasena_encriptada):
        verificacion = pbkdf2_sha256.verify(
            contrasena, contrasena_encriptada)

        return verificacion


class Cartera:
    def __init__(self, ruta, nombre_tabla):
        self.ruta = ruta
        self.tabla = nombre_tabla

    def obtenerCartera(self):
        # Inicializamos el diccionario con las diez cryptos y su cantidad en cero
        cryptos = CRIPTOS_DISPONIBLES
        self.cartera = {crypto: 0.00000 for crypto in cryptos}

        peticion = f"SELECT origen, invertido, destino, obtenido FROM {self.tabla}"
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute(peticion)

            for fila in cursor.fetchall():
                origen, invertido, destino, obtenido = fila
                self.cartera[destino] += round(obtenido, 5)

                self.cartera[origen] -= round(invertido, 5)

            conexion.close()

        except sqlite3.Error as ex:
            print(f"Error al acceder a la base de datos: {ex}")

        return self.cartera

    def saldoInvEUR(self, moneda='EUR'):
        peticion = f"SELECT origen, destino, invertido, obtenido FROM {self.tabla}"
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute(peticion)

            saldo = 0
            for fila in cursor.fetchall():
                origen, invertido, destino, obtenido = fila
                if destino == moneda:
                    saldo += obtenido
                if origen == moneda:
                    saldo -= invertido

            saldo_float = float(saldo)

            conexion.close()

            return round(saldo_float, 5)

        except sqlite3.Error as ex:
            print(f"Error al acceder a la base de datos: {ex}")

    def total_euros_invertidos(self,  moneda='EUR'):
        peticion = f"SELECT invertido FROM {self.tabla} WHERE origen=?"
        try:
            conexion = sqlite3.connect(self.ruta)
            cursor = conexion.cursor()
            cursor.execute(peticion, (moneda,))

            fila = cursor.fetchone()
            if fila is not None:
                total = fila[0]
                total_float = round(float(total), 5)
            else:
                total_float = 0.0

            conexion.close()

            return total_float

        except Exception as ex:
            print(f"Error en total_euros_invertidos: {str(ex)}")
            return 0.0

    def valor_actual_cartera(self, moneda='EUR'):
        if not self.cartera:
            self.obtenerCartera('movimientos')

        total_euros_criptos = 0
        for crypto in self.cartera:
            if crypto == 'EUR':
                continue

            numeroCryptos = self.cartera.get(crypto)
            if numeroCryptos > 0:
                api = API(API_URL, ENDPOINT, HEADERS)
                consulta = api.consultar_api(crypto)
                rate = consulta.get('rate')
                rate_float = float(rate)
                total_euros_criptos += round(self.cartera.get(crypto)
                                             * rate_float, 5)
                valorTotalCartera = round(
                    self.total_euros_invertidos() + total_euros_criptos, 5)

        return valorTotalCartera

    def verificarFondos(self, moneda, invertido):
        fondos_crypto = self.cartera.get(moneda)

        if invertido == '' or invertido == 0:
            return False

        if moneda == 'EUR':
            return True

        return invertido <= fondos_crypto


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

    def consultaSQL(self, consulta, page=DEFAULT_PAG, per_page=PAG_SIZE):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        # Calcular el número de elementos para saltar (OFFSET)
        offset = (page - 1) * per_page

        # Agregar la cláusula LIMIT y OFFSET a la consulta SQL
        consulta_paginada = consulta + " LIMIT ? OFFSET ?"
        parametros = (per_page, offset)

        cursor.execute(consulta_paginada, parametros)
        datos = cursor.fetchall()

        activos = []
        nombres_columna = []
        for columna in cursor.description:
            nombres_columna.append(columna[0])

        for dato in datos:
            indice = 0
            activo = {}
            for nombre in nombres_columna:
                activo[nombre] = dato[indice]
                indice += 1

            activos.append(activo)

        conexion.close()

        return activos


class API:

    def __init__(self, api_url, endpoint, headers):
        self.api_url = api_url
        self.endpoint = endpoint
        self.headers = headers

    def consultar_api(self, origen, destino='EUR', url=True):
        if url:
            url = f"{self.api_url}{self.endpoint}/{origen}/{destino}"
        else:
            url = f"{self.api_url}{self.endpoint}/{origen}?invert=false"
            # TODO Creo que no se puede solicitar con una APIKEY gratuita

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
    """
    Clase de excepción personalizada para errores de la API
    """

    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response

    def __str__(self):
        if self.status_code:
            return f"{self.message}. Código de estado: {self.status_code}."
        else:
            return self.message
