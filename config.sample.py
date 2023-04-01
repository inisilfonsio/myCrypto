import os

# Descripción BBDD
RUTA_PORTFOLIO = os.path.join('data', 'balance.db')
CAMPOS_TABLA = 'fecha, hora, origen, invertido, destino, obtenido, unitario'

# Datos de acceso conexión a coinapi.io
APIKEY = "escribe-aqui-tu-apikey"
API_URL = 'http://rest.coinapi.io'
ENDPOINT = '/v1/exchangerate'
HEADERS = {
    'X-CoinAPI-Key': APIKEY
}

SECRET_KEY = "escribe-aqui-tu-secret-key"
