import requests

url = "https://open.er-api.com/v6/latest/USD"
datos = requests.get(url).json()
print(datos.keys())
print(datos["rate"]["COP"])
  