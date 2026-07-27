import pandas
import requests

print("Todo instalado correctamente")

def probar_escritura():
    # Escribir un archivo de texto
    with open("data/outputs/resumen.txt", mode="w", encoding="utf-8") as archivo:
        archivo.write("Declaraciones procesadas: 185\n")
        archivo.write("Duplicados eliminados: 15\n")

probar_escritura()


