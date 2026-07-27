"""
api_client.py — ARCHIVO DE EJERCICIO
Consulta de tasa de cambio desde una API pública y enriquecimiento del DataFrame.

`obtener_tasa_usd_cop()` ya viene implementada (no es parte del ejercicio):
léela para entender cómo se consulta una API y se navega el JSON. Tu tarea es
implementar `agregar_columna_cop()` según su docstring.

Guía de trabajo:
  - Referencia teórica: Sección 3 de sesion_08.md.
  - Solución de referencia (úsala solo si te bloqueas): solucion/api_client.py
"""

import os
import sys

# Prioridad a los módulos de ejercicio; data_loader completo vive en src/.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))

import requests
import pandas as pd
from data_loader import cargar_datos
from data_cleaner import (
    reemplazar_nulos_texto, eliminar_duplicados, corregir_numericos,
)


def obtener_tasa_usd_cop():
    """
    Consulta la tasa de cambio USD/COP en tiempo real desde open.er-api.com.

    Esta función YA está implementada; no es parte del ejercicio.

    Returns:
        float: Número de pesos colombianos equivalentes a 1 USD.

    Raises:
        requests.exceptions.RequestException: Si no hay conexión o el servicio
            no responde.
        KeyError: Si la estructura del JSON de respuesta cambia.

    Examples:
        tasa = obtener_tasa_usd_cop()
        tasa   -> 4187.5   # el valor exacto varía cada día
    """
    url = "https://open.er-api.com/v6/latest/USD"
    print("  Consultando tasa USD/COP...")
    respuesta = requests.get(url, timeout=10)
    datos = respuesta.json()
    tasa = datos["rates"]["COP"]
    print(f"  Tasa obtenida: {tasa:,.2f} COP por USD")
    return tasa


def agregar_columna_cop(df, columna_usd, tasa):
    """
    Agrega una columna con el equivalente en pesos colombianos de una columna
    expresada en dólares.

    Args:
        df (pd.DataFrame): DataFrame a enriquecer.
        columna_usd (str): Nombre de la columna en USD (ya convertida a número).
        tasa (float): Tasa de cambio USD/COP obtenida de la API.

    Returns:
        pd.DataFrame: DataFrame nuevo con la columna f"{columna_usd}_cop".

    Casos a resolver:
        - La nueva columna debe llamarse exactamente f"{columna_usd}_cop".
        - Cada valor debe ser el monto en USD de esa fila convertido a COP
          usando `tasa` como factor.
        - Donde el valor en USD sea nulo, el valor en COP también debe ser nulo.
        - El DataFrame original no debe modificarse.

    Examples:
        df = agregar_columna_cop(df, "activos_exterior_usd", 4187.5)
        # activos_exterior_usd = 12000.0  ->  activos_exterior_usd_cop = 50250000.0
    """
    # EJERCICIO: crea la columna derivada f"{columna_usd}_cop" con el valor en
    #            USD convertido a COP mediante `tasa`. Trabaja sobre una copia.
    raise NotImplementedError("Implementa agregar_columna_cop()")


if __name__ == "__main__":
    RAIZ = os.path.dirname(os.path.dirname(__file__))
    ruta = os.path.join(RAIZ, "data", "inputs", "declaraciones_dirty.csv")
    df = cargar_datos(ruta)
    df = reemplazar_nulos_texto(df)
    df, _ = eliminar_duplicados(df)
    df = corregir_numericos(df, "activos_exterior_usd")

    tasa = obtener_tasa_usd_cop()
    df = agregar_columna_cop(df, "activos_exterior_usd", tasa)

    print(df[["nit", "activos_exterior_usd", "activos_exterior_usd_cop"]].head(5))
