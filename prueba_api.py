import requests

url = "https://open.er-api.com/v6/latest/USD"
respuesta = requests.get(url)
datos = respuesta.json()

print(type(datos))           # → <class 'dict'>
print(datos.keys())
# dict_keys(['result', 'documentation', 'terms_of_use',
#            'time_last_update_utc', 'base_code', 'rates'])

print(datos["base_code"])    # → USD
print(datos["result"])       # → success