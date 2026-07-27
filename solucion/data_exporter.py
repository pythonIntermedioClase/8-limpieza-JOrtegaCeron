"""
data_exporter.py
Funciones de exportación de DataFrames a CSV y Excel con múltiples hojas.
"""

import os
from datetime import date

import numpy as np
import pandas as pd


def exportar_csv(df, carpeta, nombre_base):
    """
    Exporta un DataFrame a CSV con la fecha del día en el nombre del archivo.

    Crea la carpeta de destino si no existe.

    Args:
        df (pd.DataFrame): DataFrame a exportar.
        carpeta (str): Directorio de destino.
        nombre_base (str): Prefijo del archivo. El resultado será
            "{nombre_base}_{YYYYMMDD}.csv".

    Returns:
        str: Ruta completa del archivo generado.

    Examples:
        exportar_csv(df, "data/outputs", "declaraciones_limpias")
        # -> "data/outputs/declaraciones_limpias_20260726.csv"
    """
    os.makedirs(carpeta, exist_ok=True)
    fecha_hoy = date.today().strftime("%Y%m%d")
    nombre_archivo = f"{nombre_base}_{fecha_hoy}.csv"
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    df.to_csv(ruta_completa, index=False, encoding="utf-8")
    print(f"  CSV guardado: {ruta_completa}")
    return ruta_completa


def exportar_excel_multihoja(hojas, carpeta, nombre_base):
    """
    Exporta un diccionario de DataFrames a un archivo Excel con una hoja por
    cada entrada.

    Crea la carpeta de destino si no existe.

    Args:
        hojas (dict[str, pd.DataFrame]): Claves = nombres de hoja,
            valores = DataFrames. Ej: {"Datos_limpios": df1, "Diagnostico": df2}
        carpeta (str): Directorio de destino.
        nombre_base (str): Prefijo del archivo. El resultado será
            "{nombre_base}_{YYYYMMDD}.xlsx".

    Returns:
        str: Ruta completa del archivo generado.

    Examples:
        exportar_excel_multihoja({"Datos_limpios": df}, "data/outputs", "sesion08")
        # -> "data/outputs/sesion08_20260726.xlsx"
    """
    os.makedirs(carpeta, exist_ok=True)
    fecha_hoy = date.today().strftime("%Y%m%d")
    nombre_archivo = f"{nombre_base}_{fecha_hoy}.xlsx"
    ruta_completa = os.path.join(carpeta, nombre_archivo)

    with pd.ExcelWriter(ruta_completa, engine="openpyxl") as writer:
        for nombre_hoja, df in hojas.items():
            df.to_excel(writer, sheet_name=nombre_hoja, index=False)

    print(f"  Excel guardado: {ruta_completa}")
    return ruta_completa


if __name__ == "__main__":
    df_prueba = pd.DataFrame({
        "nit": ["900123456-1", "800234568-0", "700345679-9"],
        "total_ingresos": [1_200_000, 3_450_000, 890_000],
        "fecha_presentacion": pd.to_datetime(
            ["2024-03-22", "2024-01-15", "2024-06-01"]
        ),
    })

    df_diagnostico = pd.DataFrame({
        "verificacion": ["Total filas", "Duplicados", "Nulos reales"],
        "resultado": [200, 15, 24],
        "detalle": ["Antes de limpieza", "Eliminar con drop_duplicates()", "isnull()"],
    })

    carpeta = os.path.join("data", "outputs")
    exportar_csv(df_prueba, carpeta, "prueba")
    exportar_excel_multihoja(
        {"Datos_limpios": df_prueba, "Diagnostico": df_diagnostico},
        carpeta,
        "prueba",
    )
