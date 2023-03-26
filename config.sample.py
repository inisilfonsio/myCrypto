import os

RUTA = os.path.join('data', 'balance.db')

# Datos de acceso conexión a coinapi.io
APIKEY = "escribe-aqui-tu-apikey"
API_URL = 'http://rest.coinapi.io'
ENDPOINT = '/v1/exchangerate'
HEADERS = {
    'X-CoinAPI-Key': APIKEY
}
