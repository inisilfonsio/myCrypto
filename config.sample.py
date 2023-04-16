import os
from datetime import datetime, date

# Datos BBDD
RUTA_PORTFOLIO = os.path.join('data', 'balance.db')
PAG_SIZE = 5
DEFAULT_PAG = 1
CAMPOS_TABLA = 'fecha, hora, origen, invertido, destino, obtenido, unitario'
TABLA_USERS = 'usuarios'
SALDO_INICIAL_REGALO = {'fecha': date.today().strftime('%d/%m/%Y'), 'hora': datetime.now().strftime('%H:%M:%S'), 'origen': 'EUR',
                        'destino': 'EUR', 'invertido': '0', 'obtenido': '10000', 'unitario': '1'}


# Datos API
APIKEY = "ESCRIBE-AQUI-TU-APIKEY"
API_URL = 'http://rest.coinapi.io'
ENDPOINT = '/v1/exchangerate'
ENDPOINT1 = '/v1/assets'
HEADERS = {
    'X-CoinAPI-Key': APIKEY
}
CRIPTOS_DISPONIBLES = ['EUR', 'BTC', 'ETH', 'ADA',
                       'SOL', 'BNB', 'XRP', 'DASH', 'TRX', 'DOGE']

# Datos flask
SECRET_KEY = 'ESCRIBE-AQUI-TU-SECRETKEY'
