"""
data_cleaner.py
Funciones de limpieza y corrección de datos para el pipeline de la Sesión 8.
Cada función recibe un DataFrame, aplica una transformación y retorna el resultado.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
from data_loader import cargar_datos


def reemplazar_nulos_texto(
    df,
    valores=["N/A", "NA", "n/a", "null", "NULL", "ninguno", ""],
):
    """
    Reemplaza por np.nan todas las celdas que contengan alguna de las cadenas
    indicadas (nulos "disfrazados" de texto).

    Debe ejecutarse antes que cualquier otra limpieza: las funciones que siguen
    (fillna, dropna, conteos) asumen que los faltantes ya son NaN reales.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        valores (list[str]): Cadenas que representan nulos textuales.

    Returns:
        pd.DataFrame: DataFrame con esas celdas sustituidas por NaN.

    Examples:
        df["saldo_favor"].isnull().sum()   -> 21   # antes
        df = reemplazar_nulos_texto(df)
        df["saldo_favor"].isnull().sum()   -> 25   # tras convertir los "ninguno"
    """
    df = df.replace(valores, np.nan)
    return df


def eliminar_duplicados(df):
    """
    Elimina filas duplicadas exactas conservando la primera ocurrencia.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.

    Returns:
        tuple[pd.DataFrame, int]: DataFrame sin duplicados y número de filas
        eliminadas.

    Examples:
        df, n = eliminar_duplicados(df)
        n   -> 15
    """
    filas_antes = len(df)
    df = df.drop_duplicates()
    eliminadas = filas_antes - len(df)
    print(f"  Duplicados eliminados: {eliminadas}")
    return df, eliminadas


def limpiar_texto(df, columnas):
    """
    Aplica strip y lower a las columnas de texto indicadas.

    Unifica variantes que difieren solo por espacios o mayúsculas: " Natural",
    "NATURAL" y "natural" se convierten todas en "natural". Sin esto, un
    groupby produciría grupos duplicados.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        columnas (list[str]): Nombres de columnas de texto a normalizar.

    Returns:
        pd.DataFrame: DataFrame con esas columnas sin espacios laterales y en
        minúsculas.

    Examples:
        df = limpiar_texto(df, columnas=["tipo_persona"])
        sorted(df["tipo_persona"].unique())   -> ['juridica', 'natural']
    """
    df = df.copy()
    for columna in columnas:
        df[columna] = df[columna].str.strip().str.lower()
    return df


def corregir_fechas(df, columna):
    """
    Convierte una columna de texto a datetime64, marcando como NaT los valores
    no parseables y la fecha centinela "01/01/1900".

    Usa format="mixed" y dayfirst=True porque la columna trae dos formatos
    ("18/06/2024" y "Jun 18 2024"). Desde pandas 2.0, to_datetime sin format
    infiere un único formato y mandaría a NaT todo lo que no coincida; con
    "mixed" resuelve cada valor por separado.

    El relleno "01/01/1900" (fecha desconocida en el sistema de origen) se
    marca como faltante ANTES de convertir, comparando el texto tal como viene
    en el archivo.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        columna (str): Nombre de la columna con fechas en texto.

    Returns:
        pd.DataFrame: DataFrame con la columna convertida a datetime64[ns].

    Examples:
        df = corregir_fechas(df, "fecha_presentacion")
        df["fecha_presentacion"].dtype       -> dtype('<M8[ns]')
        df["fecha_presentacion"].isna().sum() -> 8
    """
    df = df.copy()
    # "01/01/1900" es un relleno de "fecha desconocida": lo marcamos como
    # faltante usando el mismo texto del archivo, antes de convertir.
    # Marca como faltante (None) cualquier celda que contenga la fecha centinela "01/01/1900".
    df.loc[df[columna] == "01/01/1900", columna] = None
    df[columna] = pd.to_datetime(
        df[columna], format="mixed", dayfirst=True, errors="coerce"
    )
    return df


def corregir_numericos(df, columna):
    """
    Convierte una columna de texto a float64, marcando como NaN los valores que
    no se puedan interpretar como número.

    Args:
        df (pd.DataFrame): DataFrame a limpiar.
        columna (str): Nombre de la columna a convertir.

    Returns:
        pd.DataFrame: DataFrame con la columna convertida a float64.

    Examples:
        df["total_ingresos"].dtype   -> dtype('O')        # antes: texto
        df = corregir_numericos(df, "total_ingresos")
        df["total_ingresos"].dtype   -> dtype('float64')  # después
    """
    df = df.copy()
    df[columna] = pd.to_numeric(df[columna], errors="coerce")
    return df


def filtrar_negativos(df, columna):
    """
    Agrega una columna booleana que marca los valores negativos, sin eliminar
    ninguna fila.

    Un negativo puede ser un error de digitación o tener una explicación de
    negocio. En lugar de borrarlo, se marca para revisión posterior.

    Args:
        df (pd.DataFrame): DataFrame a evaluar.
        columna (str): Nombre de la columna numérica a evaluar.

    Returns:
        pd.DataFrame: DataFrame con la nueva columna f"{columna}_es_negativo"
        de tipo bool.

    Examples:
        df = filtrar_negativos(df, "activos_exterior_usd")
        df["activos_exterior_usd_es_negativo"].sum()   -> 8
    """
    df = df.copy()
    nombre_flag = f"{columna}_es_negativo"
    df[nombre_flag] = df[columna] < 0
    return df


if __name__ == "__main__":
    RAIZ = os.path.dirname(os.path.dirname(__file__))
    ruta = os.path.join(RAIZ, "data", "inputs", "declaraciones_dirty.csv")
    df = cargar_datos(ruta)

    print(f"Filas iniciales: {len(df)}")
    print(f"Nulos reales en saldo_favor antes: {df['saldo_favor'].isnull().sum()}")
    print(f"'ninguno' en saldo_favor antes: {(df['saldo_favor'] == 'ninguno').sum()}")

    df = reemplazar_nulos_texto(df)
    print(f"'ninguno' en saldo_favor después: {(df['saldo_favor'] == 'ninguno').sum()}")
    print(f"Nulos reales en saldo_favor después: {df['saldo_favor'].isnull().sum()}")

    df, eliminadas = eliminar_duplicados(df)
    print(f"Filas después de eliminar duplicados: {len(df)}")

    df = limpiar_texto(df, columnas=["tipo_persona", "municipio"])
    df = corregir_fechas(df, "fecha_presentacion")

    columnas_numericas = [
        "total_ingresos", "total_costos", "renta_liquida",
        "impuesto_cargo", "saldo_favor", "activos_exterior_usd",
    ]
    for col in columnas_numericas:
        df = corregir_numericos(df, col)

    df = filtrar_negativos(df, "activos_exterior_usd")

    print(f"\nFilas finales: {len(df)}")
    print(f"Tipos resultantes:\n{df.dtypes.to_string()}")
    print(f"Categorías en tipo_persona: {df['tipo_persona'].unique()}")
    print(f"Negativos marcados: {df['activos_exterior_usd_es_negativo'].sum()}")
