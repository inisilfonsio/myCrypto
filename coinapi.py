import requests


apikey = "7FCA21CE-D552-491B-95E8-8DC563FEE632"
api_url = 'http://rest.coinapi.io'

endpoint = '/v1/assets'
headers = {
    'X-CoinAPI-Key': apikey
}

url = api_url + endpoint

response = requests.get(url, headers=headers)
status_code = response.status_code

"""
EUR Euro
EURA Otra moneda
EURT Tercera moneda

1. voy a por las monedas (requests)
2. recorrer el listado
   2.1 si la moneda tiene un código que empieza por "EUR"
       imprimir código (asset_id) y nombre (name)

"""

if status_code == 200:
    print('Las monedas disponibles son:')
    response_json = response.json()

    for coin in response_json:
        if coin.get('asset_id').startswith('BTC'):
            print(coin.get('asset_id'), coin.get('name'))
else:
    print('La petición a la API ha fallado')
    print(f'El código de error es {status_code}')
    print(f'Motivo del error {response.reason}')
    print(response.text)
